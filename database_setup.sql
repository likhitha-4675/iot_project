CREATE DATABASE iot_db;
USE iot_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(120) UNIQUE,
    otp VARCHAR(6),
    otp_generated_time DATETIME,
    otp_used_time DATETIME,
    is_verified BOOLEAN DEFAULT FALSE,
    internet_speed FLOAT,
    usage_data VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS connected_users (
    device_name VARCHAR(50),
    device_id VARCHAR(50) PRIMARY KEY,
    connected_date VARCHAR(50),
    data_usage VARCHAR(50),
    status BOOLEAN DEFAULT TRUE
);