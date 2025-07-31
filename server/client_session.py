import json
import threading
import group_handler
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from db import memory_store

def handle_client(client_socket, memory_store):
    username = None

    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break  # client đã ngắt kết nối

            try:
                msg = json.loads(data.decode())
                print(f"🔍 DEBUG: Nhận request: {msg}")  # Debug line
            except json.JSONDecodeError:
                client_socket.send(json.dumps({"status": "error", "message": "Dữ liệu không hợp lệ"}).encode())
                continue

            action = msg.get("action")
            print(f"🔍 DEBUG: Action = {action}, Username = {username}")  # Debug line
            if action == "login":
                username = msg.get("username")
                if not username:
                    client_socket.send(json.dumps({"status": "error", "message": "Thiếu tên đăng nhập"}).encode())
                    continue

                memory_store.set_socket(username, client_socket)
                client_socket.send(json.dumps({"status": "ok", "message": f"Chào {username}!"}).encode())
                print(f"[LOGIN] {username} đã đăng nhập")
                continue

            # Xử lý các action khác sau khi đăng nhập
            if not username:
                client_socket.send(json.dumps({"status": "error", "message": "Bạn chưa đăng nhập"}).encode())
                continue

            if action == "create_group":
                group_handler.create_group(msg, client_socket)
            elif action == "send_group_message":
                group_handler.send_group_message(msg, client_socket, memory_store)
            else:
                client_socket.send(json.dumps({"status": "error", "message": f"Lệnh không hợp lệ: {action}"}).encode())

    except ConnectionResetError:
        print(f"[MẤT KẾT NỐI] {username if username else 'client'} bị ngắt")

    finally:
        if username:
            memory_store.remove_socket(username)
        client_socket.close()