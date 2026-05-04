from app.data.catalog import CATALOG, DELIVERY_CHARGE

def greeting():
    return (
        "🛵 *Welcome to Tezz Delivery!* 🛵\n\n"
        "Order groceries, beverages, snacks & daily-use items from home.\n\n"
        "👇 *Choose an option:*\n"
        "1️⃣  View Menu\n"
        "2️⃣  Place an Order\n"
        "0️⃣  Help\n\n"
        "Just send a number! 😊"
    )

def show_catalog():
    categories = {}
    for pid, product in CATALOG.items():
        cat = product["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((pid, product))

    lines = ["📦 *TEZZ DELIVERY — MENU* 📦\n"]
    for cat, items in categories.items():
        lines.append(f"*── {cat} ──*")
        for pid, p in items:
            lines.append(f"*{pid}.* {p['name']}  →  Rs. {p['price']}")
        lines.append("")

    lines.append(f"🚚 Delivery charge: Rs. {DELIVERY_CHARGE}")
    lines.append("\n➕ Send item number to add (e.g. *3* or *3x2*)")
    lines.append("🛒 Type *cart* to view your cart")
    lines.append("✅ Type *done* to place your order")
    return "\n".join(lines)

def cart_view(session):
    if not session.cart:
        return "🛒 *Your cart is empty!*\n\nType *menu* to browse products."
    lines = ["🛒 *YOUR CART:*\n"]
    lines.append(session.cart_summary_text())
    lines.append(f"\n💰 *Items Total:* Rs. {session.cart_total()}")
    lines.append(f"🚚 *Delivery:* Rs. {DELIVERY_CHARGE}")
    lines.append(f"🧾 *Grand Total:* Rs. {session.cart_total() + DELIVERY_CHARGE}")
    lines.append("\n➕ Send a number to add more items")
    lines.append("✅ Type *done* to confirm your order")
    lines.append("❌ Type *cancel* to cancel")
    return "\n".join(lines)

def item_added(product, qty, session):
    return (
        f"✅ *{product['name']}* x{qty} added to cart!\n\n"
        f"🛒 *Cart Total:* Rs. {session.cart_total()}\n\n"
        "Send more item numbers or type *done* to place your order."
    )

def ask_name():
    return "📝 *We need a few details!*\n\nPlease send your *full name*:"

def ask_phone(name):
    return (
        f"Thank you {name}! 😊\n\n"
        "📞 Please send your *phone number*:"
    )

def ask_address():
    return (
        "📍 Please send your *delivery address*\n"
        "_(Include street, area and a nearby landmark)_"
    )

def ask_time():
    return (
        "⏰ *Preferred delivery time?*\n\n"
        "• *Now* (ASAP)\n"
        "• *5 PM*\n"
        "• *This evening*"
    )

def ask_payment():
    return (
        "💳 *Select Payment Method:*\n\n"
        "1️⃣  Cash on Delivery\n"
        "2️⃣  EasyPaisa\n"
        "3️⃣  JazzCash\n\n"
        "Send the number or name!"
    )

def ask_easypaisa_number():
    return "📱 Please send your *EasyPaisa / JazzCash account number*:"

def bill_receipt(session, order_id):
    from app.data.catalog import DELIVERY_CHARGE
    lines = [
        "🧾 *TEZZ DELIVERY — ORDER RECEIPT*",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🔖 Order ID:     {order_id}",
        f"👤 Name:         {session.customer_name}",
        f"📞 Phone:        {session.customer_phone}",
        f"📍 Address:      {session.address}",
        f"⏰ Time:         {session.preferred_time}",
        f"💳 Payment:      {session.payment_method}",
    ]
    if session.easypaisa_number:
        lines.append(f"📱 Account:      {session.easypaisa_number}")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("🛒 *ITEMS:*")

    for item in session.cart.values():
        lines.append(f"  • {item.name}")
        lines.append(f"    {item.quantity} x Rs.{item.price} = Rs.{item.price * item.quantity}")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"💰 Items Total:  Rs. {session.cart_total()}")
    lines.append(f"🚚 Delivery:     Rs. {DELIVERY_CHARGE}")
    lines.append(f"💵 *GRAND TOTAL: Rs. {session.cart_total() + DELIVERY_CHARGE}*")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("\n✅ Type *YES* to confirm")
    lines.append("✏️ Type *EDIT* to make changes")
    lines.append("❌ Type *CANCEL* to cancel")
    return "\n".join(lines)

def order_confirmed(order_id, eta="30-45 min"):
    return (
        f"🎉 *Your Order is Confirmed!*\n\n"
        f"🔖 Order ID: `{order_id}`\n"
        f"🚚 Our rider will be on the way shortly!\n"
        f"⏱️ Estimated delivery: *{eta}*\n\n"
        f"Thank you for choosing Tezz Delivery! 🛵💨\n\n"
        "To place a new order, type *hi* or *start*."
    )

def order_cancelled():
    return "❌ *Your order has been cancelled.*\n\nType *hi* to start a new order. 😊"

def internal_notification(order):
    lines = [
        "🔔 *NEW ORDER — TEZZ DELIVERY* 🔔\n",
        f"🔖 Order ID:  {order.order_id}",
        f"👤 Customer: {order.customer_name}",
        f"📞 Phone:    {order.customer_phone}",
        f"📍 Address:  {order.address}",
        f"⏰ Time:     {order.preferred_time}",
        f"💳 Payment:  {order.payment_method}",
    ]
    if order.easypaisa_number:
        lines.append(f"📱 Account:  {order.easypaisa_number}")
    lines.append("\n🛒 *Items:*")
    for item in order.cart.values():
        lines.append(f"  • {item.name} x{item.quantity} = Rs. {item.price * item.quantity}")
    lines.append(f"\n💵 *Grand Total: Rs. {order.grand_total}*")
    lines.append("\n⚡ Please assign a rider and dispatch!")
    return "\n".join(lines)

def unknown_command():
    return (
        "🤔 Sorry, I didn't understand that!\n\n"
        "Type *menu* to browse products\n"
        "Type *cart* to view your cart\n"
        "Type *done* to place your order\n"
        "Type *cancel* to cancel"
    )