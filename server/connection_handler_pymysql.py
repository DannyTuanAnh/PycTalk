# server/connection_handler_pymysql.py

import pymysql

# Cấu hình thông tin kết nối đến cơ sở dữ liệu MySQL
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "pyctalk",
    "charset": "utf8mb4",
    "autocommit": True
}

def get_connection():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as err:
        print(f"[LỖI] Không thể kết nối MySQL: {err}")
        return None

def test_connection():
    """Kiểm tra kết nối và hiển thị danh sách bảng trong database"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Hiển thị danh sách bảng
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("✅ Kết nối thành công!")
            print(f"📋 Danh sách bảng trong database '{DB_CONFIG['database']}':")
            for table in tables:
                print(f"  - {table[0]}")
            
            cursor.close()
            conn.close()
            return True
        except Exception as err:
            print(f"[LỖI] Không thể truy vấn database: {err}")
            return False
    else:
        print("❌ Không thể kết nối đến database")
        return False

def query_data(query, params=None):
    """Thực hiện truy vấn SELECT và trả về kết quả"""
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        except Exception as err:
            print(f"[LỖI] Truy vấn thất bại: {err}")
            return None
    return None

# Test khi chạy file trực tiếp
if __name__ == "__main__":
    print("🔍 Đang kiểm tra kết nối bằng PyMySQL...")
    
    # Kiểm tra xem có kết nối được không trước
    print("\n1. Kiểm tra kết nối cơ bản:")
    test_connection()
    
    # Thử tạo database nếu chưa có
    print("\n2. Thử tạo database 'pyctalk' nếu chưa có:")
    try:
        config_no_db = DB_CONFIG.copy()
        config_no_db.pop('database')
        conn = pymysql.connect(**config_no_db)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS pyctalk")
        print("✅ Database 'pyctalk' đã được tạo hoặc đã tồn tại")
        cursor.close()
        conn.close()
        
        # Test lại kết nối với database
        print("\n3. Test lại kết nối với database:")
        test_connection()
    except Exception as e:
        print(f"❌ Không thể tạo database: {e}")
