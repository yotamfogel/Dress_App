#!/usr/bin/env python3
"""
App Icon Setup Script for Flutter
Automatically resizes your 1024x1024 logo to all required sizes
"""

import os
import sys
from PIL import Image
import shutil

def create_icon_sizes():
    """Create all required icon sizes from a 1024x1024 source image"""
    
    # Source image paths
    light_source = "assets/images/Logo/Light/logo1024x1024.png"
    dark_source = "assets/images/Logo/Dark/logo_dark1024x1024.png"
    
    # Check if source images exist
    if not os.path.exists(light_source):
        print(f"❌ Light logo not found: {light_source}")
        print("📁 Please place your 1024x1024 light logo at: assets/images/Logo/Light/logo1024x1024.png")
        return False
    
    if not os.path.exists(dark_source):
        print(f"⚠️  Dark logo not found: {dark_source}")
        print("📁 Dark mode icons will use light logo")
        dark_source = light_source
    
    print(f"✅ Found light logo: {light_source}")
    print(f"✅ Found dark logo: {dark_source}")
    
    # Open the source images
    try:
        with Image.open(light_source) as light_img, Image.open(dark_source) as dark_img:
            # Check if images are 1024x1024
            if light_img.size != (1024, 1024):
                print(f"⚠️  Warning: Light image is {light_img.size}, recommended size is 1024x1024")
            if dark_img.size != (1024, 1024):
                print(f"⚠️  Warning: Dark image is {dark_img.size}, recommended size is 1024x1024")
            
            print("🔄 Generating all icon sizes...")
            
            # Android icon sizes
            android_sizes = {
                "mdpi": 48,
                "hdpi": 72,
                "xhdpi": 96,
                "xxhdpi": 144,
                "xxxhdpi": 192
            }
            
            # Create Android icons (using light mode)
            for density, size in android_sizes.items():
                resized = light_img.resize((size, size), Image.Resampling.LANCZOS)
                output_path = f"android/app/src/main/res/mipmap-{density}/ic_launcher.png"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                resized.save(output_path, "PNG")
                print(f"✅ Android {density}: {size}x{size}")
            
            # iOS icon sizes (key ones)
            ios_sizes = {
                "Icon-App-20x20@1x.png": 20,
                "Icon-App-20x20@2x.png": 40,
                "Icon-App-20x20@3x.png": 60,
                "Icon-App-29x29@1x.png": 29,
                "Icon-App-29x29@2x.png": 58,
                "Icon-App-29x29@3x.png": 87,
                "Icon-App-40x40@1x.png": 40,
                "Icon-App-40x40@2x.png": 80,
                "Icon-App-40x40@3x.png": 120,
                "Icon-App-60x60@2x.png": 120,
                "Icon-App-60x60@3x.png": 180,
                "Icon-App-76x76@1x.png": 76,
                "Icon-App-76x76@2x.png": 152,
                "Icon-App-83.5x83.5@2x.png": 167,
                "Icon-App-1024x1024@1x.png": 1024
            }
            
            # Create iOS icons (using light mode)
            ios_dir = "ios/Runner/Assets.xcassets/AppIcon.appiconset"
            for filename, size in ios_sizes.items():
                resized = light_img.resize((size, size), Image.Resampling.LANCZOS)
                output_path = os.path.join(ios_dir, filename)
                resized.save(output_path, "PNG")
                print(f"✅ iOS {filename}: {size}x{size}")
            
            # Web icons
            web_sizes = {
                "Icon-192.png": 192,
                "Icon-512.png": 512,
                "Icon-maskable-192.png": 192,
                "Icon-maskable-512.png": 512
            }
            
            # Create web icons (using light mode)
            web_dir = "web/icons"
            for filename, size in web_sizes.items():
                resized = light_img.resize((size, size), Image.Resampling.LANCZOS)
                output_path = os.path.join(web_dir, filename)
                resized.save(output_path, "PNG")
                print(f"✅ Web {filename}: {size}x{size}")
            
            # Create favicon (using light mode)
            favicon = light_img.resize((32, 32), Image.Resampling.LANCZOS)
            favicon.save("web/favicon.png", "PNG")
            print("✅ Web favicon: 32x32")
            
            print("\n🎉 All icons generated successfully!")
            print("📱 Next steps:")
            print("1. Run: flutter pub get")
            print("2. Run: flutter pub run flutter_launcher_icons:main")
            print("3. Clean and rebuild: flutter clean && flutter run")
            
            return True
            
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return False

def main():
    """Main function"""
    print("🎨 Flutter App Icon Generator")
    print("=" * 40)
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("❌ PIL (Pillow) not found. Installing...")
        os.system("pip install Pillow")
        try:
            from PIL import Image
        except ImportError:
            print("❌ Failed to install PIL. Please run: pip install Pillow")
            return
    
    # Create icons
    success = create_icon_sizes()
    
    if success:
        print("\n🚀 Ready to generate Flutter launcher icons!")
    else:
        print("\n❌ Icon generation failed. Please check the errors above.")

if __name__ == "__main__":
    main() 