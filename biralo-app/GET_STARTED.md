# 🚀 Get Started with Biralo Desktop App

**Welcome!** This is your entry point to the Biralo Desktop App.

---

## ⚡ 3-Minute Quick Start

### 1. Install (1 minute)

Open terminal in the `biralo-app` folder and run:

```bash
python install.py
```

This automatically:
- ✅ Checks Python version
- ✅ Installs dependencies
- ✅ Verifies Biralo
- ✅ Creates shortcuts (Windows)

### 2. Launch (30 seconds)

**Windows:**
```bash
launch.bat
```

**macOS/Linux:**
```bash
chmod +x launch.sh
./launch.sh
```

**Or directly:**
```bash
python main.py
```

### 3. Configure (1 minute)

In the app:
1. Click **"Configuration"** tab
2. Click **"Initialize Biralo"**
3. Click **"Open in Editor"**
4. Add your API key:

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

5. Save and close

**Get API Key:** https://openrouter.ai/keys

### 4. Chat! (30 seconds)

1. Click **"Chat"** tab
2. Type: "Hello! What can you help me with?"
3. Press **Enter**
4. Get your response!

---

## 🎯 What You Can Do

### 💬 Chat with AI
- Ask questions
- Get help with code
- Research topics
- Creative writing
- And much more!

### 🌐 Enable Chat Channels
- Connect Telegram bot
- Add Discord integration
- Enable WhatsApp
- Use Email
- And more platforms!

### ⚙️ Customize Everything
- Change AI models
- Adjust settings
- Configure channels
- Personalize experience

---

## 📚 Learn More

### Essential Docs

| Document | What's Inside | Time |
|----------|---------------|------|
| [QUICKSTART.md](QUICKSTART.md) | Detailed 3-min setup | 3 min |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | Complete usage guide | 15 min |
| [FEATURES.md](FEATURES.md) | All features explained | 10 min |

### Reference Docs

| Document | What's Inside |
|----------|---------------|
| [README.md](README.md) | Project overview |
| [INSTALL.md](INSTALL.md) | Installation help |
| [INDEX.md](INDEX.md) | Documentation index |

### Technical Docs

| Document | What's Inside |
|----------|---------------|
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Technical details |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## 🆘 Need Help?

### Common Issues

**"Python not found"**
- Install Python 3.11+ from https://python.org
- Make sure "Add to PATH" is checked

**"Biralo not found"**
```bash
pip install biralo-ai
```

**"No response from AI"**
- Check your API key
- Verify internet connection
- Try a different model

**"Gateway won't start"**
- Configure at least one channel first
- Check credentials are correct
- Look at error logs

### Get Support

- 📖 **Docs**: Read [USAGE_GUIDE.md](USAGE_GUIDE.md)
- 🐛 **Bugs**: https://github.com/HKUDS/biralo/issues
- 💬 **Chat**: https://discord.gg/MnCvHqpUGB
- 📧 **Email**: Via GitHub

---

## ✨ Pro Tips

### Keyboard Shortcuts
- Press **Enter** to send messages quickly
- Use **Ctrl+C** to copy text
- Toggle **Dark Mode** in sidebar

### Best Practices
- Clear chat for new topics
- Use specific questions
- Try different models
- Monitor gateway logs

### Advanced Features
- Enable system tray: `python tray_app.py`
- Run tests: `python test_app.py`
- Multiple configs: Copy and modify config file

---

## 🎓 Learning Path

### Day 1: Basics (30 min)
1. ✅ Install and launch
2. ✅ Configure API key
3. ✅ Send first message
4. ✅ Explore interface
5. ✅ Read QUICKSTART.md

### Day 2: Features (1 hour)
1. ✅ Try different models
2. ✅ Enable a chat channel
3. ✅ Start gateway
4. ✅ Read USAGE_GUIDE.md
5. ✅ Experiment with settings

### Day 3: Advanced (2 hours)
1. ✅ Configure multiple channels
2. ✅ Try system tray version
3. ✅ Read FEATURES.md
4. ✅ Customize configuration
5. ✅ Explore source code

---

## 🌟 What's Next?

After getting started:

### Explore Features
- [FEATURES.md](FEATURES.md) - See what's possible
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Learn advanced usage

### Enable Channels
- Configure Telegram bot
- Add Discord integration
- Connect WhatsApp
- Set up Email

### Customize
- Try different AI models
- Adjust settings
- Create custom configs
- Modify the code

### Contribute
- Report bugs
- Suggest features
- Improve docs
- Submit code

---

## 📊 Quick Reference

### File Locations
- **Config**: `~/.biralo/config.json`
- **Workspace**: `~/.biralo/workspace/`
- **App**: `biralo-app/` folder

### Commands
```bash
# Install
python install.py

# Launch
python main.py

# Test
python test_app.py

# System tray
python tray_app.py
```

### API Keys
- **OpenRouter**: https://openrouter.ai/keys
- **Brave Search**: https://brave.com/search/api/

### Support
- **GitHub**: https://github.com/HKUDS/biralo
- **Discord**: https://discord.gg/MnCvHqpUGB
- **Docs**: All .md files in this folder

---

## 🎉 You're Ready!

You now have everything you need to start using Biralo Desktop App.

**Next Steps:**
1. ✅ Complete the 3-minute quick start above
2. ✅ Send your first message
3. ✅ Explore the features
4. ✅ Read more docs as needed

**Enjoy your AI assistant!** 🐈

---

## 📞 Stay Connected

- ⭐ **Star** the project on GitHub
- 💬 **Join** Discord community
- 🐛 **Report** issues you find
- 💡 **Share** your ideas
- 🤝 **Contribute** improvements

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-12  
**License**: MIT

**Built with ❤️ by the Biralo community**
