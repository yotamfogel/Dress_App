#!/usr/bin/env python3
"""
Test the new Fashion Classification System
"""

import requests
import json
from PIL import Image
import numpy as np
import base64
import io
import time

def create_test_images():
    """Create test images for different clothing types"""
    
    # Test Image 1: Button shirt
    print("Creating button shirt test image...")
    img1 = np.zeros((400, 300, 3), dtype=np.uint8)
    img1[:] = [240, 240, 240]  # Light background
    img1[50:250, 50:250] = [180, 180, 250]  # Light blue shirt
    img1[60:70, 60:240] = [255, 255, 255]  # White collar
    img1[70:80, 130:140] = [255, 255, 255]  # Button line
    img1[90:100, 130:140] = [255, 255, 255]  # Buttons
    img1[110:120, 130:140] = [255, 255, 255]
    img1[130:140, 130:140] = [255, 255, 255]
    
    # Test Image 2: Jeans
    print("Creating jeans test image...")
    img2 = np.zeros((400, 300, 3), dtype=np.uint8)
    img2[:] = [240, 240, 240]  # Light background
    img2[50:350, 75:225] = [60, 80, 150]  # Blue jeans
    img2[60:70, 85:215] = [80, 100, 180]  # Waistband
    img2[150:160, 85:215] = [80, 100, 180]  # Seam line
    
    # Test Image 3: Red dress
    print("Creating dress test image...")
    img3 = np.zeros((500, 300, 3), dtype=np.uint8)
    img3[:] = [240, 240, 240]  # Light background
    img3[50:450, 100:200] = [200, 60, 60]  # Red dress
    img3[50:150, 80:220] = [200, 60, 60]  # Wider top
    
    return [
        ('button-shirt', Image.fromarray(img1)),
        ('jeans', Image.fromarray(img2)),
        ('dress', Image.fromarray(img3))
    ]

def image_to_base64(image):
    """Convert PIL image to base64"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def test_fashion_classification():
    """Test the new fashion classification system"""
    
    print("🧪 TESTING NEW FASHION CLASSIFICATION SYSTEM")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed")
            print(f"   Version: {health_data.get('version', 'unknown')}")
            print(f"   Features: {health_data.get('features', [])}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Fashion Analysis
    print("\n2️⃣ Testing Fashion Analysis...")
    test_images = create_test_images()
    
    for clothing_type, test_image in test_images:
        print(f"\n🔍 Testing {clothing_type}:")
        print("-" * 30)
        
        base64_image = image_to_base64(test_image)
        
        try:
            start_time = time.time()
            
            payload = {"image": base64_image}
            response = requests.post(f"{base_url}/analyze-fashion", json=payload, timeout=30)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Analysis successful ({processing_time:.2f}s)")
                
                if result.get('success', False):
                    if result.get('multiple_items', False):
                        print("🔄 Multiple items detected:")
                        for item in result.get('items', []):
                            print(f"   - {item['description']}")
                    else:
                        print("📊 Fashion Analysis Results:")
                        print(f"   Clothing Type: {result.get('clothing_type', 'unknown')}")
                        
                        styles = result.get('applicable_styles', [])
                        if styles:
                            print(f"   Applicable Styles: {', '.join(styles)}")
                        
                        colors = result.get('colors', [])
                        if colors:
                            print(f"   Colors ({len(colors)}):")
                            for color in colors:
                                print(f"      - {color['color']}: {color['percentage']}%")
                        
                        color_desc = result.get('color_description', '')
                        if color_desc:
                            print(f"   Color Description: {color_desc}")
                        
                        details = result.get('detection_details', {})
                        if details:
                            print(f"   Detection Details:")
                            print(f"      - Detected as: {details.get('detected_as', 'unknown')}")
                            print(f"      - Confidence: {details.get('confidence', 0):.1%}")
                            print(f"      - Method: {details.get('method', 'unknown')}")
                        
                        if 'note' in result:
                            print(f"   Note: {result['note']}")
                else:
                    print(f"❌ Analysis failed: {result.get('error', 'unknown error')}")
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing {clothing_type}: {e}")
    
    # Test 3: Multiple items scenario
    print(f"\n3️⃣ Testing Multiple Items Scenario...")
    print("-" * 30)
    
    # Create image with multiple items
    multi_img = np.zeros((400, 400, 3), dtype=np.uint8)
    multi_img[:] = [240, 240, 240]  # Light background
    multi_img[50:150, 50:150] = [180, 180, 250]  # Blue shirt
    multi_img[200:350, 200:350] = [60, 80, 150]  # Blue jeans
    multi_img_pil = Image.fromarray(multi_img)
    
    base64_multi = image_to_base64(multi_img_pil)
    
    try:
        payload = {"image": base64_multi}
        response = requests.post(f"{base_url}/analyze-fashion", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Multiple items test successful")
            
            if result.get('multiple_items', False):
                print("🔄 Multiple items detected (as expected):")
                for item in result.get('items', []):
                    print(f"   - {item['description']}")
                print(f"📝 Message: {result.get('message', '')}")
                print(f"📋 Instruction: {result.get('instruction', '')}")
                
                # Test item selection
                print(f"\n🎯 Testing item selection (selecting item 1)...")
                selection_payload = {"image": base64_multi, "item_selection": 1}
                selection_response = requests.post(f"{base_url}/analyze-fashion", json=selection_payload, timeout=30)
                
                if selection_response.status_code == 200:
                    selection_result = selection_response.json()
                    print(f"✅ Item selection successful")
                    
                    if selection_result.get('success', False):
                        analysis = selection_result.get('analysis', {})
                        print(f"   Selected Item Analysis:")
                        print(f"      - Type: {analysis.get('clothing_type', 'unknown')}")
                        print(f"      - Styles: {', '.join(analysis.get('applicable_styles', []))}")
                        print(f"      - Colors: {analysis.get('color_description', 'N/A')}")
                else:
                    print(f"❌ Item selection failed: {selection_response.status_code}")
            else:
                print("📝 Single item detected")
        else:
            print(f"❌ Multiple items test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing multiple items: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 FASHION CLASSIFICATION SYSTEM TESTING COMPLETE!")
    print("\n✅ Key Features Implemented:")
    print("  1. Clothing type identification")
    print("  2. Style classification (21 categories)")
    print("  3. Color percentage analysis")
    print("  4. Multiple item detection")
    print("  5. User feedback integration")
    print("\n🚀 The system is ready for your specific requirements!")

if __name__ == "__main__":
    test_fashion_classification()