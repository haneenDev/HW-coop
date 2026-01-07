"""
نظام إدارة المستخدمين البسيط
هذا مشروع تعليمي لأغراض الواجب
"""

import hashlib
import sqlite3
from datetime import datetime

# ⚠️ ملاحظة: هذا المشروع يحتوي عمداً على بعض المشاكل الأمنية
# لأغراض التعلم وستكتشفها أدوات GitHub Security

class UserManager:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.connection = None
        
    def connect(self):
        """الاتصال بقاعدة البيانات"""
        self.connection = sqlite3.connect(self.db_name)
        self.create_table()
    
    def create_table(self):
        """إنشاء جدول المستخدمين"""
        cursor = self.connection.cursor()
        # استخدام SQL مباشر قد يسبب مشاكل أمنية
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TEXT
        )
        """
        cursor.execute(query)
        self.connection.commit()
    
    def hash_password(self, password):
        """تشفير كلمة المرور"""
        # استخدام MD5 (غير آمن - لأغراض تعليمية)
        return hashlib.md5(password.encode()).hexdigest()
    
    def add_user(self, username, password, email):
        """إضافة مستخدم جديد"""
        cursor = self.connection.cursor()
        hashed_password = self.hash_password(password)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # استخدام string formatting (قد يسبب SQL injection)
            query = f"INSERT INTO users (username, password, email, created_at) VALUES ('{username}', '{hashed_password}', '{email}', '{created_at}')"
            cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def login(self, username, password):
        """تسجيل دخول المستخدم"""
        cursor = self.connection.cursor()
        hashed_password = self.hash_password(password)
        
        # استخدام string formatting (مشكلة أمنية)
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{hashed_password}'"
        cursor.execute(query)
        user = cursor.fetchone()
        
        return user is not None
    
    def get_all_users(self):
        """الحصول على جميع المستخدمين"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, username, email, created_at FROM users")
        return cursor.fetchall()
    
    def close(self):
        """إغلاق الاتصال"""
        if self.connection:
            self.connection.close()


def main():
    """الدالة الرئيسية"""
    print("=== نظام إدارة المستخدمين ===")
    
    manager = UserManager()
    manager.connect()
    
    # مثال على الاستخدام
    print("\n1. إضافة مستخدم جديد")
    manager.add_user("ahmed", "password123", "ahmed@example.com")
    manager.add_user("sara", "mypassword", "sara@example.com")
    
    print("\n2. تسجيل الدخول")
    if manager.login("ahmed", "password123"):
        print("✅ تم تسجيل الدخول بنجاح")
    else:
        print("❌ فشل تسجيل الدخول")
    
    print("\n3. عرض جميع المستخدمين")
    users = manager.get_all_users()
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created: {user[3]}")
    
    manager.close()
    print("\n✅ تم الانتهاء")


if __name__ == "__main__":
    main()
