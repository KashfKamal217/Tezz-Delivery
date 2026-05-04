"""
Sends messages back to customers via WhatsApp Business API.
"""
import os
import httpx
import logging

logger = logging.getLogger(__name__)

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
API_VERSION = "v19.0"


async def send_whatsapp_message(to_phone: str, message: str):
    """Send a text message to a WhatsApp number."""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        # Local dev mode — just print
        print(f"\n📤 [BOT → {to_phone}]\n{message}\n{'─'*40}")
        return

    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_phone,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            logger.info(f"✅ Message sent to {to_phone}")
    except httpx.HTTPStatusError as e:
        logger.error(f"❌ WhatsApp API error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        logger.error(f"❌ Failed to send message: {e}")
