# 📘 Usage Guide

Complete guide to using Biralo Desktop App effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Chat Interface](#chat-interface)
3. [Configuration](#configuration)
4. [Gateway Control](#gateway-control)
5. [Tips & Tricks](#tips--tricks)
6. [Common Tasks](#common-tasks)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Launch

1. **Start the app**
   ```bash
   python main.py
   ```

2. **You'll see**:
   - Sidebar with navigation
   - Status indicator (Offline/Configured)
   - Chat interface (default view)

3. **Initial setup**:
   - Click "Configuration" in sidebar
   - Click "Initialize Biralo"
   - Wait for confirmation

4. **Add API keys**:
   - Click "Open in Editor"
   - Add your OpenRouter API key
   - Save and close

5. **Start chatting**:
   - Click "Chat" in sidebar
   - Type a message
   - Press Enter

---

## Chat Interface

### Sending Messages

**Method 1: Keyboard**
1. Type your message in the input box
2. Press `Enter`
3. Wait for response

**Method 2: Mouse**
1. Type your message
2. Click "Send" button
3. Wait for response

### Reading Responses

- Messages appear with timestamps
- Format: `[HH:MM:SS] Sender: Message`
- Auto-scrolls to latest message
- History preserved during session

### Managing Chat

**Clear Chat**
- Click "Clear" button
- Removes all messages
- Starts fresh conversation

**Copy Text**
- Select text with mouse
- Right-click → Copy
- Or use Ctrl+C (Cmd+C on Mac)

### Best Practices

✅ **Do:**
- Be specific in your questions
- Wait for responses to complete
- Clear chat for new topics
- Use proper grammar

❌ **Don't:**
- Send multiple messages rapidly
- Expect instant responses
- Include sensitive information
- Use all caps

---

## Configuration

### Viewing Configuration

1. Click "Configuration" in sidebar
2. See your current settings in JSON format
3. Syntax highlighting for readability

### Editing Configuration

**Method 1: System Editor**
1. Click "Open in Editor"
2. Edit in your default text editor
3. Save changes
4. Return to app
5. Click "Reload Config"

**Method 2: Direct Edit**
1. Open `~/.biralo/config.json` manually
2. Edit with any text editor
3. Save changes
4. Click "Reload Config" in app

### Configuration Structure

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "your-key-here"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  },
  "channels": {
    "telegram": {
      "enabled": false
    }
  }
}
```

### Common Settings

**Change Model**
```json
"agents": {
  "defaults": {
    "model": "anthropic/claude-3.5-sonnet"
  }
}
```

**Enable Telegram**
```json
"channels": {
  "telegram": {
    "enabled": true,
    "token": "YOUR_BOT_TOKEN",
    "allowFrom": ["YOUR_USER_ID"]
  }
}
```

**Add Provider**
```json
"providers": {
  "anthropic": {
    "apiKey": "sk-ant-xxx"
  }
}
```

---

## Gateway Control

### What is the Gateway?

The gateway enables Biralo to connect to chat platforms:
- Telegram
- Discord
- WhatsApp
- Slack
- Email
- And more

### Starting the Gateway

1. **Configure channels first**
   - Edit `~/.biralo/config.json`
   - Enable at least one channel
   - Add required credentials

2. **Start gateway**
   - Click "Gateway" in sidebar
   - Click "▶ Start Gateway"
   - Watch logs for status

3. **Verify connection**
   - Look for "Connected" messages
   - Check for errors
   - Test by sending a message

### Monitoring Logs

**What you'll see:**
- Connection status
- Incoming messages
- Outgoing responses
- Errors and warnings
- System events

**Log format:**
```
[HH:MM:SS] Message content
```

**Common messages:**
- `Gateway started` - Successfully started
- `Connected to Telegram` - Channel connected
- `Received message from...` - Incoming message
- `Error:...` - Something went wrong

### Stopping the Gateway

1. Click "⏹ Stop Gateway"
2. Wait for confirmation
3. Gateway disconnects from all channels

### Managing Logs

**Clear Logs**
- Click "Clear Log" button
- Removes all log entries
- Doesn't affect gateway operation

**Copy Logs**
- Select text in log area
- Right-click → Copy
- Useful for troubleshooting

---

## Tips & Tricks

### Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Send message | `Enter` |
| New line in message | `Shift+Enter` (planned) |
| Clear chat | Click button |
| Copy text | `Ctrl+C` / `Cmd+C` |

### Theme Switching

1. Find "Dark Mode" toggle in sidebar
2. Click to switch between dark/light
3. Changes apply immediately
4. Preference saved for next launch

### Window Management

**Resize**
- Drag window edges
- Minimum size: 900x600
- Layout adapts automatically

**Minimize**
- Standard minimize button
- Or use system tray version (tray_app.py)

**Close**
- Click X button
- Gateway stops automatically
- Config saved

### Performance Tips

**For faster responses:**
- Use faster models (e.g., GPT-3.5)
- Keep messages concise
- Close unused apps
- Check internet speed

**For better quality:**
- Use advanced models (e.g., Claude Opus)
- Provide context
- Be specific
- Ask follow-up questions

---

## Common Tasks

### Task 1: Change AI Model

1. Go to Configuration
2. Click "Open in Editor"
3. Find `"model"` field
4. Change to desired model:
   - `anthropic/claude-opus-4-5` (best quality)
   - `anthropic/claude-3.5-sonnet` (balanced)
   - `openai/gpt-4` (OpenAI)
   - `openai/gpt-3.5-turbo` (fast)
5. Save and reload

### Task 2: Enable Telegram Bot

1. Create bot with @BotFather
2. Get bot token
3. Get your user ID
4. Edit config:
```json
"channels": {
  "telegram": {
    "enabled": true,
    "token": "YOUR_TOKEN",
    "allowFrom": ["YOUR_USER_ID"]
  }
}
```
5. Start gateway
6. Message your bot

### Task 3: Export Chat History

Currently manual:
1. Select all text in chat
2. Copy (Ctrl+C)
3. Paste into text file
4. Save

(Auto-export planned for future version)

### Task 4: Reset Configuration

1. Close app
2. Delete `~/.biralo/config.json`
3. Restart app
4. Click "Initialize Biralo"
5. Reconfigure

### Task 5: Update Biralo

```bash
pip install --upgrade biralo-ai
```

Then restart the app.

---

## Troubleshooting

### Chat Issues

**Problem: No response**
- Check internet connection
- Verify API key is valid
- Check model name is correct
- Look for errors in terminal

**Problem: Slow responses**
- Normal for large models
- Try a faster model
- Check internet speed
- Wait patiently

**Problem: Error messages**
- Read error carefully
- Check API key
- Verify model availability
- Check API credits

### Gateway Issues

**Problem: Won't start**
- Check config syntax
- Verify channel credentials
- Look at error logs
- Ensure ports available

**Problem: Disconnects**
- Check internet stability
- Verify credentials
- Look for rate limits
- Check service status

**Problem: No messages**
- Verify bot is added to chat
- Check allowFrom list
- Test with simple message
- Review logs

### Configuration Issues

**Problem: Can't find config**
- Run "Initialize Biralo"
- Check `~/.biralo/` directory
- Verify permissions
- Try manual creation

**Problem: Invalid JSON**
- Check for missing commas
- Verify quotes
- Use JSON validator
- Copy from example

**Problem: Changes not applied**
- Click "Reload Config"
- Restart app
- Check file was saved
- Verify correct file

### UI Issues

**Problem: Window too small**
- Drag to resize
- Minimum is 900x600
- Check screen resolution
- Try maximizing

**Problem: Text not visible**
- Switch theme
- Check contrast
- Adjust system settings
- Update CustomTkinter

**Problem: Buttons not working**
- Check for errors in terminal
- Restart app
- Verify dependencies
- Reinstall if needed

---

## Getting Help

### Self-Help

1. **Check this guide** - Most answers here
2. **Read error messages** - Often self-explanatory
3. **Check logs** - Gateway tab shows details
4. **Test basics** - Verify installation

### Community Help

1. **Discord** - https://discord.gg/MnCvHqpUGB
2. **GitHub Issues** - Report bugs
3. **Discussions** - Ask questions
4. **Documentation** - Read other guides

### Reporting Issues

Include:
- Operating system
- Python version
- Error messages
- Steps to reproduce
- Screenshots if relevant

---

## Best Practices

### Security

- Keep API keys private
- Don't share config files
- Use allowFrom lists
- Review permissions
- Update regularly

### Performance

- Close when not in use
- Clear chat periodically
- Monitor resource usage
- Use appropriate models
- Keep dependencies updated

### Maintenance

- Update Biralo regularly
- Check for app updates
- Review configuration
- Clean up old logs
- Backup config

---

## Advanced Usage

### Multiple Configurations

Create different configs for different purposes:
1. Copy `~/.biralo/config.json`
2. Modify for specific use
3. Switch by editing file
4. Reload in app

### Custom Models

Add custom model endpoints:
```json
"providers": {
  "custom": {
    "apiKey": "your-key",
    "apiBase": "https://your-endpoint.com/v1"
  }
}
```

### Automation

Use with scripts:
```bash
# Start gateway automatically
python -c "from main import BiraloApp; app = BiraloApp(); app.start_gateway()"
```

---

## Conclusion

You now know how to use Biralo Desktop App effectively! 

**Remember:**
- Start with Configuration
- Test with Chat
- Enable Gateway for channels
- Refer to this guide when needed

**Enjoy your AI assistant!** 🐈

---

For more information:
- [README.md](README.md) - Overview
- [QUICKSTART.md](QUICKSTART.md) - Quick setup
- [FEATURES.md](FEATURES.md) - Feature list
- [INSTALL.md](INSTALL.md) - Installation help
