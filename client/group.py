import sys
import os
# Thêm thư mục parent để có thể import từ client/
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from client_tcp import ClientTCP

class GroupProtocol:
    def __init__(self, client: ClientTCP):
        self.client = client
        self.username = None  # Sẽ được set sau khi login

    def login(self, username: str):
        """Đăng nhập để server biết client là ai"""
        self.username = username
        self.client.send({
            "action": "login",
            "username": username
        })

    def create_group(self, group_name: str, members: list):
        self.client.send({
            "action": "create_group",
            "group_name": group_name,
            "members": members
        })

    def send_group_message(self, group_id: str, message: str):
        self.client.send({
            "action": "send_group_message",
            "group_id": group_id,
            "sender": self.username,  # Thêm sender
            "message": message
        })
