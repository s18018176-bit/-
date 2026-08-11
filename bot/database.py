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
        is_admin INTEGER DEFAULT 0
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bots(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS top(
        id INTEGER PRIMARY KEY,
        text TEXT
    )
    """)

    db.commit()
    db.close()


# USERS

def add_user(user_id):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (user_id,)
    )

    db.commit()
    db.close()


def get_user(user_id):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    )

    user = cur.fetchone()

    db.close()
    return user


# ADMINS

def add_admin(user_id):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "UPDATE users SET is_admin=1 WHERE id=?",
        (user_id,)
    )

    db.commit()
    db.close()


# NEWS

def add_news(text):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO news(text) VALUES(?)",
        (text,)
    )

    db.commit()
    db.close()


def get_news():
    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT text FROM news ORDER BY id DESC"
    )

    data = cur.fetchall()

    db.close()

    return [x[0] for x in data]


# BOTS

def add_bot(text):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO bots(text) VALUES(?)",
        (text,)
    )

    db.commit()
    db.close()


def get_bots():
    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT text FROM bots ORDER BY id DESC"
    )

    data = cur.fetchall()

    db.close()

    return [x[0] for x in data]


# TOP

def set_top(text):
    db = connect()
    cur = db.cursor()

    cur.execute("DELETE FROM top")

    cur.execute(
        "INSERT INTO top(id,text) VALUES(1,?)",
        (text,)
    )

    db.commit()
    db.close()


def get_top():
    db = connect()
    cur = db.cursor()

    cur.execute(
        "SELECT text FROM top WHERE id=1"
    )

    data = cur.fetchone()

    db.close()

    return data[0] if data else "Топ пока пуст"


# WITHDRAW

def get_withdrawals():
    db = connect()
    cur = db.cursor()

    cur.execute("SELECT * FROM withdrawals")

    data = cur.fetchall()

    db.close()

    return data


def update_withdraw(id, status):
    db = connect()
    cur = db.cursor()

    cur.execute(
        "UPDATE withdrawals SET status=? WHERE id=?",
        (status, id)
    )

    db.commit()
    db.close()


init_db()
