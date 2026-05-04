import asyncio
from app.services.bot import process_message
from app.services import session_store

TEST_PHONE = "923001234567"

async def chat(msg: str):
    print(f"\n👤 Customer: {msg}")
    reply = await process_message(TEST_PHONE, msg)
    print(f"\n🤖 Bot:\n{reply}")
    print("\n" + "═"*50)

async def main():
    print("═"*50)
    print("  TEZZ DELIVERY — Full Flow Test")
    print("═"*50)

    await chat("hi")
    await chat("show me the menu")       # NLP test
    await chat("3")
    await chat("5x2")
    await chat("i want item 7")          # NLP test
    await chat("cart")
    await chat("place my order")         # NLP test - "done"
    await chat("Ahmad Ali")
    await chat("03001234567")            # phone number
    await chat("House 12, Street 4, G-10/1, Islamabad")
    await chat("Now")
    await chat("easypaisa")              # payment method
    await chat("03211234567")            # easypaisa number
    await chat("yes confirm it")         # NLP test - confirm

    print("\n✅ Test complete!")
    for o in session_store.get_all_orders():
        print(f"  • {o.order_id} | {o.customer_name} | {o.payment_method} | Rs. {o.grand_total}")

if __name__ == "__main__":
    asyncio.run(main())