#!/usr/bin/env python3
"""
Test script for the AI backend
"""

import requests
import json
import base64
from PIL import Image
import io
import time

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get('http://192.168.1.172/health', timeout=10)
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_with_dummy_image():
    """Test with a dummy image"""
    try:
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # Test clothing detection
        print("Testing clothing detection...")
        response = requests.post(
            'http://192.168.1.172/detect-clothing',
            json={'image': base64_image},
            timeout=30
        )
        print(f"Clothing detection: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test color analysis
        print("\nTesting color analysis...")
        response = requests.post(
            'http://192.168.1.172/analyze-colors',
            json={'image': base64_image},
            timeout=30
        )
        print(f"Color analysis: {response.status_code}")
        print(f"Response: {response.json()}")
        
        return True
    except Exception as e:
        print(f"Image test failed: {e}")
        return False

if __name__ == '__main__':
    print("🧪 Testing AI Backend...")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to initialize...")
    for i in range(30):
        if test_health():
            print("✅ Server is healthy!")
            break
        time.sleep(2)
        print(f"Retry {i+1}/30...")
    else:
        print("❌ Server health check failed after 30 retries")
        exit(1)
    
    # Test with dummy image
    print("\n🖼️ Testing with dummy image...")
    if test_with_dummy_image():
        print("✅ Image testing completed!")
    else:
        print("❌ Image testing failed!")