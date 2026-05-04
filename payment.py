def choose_payment():
    print("\nSelect Payment Method:")
    print("1. Easypaisa")
    print("2. Cash on Delivery")

    choice = input("Enter choice: ")

    if choice == "1":
        return "Easypaisa"
    else:
        return "Cash on Delivery"