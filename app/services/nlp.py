"""
Custom NLP Engine for Tezz Delivery.
Recognizes user intent from natural language — no external API needed.
"""
import re

# ── Intent definitions ─────────────────────────────────────────────────────
INTENTS = {
    "greeting": [
        "hi", "hello", "start", "hey", "salam", "assalam", "helo",
        "good morning", "good evening", "good afternoon", "hii", "hiii",
        "السلام", "آداب", "shuru", "begin", "restart"
    ],
    "view_menu": [
        "menu", "show menu", "view menu", "products", "items", "catalog",
        "what do you have", "what's available", "show items", "list",
        "kya hai", "kya available", "1", "2"
    ],
    "view_cart": [
        "cart", "my cart", "view cart", "show cart", "basket",
        "what's in my cart", "check cart", "mera cart"
    ],
    "checkout": [
        "done", "finish", "complete", "place order", "order now",
        "i'm done", "im done", "that's all", "thats all", "checkout",
        "confirm order", "submit", "proceed", "place my order",
        "order karna", "ho gaya", "bas", "order kar do", "ready"
    ],
    "confirm": [
        "yes", "confirm", "y", "yep", "yup", "sure", "ok", "okay",
        "haan", "ha", "han", "bilkul", "zaroor", "correct", "right",
        "confirmed", "do it", "go ahead", "ہاں", "approved"
    ],
    "cancel": [
        "no", "cancel", "nope", "nahi", "na", "n", "stop", "quit",
        "exit", "band karo", "nahi chahiye", "reject", "nevermind",
        "never mind", "forget it", "drop it"
    ],
    "edit": [
        "edit", "change", "modify", "update", "back", "wapas",
        "go back", "redo", "fix", "correct it", "change order"
    ],
    "help": [
        "help", "0", "support", "assist", "guide", "how", "kaise",
        "samajh nahi", "confused", "?"
    ],
    "payment_cash": [
        "cash", "cod", "cash on delivery", "pay cash", "naqad",
        "cash dena", "baad mein", "delivery pe"
    ],
    "payment_easypaisa": [
        "easypaisa", "easy paisa", "ep", "mobile payment",
        "easypaisa se", "online pay", "digital"
    ],
    "payment_jazzcash": [
        "jazzcash", "jazz cash", "jc", "jazz"
    ],
}


def get_intent(text: str) -> str:
    """
    Returns the detected intent from user message.
    Falls back to 'unknown' if nothing matches.
    """
    text_clean = text.strip().lower()

    # Check item number FIRST before anything else e.g. "3", "3x2", "5x2"
    if re.match(r"^\d+(\s*[x×]\s*\d+)?$", text_clean):
        return "add_item"

    # Direct exact match
    for intent, keywords in INTENTS.items():
        if text_clean in keywords:
            return intent

    # Whole-word partial match only (avoids false positives like "no" in "know")
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            if len(kw) > 3:  # only match keywords longer than 3 chars
                if re.search(r'\b' + re.escape(kw) + r'\b', text_clean):
                    return intent

    return "unknown"


def extract_item_and_qty(text: str):
    """
    Extracts product ID and quantity from messages like:
    "3", "3x2", "3 x 2", "add 3", "i want item 3", "give me 5x2"
    Returns (pid, qty) or (None, None)
    """
    text_clean = text.strip().lower()

    # Direct: "3" or "3x2"
    m = re.search(r"\b(\d+)\s*[x×]\s*(\d+)\b", text_clean)
    if m:
        return m.group(1), int(m.group(2))

    m = re.search(r"\b(\d+)\b", text_clean)
    if m:
        return m.group(1), 1

    return None, None