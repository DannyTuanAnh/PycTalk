#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import hashlib
from datetime import datetime

class MockDatabaseConnection:
    """Mock database for testing without MySQL"""
    
    def __init__(self):
        self.data_file = "/tmp/pyctalk_users.json"
        self.logs_file = "/tmp/pyctalk_logs.json"
        self.ensure_data_files()
        
    def ensure_data_files(self):
        """Ensure data files exist with test data"""
        # Users data
        if not os.path.exists(self.data_file):
            test_users = {
                "admin": {
                    "id": 1,
                    "username": "admin",
                    "email": "admin@pyctalk.com",
                    "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                    "created_at": datetime.now().isoformat(),
                    "is_active": True
                },
                "test": {
                    "id": 2,
                    "username": "test",
                    "email": "test@pyctalk.com", 
                    "password_hash": hashlib.sha256("test123".encode()).hexdigest(),
                    "created_at": datetime.now().isoformat(),
                    "is_active": True
                }
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(test_users, f, indent=2, ensure_ascii=False)
        
        # Logs data
        if not os.path.exists(self.logs_file):
            with open(self.logs_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def get_connection(self):
        """Return mock connection"""
        return self
    
    def is_connected(self):
        """Mock connected status"""
        return True
    
    def close(self):
        """Mock close"""
        pass
    
    def cursor(self):
        """Return mock cursor"""
        return MockCursor(self.data_file, self.logs_file)
    
    def commit(self):
        """Mock commit"""
        pass
    
    def test_connection(self):
        """Test mock connection"""
        print("✅ Mock database connection successful")
        return True

class MockCursor:
    """Mock cursor for database operations"""
    
    def __init__(self, data_file, logs_file):
        self.data_file = data_file
        self.logs_file = logs_file
        self.last_result = None
        
    def execute(self, query, params=None):
        """Mock query execution"""
        query_lower = query.lower().strip()
        
        if "select" in query_lower and "from users" in query_lower:
            # Handle user lookup
            self.handle_user_select(query, params)
        elif "insert into login_logs" in query_lower:
            # Handle login logging
            self.handle_login_log(params)
        elif "select count(*)" in query_lower:
            # Handle count queries
            self.last_result = [(1,)]
        else:
            # Default success
            self.last_result = []
    
    def handle_user_select(self, query, params):
        """Handle user selection queries"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            if params and len(params) >= 2:
                username, password_hash = params[0], params[1]
                
                if username in users:
                    user = users[username]
                    if user["password_hash"] == password_hash:
                        # Return user data in format expected by main code
                        self.last_result = [(
                            user["id"],
                            user["username"], 
                            user["email"],
                            user["created_at"]
                        )]
                    else:
                        self.last_result = []
                else:
                    self.last_result = []
            else:
                self.last_result = []
                
        except Exception as e:
            print(f"Mock DB Error: {e}")
            self.last_result = []
    
    def handle_login_log(self, params):
        """Handle login logging"""
        try:
            with open(self.logs_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            if params and len(params) >= 3:
                log_entry = {
                    "username": params[0],
                    "success": params[1],
                    "login_time": datetime.now().isoformat(),
                    "ip_address": params[2]
                }
                logs.append(log_entry)
                
                with open(self.logs_file, 'w', encoding='utf-8') as f:
                    json.dump(logs, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            print(f"Mock logging error: {e}")
    
    def fetchone(self):
        """Return one result"""
        if self.last_result and len(self.last_result) > 0:
            return self.last_result[0]
        return None
    
    def fetchall(self):
        """Return all results"""
        return self.last_result or []
    
    def close(self):
        """Mock close"""
        pass
    
    def commit(self):
        """Mock commit"""
        pass

# Replace the original database connection with mock for testing
mock_db_connection = MockDatabaseConnection()

# Test the mock database
if __name__ == "__main__":
    print("🔧 Testing Mock Database...")
    
    # Test connection
    conn = mock_db_connection.get_connection()
    print(f"Connection: {conn}")
    
    # Test user lookup
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, created_at FROM users WHERE username = %s AND password_hash = %s",
        ("admin", hashlib.sha256("admin123".encode()).hexdigest())
    )
    
    result = cursor.fetchone()
    print(f"User lookup result: {result}")
    
    cursor.close()
    conn.close()
    
    print("✅ Mock database test completed")