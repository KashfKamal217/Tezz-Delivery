import asyncio
from app.services.bot import process_message

PHONE = "923001234567"

async def main():
    print("🛵 Tezz Delivery Bot — Live Test")
    print("Type your message (or 'quit' to exit)\n")
    
    while True:
        user_input = input("👤 You: ")
        if user_input.lower() == "quit":
            break
        reply = await process_message(PHONE, user_input)
        print(f"\n🤖 Bot:\n{reply}\n")

asyncio.run(main())