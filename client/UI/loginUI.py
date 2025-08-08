#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QSpacerItem, 
                             QSizePolicy, QGraphicsDropShadowEffect, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPalette, QColor

class ModernLoginUI(QWidget):
    # Signals for login events
    login_requested = pyqtSignal(str, str)  # username, password
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the modern gradient login interface"""
        self.setWindowTitle("PycTalk - Đăng Nhập")
        self.setFixedSize(400, 500)
        self.setStyleSheet(self.get_main_style())
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create login card
        self.create_login_card(main_layout)
        
        # Center window on screen
        self.center_on_screen()
        
    def create_login_card(self, parent_layout):
        """Create the main login card with gradient background"""
        # Login card frame
        login_card = QFrame()
        login_card.setObjectName("loginCard")
        login_card.setStyleSheet(self.get_card_style())
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 5)
        login_card.setGraphicsEffect(shadow)
        
        # Card layout
        card_layout = QVBoxLayout(login_card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(25)
        
        # Header section
        self.create_header(card_layout)
        
        # Form section
        self.create_form(card_layout)
        
        # Button section
        self.create_buttons(card_layout)
        
        # Footer section
        self.create_footer(card_layout)
        
        # Add to parent with margins
        container_layout = QVBoxLayout()
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        container_layout.addWidget(login_card)
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        
        container_widget = QWidget()
        container_widget.setLayout(container_layout)
        parent_layout.addWidget(container_widget)
        
    def create_header(self, layout):
        """Create header with app logo and title"""
        # App title
        title = QLabel("PycTalk")
        title.setObjectName("appTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Subtitle
        subtitle = QLabel("Đăng nhập vào tài khoản của bạn")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
    def create_form(self, layout):
        """Create login form with username and password fields"""
        # Username field
        username_label = QLabel("Tên đăng nhập")
        username_label.setObjectName("fieldLabel")
        
        self.username_input = QLineEdit()
        self.username_input.setObjectName("modernInput")
        self.username_input.setPlaceholderText("Nhập tên đăng nhập...")
        self.username_input.setMinimumHeight(45)
        
        # Password field
        password_label = QLabel("Mật khẩu")
        password_label.setObjectName("fieldLabel")
        
        self.password_input = QLineEdit()
        self.password_input.setObjectName("modernInput")
        self.password_input.setPlaceholderText("Nhập mật khẩu...")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Ghi nhớ đăng nhập")
        self.remember_checkbox.setObjectName("modernCheckbox")
        
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.remember_checkbox)
        
    def create_buttons(self, layout):
        """Create login and signup buttons"""
        # Login button
        self.login_button = QPushButton("Đăng Nhập")
        self.login_button.setObjectName("loginButton")
        self.login_button.setMinimumHeight(45)
        self.login_button.clicked.connect(self.handle_login)
        
        # Forgot password link
        forgot_link = QLabel('<a href="#" style="color: #6C5CE7;">Quên mật khẩu?</a>')
        forgot_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        forgot_link.setObjectName("linkLabel")
        
        layout.addWidget(self.login_button)
        layout.addWidget(forgot_link)
        
    def create_footer(self, layout):
        """Create footer with signup link"""
        # Spacer
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        
        # Signup section
        signup_layout = QHBoxLayout()
        signup_label = QLabel("Chưa có tài khoản?")
        signup_label.setObjectName("footerLabel")
        
        signup_link = QLabel('<a href="#" style="color: #6C5CE7; font-weight: bold;">Đăng ký ngay</a>')
        signup_link.setObjectName("linkLabel")
        
        signup_layout.addStretch()
        signup_layout.addWidget(signup_label)
        signup_layout.addWidget(signup_link)
        signup_layout.addStretch()
        
        layout.addLayout(signup_layout)
        
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_error("Vui lòng nhập đầy đủ thông tin!")
            return
            
        # Emit login signal
        self.login_requested.emit(username, password)
        
    def show_error(self, message):
        """Show error message"""
        # You can implement a more sophisticated error display here
        print(f"❌ Lỗi: {message}")
        
    def show_success(self, message):
        """Show success message"""
        print(f"✅ {message}")
        
    def center_on_screen(self):
        """Center the window on screen"""
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def get_main_style(self):
        """Return main window stylesheet with gradient background"""
        return """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """
        
    def get_card_style(self):
        """Return login card stylesheet"""
        return """
            #loginCard {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            #appTitle {
                font-size: 32px;
                font-weight: bold;
                color: #2D3436;
                margin-bottom: 5px;
            }
            
            #subtitle {
                font-size: 14px;
                color: #636E72;
                margin-bottom: 20px;
            }
            
            #fieldLabel {
                font-size: 13px;
                font-weight: 600;
                color: #2D3436;
                margin-bottom: 5px;
            }
            
            #modernInput {
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                padding: 12px 15px;
                font-size: 14px;
                background: white;
                color: #2D3436;
            }
            
            #modernInput:focus {
                border: 2px solid #6C5CE7;
                outline: none;
            }
            
            #modernInput:hover {
                border: 2px solid #A8A8A8;
            }
            
            #modernCheckbox {
                font-size: 13px;
                color: #636E72;
                margin: 10px 0;
            }
            
            #modernCheckbox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid #E0E0E0;
                background: white;
            }
            
            #modernCheckbox::indicator:checked {
                background: #6C5CE7;
                border: 2px solid #6C5CE7;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDUuNUw0IDhMMTEgMSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            }
            
            #loginButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6C5CE7, stop:1 #A29BFE);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                margin-top: 10px;
            }
            
            #loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B4CE3, stop:1 #9189FA);
            }
            
            #loginButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5A4FCF, stop:1 #8B7FF6);
            }
            
            #linkLabel {
                font-size: 13px;
                margin-top: 10px;
            }
            
            #linkLabel a {
                text-decoration: none;
            }
            
            #linkLabel a:hover {
                text-decoration: underline;
            }
            
            #footerLabel {
                font-size: 13px;
                color: #636E72;
            }
        """

# Test function to run the UI standalone
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    login_ui = ModernLoginUI()
    login_ui.show()
    
    sys.exit(app.exec())