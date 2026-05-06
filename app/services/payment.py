def get_payment_methods():
    return [
        {"id": "1", "name": "Easypaisa"},
        {"id": "2", "name": "Cash on Delivery"}
    ]


def validate_payment_method(choice):
    if choice == "1":
        return "Easypaisa"
    elif choice == "2":
        return "Cash on Delivery"
    return None  # FIX: handle invalid input


def payment_prompt():
    return "Select payment method:\n1. Easypaisa\n2. Cash on Delivery"