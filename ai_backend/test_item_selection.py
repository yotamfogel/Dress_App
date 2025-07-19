#!/usr/bin/env python3
"""
🧪 Test Item Selection and Analysis
Test the enhanced server's item selection functionality
"""

import requests
import base64
import json
from PIL import Image
import numpy as np

def create_test_image():
    """Create a simple test image with multiple colors"""
    # Create a test image with different colored regions
    img = Image.new('RGB', (224, 224), color='red')
    # Add some blue and green regions
    pixels = img.load()
    for i in range(100, 150):
        for j in range(100, 150):
            pixels[i, j] = (0, 0, 255)  # Blue
    for i in range(50, 100):
        for j in range(50, 100):
            pixels[i, j] = (0, 255, 0)  # Green
    
    return img

def image_to_base64(image):
    """Convert PIL image to base64 string"""
    import io
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def test_item_selection():
    """Test the complete item selection flow"""
    print("🧪 Testing Item Selection and Analysis")
    print("=" * 50)
    
    # Create test image
    test_image = create_test_image()
    base64_image = image_to_base64(test_image)
    
    # Step 1: Initial analysis (should detect multiple items)
    print("🔍 Step 1: Initial analysis...")
    response1 = requests.post(
        'http://localhost:5000/analyze-fashion',
        json={'image': base64_image},
        headers={'Content-Type': 'application/json'}
    )
    
    if response1.status_code != 200:
        print(f"❌ Initial analysis failed: {response1.status_code}")
        print(response1.text)
        return False
    
    result1 = response1.json()
    print(f"✅ Initial analysis response: {json.dumps(result1, indent=2)}")
    
    # Check if multiple items were detected
    if not result1.get('multiple_items', False):
        print("⚠️ No multiple items detected, testing single item analysis...")
        return test_single_item_analysis(base64_image)
    
    # Step 2: Select an item
    print("\n🔍 Step 2: Selecting item 1...")
    response2 = requests.post(
        'http://localhost:5000/analyze-fashion',
        json={
            'image': base64_image,
            'item_selection': 1
        },
        headers={'Content-Type': 'application/json'}
    )
    
    if response2.status_code != 200:
        print(f"❌ Item selection failed: {response2.status_code}")
        print(response2.text)
        return False
    
    result2 = response2.json()
    print(f"✅ Item selection response: {json.dumps(result2, indent=2)}")
    
    # Verify the response format
    if result2.get('success', False):
        print("✅ Item selection successful!")
        print(f"  Clothing type: {result2.get('clothing_type', 'N/A')}")
        print(f"  Colors: {len(result2.get('colors', []))}")
        print(f"  Styles: {len(result2.get('applicable_styles', []))}")
        print(f"  Color description: {result2.get('color_description', 'N/A')}")
        return True
    else:
        print(f"❌ Item selection failed: {result2.get('error', 'Unknown error')}")
        return False

def test_single_item_analysis(base64_image):
    """Test single item analysis"""
    print("🔍 Testing single item analysis...")
    
    response = requests.post(
        'http://localhost:5000/analyze-fashion',
        json={'image': base64_image},
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code != 200:
        print(f"❌ Single item analysis failed: {response.status_code}")
        print(response.text)
        return False
    
    result = response.json()
    print(f"✅ Single item analysis response: {json.dumps(result, indent=2)}")
    
    if result.get('success', False):
        print("✅ Single item analysis successful!")
        print(f"  Clothing type: {result.get('clothing_type', 'N/A')}")
        print(f"  Colors: {len(result.get('colors', []))}")
        print(f"  Styles: {len(result.get('applicable_styles', []))}")
        return True
    else:
        print(f"❌ Single item analysis failed: {result.get('error', 'Unknown error')}")
        return False

if __name__ == "__main__":
    try:
        success = test_item_selection()
        if success:
            print("\n🎉 All tests passed! Item selection is working correctly.")
        else:
            print("\n❌ Tests failed. Check the logs above.")
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc() 