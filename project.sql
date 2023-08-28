-- Create the database if not exists
CREATE DATABASE IF NOT EXISTS myflaskapp;

-- Switch to the database
USE myflaskapp;

-- Create the user table
CREATE TABLE IF NOT EXISTS user (
  userid int(11) NOT NULL,
  name varchar(100) NOT NULL,
  email varchar(100) NOT NULL,
  password varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Ensure that each userid value is unique and serves as a PK
ALTER TABLE user
  ADD PRIMARY KEY (userid);

-- Insert sample user records
INSERT INTO user (userid, name, email, password) VALUES
(1, 'John smith', 'smith@webdamn.com', '123'),
(2, 'Adam William', 'adam@webdamn.com', '123');
