import socket
import json
import threading

class RequestHandler:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
    
    def connect_to_server(self):
        """Kết nối tới server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Đã kết nối tới server {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Lỗi kết nối server: {e}")
            self.connected = False
            return False
    
    def send_request(self, request_data):
        """Gửi request tới server và nhận response"""
        if not self.connected:
            if not self.connect_to_server():
                return {"success": False, "message": "Không thể kết nối tới server"}
        
        try:
            # Gửi dữ liệu
            json_data = json.dumps(request_data)
            self.client_socket.send(json_data.encode('utf-8'))
            
            # Nhận response
            response = self.client_socket.recv(4096).decode('utf-8')
            return json.loads(response)
            
        except Exception as e:
            print(f"Lỗi gửi/nhận dữ liệu: {e}")
            self.connected = False
            return {"success": False, "message": f"Lỗi kết nối: {e}"}
    
    def login_request(self, username, password):
        """Gửi yêu cầu đăng nhập"""
        request_data = {
            "type": "login",
            "username": username,
            "password": password
        }
        return self.send_request(request_data)
    
    def close_connection(self):
        """Đóng kết nối"""
        try:
            if self.client_socket:
                self.client_socket.close()
                self.connected = False
                print("Đã đóng kết nối")
        except Exception as e:
            print(f"Lỗi đóng kết nối: {e}")

# Global instance
request_handler = RequestHandler()
