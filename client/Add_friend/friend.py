import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox
import requests

API_BASE = 'http://localhost:9000/api'
USER_ID = 'user1'  # Giả sử là người dùng đang đăng nhập

class FriendWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kết bạn và Gợi ý bạn bè")
        self.resize(400, 600)

        self.layout = QVBoxLayout()

        self.friend_list = QListWidget()
        self.request_list = QListWidget()
        self.suggestion_list = QListWidget()

        self.layout.addWidget(QLabel("👥 Danh sách bạn bè"))
        self.layout.addWidget(self.friend_list)

        self.layout.addWidget(QLabel("📨 Lời mời kết bạn"))
        self.layout.addWidget(self.request_list)

        self.layout.addWidget(QLabel("💡 Gợi ý bạn bè"))
        self.layout.addWidget(self.suggestion_list)

        self.setLayout(self.layout)
        self.load_data()

        self.request_list.itemClicked.connect(self.accept_request)
        self.suggestion_list.itemClicked.connect(self.send_request)

    def load_data(self):
        self.friend_list.clear()
        self.request_list.clear()
        self.suggestion_list.clear()

        r1 = requests.get(f"{API_BASE}/friend/list", params={'user_id': USER_ID})
        r2 = requests.get(f"{API_BASE}/friend/requests", params={'user_id': USER_ID})
        r3 = requests.get(f"{API_BASE}/user/suggestions", params={'user_id': USER_ID})

        if r1.ok:
            for f in r1.json().get('friends', []):
                self.friend_list.addItem(f)

        if r2.ok:
            for f in r2.json().get('requests', []):
                self.request_list.addItem(f)

        if r3.ok:
            for s in r3.json().get('suggestions', []):
                self.suggestion_list.addItem(f"{s['id']} (score: {s['score']})")

    def send_request(self, item):
        target_id = item.text().split()[0]
        r = requests.post(f"{API_BASE}/friend/request", json={'from_id': USER_ID, 'to_id': target_id})
        if r.ok and r.json().get('status') == 'sent':
            QMessageBox.information(self, "Thành công", f"Đã gửi lời mời đến {target_id}")
        else:
            QMessageBox.warning(self, "Lỗi", f"Không thể gửi lời mời đến {target_id}")
        self.load_data()

    def accept_request(self, item):
        from_id = item.text()
        r = requests.post(f"{API_BASE}/friend/accept", json={'from_id': from_id, 'to_id': USER_ID})
        if r.ok and r.json().get('status') == 'accepted':
            QMessageBox.information(self, "Thành công", f"Đã kết bạn với {from_id}")
        else:
            QMessageBox.warning(self, "Lỗi", f"Không thể kết bạn với {from_id}")
        self.load_data()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = FriendWindow()
    win.show()
    sys.exit(app.exec_())
