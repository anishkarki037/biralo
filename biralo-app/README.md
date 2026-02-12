# 🐈 Biralo Desktop App

<div align="center">
  <h3>Modern Desktop Application for Biralo AI Assistant</h3>
  <p>Built with Python & CustomTkinter</p>
  
  <img src="https://img.shields.io/badge/python-3.11+-blue" alt="Python">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</div>

---

## ✨ Features

### 💬 Interactive Chat
- Real-time messaging with Biralo AI
- Message history with timestamps
- Quick send with Enter key
- Non-blocking UI with threaded processing
- Clear chat functionality

### ⚙️ Configuration Manager
- View and edit Biralo configuration
- JSON syntax highlighting
- One-click initialization
- Open in system editor
- Real-time status indicators

### 🌐 Gateway Control
- Start/stop gateway with one click
- Real-time log streaming
- Monitor all channel activity
- Process management
- Auto-cleanup on exit

### 🎨 Modern UI
- Clean, minimalist design
- Dark/Light theme toggle
- Responsive layout (min 900x600)
- Smooth animations
- Professional appearance

### 🔔 System Tray (Optional)
- Minimize to tray
- Quick access menu
- Background operation
- Custom icon

---

## 🚀 Quick Start

### 1. Install

**Automatic (Recommended):**
```bash
cd biralo-app
python install.py
```

**Manual:**
```bash
pip install -r requirements.txt
```

### 2. Launch

**Windows:**
```bash
launch.bat
```

**macOS/Linux:**
```bash
chmod +x launch.sh
./launch.sh
```

**Direct:**
```bash
python main.py
```

### 3. Configure

1. Click "Initialize Biralo" in Configuration tab
2. Add your API keys to `~/.biralo/config.json`
3. Start chatting!

**Example config:**
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

Get API keys: [OpenRouter](https://openrouter.ai/keys)

---

## 📋 Requirements

### Minimum
- Python 3.11+
- 100 MB disk space
- 256 MB RAM
- Internet connection

### Dependencies
- `customtkinter>=5.2.0` - Modern UI framework
- `biralo-ai>=0.1.3` - Biralo AI core

### Optional
- `pystray` - System tray support
- `pillow` - Icon support
- `pywin32` - Windows shortcuts

---

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 3 minutes
- **[INSTALL.md](INSTALL.md)** - Detailed installation guide
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

---

## 🎯 Usage

### Chat Interface
1. Go to Chat tab
2. Type your message
3. Press Enter or click Send
4. View AI responses in real-time

### Gateway Control
1. Configure channels in `~/.biralo/config.json`
2. Go to Gateway tab
3. Click "Start Gateway"
4. Monitor logs in real-time

### Configuration
1. Go to Configuration tab
2. View current settings
3. Click "Open in Editor" to modify
4. Click "Reload Config" to refresh

---

## 🔧 Advanced Features

### System Tray Mode

For minimize-to-tray functionality:

```bash
pip install pystray pillow
python tray_app.py
```

Features:
- Minimize to system tray
- Quick access menu
- Background operation
- Tray notifications

### Testing

Verify your installation:

```bash
python test_app.py
```

This checks:
- Python version
- Dependencies
- Biralo CLI
- Config files
- App files

---

## 🖥️ Platform Support

### ✅ Windows
- Native look and feel
- `.bat` launcher included
- Desktop shortcuts
- System tray support

### ✅ macOS
- Native appearance
- `.sh` launcher included
- Dock integration
- System tray support

### ✅ Linux
- GTK/Qt compatible
- `.sh` launcher included
- Desktop entries
- System tray support

---

## 🐛 Troubleshooting

### "Biralo not found"
```bash
pip install biralo-ai
```

### "customtkinter not found"
```bash
pip install customtkinter
```

### "Config file not found"
Click "Initialize Biralo" in the Configuration tab.

### Gateway won't start
Ensure you have at least one channel configured in `~/.biralo/config.json`.

### More help
See [INSTALL.md](INSTALL.md) for detailed troubleshooting.

---

## 🎨 Screenshots

### Chat Interface
Clean, modern chat with real-time responses.

### Configuration Manager
View and edit your Biralo settings with syntax highlighting.

### Gateway Control
Monitor all channel activity with live log streaming.

---

## 🛠️ Development

### Project Structure
```
biralo-app/
├── main.py              # Main application
├── tray_app.py          # System tray version
├── install.py           # Installation helper
├── test_app.py          # Test suite
├── requirements.txt     # Dependencies
├── launch.bat           # Windows launcher
├── launch.sh            # Unix launcher
└── docs/
    ├── README.md        # This file
    ├── QUICKSTART.md    # Quick start guide
    ├── INSTALL.md       # Installation guide
    ├── FEATURES.md      # Feature list
    └── CHANGELOG.md     # Version history
```

### Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - Same as Biralo

---

## 🙏 Acknowledgments

- Built on [Biralo AI](https://github.com/HKUDS/biralo)
- UI powered by [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Inspired by modern desktop app design

---

## 📞 Support

- 📖 **Documentation**: [Biralo Docs](https://github.com/HKUDS/biralo#readme)
- 🐛 **Issues**: [GitHub Issues](https://github.com/HKUDS/biralo/issues)
- 💬 **Discord**: [Join Community](https://discord.gg/MnCvHqpUGB)
- 📧 **Email**: Support via GitHub

---

## 🗺️ Roadmap

- [ ] Voice input/output
- [ ] File drag & drop
- [ ] Multi-session support
- [ ] Export chat history
- [ ] Custom themes
- [ ] Keyboard shortcuts
- [ ] Plugin system
- [ ] Auto-updates

---

<div align="center">
  <p>Made with ❤️ for the Biralo community</p>
  <p>⭐ Star us on <a href="https://github.com/HKUDS/biralo">GitHub</a></p>
</div>
