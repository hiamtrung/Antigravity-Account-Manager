# ⌨️ Keyboard Shortcuts Guide

## Antigravity Manager - Quick Reference

### 🏠 Home View (Dashboard)

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Cmd/Ctrl + F` | Focus Search | Jump to search field |
| `Cmd/Ctrl + N` | New Backup | Create backup of current account |
| `Cmd/Ctrl + R` | Refresh | Reload account list |
| `↑` / `↓` | Navigate | Move through account list |
| `Enter` | Switch | Switch to selected account |
| `Delete` | Delete | Delete selected account backup |
| `Esc` | Clear Search | Clear search filter |

### ⚙️ Settings View

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Cmd/Ctrl + O` | Open Data Folder | Open backup directory |
| `Cmd/Ctrl + I` | Import Backup | Import backup file |
| `Cmd/Ctrl + E` | Export Config | Export configuration |
| `Cmd/Ctrl + Shift + C` | Clean Backups | Run cleanup utility |
| `Cmd/Ctrl + Shift + V` | Verify Backups | Verify all backups |

### 🌐 Global Shortcuts

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Cmd/Ctrl + ,` | Settings | Open settings view |
| `Cmd/Ctrl + 1` | Dashboard | Go to dashboard |
| `Cmd/Ctrl + Q` | Quit | Exit application |
| `Cmd/Ctrl + W` | Close Window | Close current window |
| `Cmd/Ctrl + M` | Minimize | Minimize to tray |
| `F5` | Refresh | Refresh current view |

### 🎨 Theme & Display

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Cmd/Ctrl + Shift + D` | Toggle Dark Mode | Switch between light/dark |
| `Cmd/Ctrl + +` | Zoom In | Increase UI scale |
| `Cmd/Ctrl + -` | Zoom Out | Decrease UI scale |
| `Cmd/Ctrl + 0` | Reset Zoom | Reset to default scale |

### 🔍 Search & Filter

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Cmd/Ctrl + F` | Search | Focus search field |
| `Esc` | Clear | Clear search query |
| `Enter` | Apply | Apply filter |
| `Cmd/Ctrl + Shift + F` | Advanced Search | Open advanced search |

### 📋 Context Menu Actions

**Right-click on account card:**
- `S` - Switch to account
- `E` - Export backup
- `D` - Delete backup
- `R` - Rename account
- `I` - View info

### 🚀 Power User Tips

1. **Quick Switch**: Type account name in search, press Enter
2. **Batch Operations**: Hold Shift to select multiple accounts
3. **Quick Backup**: Double-click status bar to backup current
4. **Emergency Stop**: `Cmd/Ctrl + Shift + Q` to force quit Antigravity

### 🎯 Planned Shortcuts (Coming Soon)

| Shortcut | Action | Status |
|----------|--------|--------|
| `Cmd/Ctrl + B` | Backup Current | 🚧 Planned |
| `Cmd/Ctrl + Shift + S` | Switch Last | 🚧 Planned |
| `Cmd/Ctrl + D` | Duplicate Account | 🚧 Planned |
| `Cmd/Ctrl + G` | Group Accounts | 🚧 Planned |

---

## 📝 Notes

- **macOS**: Use `Cmd` key
- **Windows/Linux**: Use `Ctrl` key
- Shortcuts can be customized in Settings > Keyboard
- Some shortcuts may conflict with system shortcuts

## 🔧 Customization

To customize shortcuts, edit `~/.antigravity-agent/config.json`:

```json
{
  "keyboard_shortcuts": {
    "search": "Cmd+F",
    "new_backup": "Cmd+N",
    "settings": "Cmd+,"
  }
}
```

---

**Version**: 1.1.0  
**Last Updated**: December 4, 2025
