#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import sys
import os

# Add database path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from database.db import db_connection

class LoginHandler:
    def __init__(self):
        self.db = db_connection
        
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def login_user(self, username, password):
        """Authenticate user login"""
        try:
            # Get database connection
            connection = self.db.get_connection()
            if not connection:
                return {
                    "success": False, 
                    "message": "Không thể kết nối database"
                }
            
            cursor = connection.cursor()
            
            # Hash the provided password
            hashed_password = self.hash_password(password)
            
            # Check if user exists and password matches
            query = """
                SELECT id, username, email, created_at 
                FROM users 
                WHERE username = %s AND password_hash = %s
            """
            
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()
            
            if user:
                # Login successful
                user_data = {
                    "id": user[0],
                    "username": user[1], 
                    "email": user[2],
                    "created_at": str(user[3])
                }
                
                # Log successful login
                self.log_login_attempt(username, True, connection)
                
                cursor.close()
                connection.close()
                
                return {
                    "success": True,
                    "message": "Đăng nhập thành công!",
                    "user": user_data
                }
            else:
                # Login failed
                self.log_login_attempt(username, False, connection)
                
                cursor.close()
                connection.close()
                
                return {
                    "success": False,
                    "message": "Tên đăng nhập hoặc mật khẩu không đúng"
                }
                
        except Exception as e:
            print(f"❌ Lỗi xác thực đăng nhập: {e}")
            return {
                "success": False,
                "message": "Lỗi hệ thống, vui lòng thử lại"
            }
    
    def log_login_attempt(self, username, success, connection):
        """Log login attempt to database"""
        try:
            cursor = connection.cursor()
            
            query = """
                INSERT INTO login_logs (username, success, login_time, ip_address)
                VALUES (%s, %s, NOW(), %s)
            """
            
            # For now, we'll use 'system' as IP since we don't have request context
            cursor.execute(query, (username, success, 'system'))
            connection.commit()
            cursor.close()
            
            print(f"📝 Logged login attempt: {username} - {'Success' if success else 'Failed'}")
            
        except Exception as e:
            print(f"⚠️ Could not log login attempt: {e}")
    
    def create_user_tables(self):
        """Create necessary database tables if they don't exist"""
        try:
            connection = self.db.get_connection()
            if not connection:
                print("❌ Cannot connect to database to create tables")
                return False
                
            cursor = connection.cursor()
            
            # Create users table
            users_table = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(64) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    INDEX idx_username (username),
                    INDEX idx_email (email)
                )
            """
            
            # Create login logs table  
            logs_table = """
                CREATE TABLE IF NOT EXISTS login_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    success BOOLEAN NOT NULL,
                    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address VARCHAR(45),
                    INDEX idx_username (username),
                    INDEX idx_login_time (login_time)
                )
            """
            
            cursor.execute(users_table)
            cursor.execute(logs_table)
            connection.commit()
            
            print("✅ Database tables created successfully")
            
            # Create a test user if no users exist
            self.create_test_user(connection)
            
            cursor.close()
            connection.close()
            return True
            
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            return False
    
    def create_test_user(self, connection):
        """Create a test user for demonstration"""
        try:
            cursor = connection.cursor()
            
            # Check if any users exist
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                # Create test user: admin/admin123
                test_username = "admin"
                test_password = "admin123"
                test_email = "admin@pyctalk.com"
                
                hashed_password = self.hash_password(test_password)
                
                insert_query = """
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                """
                
                cursor.execute(insert_query, (test_username, test_email, hashed_password))
                connection.commit()
                
                print(f"✅ Created test user: {test_username}/{test_password}")
            
            cursor.close()
            
        except Exception as e:
            print(f"⚠️ Could not create test user: {e}")
    
    def register_user(self, username, email, password):
        """Register a new user (future feature)"""
        try:
            connection = self.db.get_connection()
            if not connection:
                return {
                    "success": False, 
                    "message": "Không thể kết nối database"
                }
            
            cursor = connection.cursor()
            
            # Check if username or email already exists
            check_query = """
                SELECT COUNT(*) FROM users 
                WHERE username = %s OR email = %s
            """
            cursor.execute(check_query, (username, email))
            
            if cursor.fetchone()[0] > 0:
                cursor.close()
                connection.close()
                return {
                    "success": False,
                    "message": "Tên đăng nhập hoặc email đã tồn tại"
                }
            
            # Hash password and insert user
            hashed_password = self.hash_password(password)
            
            insert_query = """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
            """
            
            cursor.execute(insert_query, (username, email, hashed_password))
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return {
                "success": True,
                "message": "Đăng ký thành công!"
            }
            
        except Exception as e:
            print(f"❌ Lỗi đăng ký: {e}")
            return {
                "success": False,
                "message": "Lỗi hệ thống, vui lòng thử lại"
            }

# Global instance
login_handler = LoginHandler()

# Initialize database tables when module is imported
if __name__ == "__main__":
    # Test the login handler
    print("🔧 Testing LoginHandler...")
    
    # Create tables
    login_handler.create_user_tables()
    
    # Test login with demo user
    result = login_handler.login_user("admin", "admin123")
    print(f"Login test result: {result}")
    
    # Test wrong password
    result = login_handler.login_user("admin", "wrongpassword")
    print(f"Wrong password test: {result}")