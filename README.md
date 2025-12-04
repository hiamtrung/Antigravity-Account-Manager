# 🚀 Antigravity Account Manager

> **Quản lý và chuyển đổi nhiều tài khoản Antigravity dễ dàng chỉ với một cú click!**

Công cụ giúp bạn lưu trữ và chuyển đổi giữa nhiều tài khoản Antigravity mà không cần đăng xuất/đăng nhập lại. Hoàn hảo cho developers làm việc với nhiều tài khoản khác nhau (công ty, cá nhân, client...).

---

## ✨ Tính Năng Chính

- 🔄 **Chuyển tài khoản 1-click** - Không cần đăng xuất/đăng nhập
- 💾 **Backup tự động** - Lưu trữ an toàn thông tin đăng nhập
- 🔍 **Tìm kiếm nhanh** - Tìm tài khoản theo tên hoặc email
- 📤 **Export/Import** - Chia sẻ hoặc backup tài khoản ra file
- 🧹 **Tự động dọn dẹp** - Xóa backup cũ theo lịch trình
- 🎨 **Giao diện đẹp** - Dark/Light mode tự động theo hệ thống
- 🖥️ **Đa nền tảng** - Hỗ trợ macOS và Windows

---

## 📦 Cài Đặt

### Cách 1: Chạy từ Source (Khuyên dùng)

```bash
# 1. Clone repository
git clone https://github.com/hiamtrung/Antigravity-Account-Manager.git
cd Antigravity-Account-Manager

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Chạy ứng dụng
python gui/main.py
```

### Cách 2: Download File Thực Thi

