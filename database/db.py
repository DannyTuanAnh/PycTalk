import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'pyctalk',
            'port': 3306,
            'charset': 'utf8mb4',
            'autocommit': True
        }
        self.use_mock = False
        self.mock_db = None
    
    def get_connection(self):
        """Tạo kết nối database"""
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Lỗi kết nối MySQL: {e}")
            print("🔄 Switching to mock database for testing...")
            return self._get_mock_connection()
    
    def _get_mock_connection(self):
        """Get mock database connection"""
        try:
            if not self.use_mock:
                from .mock_db import mock_db_connection
                self.mock_db = mock_db_connection
                self.use_mock = True
                print("✅ Using mock database for testing")
            
            return self.mock_db.get_connection()
        except Exception as e:
            print(f"❌ Mock database error: {e}")
            return None
    
    def test_connection(self):
        """Test kết nối database"""
        connection = self.get_connection()
        if connection:
            if self.use_mock:
                print("✅ Mock database connection successful")
            else:
                print("✅ Kết nối database thành công")
            connection.close()
            return True
        else:
            print("❌ Không thể kết nối database")
            return False

# Global instance
db_connection = DatabaseConnection()
