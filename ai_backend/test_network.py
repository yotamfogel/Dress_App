#!/usr/bin/env python3
"""
📱 Network Test Script for Android Phone Testing
Tests connectivity from different IP addresses
"""

import requests
import json
import socket
import time

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def test_endpoint(url, description):
    """Test a specific endpoint"""
    try:
        print(f"🔍 Testing {description}: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ {description} - SUCCESS")
            result = response.json()
            print(f"   Response: {result}")
            return True
        else:
            print(f"❌ {description} - FAILED (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    local_ip = get_local_ip()
    
    print("📱 AI Backend Network Connectivity Test")
    print("=" * 50)
    print(f"🌐 Local IP Address: {local_ip}")
    print(f"📲 Android Phone URL: http://{local_ip}:5000")
    print()
    
    # Test different endpoints
    endpoints = [
        (f"http://localhost:5000/health", "Local Health Check"),
        (f"http://{local_ip}:5000/health", "Network Health Check"),
        (f"http://localhost:5000/test", "Local Test Endpoint"),
        (f"http://{local_ip}:5000/test", "Network Test Endpoint"),
    ]
    
    print("🧪 Running connectivity tests...")
    print("-" * 40)
    
    success_count = 0
    for url, description in endpoints:
        if test_endpoint(url, description):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {success_count}/{len(endpoints)} passed")
    
    if success_count >= 2:
        print("✅ Server is ready for Android phone testing!")
        print()
        print("📱 **ANDROID PHONE SETUP:**")
        print(f"   1. Connect your phone to the same WiFi network")
        print(f"   2. Use this URL in your Flutter app: http://{local_ip}:5000")
        print(f"   3. Test the connection in your app")
        print()
        print("🔧 **FLUTTER APP CONFIGURATION:**")
        print(f"   The app is already configured to use: http://{local_ip}:5000")
        print(f"   Build and run your Flutter app on Android!")
    else:
        print("❌ Server connectivity issues detected!")
        print("🔍 Check if the server is running and try again.")

if __name__ == '__main__':
    main()