#!/usr/bin/env python3
"""
🧪 Quick AI Backend Test with Sample Image
"""

import requests
import json
import base64
from PIL import Image, ImageDraw
import io

def create_test_image():
    """Create a simple test image with colors"""
    # Create a 200x200 image with different colored sections
    img = Image.new('RGB', (200, 200), 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw colored rectangles
    draw.rectangle([0, 0, 100, 100], fill='red')
    draw.rectangle([100, 0, 200, 100], fill='blue')
    draw.rectangle([0, 100, 100, 200], fill='green')
    draw.rectangle([100, 100, 200, 200], fill='yellow')
    
    return img

def image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str

def test_ai_backend():
    """Test the AI backend with sample image"""
    print("🧪 Testing AI Backend with Sample Image")
    print("=" * 50)
    
    # Create test image
    test_image = create_test_image()
    base64_image = image_to_base64(test_image)
    
    print("🎨 Created test image with red, blue, green, yellow sections")
    print()
    
    # Test color analysis
    print("🔍 Testing Color Analysis...")
    try:
        response = requests.post(
            'http://10.64.139.146:5000/analyze-colors',
            json={'image': base64_image},
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Color Analysis Success!")
            print(f"   Found {len(result['dominant_colors'])} colors:")
            for color in result['dominant_colors']:
                print(f"   - {color['name']}: {color['percentage']}%")
            print(f"   Description: {result['description']}")
        else:
            print(f"❌ Color Analysis Failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Color Analysis Error: {e}")
    
    print()
    
    # Test clothing detection
    print("🔍 Testing Clothing Detection...")
    try:
        response = requests.post(
            'http://10.64.139.146:5000/detect-clothing',
            json={'image': base64_image},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Clothing Detection Success!")
            print(f"   Found {result['total_items']} items:")
            for item in result['items']:
                print(f"   - {item['label']}: {item['confidence']*100:.1f}%")
        else:
            print(f"❌ Clothing Detection Failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Clothing Detection Error: {e}")
    
    print()
    print("🎯 Test completed! Backend is ready for your Flutter app.")

if __name__ == '__main__':
    test_ai_backend()