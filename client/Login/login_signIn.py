#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal, QTimer

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from UI.loginUI import ModernLoginUI
from Request.handle_request_client import request_handler

class LoginWorker(QThread):
    """Worker thread for handling login requests asynchronously"""
    login_result = pyqtSignal(dict)  # Emits login result
    
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        
    def run(self):
        """Execute login request in background thread"""
        try:
            # Send login request to server
            result = request_handler.login_request(self.username, self.password)
            self.login_result.emit(result)
        except Exception as e:
            self.login_result.emit({
                "success": False,
                "message": f"Lỗi kết nối: {str(e)}"
            })

class LoginController:
    """Controller for managing login process"""
    
    def __init__(self):
        self.ui = None
        self.login_worker = None
        self.app = None
        
    def initialize_ui(self):
        """Initialize the login UI"""
        self.app = QApplication(sys.argv)
        self.ui = ModernLoginUI()
        
        # Connect UI signals
        self.ui.login_requested.connect(self.handle_login_request)
        
        # Show the UI
        self.ui.show()
        
        return self.app
    
    def handle_login_request(self, username, password):
        """Handle login request from UI"""
        try:
            # Validate input
            if not username.strip() or not password.strip():
                self.show_error("Vui lòng nhập đầy đủ thông tin!")
                return
            
            # Disable login button during processing
            self.ui.login_button.setEnabled(False)
            self.ui.login_button.setText("Đang đăng nhập...")
            
            # Create and start login worker thread
            self.login_worker = LoginWorker(username, password)
            self.login_worker.login_result.connect(self.handle_login_result)
            self.login_worker.start()
            
        except Exception as e:
            self.show_error(f"Lỗi: {str(e)}")
            self.reset_login_button()
    
    def handle_login_result(self, result):
        """Handle login result from worker thread"""
        try:
            # Reset login button
            self.reset_login_button()
            
            if result.get("success", False):
                # Login successful
                user_data = result.get("user", {})
                self.show_success(
                    f"Đăng nhập thành công!\nChào mừng {user_data.get('username', 'User')}!"
                )
                
                # TODO: Open main chat window here
                # For now, we'll just close the login window
                QTimer.singleShot(2000, self.ui.close)  # Close after 2 seconds
                
            else:
                # Login failed
                error_message = result.get("message", "Đăng nhập thất bại")
                self.show_error(error_message)
                
        except Exception as e:
            self.show_error(f"Lỗi xử lý kết quả: {str(e)}")
            self.reset_login_button()
    
    def reset_login_button(self):
        """Reset login button to original state"""
        try:
            if self.ui and self.ui.login_button:
                self.ui.login_button.setEnabled(True)
                self.ui.login_button.setText("Đăng Nhập")
        except:
            pass
    
    def show_error(self, message):
        """Show error message to user"""
        try:
            if self.ui:
                msg_box = QMessageBox(self.ui)
                msg_box.setIcon(QMessageBox.Icon.Critical)
                msg_box.setWindowTitle("Lỗi đăng nhập")
                msg_box.setText(message)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()
        except:
            print(f"❌ {message}")
    
    def show_success(self, message):
        """Show success message to user"""
        try:
            if self.ui:
                msg_box = QMessageBox(self.ui)
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle("Thành công")
                msg_box.setText(message)
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()
        except:
            print(f"✅ {message}")
    
    def run(self):
        """Run the login application"""
        try:
            app = self.initialize_ui()
            
            # Set application properties
            app.setApplicationName("PycTalk")
            app.setApplicationVersion("1.0")
            app.setOrganizationName("PycTalk Team")
            
            # Run the application
            sys.exit(app.exec())
            
        except KeyboardInterrupt:
            print("\n⚡ Ứng dụng bị dừng bởi người dùng")
        except Exception as e:
            print(f"❌ Lỗi chạy ứng dụng: {e}")
        finally:
            # Cleanup
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.login_worker and self.login_worker.isRunning():
                self.login_worker.quit()
                self.login_worker.wait()
            
            # Close client connection
            request_handler.close_connection()
            
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

def main():
    """Main entry point"""
    print("🚀 Khởi động PycTalk Client...")
    
    # Create and run login controller
    controller = LoginController()
    controller.run()

if __name__ == "__main__":
    main()