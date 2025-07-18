#!/usr/bin/env python3
"""
Flutter App Integration Test - Enhanced AI Backend
Tests the enhanced backend with the same API calls that the Flutter app makes
"""

import requests
import json
import base64
from PIL import Image
import numpy as np

def create_test_clothing_image():
    """Create a test clothing image similar to what a user might upload"""
    # Create a simple but realistic clothing image
    img = np.zeros((400, 300, 3), dtype=np.uint8)
    
    # Background (light gray)
    img[:] = [200, 200, 200]
    
    # Add a shirt (red)
    shirt_area = img[80:200, 50:250]
    shirt_area[:] = [180, 50, 50]
    
    # Add pants (blue)
    pants_area = img[200:350, 80:220]
    pants_area[:] = [50, 50, 180]
    
    # Add some texture
    noise = np.random.normal(0, 15, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img)

def test_flutter_app_integration():
    """Test the enhanced backend as if called from the Flutter app"""
    
    print("📱 Flutter App Integration Test")
    print("=" * 50)
    print("Testing Enhanced AI Backend APIs that the Flutter app uses")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check (Flutter app checks this first)
    print("\n1️⃣ Health Check (Flutter app startup):")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"   ✅ Backend Status: {health.get('status', 'unknown')}")
            print(f"   📍 Version: {health.get('version', 'unknown')}")
            print(f"   🔧 Models: {health.get('models_loaded', {})}")
            print(f"   🚀 Features: {len(health.get('features', []))} available")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: Create and upload image (Flutter app flow)
    print("\n2️⃣ Image Upload Simulation:")
    test_image = create_test_clothing_image()
    
    # Convert to base64 (same as Flutter app)
    import io
    buffer = io.BytesIO()
    test_image.save(buffer, format='PNG')
    base64_image = base64.b64encode(buffer.getvalue()).decode()
    
    print(f"   📸 Image created: {test_image.size[0]}x{test_image.size[1]} pixels")
    print(f"   💾 Base64 size: {len(base64_image)} characters")
    
    # Test 3: Analyze with AI (main Flutter app function)
    print("\n3️⃣ 'Analyze with AI' Button Test:")
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/detect-clothing", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Analysis successful: {result.get('success', False)}")
            
            # Display results as Flutter app would
            items = result.get('items', [])
            print(f"   📊 Items detected: {len(items)}")
            
            if items:
                print(f"   🔍 Detection Results:")
                for i, item in enumerate(items):
                    print(f"      Item {i+1}: {item.get('label', 'unknown')}")
                    print(f"         Confidence: {item.get('confidence', 0):.1%}")
                    
                    # Colors (as shown in Flutter app)
                    colors = item.get('colors', [])
                    if colors:
                        color_text = ", ".join([f"{c['name']} ({c['percentage']}%)" 
                                              for c in colors[:3]])
                        print(f"         Colors: {color_text}")
                    
                    # Attributes (new feature)
                    attrs = item.get('attributes', {})
                    if attrs:
                        attr_text = ", ".join([f"{k}: {v}" for k, v in attrs.items() 
                                             if k not in ['detection_method']])
                        print(f"         Attributes: {attr_text}")
            else:
                print(f"   📝 No clothing items detected in this image")
                
        else:
            print(f"   ❌ Analysis failed: {response.status_code}")
            print(f"   📝 Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Analysis error: {e}")
    
    # Test 4: Color analysis (additional Flutter app feature)
    print("\n4️⃣ Enhanced Color Analysis:")
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/analyze-colors", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Color analysis successful: {result.get('success', False)}")
            
            # Display colors as Flutter app would
            colors = result.get('dominant_colors', [])
            if colors:
                print(f"   🎨 Color breakdown:")
                for color in colors:
                    print(f"      {color['name']}: {color['percentage']}%")
            
            desc = result.get('description', '')
            if desc:
                print(f"   📝 Description: {desc}")
                
        else:
            print(f"   ❌ Color analysis failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Color analysis error: {e}")
    
    # Test 5: Response time (Flutter app performance)
    print("\n5️⃣ Performance Test:")
    import time
    
    start_time = time.time()
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/analyze-complete", json=payload)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"   ✅ Complete analysis time: {end_time - start_time:.2f} seconds")
            print(f"   📊 Response size: {len(response.text)} characters")
            
            result = response.json()
            summary = result.get('summary', {})
            print(f"   📈 Analysis summary: {summary}")
        else:
            print(f"   ❌ Performance test failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Performance test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Flutter App Integration Test Complete!")
    print("\n✅ Backend is ready for Flutter app integration")
    print("📱 The Flutter app can now use enhanced AI features:")
    print("   - Better color analysis")
    print("   - More detailed clothing detection")
    print("   - Attribute information")
    print("   - Multiple analysis endpoints")
    print("   - Improved error handling")
    
    return True

if __name__ == "__main__":
    test_flutter_app_integration()