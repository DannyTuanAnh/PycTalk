from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QLabel, QHBoxLayout
)
from PyQt6.QtCore import Qt
import socket
import json

class SuggestionFriendWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Gợi ý kết bạn")
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.resize(400, 600)
        self.layout = QVBoxLayout(self)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        self.load_suggestions()

    def load_suggestions(self):
        # Kết nối đến server và lấy danh sách gợi ý
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 9000))
            request = {
                "action": "get_suggestions",
                "username": self.username
            }
            client.send(json.dumps(request).encode())
            response = json.loads(client.recv(8192).decode())
            client.close()

            if response["status"] == "ok":
                for user in response["data"]:
                    self.add_user_item(user)
        except Exception as e:
            print("Error:", e)

    def add_user_item(self, user):
        item = QListWidgetItem()
        widget = QWidget()
        layout = QHBoxLayout()
        label = QLabel(user)
        label.setStyleSheet("font-size: 14px;")
        btn = QPushButton("Kết bạn")
        btn.setStyleSheet("background-color: #3a3a3a; color: white; padding: 5px;")
        btn.clicked.connect(lambda _, u=user: self.send_friend_request(u))
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(btn)
        widget.setLayout(layout)
        widget.setStyleSheet("background-color: #2e2e2e;")
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def send_friend_request(self, to_user):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 9000))
            request = {
                "action": "add_friend",
                "from_user": self.username,
                "to_user": to_user
            }
            client.send(json.dumps(request).encode())
            response = json.loads(client.recv(4096).decode())
            client.close()
            if response["status"] == "ok":
                print(f"Đã gửi lời mời kết bạn đến {to_user}")
        except Exception as e:
            print("Kết bạn thất bại:", e)
