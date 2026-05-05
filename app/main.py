from fastapi import FastAPI
from dotenv import load_dotenv
import os

# -----------------------------
# LOAD ENV FIRST (VERY IMPORTANT)
# -----------------------------
load_dotenv()

from app.routes import webhook  # import AFTER dotenv

app = FastAPI()

# include routes
app.include_router(webhook.router)


@app.get("/")
def home():
    return {"message": "Tezz Delivery API is running 🚀"}

