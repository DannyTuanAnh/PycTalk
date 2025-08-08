#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import json
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Login_server.LoginHandle import login_handler

class PycTalkServer:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
    
    def start_server(self):
        """Khởi động server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            
            self.running = True
            print(f"🚀 PycTalk Server đã khởi động tại {self.host}:{self.port}")
            print("Đang chờ kết nối từ client...")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"✅ Client mới kết nối: {client_address}")
                    
                    # Tạo thread để xử lý client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        print(f"Lỗi accept: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ Lỗi khởi động server: {e}")
        finally:
            self.stop_server()
    
    def handle_client(self, client_socket, client_address):
        """Xử lý client request"""
        try:
            self.clients.append(client_socket)
            
            while self.running:
                try:
                    # Nhận dữ liệu từ client
                    data = client_socket.recv(4096).decode('utf-8')
                    if not data:
                        break
                    
                    print(f"📨 Nhận request từ {client_address}: {data}")
                    
                    # Parse JSON request
                    request = json.loads(data)
                    response = self.process_request(request)
                    
                    # Gửi response
                    response_json = json.dumps(response, ensure_ascii=False)
                    client_socket.send(response_json.encode('utf-8'))
                    
                    print(f"📤 Gửi response: {response}")
                    
                except json.JSONDecodeError:
                    error_response = {"success": False, "message": "Invalid JSON format"}
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                    
                except socket.error as e:
                    print(f"❌ Lỗi socket với {client_address}: {e}")
                    break
                    
        except Exception as e:
            print(f"❌ Lỗi xử lý client {client_address}: {e}")
        
        finally:
            # Cleanup
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()
            print(f"🔌 Client {client_address} đã ngắt kết nối")
    
    def process_request(self, request):
        """Xử lý các loại request"""
        request_type = request.get("type")
        
        if request_type == "login":
            username = request.get("username")
            password = request.get("password")
            
            if not username or not password:
                return {"success": False, "message": "Thiếu thông tin đăng nhập"}
            
            return login_handler.login_user(username, password)
        
        else:
            return {"success": False, "message": "Loại request không hỗ trợ"}
    
    def stop_server(self):
        """Dừng server"""
        print("\n🛑 Đang dừng server...")
        self.running = False
        
        # Đóng tất cả client connections
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        
        # Đóng server socket
        if self.server_socket:
            self.server_socket.close()
        
        print("✅ Server đã dừng")

def main():
    server = PycTalkServer()
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n⚡ Nhận tín hiệu dừng từ bàn phím")
    finally:
        server.stop_server()

if __name__ == "__main__":
    main()