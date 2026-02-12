# 📚 Biralo Desktop App - Documentation Index

Complete navigation guide to all documentation.

---

## 🚀 Quick Links

| Document | Purpose | Time to Read |
|----------|---------|--------------|
| [README.md](README.md) | Project overview & quick start | 5 min |
| [QUICKSTART.md](QUICKSTART.md) | Get running in 3 minutes | 3 min |
| [INSTALL.md](INSTALL.md) | Detailed installation guide | 10 min |
| [USAGE_GUIDE.md](USAGE_GUIDE.md) | Complete usage instructions | 15 min |
| [FEATURES.md](FEATURES.md) | Full feature list | 10 min |
| [CHANGELOG.md](CHANGELOG.md) | Version history | 5 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Technical overview | 10 min |

---

## 📖 Documentation by Purpose

### For New Users

**Start Here:**
1. [README.md](README.md) - Understand what this is
2. [QUICKSTART.md](QUICKSTART.md) - Get it running
3. [USAGE_GUIDE.md](USAGE_GUIDE.md) - Learn to use it

**Then:**
- [FEATURES.md](FEATURES.md) - See what's possible
- [INSTALL.md](INSTALL.md) - Troubleshoot if needed

### For Developers

**Start Here:**
1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical overview
2. [README.md](README.md) - Project structure
3. Source code: `main.py`, `tray_app.py`

**Then:**
- [FEATURES.md](FEATURES.md) - Feature implementation
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [INSTALL.md](INSTALL.md) - Build process

### For Troubleshooting

**Start Here:**
1. [USAGE_GUIDE.md](USAGE_GUIDE.md) - Troubleshooting section
2. [INSTALL.md](INSTALL.md) - Installation issues
3. [QUICKSTART.md](QUICKSTART.md) - Common problems

**Then:**
- Run `python test_app.py` - Verify installation
- Check GitHub Issues
- Ask on Discord

---

## 📋 Documentation by Topic

### Installation

| Topic | Document | Section |
|-------|----------|---------|
| Quick install | [QUICKSTART.md](QUICKSTART.md) | Step 1 |
| Detailed install | [INSTALL.md](INSTALL.md) | All |
| Auto installer | [INSTALL.md](INSTALL.md) | Automatic |
| Manual install | [INSTALL.md](INSTALL.md) | Manual |
| Platform-specific | [INSTALL.md](INSTALL.md) | Platform-Specific |
| Dependencies | [README.md](README.md) | Requirements |
| Verification | [INSTALL.md](INSTALL.md) | Verify Installation |
| Troubleshooting | [INSTALL.md](INSTALL.md) | Troubleshooting |

### Configuration

| Topic | Document | Section |
|-------|----------|---------|
| First setup | [QUICKSTART.md](QUICKSTART.md) | Step 3 |
| Config structure | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Configuration |
| API keys | [QUICKSTART.md](QUICKSTART.md) | Example Configuration |
| Channels | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Common Settings |
| Models | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Task 1 |
| Advanced | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Advanced Usage |

### Usage

| Topic | Document | Section |
|-------|----------|---------|
| Chat interface | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Chat Interface |
| Gateway control | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Gateway Control |
| Configuration | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Configuration |
| Tips & tricks | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Tips & Tricks |
| Common tasks | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Common Tasks |
| Best practices | [USAGE_GUIDE.md](USAGE_GUIDE.md) | Best Practices |

### Features

| Topic | Document | Section |
|-------|----------|---------|
| Overview | [README.md](README.md) | Features |
| Complete list | [FEATURES.md](FEATURES.md) | All |
| Core features | [FEATURES.md](FEATURES.md) | Core Features |
| UI/UX | [FEATURES.md](FEATURES.md) | UI/UX Features |
| Advanced | [FEATURES.md](FEATURES.md) | Advanced Features |
| Planned | [FEATURES.md](FEATURES.md) | Planned Features |

### Technical

| Topic | Document | Section |
|-------|----------|---------|
| Architecture | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Technical Architecture |
| File structure | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | File Structure |
| Dependencies | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Dependencies |
| Performance | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Performance |
| Security | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Security |
| Development | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Development Guidelines |

---

## 🎯 Quick Reference

### Installation Commands

```bash
# Automatic install
python install.py

# Manual install
pip install -r requirements.txt

# Test installation
python test_app.py

# Launch app
python main.py

# Launch with tray
python tray_app.py
```

### Configuration Locations

- **Config file**: `~/.biralo/config.json`
- **Workspace**: `~/.biralo/workspace/`
- **Logs**: Gateway tab in app

### Common Tasks

| Task | Command/Action |
|------|----------------|
| Initialize | Click "Initialize Biralo" |
| Edit config | Click "Open in Editor" |
| Start chat | Type message, press Enter |
| Start gateway | Click "▶ Start Gateway" |
| Change theme | Toggle "Dark Mode" |
| Clear chat | Click "Clear" button |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Send message |
| `Ctrl+C` | Copy text |
| `Ctrl+V` | Paste text |

### Support Links

