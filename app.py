#!/usr/bin/python3
from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt
from MySQLdb import cursor
import re


# Create the Flask application instance
app = Flask(__name__)

# Configure MySQL connection settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Nick1996'
app.config['MYSQL_DB'] = 'myflaskapp'
mysql = MySQL(app)

# Set a secret key for session management (replace with a strong secret key)
app.secret_key = 'Nick1996'

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login functionality.
    """
    message = ''
    try:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']

            # Create a MySQL cursor
            cursor = mysql.connection.cursor(dictionary=True)

            # Use parameterized query to prevent SQL injection
            query = 'SELECT * FROM user WHERE email = %s'
            cursor.execute(query, (email,))

            # Fetch user record
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                # Set session variables
                session['loggedin'] = True
                session['userid'] = user['userid']
                session['name'] = user['name']
                session['email'] = user['email']
                message = 'Logged in successfully!'
                return render_template('user.html', message=message)
            else:
                message = 'Please enter correct email or password!'
        else:
            message = 'Invalid request'
    except Exception as e:
        message = 'An error occured: ' + str(e)

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    """
    Clears session data to log out the user
    """
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.app('email', None)

    # Redirect to the login page
    return redirect(url_for('login'))  # Redirect to login page

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
	message = ''
	if request.method == 'POST':
            userName = request.form['name']
            password = request.form['password']
            email = request.form['email']

            # Validate user inputs
            if not userName or not password or not email:
                message = 'Please fill out the form!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                message = 'Invalid email address!'
            else:
                # Hash the password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                # Create a cursor for database operations
                cursor = mysql.connection.cursor()

                # Check if the account already exists
                cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
                account = cursor.fetchone()
                if account:
                    message = 'Account already exist!'
		else:
                    # Insert new user into the database
                    cursor.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)', (userName, email, hashed_password))
                    mysql.connection.commit()
                    cursor.close()
                    message = 'You have successfully registered!'
    return render_template('register.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
