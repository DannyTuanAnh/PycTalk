import sys
from console_ui import run_group_ui
from ui import run_group_gui

def main():
    print("🗨️ PycTalk - Group Chat Application")
    print("Chọn giao diện:")
    print("1. GUI (PyQt5) - Giao diện đồ họa chuyên nghiệp")
    print("2. Console - Giao diện dòng lệnh")
    
    while True:
        choice = input("Chọn (1/2): ").strip()
        if choice == "1":
            print("🚀 Khởi động GUI PyQt5...")
            run_group_gui()
            break
        elif choice == "2":
            print("🚀 Khởi động Console UI...")
            run_group_ui()
            break
        else:
            print("❌ Lựa chọn không hợp lệ! Vui lòng chọn 1 hoặc 2.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
