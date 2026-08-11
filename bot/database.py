import sqlite3

DB = "database.db"




def connect():
    return sqlite3.connect(DB)


def init_db():
    db = connect()
    cur = db.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        wallet TEXT DEFAULT '',
        wallet_type TEXT DEFAULT '',
        admin INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS withdrawals(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        status TEXT
    )
    """)
        cur.execute("""
    CREATE TABLE IF NOT EXISTS news(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT
    )
    """)

    db.commit()
    db.close()



def add_user(uid):

    db=connect()
    cur=db.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (uid,)
    )

    db.commit()
    db.close()



def get_user(uid):

    db=connect()
    cur=db.cursor()

    cur.execute(
        "SELECT * FROM users WHERE id=?",
        (uid,)
    )

    user=cur.fetchone()

    db.close()

    return user



def make_admin(uid):

    db=connect()
    cur=db.cursor()

    cur.execute(
        "UPDATE users SET admin=1 WHERE id=?",
        (uid,)
    )

    db.commit()
    db.close()



def add_admin(uid):
    make_admin(uid)



def add_balance(uid, amount):

    db=connect()
    cur=db.cursor()

    cur.execute(
        "UPDATE users SET balance=balance+? WHERE id=?",
        (amount,uid)
    )

    db.commit()
    db.close()



def set_wallet(uid, typ, wallet):

    db=connect()
    cur=db.cursor()

    cur.execute(
        """
        UPDATE users
        SET wallet=?, wallet_type=?
        WHERE id=?
        """,
        (wallet,typ,uid)
    )

    db.commit()
    db.close()



def create_withdraw(uid,amount):

    db=connect()
    cur=db.cursor()

    cur.execute(
        """
        INSERT INTO withdrawals
        (user_id,amount,status)
        VALUES(?,?,?)
        """,
        (uid,amount,"pending")
    )

    db.commit()
    db.close()



def get_withdrawals():

    db=connect()
    cur=db.cursor()

    cur.execute(
        "SELECT * FROM withdrawals"
    )

    data=cur.fetchall()

    db.close()

    return data

def update_withdraw(id, status):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        UPDATE withdrawals
        SET status=?
        WHERE id=?
        """,
        (status, id)
    )

    db.commit()
    db.close()

def add_news(text):

    db = connect()
    cur = db.cursor()

    cur.execute(
        """
        INSERT INTO news(text)
        VALUES(?)
        """,
        (text,)
    )

    db.commit()
    db.close()


def get_news():

    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM news ORDER BY id DESC"
    )

    data = cur.fetchall()

    db.close()

    return dataй
