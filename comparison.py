# So sánh PyMySQL vs MySQL Connector

# ===== PyMySQL =====
import pymysql

config = {
    "host": "localhost",
    "user": "root", 
    "password": "",
    "database": "pyctalk"
}

# Kết nối đơn giản
conn = pymysql.connect(**config)

# ===== MySQL Connector =====
import mysql.connector

config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "pyctalk",
    "auth_plugin": "mysql_native_password"  # Phải config thêm
}

# Kết nối phức tạp hơn
conn = mysql.connector.connect(**config)

# ===== KẾT QUẢ =====
"""
PyMySQL:
- ✅ Cài đặt: pip install PyMySQL
- ✅ Kết nối: Thành công ngay
- ✅ XAMPP: Không có vấn đề
- ✅ Code: Đơn giản, rõ ràng

MySQL Connector:
- ❌ Cài đặt: pip install mysql-connector-python + dependencies
- ❌ Kết nối: Lỗi authentication plugin
- ❌ XAMPP: Cần config thêm
- ❌ Code: Phức tạp hơn
"""
