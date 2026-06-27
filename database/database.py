import sqlite3
import bcrypt

DB_NAME = "fieldapp.db"


# ==========================================
# الاتصال بقاعدة البيانات
# ==========================================

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# تشفير كلمات المرور
# ==========================================

def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


# ==========================================
# إنشاء الجداول
# ==========================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # جدول المستخدمين
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        fullname TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    ```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technician TEXT NOT NULL,
    task_number TEXT UNIQUE NOT NULL,
    subscription_number TEXT NOT NULL,
    task_type TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```


    conn.commit()
    conn.close()


# ==========================================
# المستخدمون الافتراضيون
# ==========================================

def create_default_users():

    conn = get_connection()
    cursor = conn.cursor()

    users = [

        ("admin", hash_password("1234"), "أحمد شاهين", "admin"),

        ("hani", hash_password("1111"), "هاني صلاح", "technician"),

        ("arslan", hash_password("1111"), "أرسلان", "technician"),

        ("omar", hash_password("1111"), "عمر", "technician"),

        ("borhan", hash_password("1111"), "برهان", "technician"),

        ("qasim", hash_password("1111"), "قاسم", "technician")

    ]

    for user in users:

        cursor.execute("""
        INSERT OR IGNORE INTO users
        (username, password, fullname, role)

        VALUES (?, ?, ?, ?)
        """, user)

    conn.commit()
    conn.close()


# ==========================================
# تسجيل الدخول
# ==========================================

def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if user:

        if verify_password(
                password,
                user["password"]):

            return user

    return None


# ==========================================
# إدارة المهام
# ==========================================

```python
def add_task(
        technician,
        task_number,
        subscription_number,
        task_type,
        notes):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tasks
    (
        technician,
        task_number,
        subscription_number,
        task_type,
        notes
    )

    VALUES (?, ?, ?, ?, ?)
    """, (

        technician,
        task_number,
        subscription_number,
        task_type,
        notes

    ))

    conn.commit()
    conn.close()
```


    cursor.execute("""
    INSERT INTO tasks
    (
        technician,
        task_number,
        subscription_number,
        status,
        notes
    )

    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        technician,
        task_number,
        subscription_number,
        status,
        notes
    )

    conn.commit()
    conn.close()


def get_all_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM tasks
    ORDER BY id DESC
    """)

    tasks = cursor.fetchall()

    conn.close()

    return tasks


def task_exists(task_number):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM tasks
    WHERE task_number = ?
    """, (task_number,))

    task = cursor.fetchone()

    conn.close()

    return task is not None


# ==========================================
# حذف مهمة
# ==========================================

def delete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM tasks
    WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# ==========================================
# تعديل مهمة
# ==========================================

def update_task(
        task_id,
        subscription_number,
        status,
        notes):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tasks

    SET
        subscription_number = ?,
        status = ?,
        notes = ?

    WHERE id = ?
    """, (
        subscription_number,
        status,
        notes,
        task_id
    ))

    conn.commit()
    conn.close()


# ==========================================
# إدارة المستخدمين
# ==========================================

def get_all_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, fullname, role
    FROM users
    ORDER BY fullname
    """)

    users = cursor.fetchall()

    conn.close()

    return users


def add_user(username, password, fullname, role):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users
    (username, password, fullname, role)

    VALUES (?, ?, ?, ?)
    """, (
        username,
        hash_password(password),
        fullname,
        role
    ))

    conn.commit()
    conn.close()


def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM users
    WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


# ==========================================
# تغيير كلمة المرور
# ==========================================

def change_password(user_id, new_password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(new_password)

    cursor.execute("""
    UPDATE users
    SET password = ?
    WHERE id = ?
    """, (
        hashed_password,
        user_id
    ))

    conn.commit()
    conn.close()
    