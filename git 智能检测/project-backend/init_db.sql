-- 创建数据库
CREATE DATABASE IF NOT EXISTS ai_detect DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ai_detect;

-- 变更记录表
CREATE TABLE IF NOT EXISTS changes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    repo VARCHAR(128) NOT NULL,
    commit_id VARCHAR(64) NOT NULL,
    author VARCHAR(64) NOT NULL,
    time DATETIME NOT NULL,
    risk_level VARCHAR(16),
    review_status VARCHAR(16),
    diff TEXT,
    ai_result TEXT,
    lime_explain TEXT
);

-- 用户表
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(32) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 审核记录表
CREATE TABLE IF NOT EXISTS review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    change_id INT NOT NULL,
    reviewer VARCHAR(64) NOT NULL,
    result VARCHAR(16) NOT NULL,
    comment TEXT,
    time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (change_id) REFERENCES changes(id)
);

-- 通知表
CREATE TABLE IF NOT EXISTS notify (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(32),
    content TEXT,
    receiver VARCHAR(64),
    status VARCHAR(16),
    time DATETIME DEFAULT CURRENT_TIMESTAMP
); 