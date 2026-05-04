from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import webhook, admin
import uvicorn

app = FastAPI(
    title="Tezz Delivery Automation API",
    description="WhatsApp-based order automation for Cash & Carry kitchen business",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router, prefix="/webhook", tags=["WhatsApp Webhook"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"status": "Tezz Delivery Bot is running 🚀"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
