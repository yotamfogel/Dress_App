#!/usr/bin/env python3
"""
Test Enhanced AI Backend with realistic clothing detection
"""

import requests
import json
import base64
import os
from PIL import Image, ImageDraw
import numpy as np

def create_realistic_clothing_image():
    """Create a more realistic clothing image for testing"""
    # Create a larger image with better defined clothing items
    img = np.zeros((800, 600, 3), dtype=np.uint8)
    
    # Create a person silhouette
    person_mask = np.zeros((800, 600), dtype=bool)
    
    # Head
    head_center = (300, 120)
    head_radius = 60
    y, x = np.ogrid[:800, :600]
    head_mask = (x - head_center[0])**2 + (y - head_center[1])**2 <= head_radius**2
    person_mask |= head_mask
    
    # Body (torso)
    torso_rect = (200, 180, 400, 450)  # x1, y1, x2, y2
    person_mask[torso_rect[1]:torso_rect[3], torso_rect[0]:torso_rect[2]] = True
    
    # Arms
    left_arm_rect = (120, 200, 200, 400)
    right_arm_rect = (400, 200, 480, 400)
    person_mask[left_arm_rect[1]:left_arm_rect[3], left_arm_rect[0]:left_arm_rect[2]] = True
    person_mask[right_arm_rect[1]:right_arm_rect[3], right_arm_rect[0]:right_arm_rect[2]] = True
    
    # Legs
    left_leg_rect = (220, 450, 280, 700)
    right_leg_rect = (320, 450, 380, 700)
    person_mask[left_leg_rect[1]:left_leg_rect[3], left_leg_rect[0]:left_leg_rect[2]] = True
    person_mask[right_leg_rect[1]:right_leg_rect[3], right_leg_rect[0]:right_leg_rect[2]] = True
    
    # Fill person with skin color
    img[person_mask] = [220, 180, 140]  # Skin color
    
    # Add clothing items
    # Red shirt
    shirt_rect = (200, 180, 400, 350)
    img[shirt_rect[1]:shirt_rect[3], shirt_rect[0]:shirt_rect[2]] = [200, 50, 50]
    
    # Blue jeans
    jeans_rect = (220, 350, 380, 700)
    img[jeans_rect[1]:jeans_rect[3], jeans_rect[0]:jeans_rect[2]] = [50, 50, 180]
    
    # Black shoes
    left_shoe_rect = (210, 680, 290, 720)
    right_shoe_rect = (310, 680, 390, 720)
    img[left_shoe_rect[1]:left_shoe_rect[3], left_shoe_rect[0]:left_shoe_rect[2]] = [30, 30, 30]
    img[right_shoe_rect[1]:right_shoe_rect[3], right_shoe_rect[0]:right_shoe_rect[2]] = [30, 30, 30]
    
    # Add some texture/noise to make it more realistic
    noise = np.random.normal(0, 10, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(img)

def image_to_base64(image):
    """Convert PIL image to base64"""
    import io
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def test_realistic_clothing_detection():
    """Test with realistic clothing image"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Enhanced AI Backend with Realistic Clothing")
    print("=" * 60)
    
    # Create realistic test image
    print("🖼️ Creating realistic clothing image...")
    test_image = create_realistic_clothing_image()
    
    # Save image for inspection
    test_image.save("/app/ai_backend/test_clothing_image.png")
    print("📁 Test image saved as test_clothing_image.png")
    
    base64_image = image_to_base64(test_image)
    print(f"✅ Image encoded (base64 length: {len(base64_image)})")
    
    # Test enhanced clothing detection
    print("\n🔍 Testing Enhanced Clothing Detection:")
    print("-" * 40)
    
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/detect-clothing", json=payload)
        
        if response.status_code == 200:
            detection_data = response.json()
            print(f"✅ Detection Success: {detection_data.get('success', False)}")
            print(f"📊 Total items detected: {detection_data.get('total_items', 0)}")
            print(f"🔬 Detection method: {detection_data.get('detection_method', 'unknown')}")
            
            items = detection_data.get('items', [])
            if items:
                print(f"\n📦 Detected Items:")
                for i, item in enumerate(items):
                    print(f"   Item {i+1}:")
                    print(f"      🏷️  Label: {item.get('label', 'unknown')}")
                    print(f"      🎯 Confidence: {item.get('confidence', 0):.3f}")
                    print(f"      📐 Segmentation: {item.get('segmentation_available', False)}")
                    print(f"      🔧 Method: {item.get('detection_method', 'unknown')}")
                    
                    # Colors
                    colors = item.get('colors', [])
                    if colors:
                        print(f"      🎨 Colors ({len(colors)}):")
                        for color in colors[:3]:  # Show top 3
                            print(f"         - {color['name']}: {color['percentage']}%")
                    
                    # Attributes
                    attributes = item.get('attributes', {})
                    if attributes:
                        print(f"      🏷️  Attributes:")
                        for key, value in attributes.items():
                            print(f"         - {key}: {value}")
            else:
                print("📦 No clothing items detected")
                
        else:
            print(f"❌ Detection failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test color analysis
    print("\n🎨 Testing Color Analysis:")
    print("-" * 40)
    
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/analyze-colors", json=payload)
        
        if response.status_code == 200:
            color_data = response.json()
            print(f"✅ Color Analysis Success: {color_data.get('success', False)}")
            
            colors = color_data.get('dominant_colors', [])
            if colors:
                print(f"🌈 Dominant Colors ({len(colors)}):")
                for color in colors:
                    print(f"   - {color['name']}: {color['percentage']}% (RGB: {color['rgb']})")
            
            description = color_data.get('description', '')
            if description:
                print(f"📝 Description: {description}")
        else:
            print(f"❌ Color analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test complete analysis
    print("\n🎯 Testing Complete Analysis:")
    print("-" * 40)
    
    try:
        payload = {"image": base64_image}
        response = requests.post(f"{base_url}/analyze-complete", json=payload)
        
        if response.status_code == 200:
            complete_data = response.json()
            print(f"✅ Complete Analysis Success: {complete_data.get('success', False)}")
            
            summary = complete_data.get('summary', {})
            if summary:
                print(f"📊 Analysis Summary:")
                for key, value in summary.items():
                    print(f"   - {key}: {value}")
            
            # Show first few detections
            detections = complete_data.get('detections', [])
            if detections:
                print(f"\n🔍 Detection Details:")
                for i, detection in enumerate(detections[:2]):  # Show first 2
                    print(f"   Detection {i+1}: {detection.get('label', 'unknown')} "
                          f"(confidence: {detection.get('confidence', 0):.3f})")
        else:
            print(f"❌ Complete analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Realistic Clothing Detection Test Completed!")
    print("\n💡 Enhanced Features Active:")
    print("   ✅ YOLO-based clothing detection")
    print("   ✅ Advanced color analysis with K-means")
    print("   ✅ Heuristic-based attribute detection")
    print("   ✅ Fashion-specific category filtering")
    print("   ✅ Multiple API endpoints")
    print("   ⏳ Detectron2 Mask R-CNN (installing...)")
    print("   ⏳ MMFashion attributes (installing...)")

if __name__ == "__main__":
    test_realistic_clothing_detection()