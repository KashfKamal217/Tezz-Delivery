from fastapi import APIRouter, Request, Body
from fastapi.responses import PlainTextResponse
import os

from app.services.order_flow import handle_user_message
from app.services.notification import send_whatsapp_message

router = APIRouter()

# -----------------------------
# TEMP MEMORY (replace with Redis later)
# -----------------------------
user_state = {}

# IMPORTANT: ensure .env is loaded in main.py
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


# --------------------------------------------------
# 1. WEBHOOK VERIFICATION (GET)
# --------------------------------------------------
@router.get("/webhook")
async def verify_webhook(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print("MODE:", mode)
    print("TOKEN FROM META:", token)
    print("TOKEN FROM ENV:", VERIFY_TOKEN)

    # Meta verification check
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge, status_code=200)

    return PlainTextResponse("Forbidden", status_code=403)


# --------------------------------------------------
# 2. WHATSAPP MESSAGE RECEIVER (POST)
# --------------------------------------------------
@router.post("/webhook")
async def whatsapp_webhook(data: dict = Body(...)):

    try:
        # -----------------------------
        # SAFE EXTRACTION (Meta format)
        # -----------------------------
        entry = data.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})

        messages = value.get("messages")

        # Ignore non-message events (status updates, etc.)
        if not messages:
            return {"status": "no_message"}

        message = messages[0]
        user_id = message.get("from")
        text = message.get("text", {}).get("body")

        # Safety check
        if not user_id or not text:
            return {"status": "invalid_message"}

    except Exception as e:
        print(" PARSING ERROR:", str(e))
        return {"status": "error_parsing"}

    # -----------------------------
    # USER STATE INIT
    # -----------------------------
    user_data = user_state.get(user_id, {
        "state": "GREETING",
        "address": None
    })

    state = user_data["state"]

    # -----------------------------
    # CHATBOT LOGIC
    # -----------------------------
    response, new_state, updated_data = handle_user_message(
        user_id,
        text,
        state,
        user_data
    )

    # Save state
    updated_data["state"] = new_state
    user_state[user_id] = updated_data

    # -----------------------------
    # SEND RESPONSE TO WHATSAPP
    # -----------------------------
    try:
        await send_whatsapp_message(user_id, response)
        print(f" Message sent to {user_id}")
    except Exception as e:
        print(" WHATSAPP SEND ERROR:", str(e))

    return {"status": "ok"}
