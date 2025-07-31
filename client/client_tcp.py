import socket
from utils import encode_message, decode_message

class ClientTCP:
    def __init__(self, host='127.0.0.1', port=9999):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
        except ConnectionRefusedError:
            print(f"❌ Không thể kết nối đến server {host}:{port}")
            print("Hãy kiểm tra server có đang chạy không?")
            raise

    def send(self, data: dict):
        try:
            self.sock.sendall(encode_message(data))
        except (ConnectionResetError, BrokenPipeError):
            print("❌ Kết nối đến server bị ngắt")
            raise

    def receive(self) -> dict:
        try:
            print("🔍 DEBUG: Đang đợi nhận data từ server...")
            data = self.sock.recv(4096)
            if not data:
                raise ConnectionError("Server đã đóng kết nối")
            result = decode_message(data)
            print(f"🔍 DEBUG: Nhận từ server: {result}")
            return result
        except (ConnectionResetError, ConnectionAbortedError):
            print("❌ Server ngắt kết nối đột ngột")
            raise
    
    def close(self):
        """Đóng kết nối"""
        try:
            self.sock.close()
        except:
            pass
