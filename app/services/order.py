orders = []

def create_order(user_id, cart, address):

    order = {
        "user_id": user_id,
        "items": cart,
        "address": address
    }

    orders.append(order)

    print("🚀 NEW ORDER CREATED:", order)

    return order