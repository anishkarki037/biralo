# 🚀 Quick Start Guide

Get up and running with Biralo Desktop App in 3 minutes!

## Step 1: Install

### Option A: Automatic Installation (Recommended)
```bash
python install.py
```

### Option B: Manual Installation
```bash
pip install -r requirements.txt
```

## Step 2: Launch

### Windows
```bash
launch.bat
```
Or double-click `launch.bat`

### macOS/Linux
```bash
chmod +x launch.sh
./launch.sh
```

Or directly:
```bash
python main.py
```

## Step 3: Configure

1. Click **"Initialize Biralo"** in the Configuration tab
2. The app will create `~/.biralo/config.json`
3. Click **"Open in Editor"** to add your API keys

### Example Configuration

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-YOUR_KEY_HERE"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

Get API keys:
- **OpenRouter**: https://openrouter.ai/keys (recommended)
- **Brave Search**: https://brave.com/search/api/ (optional, for web search)

## Step 4: Start Chatting!

1. Go to the **Chat** tab
2. Type your message
3. Press Enter or click Send
4. Enjoy your AI assistant!

## Optional: Enable Chat Channels

Want to chat via Telegram, Discord, or WhatsApp?

1. Go to **Gateway** tab
2. Click **"Start Gateway"**
3. Configure your channels in `~/.biralo/config.json`

See the main README for channel setup instructions.

## Troubleshooting

### "Biralo not found"
Install Biralo:
```bash
pip install biralo-ai
```

### "Config file not found"
Click "Initialize Biralo" in the Configuration tab.

### Gateway won't start
Make sure you've configured at least one channel in your config file.

### Chat not responding
Check that:
1. You have a valid API key in config
2. You have internet connection
3. The model name is correct

## Tips

- Use **Dark/Light mode** toggle in the sidebar
- **Clear Chat** to start fresh conversations
- **Gateway logs** show real-time activity
- Press **Enter** to send messages quickly

## Need Help?

- 📖 Full docs: https://github.com/HKUDS/biralo
- 💬 Discord: https://discord.gg/MnCvHqpUGB
- 🐛 Issues: https://github.com/HKUDS/biralo/issues

Enjoy using Biralo! 🐈
