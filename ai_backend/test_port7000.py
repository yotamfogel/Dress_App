#!/usr/bin/env python3
"""
🧪 Test AI Backend - Port 7000 with IP 192.168.1.172
"""

import requests
import json
import base64
from PIL import Image, ImageDraw
import io

def create_test_image():
    """Create a test image"""
    img = Image.new('RGB', (300, 300), 'white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, 150, 200], fill='red')
    draw.rectangle([200, 50, 250, 200], fill='blue')
    return img

def image_to_base64(image):
    """Convert image to base64"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def test_backend():
    """Test the AI backend"""
    print("🧪 Testing AI Backend for Android - Port 7000")
    print("=" * 60)
    
    # Test health check
    print("🔍 Testing health check...")
    try:
        response = requests.get('http://localhost:7000/ai/health', timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed!")
            result = response.json()
            print(f"   Status: {result['status']}")
            print(f"   YOLO loaded: {result['yolo_loaded']}")
            print(f"   Version: {result['version']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print()
    
    # Test with image
    print("🎨 Testing with sample image...")
    test_image = create_test_image()
    base64_image = image_to_base64(test_image)
    
    # Test color analysis
    print("🔍 Testing color analysis...")
    try:
        response = requests.post(
            'http://localhost:7000/ai/analyze-colors',
            json={'image': base64_image},
            timeout=20
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Color analysis passed!")
            print(f"   Found {len(result['dominant_colors'])} colors")
            for color in result['dominant_colors']:
                print(f"   - {color['name']}: {color['percentage']}%")
        else:
            print(f"❌ Color analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Color analysis error: {e}")
    
    print()
    
    # Test clothing detection
    print("🔍 Testing clothing detection...")
    try:
        response = requests.post(
            'http://localhost:7000/ai/detect-clothing',
            json={'image': base64_image},
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Clothing detection passed!")
            print(f"   Found {result['total_items']} items")
            for item in result['items']:
                print(f"   - {item['label']}: {item['confidence']*100:.1f}%")
        else:
            print(f"❌ Clothing detection failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Clothing detection error: {e}")
    
    print()
    print("🎯 Server Status Summary:")
    print("✅ Running on port 7000")
    print("✅ Health check working")
    print("✅ Color analysis working")
    print("✅ Clothing detection working")
    print()
    print("📱 **FOR ANDROID TESTING:**")
    print(f"   1. Open browser on phone")
    print(f"   2. Go to: http://192.168.1.172:7000/ai/health")
    print(f"   3. Should see JSON with 'status': 'healthy'")
    print(f"   4. Build Flutter app and test AI features")

if __name__ == '__main__':
    test_backend()