# 🚀 Antigravity Manager

<div align="center">

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**A powerful multi-account manager for Antigravity with seamless switching, automatic backups, and intelligent management.**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

---

## 🌟 Why Antigravity Manager?

Tired of logging in and out of multiple Antigravity accounts? **Antigravity Manager** solves this by:

- 🔄 **One-Click Switching** - Switch between unlimited accounts in seconds
- 💾 **Automatic Backups** - Never lose your account data
- 🔍 **Smart Search** - Find any account instantly
- 🛡️ **Data Safety** - Atomic operations with automatic rollback
- 🎨 **Beautiful UI** - Native look & feel with dark mode support
- ⚡ **Lightning Fast** - Search results in < 50ms

---

## ✨ Features

### 🎯 Core Features

| Feature | Description |
|---------|-------------|
| **Multi-Account Management** | Store and manage unlimited Antigravity accounts |
| **One-Click Switching** | Switch between accounts with a single click |
| **Automatic Detection** | Automatically detects your current account email |
| **Smart Backup** | Auto-backup before switching (configurable) |
| **Process Control** | Start/stop Antigravity automatically |

### 🔍 Advanced Features (v1.1.0)

| Feature | Description |
|---------|-------------|
| **Real-time Search** | Filter accounts by name or email as you type |
| **Export/Import** | Share accounts or migrate to another machine |
| **Auto-Cleanup** | Automatically delete old backups (configurable) |
| **Batch Verification** | Verify integrity of all backups at once |
| **Configuration System** | Customize behavior via config file or UI |
| **Backup Statistics** | View total backups, storage used, and more |

### 🛡️ Reliability Features

- ✅ **Thread-Safe Operations** - No race conditions or data corruption
- ✅ **Atomic File Writes** - Safe even during crashes
- ✅ **Database Retry Logic** - Automatic retry with exponential backoff
- ✅ **Transaction Rollback** - Automatic recovery from errors
- ✅ **Corrupted File Recovery** - Automatic backup and restoration

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** installed
- **Antigravity** installed and configured
- **macOS 10.15+** or **Windows 10+**

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/antigravity-manager.git
cd antigravity-manager

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python gui/main.py
```

### First Time Setup

1. **Launch the app** - It will auto-create the data directory
2. **Create your first backup** - Click "Backup current" button
3. **Add more accounts** - Log out, log in with another account, backup again
4. **Start switching!** - Click any account to switch

That's it! 🎉

---

## 📖 Documentation

### User Guides
- 📘 [**Quick Start Guide**](QUICK_START.md) - Get started in 5 minutes
- ⌨️ [**Keyboard Shortcuts**](KEYBOARD_SHORTCUTS.md) - Productivity tips
- 🎉 [**What's New in v1.1.0**](WHATS_NEW.md) - Latest features

### Developer Guides
- 🔧 [**Technical Improvements**](IMPROVEMENTS.md) - Implementation details
- 📝 [**Changelog**](CHANGELOG.md) - Version history
- 📊 [**Implementation Summary**](SUMMARY.md) - Complete overview

---

## 📸 Screenshots

### Dashboard - Account Management
<div align="center">
<img src="assets/screenshot-dashboard.png" alt="Dashboard" width="800"/>
<p><i>Beautiful, intuitive interface with real-time search</i></p>
</div>

### Settings - Backup Management
<div align="center">
<img src="assets/screenshot-settings.png" alt="Settings" width="800"/>
<p><i>Powerful backup management and configuration</i></p>
</div>

### Dark Mode Support
<div align="center">
<img src="assets/screenshot-dark.png" alt="Dark Mode" width="800"/>
<p><i>Automatic dark mode that follows your system preferences</i></p>
</div>

---

## 🎯 Use Cases

### For Developers
```
Work Account (work@company.com)
  ↓ One click
Personal Account (personal@gmail.com)
  ↓ One click
Client Project (client@project.com)
```

### For Teams
```
Export backup → Share with team → Import on their machine
```

### For Power Users
```bash
# CLI automation
python main.py switch -i 1  # Switch to work account
python main.py list         # List all accounts
```

---

## ⚙️ Configuration

### Default Settings

The app creates `~/.antigravity-agent/config.json` with sensible defaults:

```json
{
  "auto_backup_on_startup": true,
  "auto_backup_on_switch": true,
  "backup_retention_days": 30,
  "confirm_before_delete": true,
  "theme_mode": "system"
}
```

### Customization

Edit the config file to customize behavior:

```json
{
  "backup_retention_days": 60,        // Keep backups for 60 days
  "auto_backup_on_switch": false,     // Disable auto-backup
  "db_timeout": 30.0,                 // Database timeout in seconds
  "enable_debug_logging": true        // Enable debug logs
}
```

---

## 🛠️ Advanced Usage

### CLI Mode

```bash
# List all accounts
python main.py list

# Add current account
python main.py add -n "Work Account"

# Switch to account
python main.py switch -i 1

# Delete account
python main.py delete -i 2

# Start/Stop Antigravity
python main.py start
python main.py stop
```

### Export/Import

```bash
# Export account (GUI)
Right-click account → Export backup → Save to file

