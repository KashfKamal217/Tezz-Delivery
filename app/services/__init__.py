"""
Core chatbot state machine for Tezz Delivery.
Handles every step: greeting → catalog → cart → info → confirm → notify
"""
import re
import logging
from app.models.session import CustomerSession, OrderState, CartItem, Order
from app.services import session_store, messages
from app.data.catalog import CATALOG, DELIVERY_CHARGE, MIN_ORDER

logger = logging.getLogger(__name__)


async def process_message(phone: str, text: str) -> str:
    """
    Main entry point: takes a phone number + message text,
    returns the bot's reply string.
    """
    text = text.strip()
    text_lower = text.lower()

    session = session_store.get_session(phone)

    # ── Global commands (work from any state) ──────────────────────────────
    if text_lower in ["hi", "hello", "start", "helo", "salam", "السلام"]:
        session.state = OrderState.NEW
        session.cart = {}
        session_store.save_session(session)
        return messages.greeting()

    if text_lower == "menu":
        session.state = OrderState.BROWSING
        session_store.save_session(session)
        return messages.show_catalog()

    if text_lower == "cart":
        return messages.cart_view(session)

    if text_lower == "cancel":
        session_store.clear_session(phone)
        return messages.order_cancelled()

    if text_lower == "0" or text_lower == "help":
        return (
            "ℹ️ *Tezz Delivery Help*\n\n"
            "*menu* — Products dekhein\n"
            "*cart* — Apna cart dekhein\n"
            "*done* — Order submit karna\n"
            "*cancel* — Order cancel karna\n"
            "*hi* — Restart karna\n\n"
            "Items add karne ke liye number bhejein jaise: *3* ya *3x2*"
        )

    # ── State machine ───────────────────────────────────────────────────────
    state = session.state

    # NEW / BROWSING — handle menu choice or direct item
    if state in [OrderState.NEW, OrderState.BROWSING, OrderState.ADDING_ITEMS]:
        # "1" → show menu, "2" → also show menu
        if text_lower in ["1", "2"]:
            session.state = OrderState.BROWSING
            session_store.save_session(session)
            return messages.show_catalog()

        # Item selection: "3" or "3x2" or "3 x 2"
        item_match = re.match(r"^(\d+)\s*[x×]\s*(\d+)$", text_lower) or \
                     re.match(r"^(\d+)$", text_lower)

        if item_match:
            if len(item_match.groups()) == 2:
                pid, qty = item_match.group(1), int(item_match.group(2))
            else:
                pid, qty = item_match.group(1), 1

            if pid not in CATALOG:
                return f"❌ Product #{pid} nahi mila. *menu* bhejein catalog dekhne ke liye."

            qty = max(1, min(qty, 20))  # cap at 20
            product = CATALOG[pid]

            if pid in session.cart:
                session.cart[pid].quantity += qty
            else:
                session.cart[pid] = CartItem(
                    product_id=pid,
                    name=product["name"],
                    price=product["price"],
                    quantity=qty
                )

            session.state = OrderState.ADDING_ITEMS
            session_store.save_session(session)
            return messages.item_added(product, qty, session)

        if text_lower == "done":
            if not session.cart:
                return "🛒 Cart khali hai! Pehle kuch items add karein."
            if session.cart_total() < MIN_ORDER:
                return f"⚠️ Minimum order Rs. {MIN_ORDER} hai. Abhi Rs. {session.cart_total()} hai."
            session.state = OrderState.COLLECTING_INFO
            session_store.save_session(session)
            return messages.ask_name()

        return messages.unknown_command()

    # COLLECTING_INFO — get customer name
    if state == OrderState.COLLECTING_INFO:
        if len(text) < 2:
            return "📝 Sahi naam bhejein please."
        session.customer_name = text.title()
        session.state = OrderState.COLLECTING_ADDRESS
        session_store.save_session(session)
        return messages.ask_address(session.customer_name)

    # COLLECTING_ADDRESS
    if state == OrderState.COLLECTING_ADDRESS:
        if len(text) < 5:
            return "📍 Thoda detail mein address bhejein (gali, mohalla, landmark)."
        session.address = text
        session.state = OrderState.COLLECTING_TIME
        session_store.save_session(session)
        return messages.ask_time()

    # COLLECTING_TIME
    if state == OrderState.COLLECTING_TIME:
        session.preferred_time = text
        order_id = session_store.generate_order_id()
        session.last_message = order_id  # temporarily store
        session.state = OrderState.CONFIRMING
        session_store.save_session(session)
        return messages.order_summary(session, order_id)

    # CONFIRMING — YES / NO / EDIT
    if state == OrderState.CONFIRMING:
        if text_lower in ["yes", "confirm", "haan", "ha", "y", "ہاں"]:
            return await _confirm_order(session)

        if text_lower in ["edit", "change", "wapas", "back"]:
            session.state = OrderState.ADDING_ITEMS
            session_store.save_session(session)
            return (
                "✏️ *Edit mode on!*\n\n"
                + messages.cart_view(session)
                + "\n\nItems add/remove karein ya *done* likhein."
            )

        if text_lower in ["no", "nahi", "na", "cancel", "n"]:
            session_store.clear_session(phone)
            return messages.order_cancelled()

        return "❓ *YES* (confirm) ya *NO* (cancel) ya *EDIT* likhein please."

    # CONFIRMED
    if state == OrderState.CONFIRMED:
        return (
            "✅ Aapka order already confirm ho chuka hai!\n\n"
            "Naya order karne ke liye *hi* likhein."
        )

    # Fallback
    return messages.greeting()


async def _confirm_order(session: CustomerSession) -> str:
    """Lock the order, save it, trigger internal notification."""
    order_id = session.last_message or session_store.generate_order_id()
    cart_total = session.cart_total()
    grand_total = cart_total + DELIVERY_CHARGE

    order = Order(
        order_id=order_id,
        phone=session.phone,
        customer_name=session.customer_name,
        address=session.address,
        preferred_time=session.preferred_time,
        cart=session.cart,
        cart_total=cart_total,
        delivery_charge=DELIVERY_CHARGE,
        grand_total=grand_total,
        status="confirmed"
    )

    session_store.save_order(order)

    # Mark session as confirmed
    session.state = OrderState.CONFIRMED
    session_store.save_session(session)

    # Send internal notification (to admin WhatsApp group)
    notification = messages.internal_notification(order, session)
    await _notify_admin(notification, order)

    logger.info(f"✅ Order confirmed: {order_id} | {session.customer_name} | Rs. {grand_total}")

    return messages.order_confirmed(order_id)


async def _notify_admin(message_text: str, order: Order):
    """
    Sends order notification to admin WhatsApp group.

    In production: call WhatsApp Business API to send message to
    your admin group or phone number.

    Replace ADMIN_GROUP_ID and WHATSAPP_TOKEN with real values.
    """
    import os
    import httpx

    token = os.getenv("WHATSAPP_TOKEN")
    admin_phone = os.getenv("ADMIN_PHONE_NUMBER", "923001234567")  # your number
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

    if not token or not phone_number_id:
        logger.warning("⚠️ WHATSAPP_TOKEN or PHONE_NUMBER_ID not set — skipping admin notification")
        logger.info(f"[ADMIN NOTIFICATION]\n{message_text}")
        return

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": admin_phone,
        "type": "text",
        "text": {"body": message_text}
    }
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            logger.info(f"Admin notified for order {order.order_id}")
    except Exception as e:
        logger.error(f"Admin notification failed: {e}")