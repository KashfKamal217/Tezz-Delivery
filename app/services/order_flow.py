from app.services.cart import add_to_cart, get_cart, get_total
from app.services.order import create_order


def handle_user_message(user_id, message, state, user_data):

    message = message.lower()

    # ----------------------
    # 1. GREETING
    # ----------------------
    if state == "GREETING":
        return (
            "Welcome to Tezz Delivery!\nSend item name to order.",
            "SELECTING_PRODUCT",
            user_data
        )

    # ----------------------
    # 2. PRODUCT SELECTION
    # ----------------------
    elif state == "SELECTING_PRODUCT":

        if message == "done":
            cart = get_cart(user_id)
            total = get_total(user_id)

            return (
                f"Your cart: {cart}\nTotal: {total}\nSend your address.",
                "ENTER_ADDRESS",
                user_data
            )

        price = 100
        add_to_cart(user_id, message, price)

        return (
            f"{message} added to cart.\nType DONE when finished.",
            "SELECTING_PRODUCT",
            user_data
        )

    # ----------------------
    # 3. ADDRESS INPUT (FIXED)
    # ----------------------
    elif state == "ENTER_ADDRESS":

        user_data["address"] = message  #  SAVE ADDRESS

        return (
            f"Address saved: {message}\nConfirm order? YES / NO",
            "CONFIRMATION",
            user_data
        )

    # ----------------------
    # 4. CONFIRMATION (FIXED)
    # ----------------------
    elif state == "CONFIRMATION":

        if message == "yes":
            cart = get_cart(user_id)
            address = user_data.get("address")

            order = create_order(user_id, cart, address)

            return (
                f"Order Confirmed!\n{order}",
                "COMPLETED",
                user_data
            )

        elif message == "no":
            return (
                "Order cancelled. Start again.",
                "GREETING",
                {"address": None}
            )

        else:
            return (
                "Please type YES or NO",
                "CONFIRMATION",
                user_data
            )

    return "Something went wrong", state, user_data