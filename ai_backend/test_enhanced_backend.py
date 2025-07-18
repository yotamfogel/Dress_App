#!/usr/bin/env python3
"""
Test script for Enhanced AI Backend
"""

import requests
import json
import base64
import os
from PIL import Image
import numpy as np

def create_test_image():
    """Create a simple test image with colored squares"""
    # Create a 400x400 image with colored squares
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    
    # Red square (top-left)
    img[50:150, 50:150] = [255, 0, 0]
    
    # Blue square (top-right)
    img[50:150, 250:350] = [0, 0, 255]
    
    # Green square (bottom-left)
    img[250:350, 50:150] = [0, 255, 0]
    
    # Yellow square (bottom-right)
    img[250:350, 250:350] = [255, 255, 0]
    
    return Image.fromarray(img)

def image_to_base64(image):
    """Convert PIL image to base64"""
    import io
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def test_enhanced_backend():
    """Test the enhanced AI backend"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Enhanced AI Backend")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed")
            print(f"   Version: {health_data.get('version', 'unknown')}")
            print(f"   Models loaded: {health_data.get('models_loaded', {})}")
            print(f"   Features: {health_data.get('features', [])}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Create and encode test image
    print("\n2️⃣ Creating test image...")
    test_image = create_test_image()
    base64_image = image_to_base64(test_image)
    print(f"✅ Test image created (base64 length: {len(base64_image)})")
    
    # Test 3: Test enhanced clothing detection
    print("\n3️⃣ Testing Enhanced Clothing Detection...")
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/detect-clothing", json=payload)
        
        if response.status_code == 200:
            detection_data = response.json()
            print(f"✅ Enhanced detection successful")
            print(f"   Success: {detection_data.get('success', False)}")
            print(f"   Total items: {detection_data.get('total_items', 0)}")
            print(f"   Detection method: {detection_data.get('detection_method', 'unknown')}")
            
            # Print details of detected items
            items = detection_data.get('items', [])
            for i, item in enumerate(items):
                print(f"   Item {i+1}: {item.get('label', 'unknown')} "
                      f"(confidence: {item.get('confidence', 0):.2f})")
                colors = item.get('colors', [])
                if colors:
                    print(f"     Colors: {[c['name'] for c in colors]}")
                attributes = item.get('attributes', {})
                if attributes:
                    print(f"     Attributes: {attributes}")
        else:
            print(f"❌ Enhanced detection failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Enhanced detection error: {e}")
    
    # Test 4: Test color analysis
    print("\n4️⃣ Testing Enhanced Color Analysis...")
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/analyze-colors", json=payload)
        
        if response.status_code == 200:
            color_data = response.json()
            print(f"✅ Enhanced color analysis successful")
            print(f"   Success: {color_data.get('success', False)}")
            print(f"   Analysis method: {color_data.get('analysis_method', 'unknown')}")
            
            # Print color details
            colors = color_data.get('dominant_colors', [])
            print(f"   Dominant colors ({len(colors)}):")
            for color in colors:
                print(f"     - {color['name']}: {color['percentage']}% "
                      f"(RGB: {color['rgb']})")
            
            description = color_data.get('description', '')
            if description:
                print(f"   Description: {description}")
        else:
            print(f"❌ Enhanced color analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Enhanced color analysis error: {e}")
    
    # Test 5: Test attribute detection (new endpoint)
    print("\n5️⃣ Testing Attribute Detection...")
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/detect-attributes", json=payload)
        
        if response.status_code == 200:
            attr_data = response.json()
            print(f"✅ Attribute detection successful")
            print(f"   Success: {attr_data.get('success', False)}")
            print(f"   Total items: {attr_data.get('total_items', 0)}")
            print(f"   Method: {attr_data.get('method', 'unknown')}")
            
            # Print attribute details
            items = attr_data.get('items', [])
            for i, item in enumerate(items):
                print(f"   Item {i+1}: {item.get('label', 'unknown')}")
                attributes = item.get('attributes', {})
                for key, value in attributes.items():
                    print(f"     {key}: {value}")
        else:
            print(f"❌ Attribute detection failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Attribute detection error: {e}")
    
    # Test 6: Test complete analysis (new endpoint)
    print("\n6️⃣ Testing Complete Analysis...")
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/analyze-complete", json=payload)
        
        if response.status_code == 200:
            complete_data = response.json()
            print(f"✅ Complete analysis successful")
            print(f"   Success: {complete_data.get('success', False)}")
            print(f"   Method: {complete_data.get('method', 'unknown')}")
            
            # Print summary
            summary = complete_data.get('summary', {})
            print(f"   Summary:")
            for key, value in summary.items():
                print(f"     {key}: {value}")
        else:
            print(f"❌ Complete analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Complete analysis error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Enhanced AI Backend testing completed!")
    
    return True

if __name__ == "__main__":
    test_enhanced_backend()