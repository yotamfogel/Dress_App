# 🎨 App Icon Setup Guide

This guide will help you automatically resize your 1024x1024 logos to all required sizes for your Flutter app.

## 📁 Logo Requirements

Your logos should be placed in these locations:
- **Light Mode Logo:** `assets/images/Logo/Light/logo1024x1024.png`
- **Dark Mode Logo:** `assets/images/Logo/Dark/logo_dark1024x1024.png`

## 🚀 Quick Setup (Recommended)

### Option 1: Windows Batch Script
```bash
scripts\setup_icons.bat
```

### Option 2: PowerShell Script
```powershell
.\scripts\setup_icons.ps1
```

### Option 3: Python Script
```bash
python scripts\setup_app_icons.py
```

## 📋 What Gets Generated

The script will automatically create icons for:

### 📱 Android
- `mipmap-mdpi/ic_launcher.png` (48x48)
- `mipmap-hdpi/ic_launcher.png` (72x72)
- `mipmap-xhdpi/ic_launcher.png` (96x96)
- `mipmap-xxhdpi/ic_launcher.png` (144x144)
- `mipmap-xxxhdpi/ic_launcher.png` (192x192)

### 🍎 iOS
- All required sizes from 20x20 to 1024x1024
- App Store icon (1024x1024)
- iPhone and iPad icons

### 🌐 Web
- `Icon-192.png` (192x192)
- `Icon-512.png` (512x512)
- `Icon-maskable-192.png` (192x192)
- `Icon-maskable-512.png` (512x512)
- `favicon.png` (32x32)

### 🖥️ Desktop
- Windows icons
- macOS icons
- Linux icons

## 🎯 Features

- ✅ **Automatic Resizing:** Converts 1024x1024 to all required sizes
- ✅ **Light/Dark Mode Support:** Uses appropriate logos for each mode
- ✅ **Splash Screen Integration:** Configures native splash screens
- ✅ **Cross-Platform:** Works on Android, iOS, Web, Windows, macOS, Linux
- ✅ **High Quality:** Uses LANCZOS resampling for best quality

## 🔧 Manual Steps (if needed)

1. **Install Dependencies:**
   ```bash
   flutter pub get
   pip install Pillow
   ```

2. **Generate Icons:**
   ```bash
   python scripts/setup_app_icons.py
   ```

3. **Generate Flutter Launcher Icons:**
   ```bash
   flutter pub run flutter_launcher_icons:main
   ```

4. **Generate Splash Screens:**
   ```bash
   flutter pub run flutter_native_splash:create
   ```

5. **Clean and Rebuild:**
   ```bash
   flutter clean
   flutter pub get
   flutter run
   ```

## 🎨 Configuration Details

### Flutter Launcher Icons
- **Source:** `assets/images/Logo/Light/logo1024x1024.png`
- **Background:** `#1a1a1a` (dark theme)
- **Platforms:** Android, iOS, Web, Windows, macOS, Linux

### Native Splash Screen
- **Light Mode:** `assets/images/Logo/Light/logo1024x1024.png`
- **Dark Mode:** `assets/images/Logo/Dark/logo_dark1024x1024.png`
- **Background:** `#1a1a1a` (light) / `#000000` (dark)

## 🐛 Troubleshooting

### Logo Not Found
- Ensure your logos are in the correct paths
- Check file names match exactly (case-sensitive)
- Verify images are PNG format

### Size Warnings
- Recommended size is 1024x1024 pixels
- Script will work with other sizes but may not look optimal

### Permission Errors
- Run scripts as administrator if needed
- Ensure write permissions to project directories

## 📱 Testing

After setup, test your app on different platforms:
- **Android:** Check launcher icon and splash screen
- **iOS:** Verify app icon and splash screen
- **Web:** Test favicon and PWA icons
- **Desktop:** Confirm window icons

## 🔄 Updating Icons

To update icons later:
1. Replace the logo files in the same locations
2. Run the setup script again
3. Clean and rebuild the project

---

**Note:** The script uses your light mode logo for most icons and your dark mode logo for dark mode splash screens. This provides the best user experience across different themes. 