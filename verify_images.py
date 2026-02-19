import asyncio
import os
import httpx
from pathlib import Path
from biralo.agent.tools.web import WebImageSearchTool
from biralo.agent.tools.message import MessageTool
from biralo.bus.events import OutboundMessage

async def send_mock_callback(msg: OutboundMessage):
    print(f"\n[MOCK CALLBACK]")
    print(f"Content: {msg.content}")
    print(f"Media count: {len(msg.media)}")
    if msg.media:
        print(f"Media paths: {msg.media}")
        for path in msg.media:
            if os.path.exists(path):
                print(f"✅ Verified: Downloaded image exists at {path}")

async def test_image_integration():
    print("Starting Internet Image Integration Verification...")
    
    # 1. Search for Image
    print("Step 1: Searching for 'cute cat' image...")
    search_tool = WebImageSearchTool()
    search_results = await search_tool.execute("cute cat", count=1)
    print(f"Search Results:\n{search_results}")
    
    # Extract first URL (simple parsing for verification)
    import re
    urls = re.findall(r'https?://[^\s]+', search_results)
    if not urls:
        print("❌ No URLs found in search results.")
        return
    img_url = urls[0]
    print(f"Selected Image URL: {img_url}")

    # 2. Download Image
    print("\nStep 2: Downloading image...")
    download_path = str(Path("internet_image_test.jpg").resolve())
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            r = await client.get(img_url)
            r.raise_for_status()
            with open(download_path, 'wb') as f:
                f.write(r.content)
        print(f"✅ Image downloaded to: {download_path}")
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return

    # 3. Send Message with Downloaded Image
    print("\nStep 3: Sending message with media...")
    msg_tool = MessageTool(send_callback=send_mock_callback)
    msg_tool.set_context(channel="telegram", chat_id="12345678")
    
    await msg_tool.execute(
        content="Here is a cat image I found on the internet!",
        media=[download_path]
    )

    # 4. Cleanup
    if os.path.exists(download_path):
        os.remove(download_path)
        print(f"\nStep 4: Cleaned up {download_path}")

if __name__ == "__main__":
    asyncio.run(test_image_integration())
    print("\nImage integration verification complete!")
