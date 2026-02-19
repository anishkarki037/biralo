import asyncio
import os
import mss
from pathlib import Path
from biralo.agent.tools.message import MessageTool
from biralo.bus.events import OutboundMessage

async def send_mock_callback(msg: OutboundMessage):
    print(f"\n[MOCK CALLBACK]")
    print(f"Channel: {msg.channel}")
    print(f"Chat ID: {msg.chat_id}")
    print(f"Content: {msg.content}")
    print(f"Media count: {len(msg.media)}")
    if msg.media:
        print(f"Media paths: {msg.media}")
        for path in msg.media:
            if os.path.exists(path):
                print(f"✅ Verified: Media exists at {path}")
            else:
                print(f"❌ Error: Media NOT found at {path}")

async def test_vision_flow():
    print("Starting Vision Verification Flow...")
    
    # 1. Capture Screenshot
    print("Step 1: Capturing screenshot using 'mss'...")
    try:
        with mss.mss() as sct:
            filename = sct.shot(output="vision_test.png")
            full_path = str(Path(filename).resolve())
            print(f"✅ Screenshot captured: {full_path}")
    except Exception as e:
        print(f"❌ Screenshot capture failed: {e}")
        return

    # 2. Setup MessageTool with Mock Callback
    print("\nStep 2: Initializing MessageTool with mock sender...")
    tool = MessageTool(send_callback=send_mock_callback)
    tool.set_context(channel="telegram", chat_id="12345678")

    # 3. Attempt to send message with media
    print("Step 3: Sending message with media...")
    result = await tool.execute(
        content="Vision Verification: Screenshot attached.",
        media=[full_path]
    )
    print(f"Tool call result: {result}")

    # 4. Cleanup
    if os.path.exists(full_path):
        os.remove(full_path)
        print(f"\nStep 4: Cleaned up {full_path}")

if __name__ == "__main__":
    asyncio.run(test_vision_flow())
    print("\nVision verification complete!")
