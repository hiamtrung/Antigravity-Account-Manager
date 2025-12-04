# 🎨 Icon Files

## Note about .icns files

The `.icns` files (macOS icon format) are excluded from the repository due to their large size (1.6MB each).

### Locations:
- `assets/icon.icns` - Main application icon
- `gui/assets/icon.icns` - GUI application icon

### How to get them:

#### Option 1: Generate from PNG
```bash
# Install iconutil (comes with Xcode on macOS)
# Convert PNG to ICNS
mkdir icon.iconset
sips -z 16 16     assets/icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     assets/icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     assets/icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     assets/icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   assets/icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   assets/icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   assets/icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   assets/icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   assets/icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 assets/icon.png --out icon.iconset/icon_512x512@2x.png

iconutil -c icns icon.iconset -o assets/icon.icns
cp assets/icon.icns gui/assets/icon.icns
rm -rf icon.iconset
```

#### Option 2: Use PNG directly
The application will work fine with just the PNG icons. The .icns files are only needed for:
- macOS .app bundle icon
- Better icon quality on macOS

#### Option 3: Download from releases
If available, download the complete package from GitHub releases which includes all icon files.

### File Sizes:
- `icon.png`: ~50KB (included in repo)
- `icon.ico`: ~100KB (included in repo)
- `icon.icns`: ~1.6MB (excluded from repo)

### Why excluded?
- Large file size (3.2MB total for both files)
- Can be regenerated from PNG
- Not required for basic functionality
- Reduces repository size

---

**Note**: If you're building the macOS .app, you'll need to generate the .icns files first using Option 1 above.
