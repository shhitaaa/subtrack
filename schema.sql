
CREATE DATABASE IF NOT EXISTS subtrack;
USE subtrack;

-- SPRINT 1: User management
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SPRINT 1: Subscription management
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

-- SPRINT 3: Monthly budget tracking
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    monthly_limit DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- SPRINT 3: Subscription price change history
CREATE TABLE IF NOT EXISTS price_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subscription_id INT NOT NULL,
    old_amount DECIMAL(10,2) NOT NULL,
    new_amount DECIMAL(10,2) NOT NULL,
    changed_on DATE NOT NULL,
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(id) ON DELETE CASCADE
);

-- SPRINT 3: Shared subscription groups
CREATE TABLE IF NOT EXISTS shared_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    group_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- SPRINT 3: Members and their payment contributions
CREATE TABLE IF NOT EXISTS group_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    member_name VARCHAR(100) NOT NULL,
    share_amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (group_id) REFERENCES shared_groups(id) ON DELETE CASCADE
);
