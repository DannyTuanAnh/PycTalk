import json
from .Login_server.RegisterHandle import register
from .Login_server.LoginHandle import login

import json
import socket

class ClientSession:
    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address
        self.running = True

    def run(self):
        print(f"🟢 Client {self.client_address} session started.")
        try:
            while self.running:
                # Nhận 4 byte độ dài
                length_prefix = self.client_socket.recv(4)
                if not length_prefix:
                    self.handle_disconnect("Không nhận được độ dài thông điệp")
                    break

                message_length = int.from_bytes(length_prefix, 'big')
                message_data = b''
                while len(message_data) < message_length:
                    chunk = self.client_socket.recv(message_length - len(message_data))
                    if not chunk:
                        self.handle_disconnect("Không nhận đủ dữ liệu từ client")
                        break
                    message_data += chunk

                if not message_data:
                    self.handle_disconnect("Không nhận được dữ liệu nào")
                    break

                self.handle_message(message_data)

        except (ConnectionResetError, socket.error) as e:
            self.handle_disconnect(f"Lỗi kết nối: {e}")

        finally:
            self.cleanup()

    def handle_disconnect(self, reason):
        print(f"⛔ Client {self.client_address} disconnected. Lý do: {reason}")
        self.running = False  # Gửi tín hiệu dừng vòng lặp

    def cleanup(self):
        try:
            self.client_socket.close()
            print(f"🔌 Đã đóng kết nối với {self.client_address}")
        except Exception as e:
            print(f"⚠️ Lỗi khi đóng socket {self.client_address}: {e}")

    def send_response(self, response_dict):
        try:
            response_json = json.dumps(response_dict).encode()
            response_length = len(response_json).to_bytes(4, 'big')
            self.client_socket.sendall(response_length + response_json)
        except Exception as e:
            print(f"❌ Không gửi được phản hồi cho {self.client_address}: {e}")
            self.running = False  # Tự dừng nếu không gửi được

            
    def send_response(self, response_dict):
        response_json = json.dumps(response_dict).encode()
        response_length = len(response_json).to_bytes(4, 'big')
        self.client_socket.sendall(response_length + response_json)

    def handle_message(self, raw_data):
        try:
            data = json.loads(raw_data.decode())
            action = data.get("action")
            if action == "ping":
                print(f"💓 Ping từ {self.client_address}({data['data']['username']})")
                return
            elif action == "login":
                username = data["data"]["username"]
                password = data["data"]["password"]
                result = login.login_user(username, password)
                self.send_response(result)
                 
            elif action == "register":
                username = data["data"]["username"]
                password = data["data"]["password"]
                email = data["data"]["email"]
                result = register.register_user(username, password, email)
                self.send_response(result)
                self.running = False # Dừng phiên sau khi đăng ký thành công
                
            elif action == "logout":
                print(f"🔒 {self.client_address}({data['data']['username']}) yêu cầu đăng xuất.")
                self.send_response({"success": True, "message": "Đã đăng xuất."})
                self.running = False
            elif action == "get_suggestions":
                # Trả về danh sách gợi ý kết bạn (giả lập)
                username = data["data"]["username"]
                print(f"📋 {self.client_address} yêu cầu gợi ý kết bạn cho {username}")
                suggestions = ["user1", "user2", "user3", "user4", "user5"]  # Danh sách giả lập
                self.send_response({"status": "ok", "data": suggestions})
            elif action == "add_friend":
                # Xử lý yêu cầu kết bạn
                from_user = data["data"]["from_user"]
                to_user = data["data"]["to_user"]
                print(f"👥 {self.client_address} yêu cầu kết bạn: {from_user} -> {to_user}")
                # Giả lập thành công
                self.send_response({"status": "ok", "message": f"Đã gửi lời mời kết bạn từ {from_user} đến {to_user}"})
            elif action == "send_message":
                pass  # handle_send_message(data)
            elif action == "create_group":
                pass  # handle_create_group(data)
            else:
                print(f"❓ Unknown action from {self.client_address}: {action}")

        except json.JSONDecodeError:
            print(f"❌ Invalid JSON from {self.client_address}")
