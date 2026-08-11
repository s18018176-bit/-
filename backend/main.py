from fastapi import FastAPI

app = FastAPI(
    title="Worker Panel API"
)


@app.get("/")
async def home():
    return {
        "status": "Worker Panel работает"
    }
