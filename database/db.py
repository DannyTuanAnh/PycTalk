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
    
    def get_connection(self):
        """Tạo kết nối database"""
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Lỗi kết nối database: {e}")
            return None
    
    def test_connection(self):
        """Test kết nối database"""
        connection = self.get_connection()
        if connection:
            print("✅ Kết nối database thành công")
            connection.close()
            return True
        else:
            print("❌ Không thể kết nối database")
            return False

# Global instance
db_connection = DatabaseConnection()
