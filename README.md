# 🛵 Tezz Delivery — WhatsApp Order Automation

A complete WhatsApp chatbot backend for Cash & Carry kitchen business with in-house delivery.

---

## 📁 Project Structure

```
tezz_delivery/
├── app/
│   ├── main.py                  ← FastAPI entry point
│   ├── data/
│   │   └── catalog.py           ← 🛒 Product catalog (edit here!)
│   ├── models/
│   │   └── session.py           ← Data models
│   ├── routers/
│   │   ├── webhook.py           ← WhatsApp webhook (GET + POST)
│   │   └── admin.py             ← Admin endpoints
│   └── services/
│       ├── bot.py               ← 🧠 Core state machine
│       ├── messages.py          ← 💬 All bot messages (edit here!)
│       ├── session_store.py     ← Session management
│       └── whatsapp_sender.py   ← WhatsApp API sender
├── test_bot.py                  ← Local test (no WhatsApp needed)
├── requirements.txt
└── .env.example
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your WhatsApp credentials
```

### 3. Test locally (no WhatsApp needed)
```bash
python test_bot.py
```

### 4. Run the server
```bash
python -m app.main
# OR
uvicorn app.main:app --reload --port 8000
```

---

## 📱 WhatsApp Setup (Meta Developer Console)

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Create an App → Add WhatsApp product
3. Get your **Phone Number ID** and **Permanent Token**
4. Set webhook URL to: `https://yourdomain.com/webhook`
5. Set Verify Token to: `tezz_delivery_secret_2026` (or change in `.env`)
6. Subscribe to `messages` webhook event

---

## 💬 Full Bot Flow

```
Customer says "hi"
  → Bot greets + shows options

Customer picks "1" (Menu)
  → Bot shows product catalog

Customer sends "3" or "3x2"
  → Bot adds to cart, shows updated total

Customer sends "done"
  → Bot asks name → address → delivery time

Bot shows order summary
  → Customer sends "YES"

✅ Order confirmed!
  → Admin gets WhatsApp notification
  → Rider dispatched
```

---

## 🛒 Adding Products

Edit `app/data/catalog.py`:
```python
CATALOG = {
    "11": {
        "name": "Mineral Water (1.5L)",
        "price": 60,
        "emoji": "💧",
        "category": "Beverages"
    },
    # ...
}
```

---

## 📊 Admin Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /admin/orders` | All confirmed orders |
| `GET /admin/orders/{id}` | Single order |
| `GET /admin/sessions` | Active customer sessions |
| `DELETE /admin/sessions/{phone}` | Clear stuck session |

---

## 🔮 Phase 2 (Future)

- EasyPaisa / JazzCash payment integration
- Real-time GPS order tracking
- Web admin dashboard
- Firebase persistence (replace in-memory store)
- Customer order history
- Discount & promo codes
