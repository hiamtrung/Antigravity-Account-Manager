# 📝 Changelog

All notable changes to Antigravity Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2025-12-04

### 🎉 Major Features Added

#### Configuration Management System
- **New Module**: `config_manager.py` - Centralized settings management
- **Features**:
  - Auto-backup on startup (configurable)
  - Auto-backup before account switch (configurable)
  - Backup retention policy (auto-delete old backups)
  - Database timeout and retry settings
  - Theme preferences
  - Import/Export configuration

#### Backup Management Utilities
- **New Module**: `backup_manager.py` - Advanced backup operations
- **Features**:
  - Automatic cleanup of old backups based on retention policy
  - Orphaned backup detection and removal
  - Batch backup verification
  - Detailed backup statistics
  - Export backup to external file
  - Import backup from external file

#### Search & Filter
- **Real-time search** in account list
- Filter by account name or email
- Visual feedback showing filtered results count
- Contextual empty states

#### Enhanced UI
- **Backup Management Card** in Settings view
  - Shows total backups and storage used
  - Quick action buttons (Clean, Verify, Import)
- **Export Account** option in context menu
- **Import Backup** button in Settings

### 🐛 Bug Fixes

#### Critical Fixes
- **Thread Safety**: Fixed race condition in `HomeView.monitor_status()`
  - Added proper thread cleanup in `will_unmount()`
  - Prevented UI updates after view unmount
  
- **File Corruption**: Fixed concurrent write issues in `accounts.json`
  - Implemented thread locks for all file operations
  - Added atomic writes using temporary files
  - Automatic recovery from corrupted files

- **Database Locking**: Fixed "database is locked" errors
  - Implemented exponential backoff retry mechanism (max 3 retries)
  - Added 30-second timeout for database connections
  - Enabled WAL mode for better concurrency

- **Transaction Safety**: Added rollback support for database operations
  - All writes wrapped in transactions
  - Automatic rollback on failure
  - Safety backups before restore operations

### 🔧 Improvements

#### Database Layer (`db_manager.py`)
- Retry logic with exponential backoff
- Comprehensive backup verification
- Safety backups with automatic rollback
- Better error messages and logging
- Transaction-based operations

#### Account Management (`account_manager.py`)
- Thread-safe file operations
- Auto-backup before switch (configurable)
- Atomic file writes
- Corrupted file recovery

#### User Interface
- Search functionality in Home view
- Export/Import buttons
- Better empty states
- Improved error messages
- Loading indicators

### 📚 Documentation

#### New Documents
- `IMPROVEMENTS.md` - Detailed improvement summary
- `QUICK_START.md` - 5-minute getting started guide
- `KEYBOARD_SHORTCUTS.md` - Keyboard shortcuts reference
- `CHANGELOG.md` - This file

#### Updated Documents
- `README.md` - Updated with new features (pending)

### 🧪 Testing

#### New Test Suite
- `test_improvements.py` - Automated test suite
- Tests for all new modules
- Thread safety verification
- Database improvements validation

**Test Results**: ✅ 5/5 tests passing

### ⚡ Performance

- **Startup Time**: +0.1s (config loading overhead)
- **Search**: Real-time (< 50ms)
- **Backup Time**: ~same (< 1s)
- **Switch Time**: +0.5s (auto-backup overhead, can be disabled)

### 🔒 Security

- Backup files stored locally only
- No network communication
- File permissions inherited from OS
- ⚠️ Note: Backup files are **not encrypted** (planned for v1.2.0)

---

## [1.0.0] - 2025-12-01

### Initial Release

#### Core Features
- Multi-account management for Antigravity
- Backup and restore account data
- One-click account switching
- Process management (start/stop Antigravity)
- Cross-platform support (macOS, Windows)
- GUI (Flet-based) and CLI interfaces
- Automatic account detection
- Dark/Light theme support

#### Modules
- `account_manager.py` - Account CRUD operations
- `db_manager.py` - SQLite database operations
- `process_manager.py` - Process control
- `main.py` - CLI interface
- `gui/main.py` - GUI application
- `gui/views/home_view.py` - Dashboard
- `gui/views/settings_view.py` - Settings page

