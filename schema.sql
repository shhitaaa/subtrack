CREATE DATABASE IF NOT EXISTS subtrack;
USE subtrack;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(120) NOT NULL,
    category VARCHAR(80) NOT NULL DEFAULT 'Other',
    amount DECIMAL(10,2) NOT NULL,
    billing_cycle ENUM('monthly','quarterly','half-yearly','yearly') NOT NULL DEFAULT 'monthly',
    next_renewal DATE NOT NULL,
    status ENUM('active','cancelled','expired') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
