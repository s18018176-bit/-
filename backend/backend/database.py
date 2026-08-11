import sqlite3


DB = "worker.db"


def connect():
    return sqlite3.connect(DB)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 0,
        banned INTEGER DEFAULT 0,
        requisites TEXT
    )
    """)

    conn.commit()
    conn.close()


create_tables()
