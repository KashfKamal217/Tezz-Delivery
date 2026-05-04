from pydantic import BaseModel
from typing import Dict, Optional
from enum import Enum

class OrderState(str, Enum):
    NEW = "new"
    BROWSING = "browsing"
    ADDING_ITEMS = "adding_items"
    COLLECTING_NAME = "collecting_name"
    COLLECTING_PHONE = "collecting_phone"
    COLLECTING_ADDRESS = "collecting_address"
    COLLECTING_TIME = "collecting_time"
    COLLECTING_PAYMENT = "collecting_payment"
    COLLECTING_EASYPAISA = "collecting_easypaisa"
    CONFIRMING = "confirming"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class CartItem(BaseModel):
    product_id: str
    name: str
    price: int
    quantity: int

class CustomerSession(BaseModel):
    phone: str
    state: OrderState = OrderState.NEW
    cart: Dict[str, CartItem] = {}
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    address: Optional[str] = None
    preferred_time: Optional[str] = None
    payment_method: Optional[str] = None
    easypaisa_number: Optional[str] = None
    last_message: Optional[str] = None

    def cart_total(self) -> int:
        return sum(item.price * item.quantity for item in self.cart.values())

    def cart_summary_text(self) -> str:
        if not self.cart:
            return "_(Cart is empty)_"
        lines = []
        for item in self.cart.values():
            lines.append(f"  {item.name} x{item.quantity} = Rs. {item.price * item.quantity}")
        return "\n".join(lines)

class Order(BaseModel):
    order_id: str
    phone: str
    customer_name: str
    customer_phone: str
    address: str
    preferred_time: str
    payment_method: str
    easypaisa_number: Optional[str] = None
    cart: Dict[str, CartItem]
    cart_total: int
    delivery_charge: int
    grand_total: int
    status: str = "pending"