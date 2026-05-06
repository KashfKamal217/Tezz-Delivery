def get_payment_methods():
    return [
        {"id": "1", "name": "Easypaisa"},
        {"id": "2", "name": "Cash on Delivery"}
    ]

def validate_payment_method(choice):
    if choice == "1":
        return "Easypaisa"
    else:
        return "Cash on Delivery"
