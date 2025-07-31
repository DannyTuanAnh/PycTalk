# server/group_handler.py

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
from db import db_instance  # Sử dụng database instance

def create_group(data, sender_socket):
    print(f"🔍 DEBUG: create_group called with data: {data}")
    group_name = data.get("group_name")
    members = data.get("members")

    if not group_name or not members or len(members) < 2:
        response = {
            "status": "error",
            "message": "Cần ít nhất 2 thành viên để tạo nhóm"
        }
        print(f"🔍 DEBUG: Sending error response: {response}")
        sender_socket.send(json.dumps(response).encode())
        return

    # Kiểm tra xem tất cả members có tồn tại không
    invalid_users = [user for user in members if not db_instance.user_exists(user)]
    if invalid_users:
        response = {
            "status": "error",
            "message": f"Không tìm thấy user: {', '.join(invalid_users)}"
        }
        print(f"🔍 DEBUG: Sending invalid users response: {response}")
        sender_socket.send(json.dumps(response).encode())
        return

    group_id = db_instance.create_group(group_name, members)
    if not group_id:
        response = {
            "status": "error",
            "message": "Tạo nhóm thất bại"
        }
        print(f"🔍 DEBUG: Sending create failed response: {response}")
        sender_socket.send(json.dumps(response).encode())
        return

    response = {
        "status": "ok",
        "group_id": group_id,
        "message": f"Đã tạo nhóm '{group_name}'"
    }
    print(f"🔍 DEBUG: Sending success response: {response}")
    sender_socket.send(json.dumps(response).encode())

def send_group_message(data, sender_socket, memory_store):
    group_id = data.get("group_id")
    sender = data.get("sender")
    message = data.get("message")

    if not all([group_id, sender, message]):
        sender_socket.send(json.dumps({
            "status": "error",
            "message": "Thiếu thông tin: group_id, sender hoặc message"
        }).encode())
        return

    sender_id = db_instance.get_user_id(sender)
    if sender_id is None:
        sender_socket.send(json.dumps({
            "status": "error",
            "message": "Người gửi không tồn tại"
        }).encode())
        return

    # Kiểm tra sender có trong nhóm không
    if not db_instance.is_user_in_group(sender_id, group_id):
        sender_socket.send(json.dumps({
            "status": "error",
            "message": "Bạn không thuộc nhóm này"
        }).encode())
        return

    member_ids = db_instance.get_group_members(group_id)
    group_name = db_instance.get_group_name(group_id)

    # Gửi tin nhắn đến tất cả các thành viên trong nhóm (trừ người gửi)
    sent_count = 0
    for uid in member_ids:
        receiver_username = db_instance.get_username_by_id(uid)
        if not receiver_username:
            continue
            
        sock = memory_store.get_socket_by_username(receiver_username)
        if sock and sock != sender_socket:
            try:
                sock.send(json.dumps({
                    "type": "group_message",
                    "group_id": group_id,
                    "group_name": group_name,
                    "sender": sender,
                    "message": message
                }).encode())
                sent_count += 1
            except:
                # Socket có thể đã đóng
                pass

    # Gửi confirmation cho người gửi
    sender_socket.send(json.dumps({
        "status": "ok",
        "message": f"Đã gửi tin nhắn đến {sent_count} thành viên"
    }).encode())
