# Changelog

All notable changes to Biralo Desktop App will be documented in this file.

## [1.0.0] - 2026-02-12

### 🎉 Initial Release

#### Added
- **Chat Interface**
  - Real-time messaging with Biralo AI
  - Message history with timestamps
  - Send with Enter key
  - Clear chat functionality
  - Non-blocking threaded message processing

- **Configuration Manager**
  - View current configuration
  - JSON syntax highlighting
  - Reload configuration
  - Open config in system editor
  - One-click initialization
  - Status indicator

- **Gateway Control**
  - Start/stop gateway
  - Real-time log streaming
  - Clear logs
  - Process management
  - Auto-cleanup on exit

- **User Interface**
  - Modern CustomTkinter design
  - Dark/Light theme toggle
  - Responsive layout (min 900x600)
  - Sidebar navigation
  - Status indicators
  - About page with links

- **Platform Support**
  - Windows support with .bat launcher
  - macOS support with .sh launcher
  - Linux support with .sh launcher
  - Cross-platform compatibility

- **Installation**
  - Automated install script
  - Dependency checking
  - Python version validation
  - Desktop shortcut creation (Windows)

- **Documentation**
  - Comprehensive README
  - Quick start guide
  - Installation guide
  - Features documentation
  - Changelog

#### Optional Features
- System tray support (tray_app.py)
- Minimize to tray
- Tray menu with quick actions
- Custom tray icon

### Technical Details
- Python 3.11+ required
- CustomTkinter for modern UI
- Subprocess management for Biralo CLI
- Threading for non-blocking operations
- JSON configuration handling
- Cross-platform file operations

### Known Issues
- None reported yet

### Future Plans
- Voice input/output
- File drag & drop
- Multi-session support
- Export chat history
- Custom themes
- Keyboard shortcuts
- Plugin system
- Auto-updates

---

## Version History

### [1.0.0] - 2026-02-12
- Initial public release
- Core features complete
- Documentation complete
- Cross-platform support

---

## Upgrade Guide

### From Source
```bash
cd biralo-app
git pull
pip install -r requirements.txt --upgrade
```

### Dependencies
```bash
pip install --upgrade biralo-ai customtkinter
```

---

## Breaking Changes

None yet - this is the first release!

---

## Contributors

Thanks to all contributors who helped make this possible!

- Initial development by Biralo community
- Built on top of Biralo AI framework
- Inspired by modern desktop app design

---

## License

MIT License - Same as Biralo

---

## Support

- Report bugs: https://github.com/HKUDS/biralo/issues
- Feature requests: https://github.com/HKUDS/biralo/discussions
- Discord: https://discord.gg/MnCvHqpUGB

---

**Note:** This desktop app is a community contribution to the Biralo project. It provides a graphical interface to the Biralo CLI tools.
