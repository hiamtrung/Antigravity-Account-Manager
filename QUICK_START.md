# 🚀 Quick Start Guide

## Antigravity Manager - Get Started in 5 Minutes

### 📦 Installation

#### Option 1: Run from Source (Recommended for Development)
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/antigravity-manager.git
cd antigravity-manager

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python gui/main.py
```

#### Option 2: Use Pre-built Binary
- **macOS**: Download `Antigravity Manager.dmg`, drag to Applications
- **Windows**: Download `Antigravity Manager.exe`, run directly

---

## 🎯 First Time Setup

### Step 1: Launch the App
```bash
python gui/main.py
```

The app will automatically:
- ✅ Create data directory at `~/.antigravity-agent`
- ✅ Initialize configuration file
- ✅ Detect your current Antigravity account

### Step 2: Create Your First Backup
1. Click **"Backup current"** button in the dashboard
2. The app will automatically detect your email
3. Your first backup is created! 🎉

### Step 3: Add More Accounts
1. Log out from Antigravity
2. Log in with a different account
3. Return to Antigravity Manager
4. Click **"Backup current"** again
5. Repeat for all your accounts

---

## 💡 Common Use Cases

### 🔄 Switching Between Accounts

**Method 1: From Dashboard**
1. Open Antigravity Manager
2. Find the account you want to switch to
3. Click the **⋮** menu button
4. Select **"Switch to this account"**
5. Wait for Antigravity to restart
6. Done! You're now logged in with the new account

**Method 2: Using Search**
1. Type account name or email in search box
2. Press Enter on the account
3. Confirm the switch

**Method 3: CLI (for automation)**
```bash
# List all accounts
python main.py list

# Switch to account #1
python main.py switch -i 1
```

---

### 📤 Exporting Backups (Portable)

**Use Case**: Share account with team member or backup to cloud

1. Right-click on account card
2. Select **"Export backup"**
3. Choose save location
4. Share the `.json` file

**Import on Another Machine:**
1. Open Settings
2. Click **"Import"** button
3. Select the `.json` file
4. Account is now available!

---

### 🧹 Cleaning Old Backups

**Automatic Cleanup** (Recommended):
1. Open Settings
2. Set "Backup Retention Days" to 30 (or your preference)
3. Old backups are automatically deleted

**Manual Cleanup**:
1. Open Settings > Backup Management
2. Click **"Clean Old Backups"**
3. Review what will be deleted
4. Confirm

---

### 🔍 Finding Accounts Quickly

**Search by Name:**
```
Type: "work"
Results: All accounts with "work" in name
```

**Search by Email:**
```
Type: "@gmail.com"
Results: All Gmail accounts
```

**Clear Search:**
- Press `Esc` or clear the search box

---

## 🛠️ Troubleshooting

### ❌ "Database is locked"
**Solution**: Close Antigravity completely before switching accounts
```bash
# Force close Antigravity
python main.py stop
```

### ❌ "Backup file missing"
**Solution**: The backup file was deleted or moved
1. Log in to that account in Antigravity
2. Create a new backup
3. The account will be restored

### ❌ "Cannot find Antigravity"
**Solution**: Antigravity is not installed in the default location
1. Install Antigravity to default location:
   - macOS: `/Applications/Antigravity.app`
   - Windows: `C:\Program Files\Antigravity`
2. Or use URI protocol (automatic fallback)

### ❌ "Import failed"
**Solution**: Backup file is corrupted or invalid
1. Verify the file is a valid JSON
2. Check file size (should be > 0 bytes)
3. Try exporting again from source

---

## 🎓 Pro Tips

### 1. **Auto-Backup on Switch**
Enable in config to never lose your current state:
```json
{
  "auto_backup_on_switch": true
}
```

### 2. **Organize with Names**
Use descriptive names:
- ❌ "Account 1", "Account 2"
- ✅ "Work Gmail", "Personal Outlook", "Client Project"

### 3. **Regular Verification**
Run backup verification monthly:
```bash
python main.py verify
```

### 4. **Backup Your Backups**
Export important accounts to external drive:
1. Right-click account
2. Export to USB drive or cloud folder
3. Keep safe copy

### 5. **Use CLI for Automation**
Create scripts for common tasks:
```bash
#!/bin/bash
# Switch to work account every morning
python main.py switch -i 1
```

---

## 📊 Understanding the Dashboard

### Status Bar Colors:
- 🟢 **Green**: Antigravity is running
- 🔴 **Red**: Antigravity is stopped (click to start)
- 🟡 **Yellow**: Operation in progress

### Account Card Badges:
- **"当前 - Current"**: This is your active account
- **Last Used**: When you last switched to this account

### Statistics:
- **"X Backup"**: Total number of backups
- **"X/Y Backup"**: Filtered results (X shown out of Y total)

---

## 🔐 Security Best Practices

1. **Keep Backups Private**: Don't share backup files publicly
2. **Regular Cleanup**: Delete old/unused backups
3. **Verify Integrity**: Run verification after system updates
4. **Backup the Backups**: Export important accounts to secure location
5. **Use Strong Passwords**: For your Antigravity accounts

---

## 📚 Next Steps

- 📖 Read [IMPROVEMENTS.md](IMPROVEMENTS.md) for advanced features
- ⌨️ Check [KEYBOARD_SHORTCUTS.md](KEYBOARD_SHORTCUTS.md) for shortcuts
- 🐛 Report issues on GitHub
- ⭐ Star the repo if you find it useful!

---

## 🆘 Getting Help

- **Documentation**: Check README.md
- **Issues**: GitHub Issues
- **Community**: Discord/Slack (coming soon)
- **Email**: support@example.com

---

**Happy Account Switching! 🎉**

*Made with ❤️ by the Antigravity Manager Team*
