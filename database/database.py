import sqlite3

DB_NAME = "fieldapp.db"


# الاتصال بقاعدة البيانات
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# إنشاء الجداول
def create_tables():
    conn = get_connection()
    c = conn.cursor()

    # جدول المستخدمين
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fullname TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # جدول المهام
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technician TEXT NOT NULL,
            task_number TEXT UNIQUE NOT NULL,
            subscription_number TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# إنشاء المستخدمين الافتراضيين
def create_default_users():
    conn = get_connection()
    c = conn.cursor()

    users = [
        ("admin", "1234", "أحمد شاهين", "admin"),
        ("hani", "1234", "هاني صلاح", "technician"),
        ("arslan", "1234", "أرسلان", "technician"),
        ("omar", "1234", "عمر", "technician"),
        ("borhan", "1234", "برهان", "technician"),
        ("qasim", "1234", "قاسم", "technician")
    ]

    for user in users:
        c.execute("""
            INSERT OR IGNORE INTO users
            (username, password, fullname, role)
            VALUES (?, ?, ?, ?)
        """, user)

    conn.commit()
    conn.close()


# تسجيل الدخول
def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM users
        WHERE username = ? AND password = ?
    """, (username, password))

    user = c.fetchone()

    conn.close()

    return user


# إضافة مهمة جديدة
def add_task(technician, task_number,
             subscription_number, status, notes):

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO tasks
        (technician, task_number,
         subscription_number, status, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        technician,
        task_number,
        subscription_number,
        status,
        notes
    ))

    conn.commit()
    conn.close()


# التحقق من وجود المهمة
def task_exists(task_number):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT id FROM tasks WHERE task_number = ?",
        (task_number,)
    )

    exists = c.fetchone() is not None

    conn.close()

    return exists


# جلب جميع المهام
def get_all_tasks():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM tasks
        ORDER BY id DESC
    """)

    tasks = c.fetchall()

    conn.close()

    return tasks


# جلب جميع المستخدمين
def get_all_users():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT id,
               username,
               fullname,
               role
        FROM users
        ORDER BY fullname
    """)

    users = c.fetchall()

    conn.close()

    return users


# تغيير كلمة المرور
def change_password(username, new_password):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        UPDATE users
        SET password = ?
        WHERE username = ?
    """, (new_password, username))

    conn.commit()
    conn.close()
    
