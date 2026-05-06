from fastapi import FastAPI
from dotenv import load_dotenv
import os

from app.routes.webhook import router as webhook_router

# Load env
load_dotenv()

print("VERIFY TOKEN:", os.getenv("VERIFY_TOKEN"))

# FastAPI app
app = FastAPI()

# register webhook routes
app.include_router(webhook_router)


@app.get("/")
def home():
    return {"message": "Tezz Delivery API running"}