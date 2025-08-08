# PycTalk - Ứng dụng Chat Nhóm

## Mô tả
PycTalk là ứng dụng chat nhóm được phát triển bằng Python với giao diện PyQt6 và database MySQL.

## Tính năng chính
- 🔐 Đăng nhập/Đăng ký người dùng
- 💬 Chat 1-1 và chat nhóm
- 👥 Quản lý bạn bè
- 🎨 Giao diện hiện đại với gradient design
- 🔒 Bảo mật mật khẩu với SHA256

## Cấu trúc dự án
```
PycTalk/
├── client/                 # Client-side code
│   ├── Login/              # Xử lý đăng nhập
│   ├── UI/                 # Giao diện người dùng
│   └── Request/            # Xử lý request-response
├── server/                 # Server-side code
│   ├── Login_server/       # Xử lý đăng nhập server
│   └── main_server.py      # Server chính
├── database/               # Database utilities
│   └── db.py              # Kết nối database
└── README.md
```

## Yêu cầu hệ thống
- Python 3.8+
- PyQt6
- MySQL Server
- mysql-connector-python

## Cài đặt

### 1. Cài đặt dependencies
```bash
pip install PyQt6 mysql-connector-python
```

### 2. Thiết lập database
- Tạo database `pyctalk` trong MySQL
- Import schema và sample data

### 3. Chạy ứng dụng

#### Khởi động server:
```bash
cd server
python main_server.py
```

#### Khởi động client:
```bash
cd client/Login
python login_signIn.py
```

## Tác giả
- **Phương** - Developer trên nhánh Phuong
- **Team PycTalk** - Collaborative development

## Ghi chú phát triển
- Server chạy trên `localhost:9000`
- Database: `pyctalk` trên MySQL
- UI sử dụng modern gradient design với PyQt6

## TODO
- [ ] Implement main chat window
- [ ] Group chat functionality
- [ ] Friend management system
- [ ] File sharing feature
- [ ] Emoji support

---
*Phiên bản hiện tại: v1.0 - Nhánh Phuong Development*