- **GitHub**: https://github.com/HKUDS/biralo
- **Discord**: https://discord.gg/MnCvHqpUGB
- **Issues**: https://github.com/HKUDS/biralo/issues
- **Docs**: https://github.com/HKUDS/biralo#readme

---

## 📁 File Reference

### Application Files

| File | Purpose | Lines |
|------|---------|-------|
| `main.py` | Main application | ~800 |
| `tray_app.py` | System tray version | ~200 |
| `install.py` | Auto installer | ~150 |
| `test_app.py` | Test suite | ~150 |
| `setup.py` | Package setup | ~30 |

### Launcher Files

| File | Platform | Purpose |
|------|----------|---------|
| `launch.bat` | Windows | Quick launcher |
| `launch.sh` | Unix | Quick launcher |

### Configuration Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Dependencies |
| `.gitignore` | Git ignore rules |

### Documentation Files

| File | Purpose | Pages |
|------|---------|-------|
| `README.md` | Main docs | 3 |
| `QUICKSTART.md` | Quick start | 2 |
| `INSTALL.md` | Installation | 4 |
| `USAGE_GUIDE.md` | Usage guide | 6 |
| `FEATURES.md` | Feature list | 4 |
| `CHANGELOG.md` | Version history | 2 |
| `PROJECT_SUMMARY.md` | Technical overview | 5 |
| `INDEX.md` | This file | 2 |

---

## 🔍 Search Guide

### Looking for...

**"How do I install?"**
→ [INSTALL.md](INSTALL.md) or [QUICKSTART.md](QUICKSTART.md)

**"How do I use the chat?"**
→ [USAGE_GUIDE.md](USAGE_GUIDE.md) - Chat Interface

**"How do I configure?"**
→ [USAGE_GUIDE.md](USAGE_GUIDE.md) - Configuration

**"What features are available?"**
→ [FEATURES.md](FEATURES.md)

**"How do I enable Telegram?"**
→ [USAGE_GUIDE.md](USAGE_GUIDE.md) - Task 2

**"Something's not working"**
→ [USAGE_GUIDE.md](USAGE_GUIDE.md) - Troubleshooting

**"Technical details?"**
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**"What's new?"**
→ [CHANGELOG.md](CHANGELOG.md)

**"How do I contribute?"**
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Contribution Guidelines

---

## 📊 Documentation Stats

- **Total files**: 8 documentation files
- **Total pages**: ~30 pages
- **Total words**: ~15,000 words
- **Reading time**: ~90 minutes (all docs)
- **Quick start time**: 3 minutes
- **Coverage**: Complete

---

## 🎓 Learning Path

### Beginner Path (30 minutes)

1. **Read**: [README.md](README.md) (5 min)
2. **Follow**: [QUICKSTART.md](QUICKSTART.md) (3 min)
3. **Install**: Run `python install.py` (2 min)
4. **Configure**: Add API key (5 min)
5. **Try**: Send first message (5 min)
6. **Explore**: [USAGE_GUIDE.md](USAGE_GUIDE.md) basics (10 min)

### Intermediate Path (60 minutes)

1. Complete Beginner Path
2. **Read**: [FEATURES.md](FEATURES.md) (10 min)
3. **Read**: [USAGE_GUIDE.md](USAGE_GUIDE.md) fully (15 min)
4. **Try**: Enable a channel (15 min)
5. **Experiment**: Different models (10 min)
6. **Practice**: Common tasks (10 min)

### Advanced Path (120 minutes)

1. Complete Intermediate Path
2. **Read**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) (10 min)
3. **Study**: Source code (30 min)
4. **Read**: [INSTALL.md](INSTALL.md) fully (10 min)
5. **Experiment**: System tray version (10 min)
6. **Customize**: Modify code (30 min)
7. **Contribute**: Submit improvements (30 min)

---

## 🆘 Help Decision Tree

```
Problem?
├─ Installation issue?
│  └─ See INSTALL.md → Troubleshooting
├─ Usage question?
│  └─ See USAGE_GUIDE.md → Relevant section
├─ Feature question?
│  └─ See FEATURES.md
├─ Technical question?
│  └─ See PROJECT_SUMMARY.md
├─ Bug report?
│  └─ GitHub Issues
└─ General question?
   └─ Discord Community
```

---

## 📝 Documentation Maintenance

### For Contributors

When updating docs:
1. Update relevant file
2. Update this INDEX.md if structure changes
3. Update CHANGELOG.md
4. Check all cross-references
5. Test all commands
6. Verify all links

### Documentation Standards

- Clear, concise language
- Code examples for technical content
- Screenshots where helpful (planned)
- Cross-references between docs
- Table of contents for long docs
- Consistent formatting

---

## 🎉 Conclusion

This index helps you navigate all Biralo Desktop App documentation efficiently.

**Quick Start**: [QUICKSTART.md](QUICKSTART.md)  
**Full Guide**: [USAGE_GUIDE.md](USAGE_GUIDE.md)  
**Support**: Discord or GitHub Issues

Happy exploring! 🐈

---

**Last Updated**: 2026-02-12  
**Version**: 1.0.0  
**Maintained By**: Biralo Community
