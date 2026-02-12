# 📦 Installation Guide

Complete installation instructions for all platforms.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Internet connection

## Quick Install

### Automatic (Recommended)

```bash
cd biralo-app
python install.py
```

This will:
1. Check Python version
2. Install all dependencies
3. Verify Biralo installation
4. Create desktop shortcuts (Windows)

### Manual Install

```bash
cd biralo-app
pip install -r requirements.txt
```

## Platform-Specific Instructions

### Windows

1. **Install Python 3.11+**
   - Download from https://python.org
   - Check "Add Python to PATH" during installation

2. **Install the app**
   ```cmd
   cd biralo-app
   python install.py
   ```

3. **Launch**
   - Double-click `launch.bat`
   - Or run: `python main.py`

4. **Optional: Create Desktop Shortcut**
   - Right-click `launch.bat`
   - Send to → Desktop (create shortcut)

### macOS

1. **Install Python 3.11+**
   ```bash
   brew install python@3.11
   ```

2. **Install the app**
   ```bash
   cd biralo-app
   python3 install.py
   ```

3. **Make launcher executable**
   ```bash
   chmod +x launch.sh
   ```

4. **Launch**
   ```bash
   ./launch.sh
   ```

5. **Optional: Add to Applications**
   - Create an Automator app that runs `launch.sh`
   - Move to Applications folder

### Linux

1. **Install Python 3.11+**
   
   Ubuntu/Debian:
   ```bash
   sudo apt update
   sudo apt install python3.11 python3-pip
   ```
   
   Fedora:
   ```bash
   sudo dnf install python3.11 python3-pip
   ```
   
   Arch:
   ```bash
   sudo pacman -S python python-pip
   ```

2. **Install the app**
   ```bash
   cd biralo-app
   python3 install.py
   ```

3. **Make launcher executable**
   ```bash
   chmod +x launch.sh
   ```

4. **Launch**
   ```bash
   ./launch.sh
   ```

5. **Optional: Create Desktop Entry**
   Create `~/.local/share/applications/biralo.desktop`:
   ```ini
   [Desktop Entry]
   Name=Biralo AI Assistant
   Comment=Desktop app for Biralo
   Exec=/path/to/biralo-app/launch.sh
   Icon=/path/to/biralo-app/icon.png
   Terminal=false
   Type=Application
   Categories=Utility;
   ```

## Optional Features

### System Tray Support

For minimize-to-tray functionality:

```bash
pip install pystray pillow
```

Then launch with:
```bash
python tray_app.py
```

### Windows Desktop Shortcuts

```bash
pip install pywin32
```

Then run `install.py` again to create shortcuts.

## Verify Installation

1. **Check Python version**
   ```bash
   python --version
   # Should show 3.11 or higher
   ```

2. **Check Biralo**
   ```bash
   biralo --help
   # Should show Biralo commands
   ```

3. **Check dependencies**
   ```bash
   pip list | grep -E "customtkinter|biralo"
   ```

4. **Test the app**
   ```bash
   python main.py
   ```

## Troubleshooting

### "Python not found"

**Windows:**
- Reinstall Python with "Add to PATH" checked
- Or add manually: System Properties → Environment Variables

**macOS/Linux:**
- Use `python3` instead of `python`
- Install via package manager

### "pip not found"

```bash
python -m ensurepip --upgrade
```

### "customtkinter not found"

```bash
pip install customtkinter
```

### "biralo not found"

```bash
pip install biralo-ai
```

### Permission errors (Linux/macOS)

```bash
pip install --user -r requirements.txt
```

### Import errors

Make sure you're in the correct directory:
```bash
cd biralo-app
python main.py
```

### "tkinter not found" (Linux)

Ubuntu/Debian:
```bash
sudo apt install python3-tk
```

Fedora:
```bash
sudo dnf install python3-tkinter
```

### App won't start

1. Check Python version: `python --version`
2. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
3. Try: `python -m main`

## Uninstall

### Remove the app

```bash
cd ..
rm -rf biralo-app
```

### Remove Biralo (optional)

```bash
pip uninstall biralo-ai
```

### Remove config (optional)

**Windows:**
```cmd
rmdir /s %USERPROFILE%\.biralo
```

**macOS/Linux:**
```bash
rm -rf ~/.biralo
```

## Upgrade

### Upgrade the app

```bash
cd biralo-app
git pull  # If installed from git
```

### Upgrade dependencies

```bash
pip install -r requirements.txt --upgrade
```

### Upgrade Biralo

```bash
pip install --upgrade biralo-ai
```

## Development Install

For developers who want to modify the app:

```bash
git clone https://github.com/HKUDS/biralo.git
cd biralo/biralo-app
pip install -e .
```

This creates an editable installation.

## Virtual Environment (Recommended)

Keep dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install
pip install -r requirements.txt

# Run
python main.py
```

## Docker (Advanced)

Run in a container:

```bash
# Build
docker build -t biralo-desktop .

# Run (with X11 forwarding on Linux)
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix biralo-desktop
```

Note: GUI apps in Docker require additional setup for display forwarding.

## Next Steps

After installation:

1. Read [QUICKSTART.md](QUICKSTART.md) for first-time setup
2. Configure your API keys
3. Start chatting with Biralo!

## Support

- 📖 Documentation: [README.md](README.md)
- 🐛 Issues: https://github.com/HKUDS/biralo/issues
- 💬 Discord: https://discord.gg/MnCvHqpUGB

---

Happy installing! 🐈
