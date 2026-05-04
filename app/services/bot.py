"""
Tezz Delivery Bot — Custom NLP + State Machine
Full flow: greeting → menu → cart → name → phone → address → time → payment → receipt → confirm
"""
import re
import logging
from app.models.session import CustomerSession, OrderState, CartItem, Order
from app.services import session_store, messages
from app.services.nlp import get_intent, extract_item_and_qty
from app.data.catalog import CATALOG, DELIVERY_CHARGE, MIN_ORDER

logger = logging.getLogger(__name__)


async def process_message(phone: str, text: str) -> str:
    text = text.strip()
    session = session_store.get_session(phone)
    intent = get_intent(text)

    # ── Global commands (any state) ────────────────────────────────────────
    if intent == "greeting":
        session.state = OrderState.NEW
        session.cart = {}
        session_store.save_session(session)
        return messages.greeting()

    if intent == "view_menu":
        session.state = OrderState.BROWSING
        session_store.save_session(session)
        return messages.show_catalog()

    if intent == "view_cart":
        return messages.cart_view(session)

    if intent == "cancel" and session.state not in [OrderState.CONFIRMING, OrderState.COLLECTING_PAYMENT]:
        session_store.clear_session(phone)
        return messages.order_cancelled()

    if intent == "help":
        return (
            "ℹ️ *Tezz Delivery Help*\n\n"
            "*menu* — View products\n"
            "*cart* — View your cart\n"
            "*done* — Place your order\n"
            "*cancel* — Cancel your order\n"
            "*hi* — Restart\n\n"
            "Send item number to add (e.g. *3* or *3x2*)"
        )

    state = session.state

    # ── BROWSING / ADDING ITEMS ────────────────────────────────────────────
    if state in [OrderState.NEW, OrderState.BROWSING, OrderState.ADDING_ITEMS]:

        # "1" and "2" show menu when not already adding items
        if text.strip() in ["1", "2"] and state in [OrderState.NEW, OrderState.BROWSING]:
            session.state = OrderState.BROWSING
            session_store.save_session(session)
            return messages.show_catalog()

        if intent == "add_item" or re.match(r"^\d+(\s*[x×]\s*\d+)?$", text.strip()):
            pid, qty = extract_item_and_qty(text)
            if not pid or pid not in CATALOG:
                return f"❌ Product #{pid} not found. Type *menu* to see available items."
            qty = max(1, min(qty, 20))
            product = CATALOG[pid]
            if pid in session.cart:
                session.cart[pid].quantity += qty
            else:
                session.cart[pid] = CartItem(
                    product_id=pid, name=product["name"],
                    price=product["price"], quantity=qty
                )
            session.state = OrderState.ADDING_ITEMS
            session_store.save_session(session)
            return messages.item_added(product, qty, session)

        if intent == "checkout":
            if not session.cart:
                return "🛒 Your cart is empty! Add some items first."
            if session.cart_total() < MIN_ORDER:
                return f"⚠️ Minimum order is Rs. {MIN_ORDER}. Current total: Rs. {session.cart_total()}"
            session.state = OrderState.COLLECTING_NAME
            session_store.save_session(session)
            return messages.ask_name()

        return messages.unknown_command()

    # ── COLLECTING NAME ────────────────────────────────────────────────────
    if state == OrderState.COLLECTING_NAME:
        if len(text) < 2:
            return "📝 Please enter a valid name."
        session.customer_name = text.title()
        session.state = OrderState.COLLECTING_PHONE
        session_store.save_session(session)
        return messages.ask_phone(session.customer_name)

    # ── COLLECTING PHONE ───────────────────────────────────────────────────
    if state == OrderState.COLLECTING_PHONE:
        digits = re.sub(r"\D", "", text)
        if len(digits) < 10:
            return "📞 Please enter a valid phone number (e.g. 03001234567):"
        session.customer_phone = digits
        session.state = OrderState.COLLECTING_ADDRESS
        session_store.save_session(session)
        return messages.ask_address()

    # ── COLLECTING ADDRESS ─────────────────────────────────────────────────
    if state == OrderState.COLLECTING_ADDRESS:
        if len(text) < 5:
            return "📍 Please provide a detailed address (street, area, landmark)."
        session.address = text
        session.state = OrderState.COLLECTING_TIME
        session_store.save_session(session)
        return messages.ask_time()

    # ── COLLECTING TIME ────────────────────────────────────────────────────
    if state == OrderState.COLLECTING_TIME:
        session.preferred_time = text
        session.state = OrderState.COLLECTING_PAYMENT
        session_store.save_session(session)
        return messages.ask_payment()

    # ── COLLECTING PAYMENT ─────────────────────────────────────────────────
    if state == OrderState.COLLECTING_PAYMENT:
        if intent == "payment_easypaisa" or text.strip() in ["2", "easypaisa"]:
            session.payment_method = "EasyPaisa"
            session.state = OrderState.COLLECTING_EASYPAISA
            session_store.save_session(session)
            return messages.ask_easypaisa_number()
        elif intent == "payment_jazzcash" or text.strip() in ["3", "jazzcash"]:
            session.payment_method = "JazzCash"
            session.state = OrderState.COLLECTING_EASYPAISA
            session_store.save_session(session)
            return messages.ask_easypaisa_number()
        elif intent == "payment_cash" or text.strip() in ["1", "cash", "cod"]:
            session.payment_method = "Cash on Delivery"
            session.state = OrderState.CONFIRMING
            order_id = session_store.generate_order_id()
            session.last_message = order_id
            session_store.save_session(session)
            return messages.bill_receipt(session, order_id)
        else:
            return "❓ Please choose:\n1️⃣ Cash on Delivery\n2️⃣ EasyPaisa\n3️⃣ JazzCash"

    # ── COLLECTING EASYPAISA NUMBER ────────────────────────────────────────
    if state == OrderState.COLLECTING_EASYPAISA:
        digits = re.sub(r"\D", "", text)
        if len(digits) < 10:
            return "📱 Please enter a valid account number:"
        session.easypaisa_number = digits
        session.state = OrderState.CONFIRMING
        order_id = session_store.generate_order_id()
        session.last_message = order_id
        session_store.save_session(session)
        return messages.bill_receipt(session, order_id)

    # ── CONFIRMING ─────────────────────────────────────────────────────────
    if state == OrderState.CONFIRMING:
        if intent == "confirm":
            return await _confirm_order(session)
        if intent == "edit":
            session.state = OrderState.ADDING_ITEMS
            session_store.save_session(session)
            return "✏️ *Edit mode!*\n\n" + messages.cart_view(session) + "\n\nAdd/remove items or type *done*."
        if intent == "cancel":
            session_store.clear_session(phone)
            return messages.order_cancelled()
        return "❓ Please type *YES* to confirm, *EDIT* to change, or *CANCEL* to cancel."

    # ── CONFIRMED ──────────────────────────────────────────────────────────
    if state == OrderState.CONFIRMED:
        return "✅ Your order is already confirmed!\n\nType *hi* to place a new order."

    return messages.greeting()


