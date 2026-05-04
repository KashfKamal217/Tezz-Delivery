# Tezz Delivery Backend 🚀

FastAPI backend for WhatsApp chatbot integration.

## Features
- WhatsApp Cloud API Webhook
- Cart Management System
- Order Processing Flow
- State-based Chatbot Logic

## Tech Stack
- FastAPI
- Python
- HTTPX
- Uvicorn

## Setup Instructions

1. Clone repo:
   git clone https://github.com/your-username/tezz-backend.git

2. Install dependencies:
   pip install -r requirements.txt

3. Create .env file:
   WHATSAPP_TOKEN=your_token
   PHONE_NUMBER_ID=your_id
   VERIFY_TOKEN=your_verify_token

4. Run server:
   uvicorn app.main:app --reload

## API Endpoints

- GET /webhook → Meta verification
- POST /webhook → Receive WhatsApp messages

## Status

Backend is fully functional and tested using Postman/Swagger.  
WhatsApp integration is ready but pending live webhook connection.

---