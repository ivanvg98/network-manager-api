CREATE DATABASE IF NOT EXISTS usersdb;
USE usersdb;

CREATE TABLE IF NOT EXISTS Users (
  user_name VARCHAR(20) NOT NULL,
  name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  password VARCHAR(20) NOT NULL,
  email VARCHAR(40) NOT NULL,
  admin TINYINT(1) NOT NULL,
  PRIMARY KEY (user_name)
) ENGINE=INNODB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS Devices (
  device_name VARCHAR(50) NOT NULL,
  loopback VARCHAR(20) NOT NULL,
  routing_type VARCHAR(20) Not NULL,
  PRIMARY KEY (device_name)
) ENGINE=INNODB DEFAULT CHARSET=utf8;

INSERT INTO Users(user_name, name, last_name, password, email, admin) VALUES('admin', 'Admin', 'Admin', '123', 'example@mail.com', '1');