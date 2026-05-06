# 🚀 Tezz Delivery - WhatsApp Automation System

## 📌 Overview
Tezz Delivery is a WhatsApp-based automation system for a Cash & Carry kitchen business.

It automates:
- Customer chat handling
- Product selection
- Cart management
- Order confirmation
- Payment processing
- Language switching (English / Urdu)

---

## 🧠 Core Features

### 🤖 WhatsApp Chatbot
- Auto replies to customers
- Shows product catalog
- Handles order flow step-by-step

---

### 🛒 Cart System
- Add/remove items
- Live total calculation
- Order summary before confirmation

---

### 💰 Payment Module
- Easypaisa integration (planned / backend ready)
- Cash on Delivery (COD)

---

### 🌐 Language Support
- English 🇬🇧
- Urdu 🇵🇰
- Dynamic switching based on user choice

---

## 🔄 System Workflow

1. Customer sends message on WhatsApp  
2. Bot greets and shows products  
3. User selects items  
4. Items added to cart  
5. Bot asks: "Do you want more items?"  
6. Final bill is generated  
7. User selects payment method  
8. User provides name + address  
9. Order sent to admin/delivery group  

---

## 🧱 Tech Stack
- Python / FastAPI  
- WhatsApp Cloud API  
- Firebase / MongoDB (optional backend)  
- GitHub collaboration workflow  

---

## 📁 Project Structure


tezz-delivery/
│
├── app/
│ ├── main.py
│ ├── routes/
│ ├── services/
│ ├── utils/
│ └── schemas/
│
├── database/
├── requirements.txt
└── README.md


---

## ▶️ How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload

👨‍💻 Team Modules
Payment Integration (Easypaisa + COD)
Language Support (EN/UR)
Backend WhatsApp webhook system
Cart & order flow logic
📌 Notes

This system is part of a group project and integrates multiple backend modules into a WhatsApp automation pipeline.