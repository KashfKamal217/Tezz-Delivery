"""
WhatsApp Business API webhook.
- GET  /webhook  → verification (required by Meta)
- POST /webhook  → incoming messages
"""
import os
import logging
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse
from app.services.bot import process_message
from app.services.whatsapp_sender import send_whatsapp_message

router = APIRouter()
logger = logging.getLogger(__name__)

VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "tezz_delivery_secret_2026")


# ── Webhook verification (Meta requires this) ──────────────────────────────
@router.get("")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        logger.info("✅ Webhook verified by Meta")
        return PlainTextResponse(hub_challenge)
    raise HTTPException(status_code=403, detail="Invalid verify token")


# ── Incoming messages ──────────────────────────────────────────────────────
@router.post("")
async def receive_message(request: Request):
    try:
        body = await request.json()
        logger.debug(f"Incoming webhook: {body}")

        entry = body.get("entry", [])
        for e in entry:
            for change in e.get("changes", []):
                value = change.get("value", {})
                messages_list = value.get("messages", [])

                for msg in messages_list:
                    phone = msg["from"]
                    msg_type = msg.get("type", "")

                    if msg_type == "text":
                        text = msg["text"]["body"]
                    elif msg_type == "interactive":
                        # Button reply
                        interactive = msg.get("interactive", {})
                        if interactive.get("type") == "button_reply":
                            text = interactive["button_reply"]["title"]
                        else:
                            text = interactive.get("list_reply", {}).get("title", "")
                    else:
                        # Ignore non-text messages
                        continue

                    logger.info(f"📩 [{phone}]: {text}")

                    # Get bot reply
                    reply = await process_message(phone, text)

                    # Send reply back via WhatsApp
                    await send_whatsapp_message(phone, reply)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Webhook error: {e}", exc_info=True)
        return {"status": "error", "detail": str(e)}
