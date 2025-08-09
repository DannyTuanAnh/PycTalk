# 🚀 Hướng dẫn chạy PycTalk Group Chat

## 📋 Yêu cầu hệ thống

- Python 3.7+
- MySQL Server
- PyQt6 (cho GUI)

## ⚙️ Thiết lập

### 1. Cài đặt dependencies

```bash
pip install PyQt6 mysql-connector-python
```

### 2. Thiết lập MySQL Database

1. Tạo database và chạy schema:

```sql
-- Chạy file database/schema.sql trong MySQL
source database/schema.sql;
```

2. Cập nhật thông tin kết nối database trong `database/db.py`:

```python
# Sửa thông tin connection phù hợp với MySQL của bạn
def __init__(self, host="localhost", user="root", password="YOUR_PASSWORD", database="pyctalk"):
```

## 🖥️ Chạy Server

### Bước 1: Khởi động server

**Cách 1: Chạy từ thư mục gốc (Khuyến nghị)**

```bash
# Từ thư mục PycTalk-main
python -m server.main_server
```

**Cách 2: Chạy trực tiếp**

```bash
cd server
python main_server.py
```

Server sẽ chạy trên `127.0.0.1:9000`

## 🧪 Test chức năng Group Chat

### Option 1: Test với script tự động

```bash
# Từ thư mục gốc
python test_group_chat.py
```

### Option 2: Test với GUI Client

```bash
cd client
python main.py
```

## 📱 Sử dụng GUI Client

### 1. Đăng ký/Đăng nhập

- Mở ứng dụng client
- Đăng ký tài khoản mới hoặc đăng nhập
- Username, password, email

### 2. Sử dụng Group Chat

1. **Tạo nhóm mới:**

   - Click "Group Chat" từ main window
   - Click "Tạo nhóm"
   - Nhập tên nhóm

2. **Thêm thành viên:**

   - Chọn nhóm từ danh sách
   - Click "Thêm thành viên"
   - Nhập User ID của người muốn thêm

3. **Chat trong nhóm:**

   - Chọn nhóm từ danh sách
   - Nhập tin nhắn ở khung phía dưới
   - Enter hoặc click "Gửi"

4. **Xem thành viên:**

   - Click "Xem thành viên" để xem danh sách

5. **Làm mới:**
   - Click "Làm mới" để cập nhật tin nhắn mới

## 🔧 API Endpoints (Server)

Server hỗ trợ các action sau:

### Group Management

- `create_group` - Tạo nhóm mới
- `add_member_to_group` - Thêm thành viên vào nhóm
- `get_user_groups` - Lấy danh sách nhóm của user
- `get_group_members` - Lấy danh sách thành viên nhóm

### Messaging

- `send_group_message` - Gửi tin nhắn trong nhóm
- `get_group_messages` - Lấy tin nhắn trong nhóm

### Example Request Format:

```json
{
  "action": "create_group",
  "data": {
    "group_name": "My Group",
    "user_id": 1
  }
}
```

## 🐛 Troubleshooting

### Lỗi Import "No module named 'server'"

```bash
# Đảm bảo bạn đang ở thư mục gốc PycTalk-main
cd PycTalk-main
python -m server.main_server

# Hoặc chạy trực tiếp:
cd server
python main_server.py
```

### Lỗi kết nối MySQL

- Kiểm tra MySQL service đã chạy
- Kiểm tra username/password trong `database/db.py`
- Kiểm tra database `pyctalk` đã tồn tại

### Lỗi import PyQt6

```bash
pip install PyQt6
```

### Server không khởi động

- Kiểm tra port 9000 có bị chiếm dụng
- Kiểm tra firewall settings

### Client không kết nối được

- Đảm bảo server đã chạy trước
- Kiểm tra IP và port trong client config

## 📚 Cấu trúc Database

### Tables:

- `users` - Thông tin người dùng
- `group_chat` - Thông tin nhóm chat
- `group_members` - Thành viên trong nhóm
- `group_messages` - Tin nhắn trong nhóm

## 🎯 Các tính năng đã hoàn thành

✅ Tạo nhóm chat
✅ Thêm/xóa thành viên
✅ Gửi/nhận tin nhắn nhóm
✅ Xem lịch sử chat
✅ GUI PyQt6
✅ MySQL Database
✅ TCP Server-Client

## 📝 Test Cases đã kiểm tra

1. ✅ Đăng ký/Đăng nhập user
2. ✅ Tạo nhóm chat
3. ✅ Thêm thành viên vào nhóm
4. ✅ Gửi tin nhắn trong nhóm
5. ✅ Lấy danh sách tin nhắn
6. ✅ Xem thành viên nhóm
7. ✅ Xem danh sách nhóm của user

Chức năng Group Chat đã hoàn tất và sẵn sàng sử dụng! 🎉
