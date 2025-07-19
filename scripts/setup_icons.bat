@echo off
echo 🎨 Flutter App Icon Setup
echo ========================

echo.
echo 📁 Step 1: Ensure your logos are in the correct locations:
echo    Light logo: assets/images/Logo/Light/logo1024x1024.png
echo    Dark logo: assets/images/Logo/Dark/logo_dark1024x1024.png
echo    (If you haven't done this yet, please do it now)
echo.

echo 📦 Step 2: Installing dependencies...
flutter pub get

echo.
echo 🔧 Step 3: Installing Pillow for image processing...
pip install Pillow

echo.
echo 🎯 Step 4: Running icon generation script...
python scripts/setup_app_icons.py

echo.
echo 🚀 Step 5: Generating Flutter launcher icons...
flutter pub run flutter_launcher_icons:main

echo.
echo 🧹 Step 6: Cleaning and rebuilding...
flutter clean
flutter pub get

echo.
echo ✅ Icon setup complete!
echo 📱 You can now run: flutter run
echo.
pause 