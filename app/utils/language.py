def get_message(lang, key):
    messages = {
        "en": {
            "welcome": "Welcome!",
            "select_item": "Select item",
            "more": "Do you want anything else? (yes/no)",
            "confirm": "Confirm order? (yes/no)"
        },
        "ur": {
            "welcome": "خوش آمدید!",
            "select_item": "آئٹم منتخب کریں",
            "more": "کیا آپ کچھ اور چاہتے ہیں؟ (yes/no)",
            "confirm": "آرڈر کی تصدیق کریں؟ (yes/no)"
        }
    }
    return messages.get(lang, messages["en"]).get(key, "")
