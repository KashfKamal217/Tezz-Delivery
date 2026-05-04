"""
In-memory session store.
In production, replace with Firebase / Redis for persistence.
"""
from app.models.session import CustomerSession, Order
from typing import Dict, Optional
import uuid

# Active sessions keyed by phone number
sessions: Dict[str, CustomerSession] = {}

# Confirmed orders
orders: Dict[str, Order] = {}


def get_session(phone: str) -> CustomerSession:
    if phone not in sessions:
        sessions[phone] = CustomerSession(phone=phone)
    return sessions[phone]


def save_session(session: CustomerSession):
    sessions[session.phone] = session


def clear_session(phone: str):
    if phone in sessions:
        del sessions[phone]


def save_order(order: Order):
    orders[order.order_id] = order


def get_all_orders() -> list:
    return list(orders.values())


def generate_order_id() -> str:
    return "TZD-" + str(uuid.uuid4())[:6].upper()
