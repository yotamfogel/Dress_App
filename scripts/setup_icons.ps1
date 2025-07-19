Write-Host "🎨 Flutter App Icon Setup" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

Write-Host ""
Write-Host "📁 Step 1: Ensure your logos are in the correct locations:" -ForegroundColor Yellow
Write-Host "   Light logo: assets/images/Logo/Light/logo1024x1024.png" -ForegroundColor Yellow
Write-Host "   Dark logo: assets/images/Logo/Dark/logo_dark1024x1024.png" -ForegroundColor Yellow
Write-Host "   (If you haven't done this yet, please do it now)" -ForegroundColor Yellow
Write-Host ""

Write-Host "📦 Step 2: Installing dependencies..." -ForegroundColor Green
flutter pub get

Write-Host ""
Write-Host "🔧 Step 3: Installing Pillow for image processing..." -ForegroundColor Green
pip install Pillow

Write-Host ""
Write-Host "🎯 Step 4: Running icon generation script..." -ForegroundColor Green
python scripts/setup_app_icons.py

Write-Host ""
Write-Host "🚀 Step 5: Generating Flutter launcher icons..." -ForegroundColor Green
flutter pub run flutter_launcher_icons:main

Write-Host ""
Write-Host "🧹 Step 6: Cleaning and rebuilding..." -ForegroundColor Green
flutter clean
flutter pub get

Write-Host ""
Write-Host "✅ Icon setup complete!" -ForegroundColor Green
Write-Host "📱 You can now run: flutter run" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue" 