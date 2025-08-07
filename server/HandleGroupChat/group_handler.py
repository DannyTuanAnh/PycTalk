from database.db import db
from datetime import datetime

class GroupHandler:
    def __init__(self):
        pass
    
    def create_group(self, group_name: str, created_by: int) -> dict:
        """Tạo nhóm chat mới"""
        try:
            # Kiểm tra user tồn tại
            user_exists = db.fetch_one("SELECT id FROM users WHERE id = %s", (created_by,))
            if not user_exists:
                return {"success": False, "message": "User không tồn tại"}
            
            # Tạo nhóm mới
            db.execute(
                "INSERT INTO group_chat (group_name, created_by) VALUES (%s, %s)",
                (group_name, created_by)
            )
            
            # Lấy group_id vừa tạo
            group = db.fetch_one(
                "SELECT group_id FROM group_chat WHERE group_name = %s AND created_by = %s ORDER BY group_id DESC LIMIT 1",
                (group_name, created_by)
            )
            
            if not group:
                return {"success": False, "message": "Không thể tạo nhóm"}
            
            group_id = group["group_id"]
            
            # Thêm người tạo vào nhóm
            db.execute(
                "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)",
                (group_id, created_by)
            )
            
            return {
                "success": True, 
                "message": "Tạo nhóm thành công", 
                "group_id": group_id,
                "group_name": group_name
            }
            
        except Exception as e:
            return {"success": False, "message": f"Lỗi tạo nhóm: {str(e)}"}
    
    def add_member_to_group(self, group_id: int, user_id: int, admin_id: int) -> dict:
        """Thêm thành viên vào nhóm"""
        try:
            print(f"🔧 Starting add_member_to_group: group_id={group_id}, user_id={user_id}, admin_id={admin_id}")
            
            # Kiểm tra admin có quyền (là thành viên của nhóm)
            admin_check = db.fetch_one(
                "SELECT * FROM group_members WHERE group_id = %s AND user_id = %s",
                (group_id, admin_id)
            )
            print(f"🔧 Admin check result: {admin_check}")
            if not admin_check:
                return {"success": False, "message": "Bạn không có quyền thêm thành viên vào nhóm này"}
            
            # Kiểm tra user tồn tại
            user_exists = db.fetch_one("SELECT id FROM users WHERE id = %s", (user_id,))
            print(f"🔧 User exists check: {user_exists}")
            if not user_exists:
                return {"success": False, "message": "User không tồn tại"}
            
            # Kiểm tra user đã trong nhóm chưa
            member_exists = db.fetch_one(
                "SELECT * FROM group_members WHERE group_id = %s AND user_id = %s",
                (group_id, user_id)
            )
            print(f"🔧 Member exists check: {member_exists}")
            if member_exists:
                return {"success": False, "message": "User đã là thành viên của nhóm"}
            
            # Thêm thành viên
            db.execute(
                "INSERT INTO group_members (group_id, user_id) VALUES (%s, %s)",
                (group_id, user_id)
            )
            print(f"🔧 Member added successfully")
            
            return {"success": True, "message": "Thêm thành viên thành công"}
            
        except Exception as e:
            print(f"🔧 Error in add_member_to_group: {str(e)}")
            return {"success": False, "message": f"Lỗi thêm thành viên: {str(e)}"}
    
    def send_group_message(self, sender_id: int, group_id: int, content: str) -> dict:
        """Gửi tin nhắn trong nhóm"""
        try:
            # Kiểm tra sender có trong nhóm không
            member_check = db.fetch_one(
                "SELECT * FROM group_members WHERE group_id = %s AND user_id = %s",
                (group_id, sender_id)
            )
            if not member_check:
                return {"success": False, "message": "Bạn không phải thành viên của nhóm này"}
            
            # Lưu tin nhắn vào database
            db.execute(
                "INSERT INTO group_messages (sender_id, group_id, content) VALUES (%s, %s, %s)",
                (sender_id, group_id, content)
            )
            
            # Lấy thông tin tin nhắn vừa gửi
            message = db.fetch_one(
                """SELECT gm.message_group_id, gm.sender_id, gm.group_id, gm.content, 
                          gm.time_send, u.username as sender_name
                   FROM group_messages gm 
                   JOIN users u ON gm.sender_id = u.id 
                   WHERE gm.sender_id = %s AND gm.group_id = %s 
                   ORDER BY gm.message_group_id DESC LIMIT 1""",
                (sender_id, group_id)
            )
            
            if not message:
                return {"success": False, "message": "Không thể lấy thông tin tin nhắn"}
            
            return {
                "success": True, 
                "message": "Gửi tin nhắn thành công",
                "message_data": {
                    "message_id": message["message_group_id"],
                    "sender_id": message["sender_id"],
                    "sender_name": message["sender_name"],
                    "group_id": message["group_id"],
                    "content": message["content"],
                    "time_send": message["time_send"].isoformat() if message["time_send"] else None
                }
            }
            
        except Exception as e:
            return {"success": False, "message": f"Lỗi gửi tin nhắn: {str(e)}"}
    
    def get_group_messages(self, group_id: int, user_id: int, limit: int = 50) -> dict:
        """Lấy tin nhắn trong nhóm"""
        try:
            # Kiểm tra user có trong nhóm không
            member_check = db.fetch_one(
                "SELECT * FROM group_members WHERE group_id = %s AND user_id = %s",
                (group_id, user_id)
            )
            if not member_check:
                return {"success": False, "message": "Bạn không phải thành viên của nhóm này"}
            
            # Lấy tin nhắn
            messages = db.fetch_all(
                """SELECT gm.message_group_id, gm.sender_id, gm.group_id, gm.content, 
                          gm.time_send, u.username as sender_name
                   FROM group_messages gm 
                   JOIN users u ON gm.sender_id = u.id 
                   WHERE gm.group_id = %s 
                   ORDER BY gm.time_send DESC LIMIT %s""",
                (group_id, limit)
            )
            
            # Chuyển đổi datetime thành string
            message_list = []
            for msg in messages:
                message_list.append({
                    "message_id": msg["message_group_id"],
                    "sender_id": msg["sender_id"],
                    "sender_name": msg["sender_name"],
                    "group_id": msg["group_id"],
                    "content": msg["content"],
                    "time_send": msg["time_send"].isoformat() if msg["time_send"] else None
                })
            
            return {
                "success": True,
                "messages": message_list
            }
            
        except Exception as e:
            return {"success": False, "message": f"Lỗi lấy tin nhắn: {str(e)}"}
    
    def get_user_groups(self, user_id: int) -> dict:
        """Lấy danh sách nhóm của user"""
        try:
            groups = db.fetch_all(
                """SELECT gc.group_id, gc.group_name, gc.created_by, u.username as creator_name
                   FROM group_chat gc
                   JOIN group_members gm ON gc.group_id = gm.group_id
                   JOIN users u ON gc.created_by = u.id
                   WHERE gm.user_id = %s""",
                (user_id,)
            )
            
            return {
                "success": True,
                "groups": [
                    {
                        "group_id": group["group_id"],
                        "group_name": group["group_name"],
                        "created_by": group["created_by"],
                        "creator_name": group["creator_name"]
                    }
                    for group in groups
                ]
            }
            
        except Exception as e:
            return {"success": False, "message": f"Lỗi lấy danh sách nhóm: {str(e)}"}
    
    def get_group_members(self, group_id: int, user_id: int) -> dict:
        """Lấy danh sách thành viên nhóm"""
        try:
            print(f"🔧 Starting get_group_members: group_id={group_id}, user_id={user_id}")
            
            # Kiểm tra user có trong nhóm không
            member_check = db.fetch_one(
                "SELECT * FROM group_members WHERE group_id = %s AND user_id = %s",
                (group_id, user_id)
            )
            print(f"🔧 Member check result: {member_check}")
            if not member_check:
                return {"success": False, "message": "Bạn không phải thành viên của nhóm này"}
            
            # Lấy danh sách thành viên
            members = db.fetch_all(
                """SELECT u.id, u.username, u.email
                   FROM users u
                   JOIN group_members gm ON u.id = gm.user_id
                   WHERE gm.group_id = %s""",
                (group_id,)
            )
            print(f"🔧 Found {len(members)} members: {members}")
            
            result = {
                "success": True,
                "members": [
                    {
                        "user_id": member["id"],
                        "username": member["username"],
                        "email": member["email"]
                    }
                    for member in members
                ]
            }
            print(f"🔧 Returning result: {result}")
            return result
            
        except Exception as e:
            print(f"🔧 Error in get_group_members: {str(e)}")
            return {"success": False, "message": f"Lỗi lấy danh sách thành viên: {str(e)}"}

# Instance để sử dụng
group_handler = GroupHandler()
