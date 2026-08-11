import sqlite3


db = sqlite3.connect("bot.db")
cursor = db.cursor()


def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        wallet_type TEXT,
        wallet TEXT,
        balance INTEGER DEFAULT 0,
        is_admin INTEGER DEFAULT 0
    )
    """)
    db.commit()


def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (user_id,)
    )
    db.commit()


def get_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    )
    return cursor.fetchone()


def set_wallet(user_id, wtype, wallet):
    cursor.execute(
        """
        UPDATE users
        SET wallet_type=?, wallet=?
        WHERE id=?
        """,
        (wtype, wallet, user_id)
    )
    db.commit()


def make_admin(user_id):
    cursor.execute(
        "UPDATE users SET is_admin=1 WHERE id=?",
        (user_id,)
    )
    db.commit()


def admins():
    cursor.execute(
        "SELECT id FROM users WHERE is_admin=1"
    )
    return cursor.fetchall()


def all_users():
    cursor.execute(
        "SELECT * FROM users"
    )
    return cursor.fetchall()
