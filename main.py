from payment import choose_payment
from language import get_message

# STEP 1: Language
lang = input("Select language (en/ur): ")

print(get_message(lang, "welcome"))

# STEP 2: Products (simple demo)
products = {
    1: ("Tea", 200),
    2: ("Chips", 100),
    3: ("Shampoo", 300)
}

cart = []
total = 0

# STEP 3: Order loop (IMPORTANT SRS PART)
while True:
    print("\nAvailable Products:")
    for k, v in products.items():
        print(k, v)

    choice = int(input(get_message(lang, "select_item") + ": "))

    name, price = products[choice]
    cart.append(name)
    total += price

    more = input(get_message(lang, "more") + ": ")
    if more.lower() == "no":
        break

# STEP 4: Payment (YOUR TASK)
payment = choose_payment()

# STEP 5: User Info
name = input("Enter name: ")
phone = input("Enter phone: ")
address = input("Enter address: ")

# STEP 6: Confirm Order (IMPORTANT SRS)
confirm = input(get_message(lang, "confirm") + ": ")

if confirm.lower() == "yes":
    print("\nNEW ORDER SENT TO ADMIN")
    print("Name:", name)
    print("Phone:", phone)
    print("Address:", address)
    print("Items:", cart)
    print("Total:", total)
    print("Payment:", payment)
else:
    print("Order cancelled")