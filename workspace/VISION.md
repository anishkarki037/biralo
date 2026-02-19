# Vision Skill

You are now capable of capturing your system's visual output and communicating it to users via chat channels.

## Core Capabilities

- **Screen Capture**: Take screenshots of the entire display.
- **Visual Reporting**: Send captured images to Telegram, Discord, or other channels to provide visual status updates.

## How to Capture

Use the `mss` library to capture the screen. Here is a standard implementation:

```python
import mss
import os

with mss.mss() as sct:
    # Capture the first monitor
    filename = sct.shot(output="screenshot.png")
    print(f"Captured: {os.path.abspath(filename)}")
```

## How to Send

Use the `message` tool with the `media` parameter:

```python
# Send to the current chat
message(
    content="Here is a screenshot of my current state.",
    media=["D:\\biralo\\workspace\\screenshot.png"]
)
```

## Internet Image Search

You can search for images on the web using the `web_image_search` tool and send them to the user.

### Workflow

1. **Search**: Find image URLs based on a query.
2. **Send (Direct)**: You can pass the URL directly to the `message` tool in the `media` list. The channel will handle the delivery.
3. **Send (Downloaded)**: If a specific file format is needed or the URL is unstable, download it first, then send the local path.

```python
# 1. Search
results = web_image_search(query="majestic mountains")

# 2. Send Direct URL
message(
    content="I found this majestic mountain image from the web.",
    media=["https://example.com/mountain_direct_url.jpg"]
)
```

## Best Practices

1. **Privacy**: Always inform the user before taking a screenshot.
2. **Context**: Provide a text description along with the media to explain what the user is seeing.
3. **Cleanup**: Proactively delete the screenshot file from the workspace after sending it to keep the environment clean.
