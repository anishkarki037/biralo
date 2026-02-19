import asyncio
import json
from pathlib import Path
from biralo.agent.loop import AgentLoop
from biralo.bus.queue import MessageBus
from biralo.bus.events import InboundMessage, OutboundMessage
from biralo.providers.base import LLMProvider, LLMResponse

class MockVisionProvider(LLMProvider):
    async def chat(self, messages, tools=None, model=None, **kwargs):
        model_name = model or "default-model"
        print(f"\n[MOCK PROVIDER] Calling model: {model_name}")
        
        # Check if it's the vision model
        if "gemini" in model_name.lower() or "vision" in model_name.lower():
            # Check if messages contain image data
            has_image = any(isinstance(m.get('content'), list) for m in messages)
            if has_image:
                print("📸 Vision model detected image data!")
                return LLMResponse(content="This is a beautiful landscape with mountains and a lake.")
        
        # Main model response
        # Find if visual context was injected
        content = str(messages[-1]['content'])
        if "[Visual Context:" in content:
            print("🧠 Main model received visual context!")
            return LLMResponse(content="I see the mountains and lake you mentioned. It looks very peaceful.")
            
        return LLMResponse(content="I don't see any visual context here.")

    def get_default_model(self):
        return "claude-3-opus"

async def test_vision_switch():
    print("Starting Agentic Vision Switch Verification...")
    
    bus = MessageBus()
    provider = MockVisionProvider()
    workspace = Path("./test_workspace")
    workspace.mkdir(exist_ok=True)
    
    # Initialize AgentLoop with a vision model
    agent = AgentLoop(
        bus=bus,
        provider=provider,
        workspace=workspace,
        vision_model="gemini-1.5-pro"
    )
    
    # Create a mock message with media
    # We'll use a dummy path, the provider is mocked anyway
    msg = InboundMessage(
        channel="telegram",
        sender_id="user123",
        chat_id="chat456",
        content="What do you think of this view?",
        media=["D:/biralo/biralo-logo.png"] # Use an existing file to pass checks
    )
    
    # Process the message
    print("\nProcessing message with image...")
    response = await agent._process_message(msg)
    
    print(f"\nFinal Agent Response: {response.content}")
    
    if "I see the mountains" in response.content:
        print("\n✅ VERIFICATION SUCCESS: Vision switch worked perfectly!")
    else:
        print("\n❌ VERIFICATION FAILED: Visual context was not processed or injected correctly.")

if __name__ == "__main__":
    asyncio.run(test_vision_switch())