- **macOS**: Download `Antigravity Manager.dmg` từ [Releases](https://github.com/hiamtrung/Antigravity-Account-Manager/releases)
- **Windows**: Download `Antigravity Manager.exe` từ [Releases](https://github.com/hiamtrung/Antigravity-Account-Manager/releases)

---

## 🎯 Hướng Dẫn Sử Dụng

### Bước 1: Tạo Backup Đầu Tiên

1. Mở Antigravity Manager
2. Click nút **"Backup current"**
3. App sẽ tự động phát hiện email của bạn
4. Backup đầu tiên đã được tạo! 🎉

### Bước 2: Thêm Tài Khoản Khác

1. Đăng xuất khỏi Antigravity
2. Đăng nhập bằng tài khoản khác
3. Quay lại Antigravity Manager
4. Click **"Backup current"** lần nữa
5. Lặp lại cho tất cả tài khoản của bạn

### Bước 3: Chuyển Đổi Tài Khoản

1. Tìm tài khoản muốn chuyển (dùng thanh tìm kiếm)
2. Click vào menu **⋮** bên phải
3. Chọn **"Switch to this account"**
4. Đợi Antigravity khởi động lại
5. Xong! Bạn đã đăng nhập tài khoản mới 🚀

---

## 🔍 Tính Năng Nổi Bật

### Tìm Kiếm Thông Minh
```
Gõ: "work"     → Hiện tất cả tài khoản công việc
Gõ: "@gmail"   → Hiện tất cả tài khoản Gmail
```

### Export/Import Tài Khoản
- **Export**: Click chuột phải → Export backup → Lưu file `.json`
- **Import**: Settings → Import → Chọn file `.json`
- Dùng để backup hoặc chia sẻ tài khoản giữa các máy

### Tự Động Dọn Dẹp
- Tự động xóa backup cũ hơn 30 ngày (có thể tùy chỉnh)
- Xóa file backup không còn dùng
- Xem thống kê: Settings → Backup Management

---

## ⚙️ Cấu Hình

File cấu hình: `~/.antigravity-agent/config.json`

```json
{
  "auto_backup_on_startup": true,        // Tự động backup khi mở app
  "auto_backup_on_switch": true,         // Tự động backup trước khi chuyển
  "backup_retention_days": 30,           // Xóa backup cũ hơn 30 ngày
  "confirm_before_delete": true,         // Xác nhận trước khi xóa
  "theme_mode": "system"                 // "light", "dark", hoặc "system"
}
```

---

## �[️ CLI Mode (Cho Người Dùng Nâng Cao)

```bash
# Xem danh sách tài khoản
python main.py list

# Tạo backup
python main.py add

# Chuyển tài khoản (dùng số thứ tự)
python main.py switch -i 1

# Xóa backup
python main.py delete -i 1

# Khởi động/Dừng Antigravity
python main.py start
python main.py stop
```

---

## ❓ Câu Hỏi Thường Gặp

### "Database is locked" - Làm sao?
**Giải pháp**: Đóng hoàn toàn Antigravity trước khi chuyển tài khoản.

### Backup được lưu ở đâu?
**Vị trí**: `~/.antigravity-agent/backups/`

### Có thể dùng trên nhiều máy không?
**Có**: Export tài khoản ra file `.json` và import trên máy khác.

### Dữ liệu có an toàn không?
**Có**: Tất cả dữ liệu lưu local, không gửi lên internet.

### Làm sao xóa backup cũ?
**Cách 1**: Settings → Backup Management → Clean Old Backups  
**Cách 2**: Tự động xóa theo `backup_retention_days` trong config

---

## 🔐 Bảo Mật

- ✅ Dữ liệu lưu trữ local (không upload lên cloud)
- ✅ Không có kết nối mạng
- ✅ Quyền file theo hệ điều hành
- ⚠️ Backup files **chưa được mã hóa** (sẽ có trong v1.2.0)

**Khuyến nghị**: 
- Không chia sẻ file backup công khai
- Backup định kỳ folder `~/.antigravity-agent`
- Sử dụng mật khẩu mạnh cho tài khoản Antigravity

---

## 📚 Tài Liệu Thêm

- 📖 [Quick Start Guide](QUICK_START.md) - Hướng dẫn chi tiết 5 phút
- ⌨️ [Keyboard Shortcuts](KEYBOARD_SHORTCUTS.md) - Phím tắt
- 🔧 [Technical Details](IMPROVEMENTS.md) - Chi tiết kỹ thuật
- 📝 [Changelog](CHANGELOG.md) - Lịch sử phiên bản

---

## 🐛 Báo Lỗi & Góp Ý

Gặp vấn đề? Có ý tưởng mới?

- 🐛 [Báo lỗi](https://github.com/hiamtrung/Antigravity-Account-Manager/issues)
- 💡 [Đề xuất tính năng](https://github.com/hiamtrung/Antigravity-Account-Manager/issues)
- ⭐ [Star repo](https://github.com/hiamtrung/Antigravity-Account-Manager) nếu thấy hữu ích!

---

## 🚀 Tính Năng Sắp Có (v1.2.0)

- 🔐 Mã hóa backup files
- 🔔 Thông báo desktop
- ⌨️ Phím tắt
- 🏷️ Gắn tag cho tài khoản
- ☁️ Đồng bộ cloud (tùy chọn)

---

## 📊 Thống Kê

![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey)
![Python](https://img.shields.io/badge/python-3.10%2B-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🙏 Credits

- **Tác giả**: [TrungNguyen](https://github.com/hiamtrung)
- **Framework**: [Flet](https://flet.dev) - Cross-platform GUI
- **Inspired by**: Cursor Account Manager

---

## 📄 License

MIT License - Xem [LICENSE](LICENSE) để biết thêm chi tiết.

---

## 💖 Ủng Hộ Dự Án

Nếu project này hữu ích với bạn:

- ⭐ Star repo trên GitHub
- 🐛 Báo lỗi và góp ý
- 📢 Chia sẻ với bạn bè
- ☕ [Mua tôi một ly cà phê] (ko-fi.com/hiamtrungnguyen) (tùy chọn)

---

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
- **TrungNguyen** - Original author and maintainer
- **Community** - Bug reports and feature suggestions
- **You?** - [Become a contributor!](#-contributing)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025

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
- 🐛 [Report Issues](https://github.com/hiamtrung/antigravity-account-manager/issues)
- 💬 [Discussions](https://github.com/yourusername/antigravity-account-manager/discussions)
- 📧 Email: trungnguyen.ui@gmail.com

### Stay Updated
- ⭐ Star this repo
- 👀 Watch for releases

---

<div align="center"></div>

If you find this project useful, please consider giving it a ⭐!

[⬆ Back to Top](#-antigravity-manager)

</div>
