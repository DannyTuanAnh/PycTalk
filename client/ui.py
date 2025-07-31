import sys
import os

# Fix PyQt5 plugin path issue
def fix_pyqt5_path():
    try:
        import PyQt5
        pyqt5_path = os.path.dirname(PyQt5.__file__)
        qt_plugin_path = os.path.join(pyqt5_path, 'Qt5', 'plugins')
        if os.path.exists(qt_plugin_path):
            os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
            os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_plugin_path
    except:
        pass

fix_pyqt5_path()

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QGroupBox, QMessageBox, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon
import threading
import queue

# Thêm thư mục parent để có thể import từ client/
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from client_tcp import ClientTCP
from group import GroupProtocol
from utils import decode_message

class MessageListener(QThread):
    """Thread để lắng nghe tin nhắn từ server"""
    message_received = pyqtSignal(dict)
    connection_lost = pyqtSignal()
    
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.running = True
        
    def run(self):
        while self.running:
            try:
                if self.client and self.client.sock:
                    response = self.client.receive()
                    self.message_received.emit(response)
            except Exception as e:
                self.connection_lost.emit()
                break
                
    def stop(self):
        self.running = False

class PycTalkGUIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = None
        self.group_protocol = None
        self.username = ""
        self.is_connected = False
        self.current_group_id = ""
        
        # Response waiting system
        self.waiting_for_response = False
        self.response_callback = None
        self.message_listener = None
        
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle("🗨️ PycTalk - Group Chat")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #0084ff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #006ce7;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #0084ff;
            }
            QTextEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("🗨️ PycTalk - Group Chat Application")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # Connection section
        self.setup_connection_section(main_layout)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Group management
        self.setup_left_panel(splitter)
        
        # Right panel - Chat display
        self.setup_right_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([400, 600])
        
        # Status bar
        self.statusBar().showMessage("🔴 Chưa kết nối")
        
    def setup_connection_section(self, parent_layout):
        """Thiết lập phần kết nối"""
        conn_group = QGroupBox("Kết nối Server")
        conn_layout = QHBoxLayout()
        
        # Username input
        conn_layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nhập username của bạn...")
        self.username_input.returnPressed.connect(self.connect_to_server)
        conn_layout.addWidget(self.username_input)
        
        # Connect button
        self.connect_btn = QPushButton("🔗 Kết nối")
        self.connect_btn.clicked.connect(self.connect_to_server)
        conn_layout.addWidget(self.connect_btn)
        
        # Status label
        self.status_label = QLabel("🔴 Chưa kết nối")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        conn_layout.addWidget(self.status_label)
        
        conn_group.setLayout(conn_layout)
        parent_layout.addWidget(conn_group)
        
    def setup_left_panel(self, splitter):
        """Thiết lập panel bên trái"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Create group section
        create_group = QGroupBox("🆕 Tạo nhóm mới")
        create_layout = QVBoxLayout()
        
        # Group name
        create_layout.addWidget(QLabel("Tên nhóm:"))
        self.group_name_input = QLineEdit()
        self.group_name_input.setPlaceholderText("Nhập tên nhóm...")
        create_layout.addWidget(self.group_name_input)
        
        # Members
        create_layout.addWidget(QLabel("Thành viên (phân cách bởi dấu phẩy):"))
        self.members_input = QLineEdit()
        self.members_input.setPlaceholderText("alice, bob, charlie...")
        create_layout.addWidget(self.members_input)
        
        # Hint
        hint_label = QLabel("💡 Gợi ý: alice, bob, charlie, david, emma")
        hint_label.setStyleSheet("color: gray; font-size: 12px;")
        create_layout.addWidget(hint_label)
        
        # Create button
        self.create_group_btn = QPushButton("🆕 Tạo nhóm")
        self.create_group_btn.setEnabled(False)
        self.create_group_btn.clicked.connect(self.create_group)
        create_layout.addWidget(self.create_group_btn)
        
        create_group.setLayout(create_layout)
        left_layout.addWidget(create_group)
        
        # Send message section
        send_group = QGroupBox("📤 Gửi tin nhắn")
        send_layout = QVBoxLayout()
        
        # Group ID
        send_layout.addWidget(QLabel("Group ID:"))
        self.group_id_input = QLineEdit()
        self.group_id_input.setPlaceholderText("Nhập hoặc paste Group ID...")
        send_layout.addWidget(self.group_id_input)
        
        # Message
        send_layout.addWidget(QLabel("Tin nhắn:"))
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Nhập tin nhắn...")
        self.message_input.returnPressed.connect(self.send_message)
        send_layout.addWidget(self.message_input)
        
        # Send button
        self.send_btn = QPushButton("📤 Gửi tin nhắn")
        self.send_btn.setEnabled(False)
        self.send_btn.clicked.connect(self.send_message)
        send_layout.addWidget(self.send_btn)
        
        send_group.setLayout(send_layout)
        left_layout.addWidget(send_group)
        
        # Stretch to push everything to top
        left_layout.addStretch()
        
        splitter.addWidget(left_widget)
        
    def setup_right_panel(self, splitter):
        """Thiết lập panel bên phải"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Chat display
        chat_group = QGroupBox("💬 Tin nhắn")
        chat_layout = QVBoxLayout()
        
        # Messages area
        self.messages_display = QTextEdit()
        self.messages_display.setReadOnly(True)
        self.messages_display.setMinimumHeight(400)
        chat_layout.addWidget(self.messages_display)
        
        # Clear button
        clear_btn = QPushButton("🗑️ Xóa tin nhắn")
        clear_btn.clicked.connect(self.clear_messages)
        chat_layout.addWidget(clear_btn)
        
        chat_group.setLayout(chat_layout)
        right_layout.addWidget(chat_group)
        
        splitter.addWidget(right_widget)
        
    def add_message(self, message, msg_type="info"):
        """Thêm tin nhắn vào display"""
        colors = {
            "info": "#333333",
            "success": "#28a745", 
            "error": "#dc3545",
            "system": "#007bff",
            "group_id": "#6f42c1",
            "message": "#000000"
        }
        
        color = colors.get(msg_type, "#333333")
        formatted_message = f'<span style="color: {color};">{message}</span>'
        
        self.messages_display.append(formatted_message)
        
        # Auto scroll to bottom
        scrollbar = self.messages_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def clear_messages(self):
        """Xóa tất cả tin nhắn"""
        self.messages_display.clear()
        
    def connect_to_server(self):
        """Kết nối đến server"""
        if self.is_connected:
            self.disconnect_from_server()
            return
            
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập username!")
            return
            
        try:
            self.add_message("🔄 Đang kết nối đến server...", "system")
            self.client = ClientTCP()
            self.group_protocol = GroupProtocol(self.client)
            self.username = username
            
            # Login
            self.group_protocol.login(username)
            response = self.client.receive()
            
            if response.get("status") == "ok":
                self.is_connected = True
                self.connect_btn.setText("🔌 Ngắt kết nối")
                self.status_label.setText(f"🟢 Kết nối: {username}")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
                self.create_group_btn.setEnabled(True)
                self.send_btn.setEnabled(True)
                self.username_input.setEnabled(False)
                
                self.add_message(f"✅ {response.get('message', 'Đăng nhập thành công')}", "success")
                self.statusBar().showMessage(f"🟢 Đã kết nối với username: {username}")
                
                # Start message listener
                self.start_message_listener()
            else:
                self.add_message(f"❌ Đăng nhập thất bại: {response.get('message', 'Lỗi không xác định')}", "error")
                self.client.close()
                
        except Exception as e:
            self.add_message(f"❌ Không thể kết nối: {str(e)}", "error")
            QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến server:\n{str(e)}")
            
    def disconnect_from_server(self):
        """Ngắt kết nối"""
        if self.message_listener:
            self.message_listener.stop()
            self.message_listener.wait()
            
        if self.client:
            self.client.close()
            
        self.is_connected = False
        self.connect_btn.setText("🔗 Kết nối")
        self.status_label.setText("🔴 Chưa kết nối")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.create_group_btn.setEnabled(False)
        self.send_btn.setEnabled(False)
        self.username_input.setEnabled(True)
        self.add_message("🔴 Đã ngắt kết nối", "system")
        self.statusBar().showMessage("🔴 Đã ngắt kết nối")
        
    def start_message_listener(self):
        """Bắt đầu lắng nghe tin nhắn"""
        self.message_listener = MessageListener(self.client)
        self.message_listener.message_received.connect(self.handle_message)
        self.message_listener.connection_lost.connect(self.on_connection_lost)
        self.message_listener.start()
        
    def handle_message(self, response):
        """Xử lý tin nhắn từ server"""
        if self.waiting_for_response and self.response_callback:
            # Handle expected response
            self.response_callback(response)
        else:
            # Handle other messages
            msg_type = response.get("type")
            
            if msg_type == "group_message":
                group_id = response["group_id"]
                sender = response["sender"]
                content = response["message"]
                group_name = response.get("group_name", group_id)
                
                self.add_message(f"💬 [{group_name}] {sender}: {content}", "message")
            else:
                self.add_message(f"📥 Nhận tin: {response}", "system")
                
    def on_connection_lost(self):
        """Xử lý khi mất kết nối"""
        self.add_message("❌ Mất kết nối đến server", "error")
        self.disconnect_from_server()
        
    def create_group(self):
        """Tạo nhóm mới"""
        if not self.is_connected:
            QMessageBox.warning(self, "Lỗi", "Vui lòng kết nối trước!")
            return
            
        if self.waiting_for_response:
            QMessageBox.information(self, "Thông báo", "Đang đợi phản hồi từ server...")
            return
            
        group_name = self.group_name_input.text().strip()
        members_str = self.members_input.text().strip()
        
        if not group_name:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên nhóm!")
            return
            
        if not members_str:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập danh sách thành viên!")
            return
            
        members = [m.strip() for m in members_str.split(",") if m.strip()]
        if not members:
            QMessageBox.warning(self, "Lỗi", "Danh sách thành viên không hợp lệ!")
            return
            
        try:
            self.add_message(f"🔄 Đang tạo nhóm '{group_name}' với thành viên: {', '.join(members)}", "system")
            
            # Set up response callback
            self.waiting_for_response = True
            self.response_callback = self.handle_create_group_response
            self.create_group_btn.setEnabled(False)
            
            # Send request
            self.group_protocol.create_group(group_name, members)
            
            # Set timeout
            QTimer.singleShot(5000, self.reset_response_waiting)
                
        except Exception as e:
            self.waiting_for_response = False
            self.response_callback = None
            self.create_group_btn.setEnabled(True)
            self.add_message(f"❌ Lỗi tạo nhóm: {str(e)}", "error")
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tạo nhóm:\n{str(e)}")
            
    def handle_create_group_response(self, response):
        """Xử lý response của create_group"""
        status = response.get("status")
        
        if status == "ok":
            group_id = response.get("group_id")
            message = response.get("message")
            self.add_message(f"✅ {message}", "success")
            self.add_message(f"🆔 Group ID: {group_id}", "group_id")
            self.group_id_input.setText(group_id)
            
            # Clear form
            self.group_name_input.clear()
            self.members_input.clear()
            
            QMessageBox.information(self, "Thành công", f"Đã tạo nhóm thành công!\nGroup ID: {group_id}")
            
        elif status == "error":
            error_msg = response.get("message", "Lỗi không xác định")
            self.add_message(f"⚠️ Lỗi tạo nhóm: {error_msg}", "error")
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo nhóm:\n{error_msg}")
        else:
            self.add_message(f"📥 Response không xác định: {response}", "system")
            
        # Reset waiting state
        self.waiting_for_response = False
        self.response_callback = None
        self.create_group_btn.setEnabled(True)
        
    def send_message(self):
        """Gửi tin nhắn nhóm"""
        if not self.is_connected:
            QMessageBox.warning(self, "Lỗi", "Vui lòng kết nối trước!")
            return
            
        if self.waiting_for_response:
            QMessageBox.information(self, "Thông báo", "Đang đợi phản hồi từ server...")
            return
            
        group_id = self.group_id_input.text().strip()
        message = self.message_input.text().strip()
        
        if not group_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Group ID!")
            return
            
        if not message:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tin nhắn!")
            return
            
        try:
            # Set up response callback
            self.waiting_for_response = True
            self.response_callback = self.handle_send_message_response
            self.send_btn.setEnabled(False)
            
            # Send message
            self.group_protocol.send_group_message(group_id, message)
            self.add_message(f"📤 [{self.username}]: {message}", "message")
            
            # Clear message input
            self.message_input.clear()
            
            # Set timeout
            QTimer.singleShot(5000, self.reset_response_waiting)
                
        except Exception as e:
            self.waiting_for_response = False
            self.response_callback = None
            self.send_btn.setEnabled(True)
            self.add_message(f"❌ Lỗi gửi tin nhắn: {str(e)}", "error")
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi gửi tin nhắn:\n{str(e)}")
            
    def handle_send_message_response(self, response):
        """Xử lý response của send_message"""
        status = response.get("status")
        
        if status == "ok":
            self.add_message(f"✅ {response.get('message', 'Tin nhắn đã được gửi')}", "success")
        elif status == "error":
            error_msg = response.get("message", "Lỗi không xác định")
            self.add_message(f"⚠️ Lỗi gửi tin nhắn: {error_msg}", "error")
            QMessageBox.critical(self, "Lỗi", f"Không thể gửi tin nhắn:\n{error_msg}")
            
        # Reset waiting state
        self.waiting_for_response = False
        self.response_callback = None
        self.send_btn.setEnabled(True)
        
    def reset_response_waiting(self):
        """Reset response waiting state (timeout)"""
        if self.waiting_for_response:
            self.waiting_for_response = False
            self.response_callback = None
            self.create_group_btn.setEnabled(True)
            self.send_btn.setEnabled(True)
            self.add_message("⏰ Timeout - không nhận được phản hồi từ server", "error")
            
    def closeEvent(self, event):
        """Xử lý khi đóng ứng dụng"""
        if self.is_connected:
            self.disconnect_from_server()
        event.accept()

def run_group_gui():
    """Function để chạy GUI version"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("PycTalk")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("PycTalk Team")
    
    # Create and show main window
    window = PycTalkGUIApp()
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_group_gui()