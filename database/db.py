# database/db.py - Database abstraction layer

import pymysql
from typing import List, Optional
import uuid

# Database configuration
DB_CONFIG = {
    "host": "localhost", 
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "pyctalk"
}

class DatabaseManager:
    """
    Unified database manager for PycTalk
    Handles both MySQL operations and in-memory fallback
    """
    
    def __init__(self, use_mysql=False):
        self.use_mysql = use_mysql
        self.connection = None
        
        if use_mysql:
            try:
                self.connection = pymysql.connect(**DB_CONFIG)
                print("[DB] Connected to MySQL")
            except Exception as e:
                print(f"[DB] MySQL connection failed: {e}")
                print("[DB] Falling back to in-memory storage")
                self.use_mysql = False
                
        if not self.use_mysql:
            self._init_memory_storage()
            
    def _init_memory_storage(self):
        """Initialize in-memory storage (mock database)"""
        # Mock users (from old group_db_mock.py)
        self.mock_users = {
            "alice": 1, "bob": 2, "charlie": 3, "david": 4, "emma": 5
        }
        self.id_to_username = {v: k for k, v in self.mock_users.items()}
        self.groups = {}
        self.group_members = {}
        self.user_socket_map = {}  # From old memory_store.py
        
    # User management
    def get_user_id(self, username: str) -> Optional[int]:
        if self.use_mysql:
            # TODO: MySQL query
            pass
        else:
            return self.mock_users.get(username)
            
    def user_exists(self, username: str) -> bool:
        return self.get_user_id(username) is not None
        
    # Socket management (from memory_store.py)
    def set_socket(self, username: str, socket):
        """Map username to socket"""
        self.user_socket_map[username] = socket
        
    def get_socket_by_username(self, username: str):
        """Get socket by username"""
        return self.user_socket_map.get(username)
        
    def remove_socket(self, username: str):
        """Remove socket mapping"""
        if username in self.user_socket_map:
            del self.user_socket_map[username]
            
    # Group management (from group_db_mock.py)
    def create_group(self, group_name: str, member_usernames: List[str]) -> Optional[str]:
        """Create new group"""
        if self.use_mysql:
            # TODO: MySQL implementation
            pass
        else:
            # Mock implementation
            user_ids = [self.get_user_id(u) for u in member_usernames if self.get_user_id(u)]
            if len(user_ids) < 2:
                return None
                
            group_id = str(uuid.uuid4())
            self.groups[group_id] = {
                "name": group_name,
                "members": user_ids
            }
            self.group_members[group_id] = user_ids
            return group_id

# Global database instance  
db_instance = DatabaseManager(use_mysql=False)

# Alias for backward compatibility
memory_store = db_instance
