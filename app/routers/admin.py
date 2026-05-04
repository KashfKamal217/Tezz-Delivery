"""
Admin endpoints to view orders and sessions.
Protect these with auth in production!
"""
from fastapi import APIRouter, HTTPException
from app.services import session_store

router = APIRouter()


@router.get("/orders")
def get_all_orders():
    """View all confirmed orders."""
    orders = session_store.get_all_orders()
    return {
        "total": len(orders),
        "orders": [o.dict() for o in orders]
    }


@router.get("/orders/{order_id}")
def get_order(order_id: str):
    orders = session_store.get_all_orders()
    for o in orders:
        if o.order_id == order_id:
            return o.dict()
    raise HTTPException(status_code=404, detail="Order not found")


@router.get("/sessions")
def get_active_sessions():
    """View all active customer sessions."""
    return {
        "active_sessions": len(session_store.sessions),
        "sessions": {
            phone: {
                "state": s.state,
                "cart_items": len(s.cart),
                "cart_total": s.cart_total(),
                "name": s.customer_name
            }
            for phone, s in session_store.sessions.items()
        }
    }


@router.delete("/sessions/{phone}")
def clear_session(phone: str):
    """Manually clear a stuck session."""
    session_store.clear_session(phone)
    return {"status": "cleared", "phone": phone}
