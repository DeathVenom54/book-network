CREATE DATABASE IF NOT EXISTS book_network;
USE book_network;
CREATE TABLE IF NOT EXISTS users (username VARCHAR(30) PRIMARY KEY, password VARCHAR(255) NOT NULL, display_name VARCHAR(30), bio VARCHAR(500));
CREATE TABLE IF NOT EXISTS friends (user1 VARCHAR(30), user2 VARCHAR(30), PRIMARY KEY (user1, user2), FOREIGN KEY (user1) REFERENCES users(username) ON UPDATE CASCADE, FOREIGN KEY (user2) REFERENCES users(username) ON UPDATE CASCADE);
CREATE TABLE IF NOT EXISTS friend_requests (u_from VARCHAR(30), u_to VARCHAR(30), PRIMARY KEY (u_from, u_to), FOREIGN KEY (u_from) REFERENCES users(username), FOREIGN KEY (u_to) REFERENCES users(username) ON UPDATE CASCADE);
CREATE TABLE IF NOT EXISTS user_books (username VARCHAR(30), work_id VARCHAR(40), action INTEGER DEFAULT 0, wtr_date DATETIME, rng_date DATETIME, rd_date DATETIME, PRIMARY KEY (username, work_id), FOREIGN KEY (username) REFERENCES users(username) ON UPDATE CASCADE);
CREATE TABLE IF NOT EXISTS reviews (username VARCHAR(30), work_id VARCHAR(40), rating INTEGER, review VARCHAR(1000), date DATE, PRIMARY KEY (username, work_id), FOREIGN KEY (username) REFERENCES users(username) ON UPDATE CASCADE);
CREATE TABLE IF NOT EXISTS book_data (work_id VARCHAR(40) PRIMARY KEY, title VARCHAR(100), description VARCHAR(2000), author VARCHAR(100), cover VARCHAR(40), subjects VARCHAR(10000));