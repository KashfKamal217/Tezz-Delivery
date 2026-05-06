from fastapi import FastAPI
from app.routes import webhook
from dotenv import load_dotenv

load_dotenv()  # ADD THIS

app = FastAPI()

app.include_router(webhook.router)

@app.get("/")
def home():
    return {"message": "Tezz Delivery API is running 🚀"}

