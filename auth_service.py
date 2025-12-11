import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'cpe101finalproject'))
from firebase_config import auth

def register_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"success": True, "uid": user.uid}
    except Exception as e:
        error_msg = str(e)
        
        # แปลง error messages เป็นข้อความที่เป็นมิตรกว่า
        if "EMAIL_EXISTS" in error_msg or "email already exists" in error_msg.lower():
            return {"success": False, "error": "อีเมลนี้ถูกใช้งานแล้ว กรุณาใช้อีเมลอื่นหรือเข้าสู่ระบบ"}
        elif "INVALID_EMAIL" in error_msg or "invalid email" in error_msg.lower():
            return {"success": False, "error": "รูปแบบอีเมลไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง"}
        elif "WEAK_PASSWORD" in error_msg or "password" in error_msg.lower() and "weak" in error_msg.lower():
            return {"success": False, "error": "รหัสผ่านอ่อนแอเกินไป ควรมีอย่างน้อย 6 ตัวอักษร"}
        elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_msg:
            return {"success": False, "error": "มีการพยายามสมัครสมาชิกบ่อยเกินไป กรุณาลองใหม่ในภายหลัง"}
        else:
            return {"success": False, "error": f"ไม่สามารถสมัครสมาชิกได้: {error_msg}"}

def login_user(id_token):
    try:
        decoded = auth.verify_id_token(id_token)
        return {"success": True, "uid": decoded["uid"]}
    except Exception as e:
        error_msg = str(e)
        
        # แปลง error messages เป็นข้อความที่เป็นมิตรกว่า
        if "INVALID_ID_TOKEN" in error_msg or "invalid" in error_msg.lower() and "token" in error_msg.lower():
            return {"success": False, "error": "Token ไม่ถูกต้อง กรุณาเข้าสู่ระบบอีกครั้ง"}
        elif "EXPIRED_ID_TOKEN" in error_msg or "expired" in error_msg.lower():
            return {"success": False, "error": "Token หมดอายุแล้ว กรุณาเข้าสู่ระบบอีกครั้ง"}
        else:
            return {"success": False, "error": f"ไม่สามารถเข้าสู่ระบบได้: {error_msg}"}

def verify_token(id_token):
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded["uid"]
    except:
        return None
