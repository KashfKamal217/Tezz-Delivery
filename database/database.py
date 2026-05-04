import firebase_admin
from firebase_admin import credentials, firestore
import os

# --- Configuration ---
# Path to your Firebase Service Account JSON file
SERVICE_ACCOUNT_PATH = "serviceAccountKey.json"

def initialize_db():
    if not os.path.exists(SERVICE_ACCOUNT_PATH):
        print(f"❌ Error: {SERVICE_ACCOUNT_PATH} not found!")
        print("Please place your Firebase service account key in this folder.")
        return None
    
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def seed_catalog(db):
    products = [
        {"id": "1", "name": "Basmati Rice (1kg)", "price": 280, "category": "Groceries", "emoji": "🍚", "stock_status": True},
        {"id": "2", "name": "Cooking Oil (1L)", "price": 420, "category": "Groceries", "emoji": "🫙", "stock_status": True},
        {"id": "3", "name": "Doodh (1L)", "price": 170, "category": "Dairy", "emoji": "🥛", "stock_status": True},
        {"id": "4", "name": "Anda (12 pcs)", "price": 240, "category": "Dairy", "emoji": "🥚", "stock_status": True},
        {"id": "5", "name": "Pepsi (500ml)", "price": 80, "category": "Beverages", "emoji": "🥤", "stock_status": True},
        {"id": "6", "name": "7UP (500ml)", "price": 80, "category": "Beverages", "emoji": "🥤", "stock_status": True},
        {"id": "7", "name": "Lay's Chips (Large)", "price": 120, "category": "Snacks", "emoji": "🍟", "stock_status": True},
        {"id": "8", "name": "Biscuit Pack (Oreo)", "price": 90, "category": "Snacks", "emoji": "🍪", "stock_status": True},
        {"id": "9", "name": "Aata (5kg)", "price": 650, "category": "Groceries", "emoji": "🌾", "stock_status": True},
        {"id": "10", "name": "Daal Mash (500g)", "price": 180, "category": "Groceries", "emoji": "🫘", "stock_status": True}
    ]

    print("🚀 Seeding products to Firestore...")
    for p in products:
        db.collection("products").document(p["id"]).set(p)
        print(f"✅ Added: {p['name']}")
    print("\n✨ Database initialization complete!")

if __name__ == "__main__":
    db = initialize_db()
    if db:
        seed_catalog(db)
