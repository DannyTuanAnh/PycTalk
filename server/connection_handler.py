# server/connection_handler.py

import mysql.connector

# Cấu hình thông tin kết nối đến cơ sở dữ liệu MySQL
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",        # Nhập mật khẩu nếu có
    "database": "pyctalk", # Tên cơ sở dữ liệu của bạn
    "auth_plugin": "mysql_native_password",
    "autocommit": True,
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci"
}

def get_connection():
    try:
        # Thử kết nối với cấu hình mặc định
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        if "Authentication plugin" in str(err):
            print(f"[THÔNG BÁO] Thử kết nối với phương thức khác...")
            try:
                # Thử kết nối không có auth_plugin
                config_alt = DB_CONFIG.copy()
                config_alt.pop('auth_plugin', None)
                conn = mysql.connector.connect(**config_alt)
                return conn
            except mysql.connector.Error as err2:
                print(f"[LỖI] Không thể kết nối MySQL: {err2}")
                return None
        else:
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
        except mysql.connector.Error as err:
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
        except mysql.connector.Error as err:
            print(f"[LỖI] Truy vấn thất bại: {err}")
            return None
    return None

# Test khi chạy file trực tiếp
if __name__ == "__main__":
    test_connection()