async def _confirm_order(session: CustomerSession) -> str:
    order_id = session.last_message or session_store.generate_order_id()
    cart_total = session.cart_total()
    grand_total = cart_total + DELIVERY_CHARGE

    order = Order(
        order_id=order_id,
        phone=session.phone,
        customer_name=session.customer_name,
        customer_phone=session.customer_phone,
        address=session.address,
        preferred_time=session.preferred_time,
        payment_method=session.payment_method,
        easypaisa_number=session.easypaisa_number,
        cart=session.cart,
        cart_total=cart_total,
        delivery_charge=DELIVERY_CHARGE,
        grand_total=grand_total,
        status="confirmed"
    )

    session_store.save_order(order)
    session.state = OrderState.CONFIRMED
    session_store.save_session(session)

    notification = messages.internal_notification(order)
    await _notify_admin(notification, order)

    logger.info(f"✅ Order confirmed: {order_id} | {session.customer_name} | Rs. {grand_total}")
    return messages.order_confirmed(order_id)


async def _notify_admin(message_text: str, order: Order):
    import os, httpx
    token = os.getenv("WHATSAPP_TOKEN")
    admin_phone = os.getenv("ADMIN_PHONE_NUMBER", "923001234567")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

    if not token or not phone_number_id:
        logger.warning("⚠️ WHATSAPP_TOKEN or PHONE_NUMBER_ID not set — skipping admin notification")
        logger.info(f"[ADMIN NOTIFICATION]\n{message_text}")
        return

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    payload = {"messaging_product": "whatsapp", "to": admin_phone,
               "type": "text", "text": {"body": message_text}}
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
    except Exception as e:
        logger.error(f"Admin notification failed: {e}")