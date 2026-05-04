cart_db = {}

def add_to_cart(user_id, item, price):
    if user_id not in cart_db:
        cart_db[user_id] = []

    cart_db[user_id].append({
        "item": item,
        "price": price
    })


def get_cart(user_id):
    return cart_db.get(user_id, [])


def get_total(user_id):
    return sum(i["price"] for i in cart_db.get(user_id, []))