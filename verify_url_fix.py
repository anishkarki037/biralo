import asyncio
import os
from biralo.agent.tools.message import MessageTool
from biralo.bus.events import OutboundMessage

async def send_mock_callback(msg: OutboundMessage):
    print(f"\n[MOCK CALLBACK]")
    print(f"Content: {msg.content}")
    print(f"Media count: {len(msg.media)}")
    if msg.media:
        print(f"URL passed: {msg.media[0]}")
        if msg.media[0].startswith('http'):
            print(f"✅ Verified: Direct URL passed to channel.")
        else:
            print(f"❌ Error: Expected URL, got path.")

async def verify_url_message():
    print("Verifying direct URL messaging support...")
    
    # Setup MessageTool with Mock Callback
    tool = MessageTool(send_callback=send_mock_callback)
    tool.set_context(channel="telegram", chat_id="12345678")

    # Attempt to send message with direct URL
    test_url = "https://example.com/image.jpg"
    await tool.execute(
        content="Testing direct URL send.",
        media=[test_url]
    )

if __name__ == "__main__":
    asyncio.run(verify_url_message())
    print("\nURL verification complete!")
