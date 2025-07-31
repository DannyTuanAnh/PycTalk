import socket
import threading
from client_session import handle_client
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from db import memory_store

# Thông tin server
HOST = '0.0.0.0'  # Cho phép nhận từ mọi địa chỉ
PORT = 9999       # Đồng bộ với client

# Danh sách lưu socket theo username
# memory_store sẽ quản lý việc username ↔ socket
client_sockets = []

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    print(f"[SERVER] Đang chạy tại {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"[KẾT NỐI] Client mới từ {addr}")
            client_sockets.append(client_socket)

            # Mỗi client xử lý trong một luồng riêng
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, memory_store)
            )
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        print("[TẮT] Đang tắt server...")
        for sock in client_sockets:
            sock.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()
