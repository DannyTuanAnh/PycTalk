# server/app.py - Ứng dụng quản lý database PyC Talk

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from connection_handler_pymysql import get_connection, query_data
import pymysql

class PyCTalkApp:
    def __init__(self):
        self.running = True
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def show_header(self):
        print("=" * 50)
        print("🚀 PYC TALK - DATABASE MANAGER")
        print("=" * 50)
        
    def show_menu(self):
        print("\n📋 MENU CHÍNH:")
        print("1. Kiểm tra kết nối database")
        print("2. Hiển thị danh sách bảng")
        print("3. Xem dữ liệu users")
        print("4. Xem dữ liệu messages")
        print("5. Thêm user mới")
        print("6. Thực hiện truy vấn tùy chỉnh")
        print("7. Thoát")
        print("-" * 30)
        
    def test_connection(self):
        print("\n🔍 Đang kiểm tra kết nối...")
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"✅ Kết nối thành công!")
                print(f"📊 MySQL Version: {version[0]}")
                cursor.close()
                conn.close()
                return True
            except Exception as err:
                print(f"❌ Lỗi: {err}")
                return False
        else:
            print("❌ Không thể kết nối đến database")
            return False
            
    def show_tables(self):
        print("\n📋 Danh sách bảng trong database:")
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                if tables:
                    for i, table in enumerate(tables, 1):
                        print(f"  {i}. {table[0]}")
                else:
                    print("  Không có bảng nào trong database")
                cursor.close()
                conn.close()
            except Exception as err:
                print(f"❌ Lỗi: {err}")
        else:
            print("❌ Không thể kết nối đến database")
            
    def show_users(self):
        print("\n👥 Danh sách Users:")
        try:
            results = query_data("SELECT * FROM users LIMIT 10")
            if results:
                print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Created':<20}")
                print("-" * 65)
                for row in results:
                    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {str(row[3]):<20}")
            else:
                print("  Không có dữ liệu users hoặc bảng không tồn tại")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            
    def show_messages(self):
        print("\n💬 Danh sách Messages:")
        try:
            results = query_data("SELECT * FROM messages LIMIT 10")
            if results:
                print(f"{'ID':<5} {'From':<10} {'To':<10} {'Message':<30} {'Time':<20}")
                print("-" * 75)
                for row in results:
                    message = row[3][:27] + "..." if len(str(row[3])) > 30 else row[3]
                    print(f"{row[0]:<5} {row[1]:<10} {row[2]:<10} {message:<30} {str(row[4]):<20}")
            else:
                print("  Không có dữ liệu messages hoặc bảng không tồn tại")
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            
    def add_user(self):
        print("\n➕ Thêm User Mới:")
        username = input("Nhập username: ").strip()
        email = input("Nhập email: ").strip()
        password = input("Nhập password: ").strip()
        
        if username and email and password:
            conn = get_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
                    cursor.execute(query, (username, email, password))
                    conn.commit()
                    print(f"✅ Đã thêm user '{username}' thành công!")
                    cursor.close()
                    conn.close()
                except Exception as err:
                    print(f"❌ Lỗi: {err}")
            else:
                print("❌ Không thể kết nối đến database")
        else:
            print("❌ Vui lòng nhập đầy đủ thông tin!")
            
    def custom_query(self):
        print("\n🔧 Thực hiện truy vấn tùy chỉnh:")
        print("Ví dụ: SELECT * FROM users WHERE username LIKE '%admin%'")
        query = input("Nhập truy vấn SQL: ").strip()
        
        if query:
            try:
                results = query_data(query)
                if results:
                    print(f"\n📊 Kết quả ({len(results)} dòng):")
                    for i, row in enumerate(results[:20], 1):  # Giới hạn 20 dòng
                        print(f"  {i}. {row}")
                    if len(results) > 20:
                        print(f"  ... và {len(results) - 20} dòng khác")
                else:
                    print("  Không có kết quả hoặc truy vấn thất bại")
            except Exception as e:
                print(f"❌ Lỗi: {e}")
        else:
            print("❌ Vui lòng nhập truy vấn!")
            
    def run(self):
        while self.running:
            self.clear_screen()
            self.show_header()
            self.show_menu()
            
            try:
                choice = input("Chọn chức năng (1-7): ").strip()
                
                if choice == "1":
                    self.test_connection()
                elif choice == "2":
                    self.show_tables()
                elif choice == "3":
                    self.show_users()
                elif choice == "4":
                    self.show_messages()
                elif choice == "5":
                    self.add_user()
                elif choice == "6":
                    self.custom_query()
                elif choice == "7":
                    print("\n👋 Tạm biệt!")
                    self.running = False
                else:
                    print("❌ Lựa chọn không hợp lệ!")
                    
                if self.running and choice != "7":
                    input("\nNhấn Enter để tiếp tục...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Tạm biệt!")
                self.running = False
            except Exception as e:
                print(f"\n❌ Lỗi không mong muốn: {e}")
                input("\nNhấn Enter để tiếp tục...")

# Chạy ứng dụng
if __name__ == "__main__":
    app = PyCTalkApp()
    app.run()
