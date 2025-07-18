#!/usr/bin/env python3
"""
Comprehensive test of the Enhanced AI Backend with realistic images
"""

import requests
import json
import base64
import os
from PIL import Image, ImageDraw
import numpy as np

def create_person_silhouette():
    """Create a simple person silhouette for testing"""
    # Create a 400x600 image
    img = np.zeros((600, 400, 3), dtype=np.uint8)
    
    # Create a person-like silhouette in white
    img[100:500, 150:250] = [255, 255, 255]  # Body
    img[80:150, 170:230] = [255, 255, 255]   # Head
    img[200:300, 120:150] = [255, 255, 255]  # Left arm
    img[200:300, 250:280] = [255, 255, 255]  # Right arm
    img[450:600, 130:180] = [255, 255, 255]  # Left leg
    img[450:600, 220:270] = [255, 255, 255]  # Right leg
    
    # Add some color to make it more interesting
    # Red shirt
    img[150:300, 150:250] = [255, 0, 0]
    # Blue pants
    img[300:450, 150:250] = [0, 0, 255]
    
    return Image.fromarray(img)

def create_clothing_items():
    """Create a simple clothing items image"""
    # Create a 500x500 image
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    
    # Create different clothing items
    # Red shirt (rectangle)
    img[100:200, 100:300] = [255, 0, 0]
    
    # Blue jeans (rectangle)
    img[250:400, 150:250] = [0, 0, 255]
    
    # Green dress (trapezoid-like)
    img[80:300, 350:450] = [0, 255, 0]
    
    # Yellow shoes (small rectangles)
    img[420:460, 100:150] = [255, 255, 0]
    img[420:460, 200:250] = [255, 255, 0]
    
    return Image.fromarray(img)

def image_to_base64(image):
    """Convert PIL image to base64"""
    import io
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def test_clothing_detection_comprehensive():
    """Comprehensive test of clothing detection"""
    base_url = "http://localhost:5000"
    
    print("🧪 Comprehensive Enhanced AI Backend Test")
    print("=" * 60)
    
    # Test images
    test_images = [
        ("Person Silhouette", create_person_silhouette()),
        ("Clothing Items", create_clothing_items())
    ]
    
    for image_name, test_image in test_images:
        print(f"\n🖼️ Testing with: {image_name}")
        print("-" * 40)
        
        base64_image = image_to_base64(test_image)
        
        # Test 1: Enhanced clothing detection
        print("\n1️⃣ Enhanced Clothing Detection:")
        try:
            payload = {"image": base64_image}
            response = requests.post(f"{base_url}/detect-clothing", json=payload)
            
            if response.status_code == 200:
                detection_data = response.json()
                print(f"   ✅ Success: {detection_data.get('success', False)}")
                print(f"   📊 Total items: {detection_data.get('total_items', 0)}")
                print(f"   🔬 Method: {detection_data.get('detection_method', 'unknown')}")
                
                items = detection_data.get('items', [])
                for i, item in enumerate(items):
                    print(f"   📦 Item {i+1}: {item.get('label', 'unknown')}")
                    print(f"      🎯 Confidence: {item.get('confidence', 0):.2f}")
                    print(f"      🎨 Colors: {len(item.get('colors', []))}")
                    print(f"      📐 Segmentation: {item.get('segmentation_available', False)}")
                    
                    # Show top colors
                    colors = item.get('colors', [])
                    if colors:
                        top_colors = colors[:3]
                        color_str = ", ".join([f"{c['name']} ({c['percentage']}%)" for c in top_colors])
                        print(f"      🌈 Top colors: {color_str}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: Color analysis
        print("\n2️⃣ Color Analysis:")
        try:
            payload = {"image": base64_image}
            response = requests.post(f"{base_url}/analyze-colors", json=payload)
            
            if response.status_code == 200:
                color_data = response.json()
                print(f"   ✅ Success: {color_data.get('success', False)}")
                
                colors = color_data.get('dominant_colors', [])
                print(f"   🎨 Dominant colors ({len(colors)}):")
                for color in colors:
                    print(f"      - {color['name']}: {color['percentage']}%")
                
                description = color_data.get('description', '')
                if description:
                    print(f"   📝 Description: {description}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Complete analysis
        print("\n3️⃣ Complete Analysis:")
        try:
            payload = {"image": base64_image}
            response = requests.post(f"{base_url}/analyze-complete", json=payload)
            
            if response.status_code == 200:
                complete_data = response.json()
                print(f"   ✅ Success: {complete_data.get('success', False)}")
                
                summary = complete_data.get('summary', {})
                print(f"   📊 Summary:")
                for key, value in summary.items():
                    print(f"      {key}: {value}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Comprehensive testing completed!")
    print("\n💡 Key Improvements Made:")
    print("   - Enhanced color analysis with K-means clustering")
    print("   - Fashion-specific detection categories")
    print("   - Attribute detection framework (MMFashion placeholder)")
    print("   - Mask R-CNN support (when Detectron2 is available)")
    print("   - Multiple new API endpoints")
    print("   - Comprehensive error handling")
    print("   - Fallback detection methods")

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    print("\n🔗 Testing All API Endpoints")
    print("-" * 40)
    
    endpoints = [
        ("GET", "/health", "Health Check"),
        ("GET", "/test", "Test Endpoint"),
    ]
    
    for method, endpoint, description in endpoints:
        print(f"\n🔍 Testing {description} ({method} {endpoint}):")
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}")
            else:
                response = requests.post(f"{base_url}{endpoint}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {response.status_code}")
                if 'message' in data:
                    print(f"   📝 Message: {data['message']}")
                if 'version' in data:
                    print(f"   🔢 Version: {data['version']}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_clothing_detection_comprehensive()
    test_api_endpoints()