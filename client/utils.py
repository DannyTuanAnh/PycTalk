import json

def encode_message(data: dict) -> bytes:
    return json.dumps(data).encode('utf-8')

def decode_message(data: bytes) -> dict:
    try:
        return json.loads(data.decode('utf-8'))
    except json.JSONDecodeError:
        return {}
