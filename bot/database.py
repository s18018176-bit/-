import sqlite3


db = sqlite3.connect("bot.db")
cursor = db.cursor()


def init_db():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        wallet_type TEXT,
        wallet TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS withdrawals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        status TEXT DEFAULT 'pending'
    )
    """)

    db.commit()



def add_user(uid):

    cursor.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (uid,)
    )

    db.commit()



def get_user(uid):

    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (uid,)
    )

    return cursor.fetchone()



def add_balance(uid, amount):

    cursor.execute(
        """
        UPDATE users
        SET balance = balance + ?
        WHERE id=?
        """,
        (amount, uid)
    )

    db.commit()



def set_wallet(uid, wtype, wallet):

    cursor.execute(
        """
        UPDATE users
        SET wallet_type=?, wallet=?
        WHERE id=?
        """,
        (wtype, wallet, uid)
    )

    db.commit()



def make_admin(uid):

    add_user(uid)

    cursor.execute(
        """
        UPDATE users
        SET is_admin=1
        WHERE id=?
        """,
        (uid,)
    )

    db.commit()



def create_withdraw(uid, amount):

    cursor.execute(
        """
        INSERT INTO withdrawals(user_id,amount)
        VALUES(?,?)
        """,
        (uid, amount)
    )

    db.commit()



def get_withdrawals():

    cursor.execute(
        """
        SELECT * FROM withdrawals
        WHERE status='pending'
        """
    )

    return cursor.fetchall()



def update_withdraw(wid,status):

    cursor.execute(
        """
        UPDATE withdrawals
        SET status=?
        WHERE id=?
        """,
        (status,wid)
    )

    db.commit()



def users():

    cursor.execute(
        "SELECT * FROM users"
    )

    return cursor.fetchall()