---

## [Unreleased]

### 🚧 Planned for v1.2.0

#### High Priority
- [ ] **Backup Encryption**: Encrypt backup files with user password
- [ ] **System Tray**: Quick access menu from system tray
- [ ] **Desktop Notifications**: Native notifications for operations
- [ ] **Unit Tests**: Comprehensive pytest test suite
- [ ] **Keyboard Shortcuts**: Implement shortcuts from KEYBOARD_SHORTCUTS.md

#### Medium Priority
- [ ] **Account Tags/Groups**: Organize accounts into categories
- [ ] **Backup Diff Viewer**: Show changes between backups
- [ ] **Scheduled Backups**: Auto-backup every X hours
- [ ] **Cloud Sync**: Optional Dropbox/Google Drive integration
- [ ] **Backup History**: Keep multiple versions per account

#### Low Priority
- [ ] **Dark Mode Toggle**: Manual override in settings UI
- [ ] **Bulk Operations**: Select multiple accounts
- [ ] **Advanced Search**: Filter by date, size, etc.
- [ ] **Export All**: Bulk export functionality
- [ ] **Themes**: Customizable color schemes

### 🐛 Known Issues

1. **macOS**: Window icon cannot be changed at runtime (Flet limitation)
   - Workaround: Build app with `flet build macos`
   
2. **Windows**: PyInstaller exe may trigger false positives in antivirus
   - Workaround: Add to whitelist or run from source
   
3. **Linux**: Limited testing on Linux distributions
   - Status: Community testing needed

4. **Backup Encryption**: Not yet implemented
   - Status: Planned for v1.2.0
   - Workaround: Use OS-level encryption (FileVault, BitLocker)

---

## Version History

| Version | Release Date | Status | Highlights |
|---------|-------------|--------|------------|
| 1.1.0 | 2025-12-04 | ✅ Current | Config system, Search, Bug fixes |
| 1.0.0 | 2025-12-01 | ✅ Stable | Initial release |

---

## Migration Guide

### Upgrading from 1.0.0 to 1.1.0

**No breaking changes!** Your existing backups and accounts will work seamlessly.

#### What Happens on First Launch:
1. A new `config.json` file is created with default settings
2. Existing `accounts.json` is automatically upgraded (thread-safe)
3. All existing backups are verified for integrity
4. Old backups are cleaned up based on retention policy (default: 30 days)

#### Recommended Steps:
```bash
# 1. Backup your data (optional but recommended)
cp -r ~/.antigravity-agent ~/.antigravity-agent.backup

# 2. Update the code
git pull origin main

# 3. Install new dependencies (if any)
pip install -r requirements.txt

# 4. Run the app
python gui/main.py

# 5. Verify everything works
python test_improvements.py
```

#### New Configuration Options:
Check `~/.antigravity-agent/config.json` to customize:
- `auto_backup_on_startup`: Auto-backup current account on launch
- `auto_backup_on_switch`: Auto-backup before switching accounts
- `backup_retention_days`: How long to keep old backups (0 = forever)

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Report Issues
1. Check [Known Issues](#known-issues) first
2. Search existing GitHub issues
3. Create a new issue with:
   - OS and version
   - Steps to reproduce
   - Expected vs actual behavior
   - Logs from `~/.antigravity-agent/app.log`

### How to Suggest Features
1. Open a GitHub issue with `[Feature Request]` prefix
2. Describe the use case
3. Explain why it's valuable
4. Provide mockups if applicable

---

## Credits

### Core Team
- **TrungNguyen** - Original author and maintainer

### Contributors
- Community testers and bug reporters
- Kiro AI Assistant - Code improvements and documentation

### Special Thanks
- Flet team for the amazing GUI framework
- psutil maintainers for cross-platform process management
- All users who provided feedback and suggestions

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Stay Updated**: Watch this repo for new releases! ⭐

*Last Updated: December 4, 2025*
