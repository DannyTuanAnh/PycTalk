# client/console_ui.py - Console interface for PycTalk

import threading
import time
from client_tcp import ClientTCP
from group import GroupProtocol

def run_group_ui():
    """Console UI for group chat"""
    print("🗨️ PycTalk Console - Group Chat")
    print("-" * 40)
    
    # Kết nối đến server
    try:
        client = ClientTCP()
        group_protocol = GroupProtocol(client)
        print("✅ Đã kết nối đến server!")
    except:
        print("❌ Không thể kết nối đến server!")
        print("Hãy đảm bảo server đang chạy tại 127.0.0.1:9999")
        return
    
    # Đăng nhập
    username = input("👤 Nhập username: ").strip()
    if not username:
        print("❌ Username không được để trống!")
        return
    
    group_protocol.login(username)
    print(f"👋 Chào {username}!")
    
    # Thread để nhận tin nhắn
    def receive_messages():
        while True:
            try:
                message = client.receive()
                if message:
                    action = message.get("action", "")
                    if action == "group_message_received":
                        sender = message.get("sender", "Unknown")
                        msg = message.get("message", "")
                        group_name = message.get("group_name", "Unknown Group")
                        print(f"\n📨 [{group_name}] {sender}: {msg}")
                    elif action == "group_created":
                        group_name = message.get("group_name", "Unknown")
                        print(f"\n✅ Nhóm '{group_name}' đã được tạo!")
                    elif action == "error":
                        error_msg = message.get("message", "Unknown error")
                        print(f"\n❌ Lỗi: {error_msg}")
                    
                    print("💬 Nhập tin nhắn (hoặc /help): ", end="", flush=True)
            except:
                break
    
    # Bắt đầu thread nhận tin nhắn
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()
    
    print("\n📋 Lệnh có sẵn:")
    print("  /create <tên_nhóm> <member1,member2,...> - Tạo nhóm")
    print("  /send <group_id> <tin_nhắn> - Gửi tin nhắn")
    print("  /help - Hiển thị trợ giúp")
    print("  /quit - Thoát")
    print("-" * 40)
    
    current_group_id = None
    
    try:
        while True:
            user_input = input("💬 Nhập tin nhắn (hoặc /help): ").strip()
            
            if not user_input:
                continue
            
            if user_input.startswith("/"):
                parts = user_input.split(" ", 2)
                command = parts[0]
                
                if command == "/help":
                    print("\n📋 Lệnh có sẵn:")
                    print("  /create <tên_nhóm> <member1,member2,...> - Tạo nhóm")
                    print("  /send <group_id> <tin_nhắn> - Gửi tin nhắn")
                    print("  /help - Hiển thị trợ giúp")
                    print("  /quit - Thoát")
                
                elif command == "/quit":
                    print("👋 Tạm biệt!")
                    break
                
                elif command == "/create":
                    if len(parts) >= 3:
                        group_name = parts[1]
                        members_str = parts[2]
                        members = [m.strip() for m in members_str.split(",")]
                        group_protocol.create_group(group_name, members)
                        print(f"🔄 Đang tạo nhóm '{group_name}' với thành viên: {members}")
                    else:
                        print("❌ Cú pháp: /create <tên_nhóm> <member1,member2,...>")
                
                elif command == "/send":
                    if len(parts) >= 3:
                        group_id = parts[1]
                        message = parts[2]
                        group_protocol.send_group_message(group_id, message)
                        current_group_id = group_id
                        print(f"📤 Đã gửi tin nhắn đến nhóm {group_id}")
                    else:
                        print("❌ Cú pháp: /send <group_id> <tin_nhắn>")
                
                else:
                    print(f"❌ Lệnh không hợp lệ: {command}")
                    print("Gõ /help để xem danh sách lệnh")
            
            else:
                # Tin nhắn thường - gửi đến nhóm hiện tại
                if current_group_id:
                    group_protocol.send_group_message(current_group_id, user_input)
                else:
                    print("❌ Chưa chọn nhóm! Sử dụng /send <group_id> <tin_nhắn>")
    
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    
    finally:
        try:
            client.close()
        except:
            pass

if __name__ == "__main__":
    run_group_ui()
