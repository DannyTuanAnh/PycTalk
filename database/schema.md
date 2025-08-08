# Database Schema for PycTalk

## MySQL Database Setup

### 1. Create Database
```sql
CREATE DATABASE pyctalk CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pyctalk;
```

### 2. Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email)
);
```

### 3. Login Logs Table
```sql
CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    success BOOLEAN NOT NULL,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    INDEX idx_username (username),
    INDEX idx_login_time (login_time)
);
```

### 4. Sample Data
```sql
-- Test users (passwords are SHA256 hashed)
INSERT INTO users (username, email, password_hash) VALUES
('admin', 'admin@pyctalk.com', SHA2('admin123', 256)),
('test', 'test@pyctalk.com', SHA2('test123', 256));
```

## Configuration

Update `database/db.py` with your MySQL credentials:
```python
self.config = {
    'host': 'localhost',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password',
    'database': 'pyctalk',
    'port': 3306,
    'charset': 'utf8mb4',
    'autocommit': True
}
```

## Security Features

- ✅ SHA256 password hashing
- ✅ Login attempt logging
- ✅ Input validation
- ✅ SQL injection prevention with parameterized queries
- ✅ Connection security