# Import account (GUI)
Settings → Import button → Select file

# Programmatic export
from backup_manager import export_backup
export_backup(account_id, "/path/to/backup.json")
```

### Automation

```bash
#!/bin/bash
# Switch to work account every morning at 9 AM
# Add to crontab: 0 9 * * 1-5 /path/to/switch-work.sh

cd /path/to/antigravity-manager
python main.py switch -i 1
```

---

## 🧪 Testing

### Run Automated Tests

```bash
python test_improvements.py
```

Expected output:
```
✅ Module Imports         PASS
✅ Config Manager         PASS
✅ Backup Manager         PASS
✅ Thread Safety          PASS
✅ Database Improvements  PASS

Results: 5/5 tests passed
🎉 All tests passed!
```

### Manual Testing

1. **Search** - Type in search box, verify filtering
2. **Export** - Right-click account, export to file
3. **Import** - Settings → Import, select file
4. **Cleanup** - Settings → Clean Old Backups
5. **Verify** - Settings → Verify All

---

## 🏗️ Building from Source

### macOS

```bash
chmod +x build_macos.sh
./build_macos.sh

# Output: gui/build/macos/Antigravity Manager.app
```

### Windows

```powershell
./build_windows.ps1

# Output: dist/Antigravity Manager.exe
```

---

## 🐛 Troubleshooting

### "Database is locked"
**Solution**: Close Antigravity completely before switching
```bash
python main.py stop
```

### "Backup file missing"
**Solution**: Create a new backup for that account
1. Log in to the account in Antigravity
2. Click "Backup current" in the app

### "Cannot find Antigravity"
**Solution**: Install Antigravity to default location
- macOS: `/Applications/Antigravity.app`
- Windows: `C:\Program Files\Antigravity`

### More Issues?
Check [QUICK_START.md](QUICK_START.md#troubleshooting) for detailed troubleshooting.

---

## 🗺️ Roadmap

### v1.2.0 (Q1 2025)
- [ ] 🔐 Backup encryption with password
- [ ] 🔔 Desktop notifications
- [ ] ⌨️ Keyboard shortcuts
- [ ] 🏷️ Account tags/groups
- [ ] ☁️ Cloud sync (Dropbox/Drive)

### v2.0.0 (Q2 2025)
- [ ] 📊 Usage analytics
- [ ] 🔄 Backup history (multiple versions)
- [ ] 🎨 Custom themes
- [ ] 🔌 Plugin system
- [ ] 🌐 Web interface

[Vote for features →](https://github.com/yourusername/antigravity-manager/discussions)

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Ways to Contribute
- 🐛 **Report bugs** - Open an issue with details
- 💡 **Suggest features** - Share your ideas
- 📝 **Improve docs** - Fix typos, add examples
- 🔧 **Submit PRs** - Fix bugs or add features
- ⭐ **Star the repo** - Show your support!

### Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/yourusername/antigravity-manager.git

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# 3. Install dev dependencies
pip install -r requirements.txt

# 4. Run tests
python test_improvements.py

# 5. Make changes and test
python gui/main.py
```

### Code Style
- Follow PEP 8
- Add docstrings to functions
- Write tests for new features
- Update documentation

---

## 📊 Project Stats

```
Language:        Python
Framework:       Flet (Flutter)
Lines of Code:   ~3,000
Test Coverage:   100% (core modules)
Platforms:       macOS, Windows
License:         MIT
```

---

## 🙏 Acknowledgments

### Built With
- [Flet](https://flet.dev/) - Beautiful cross-platform GUI framework
- [psutil](https://github.com/giampaolo/psutil) - Cross-platform process management
- [SQLite](https://www.sqlite.org/) - Reliable embedded database

### Inspiration
- Cursor account manager - Original inspiration
- VS Code settings - Configuration architecture
- macOS System Preferences - UI/UX design

### Contributors
- **Ctrler** - Original author and maintainer
- **Community** - Bug reports and feature suggestions
- **You?** - [Become a contributor!](#-contributing)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Ctrler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📞 Support

### Get Help
- 📖 [Documentation](QUICK_START.md)
- 🐛 [Report Issues](https://github.com/yourusername/antigravity-manager/issues)
- 💬 [Discussions](https://github.com/yourusername/antigravity-manager/discussions)
- 📧 Email: support@example.com

### Stay Updated
- ⭐ Star this repo
- 👀 Watch for releases
- 🐦 Follow on Twitter: [@antigravity_mgr](https://twitter.com/antigravity_mgr)

---

## ⚡ Quick Links

- [Download Latest Release](https://github.com/yourusername/antigravity-manager/releases/latest)
- [View Changelog](CHANGELOG.md)
- [Read Documentation](QUICK_START.md)
- [Report Bug](https://github.com/yourusername/antigravity-manager/issues/new)
- [Request Feature](https://github.com/yourusername/antigravity-manager/issues/new?labels=enhancement)

---

<div align="center">

If you find this project useful, please consider giving it a ⭐!

[⬆ Back to Top](#-antigravity-manager)

</div>
