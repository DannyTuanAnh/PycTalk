import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from Login.login_signIn import LoginWindow
from Add_friend.suggestion import SuggestionFriendWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SuggestionFriendWindow("tên_người_dùng_test")  # Thay bằng username thật nếu có
    window.show()

    sys.exit(app.exec())
