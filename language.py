def get_message(lang, key):
    messages = {
        "en": {
            "welcome": "Welcome!",
            "select_item": "Select item",
            "more": "Do you want anything else? (yes/no)",
            "confirm": "Confirm order? (yes/no)"
        },
        "ur": {
            "welcome": "Khush aamdeed!",
            "select_item": "Item select karein",
            "more": "Kya aap kuch aur chahte hain? (yes/no)",
            "confirm": "Apna order confirm karein? (yes/no)",
            "payment": "Payment method select karein:",
            "invalid": "Ghalat choice, dobara try karein",
            "confirmed": "Aap ka order confirm ho gaya hai"
}
    }
    return messages[lang][key]