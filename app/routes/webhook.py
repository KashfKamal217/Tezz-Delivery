from fastapi import APIRouter, Request, Body
from fastapi.responses import PlainTextResponse
import os

from app.services.order_flow import handle_user_message
from app.services.notification import send_whatsapp_message

router = APIRouter()

# TEMP MEMORY (replace with DB later)
user_state = {}

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


# --------------------------------------------------
# 1. WEBHOOK VERIFICATION (GET)
# --------------------------------------------------
@router.get("/webhook")
async def verify_webhook(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Forbidden", status_code=403)


# --------------------------------------------------
# 2. WHATSAPP MESSAGE RECEIVER (POST)
# --------------------------------------------------
@router.post("/webhook")
async def whatsapp_webhook(data: dict = Body(...)):

    try:
        entry = data.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})

        message = value.get("messages", [{}])[0]
        user_id = message.get("from")
        text = message.get("text", {}).get("body")

        if not user_id or not text:
            return {"status": "no_message"}

    except Exception as e:
        print("Webhook parsing error:", e)  # ✅ DEBUG ADDED
        return {"status": "error_parsing"}

    # -----------------------------
    # STATE MANAGEMENT
    # -----------------------------
    user_data = user_state.get(user_id, {
        "state": "GREETING",
        "address": None,
        "lang": "en"   # ✅ ADDED (language support)
    })

    state = user_data["state"]

    # -----------------------------
    # PROCESS MESSAGE (CORE LOGIC)
    # -----------------------------
    response, new_state, updated_data = handle_user_message(
        user_id,
        text,
        state,
        user_data
    )

    # -----------------------------
    # SAVE STATE
    # -----------------------------
    updated_data["state"] = new_state
    user_state[user_id] = updated_data

    # -----------------------------
    # SEND REPLY TO WHATSAPP
    # -----------------------------
    await send_whatsapp_message(user_id, response)

    return {"status": "ok"}