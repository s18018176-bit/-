from fastapi import FastAPI
from database import connect

app = FastAPI(
    title="Worker Panel API"
)


@app.get("/")
async def home():
    return {
        "status": "Worker Panel работает"
    }


@app.get("/users")
async def users():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    conn.close()

    return {
        "users": data
    }
