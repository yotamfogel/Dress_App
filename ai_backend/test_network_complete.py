#!/usr/bin/env python3
"""
🌐 Comprehensive Network Test for AI Backend
Tests all network interfaces and connectivity
"""

import requests
import json
import socket
import subprocess
import time
import threading

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

def test_endpoint(url, description, timeout=10):
    """Test a specific endpoint"""
    try:
        print(f"🔍 Testing {description}")
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            print(f"✅ {description} - SUCCESS")
            result = response.json()
            print(f"   Response: {result}")
            return True
        else:
            print(f"❌ {description} - FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏱️ {description} - TIMEOUT")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {description} - CONNECTION ERROR")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def test_port_connectivity(ip, port):
    """Test if port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def get_network_info():
    """Get network interface information"""
    try:
        # Try to get network interfaces
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip().split()
        return []
    except Exception:
        return []

def main():
    local_ip = get_local_ip()
    
    print("🌐 Comprehensive Network Test for AI Backend")
    print("=" * 60)
    print(f"🖥️  Local IP: {local_ip}")
    print(f"📱 Android URL: http://{local_ip}:5000")
    print()
    
    # Get all network interfaces
    all_ips = get_network_info()
    print(f"🌐 Available network interfaces: {all_ips}")
    print()
    
    # Test port connectivity first
    print("🔌 Testing port connectivity...")
    print("-" * 40)
    
    port_tests = [
        ("localhost", 5000),
        (local_ip, 5000),
        ("127.0.0.1", 5000),
    ]
    
    for ip, port in port_tests:
        if test_port_connectivity(ip, port):
            print(f"✅ Port {port} is open on {ip}")
        else:
            print(f"❌ Port {port} is closed on {ip}")
    
    print()
    
    # Test HTTP endpoints
    print("🌐 Testing HTTP endpoints...")
    print("-" * 40)
    
    endpoints = [
        (f"http://localhost:5000/health", "Local Health Check"),
        (f"http://127.0.0.1:5000/health", "Loopback Health Check"),
        (f"http://{local_ip}:5000/health", "Network Health Check"),
        (f"http://localhost:5000/test", "Local Test Endpoint"),
        (f"http://{local_ip}:5000/test", "Network Test Endpoint"),
    ]
    
    success_count = 0
    for url, description in endpoints:
        if test_endpoint(url, description):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {success_count}/{len(endpoints)} passed")
    print()
    
    if success_count >= 3:
        print("✅ Server is accessible from network!")
        print()
        print("📱 **FOR ANDROID PHONE:**")
        print(f"   1. Connect to the same WiFi network")
        print(f"   2. Open browser and go to: http://{local_ip}:5000/health")
        print(f"   3. You should see a JSON response with status 'healthy'")
        print(f"   4. Use http://{local_ip}:5000 in your Flutter app")
        print()
        print("🔧 **FLUTTER APP CONFIGURATION:**")
        print(f"   Update ai_backend_manager.dart with: http://{local_ip}:5000")
        print()
        print("🧪 **TESTING STEPS:**")
        print("   1. Build your Flutter app")
        print("   2. Install on Android device")
        print("   3. Open app and tap brain icon")
        print("   4. Check connection status")
        print("   5. Upload image and test AI")
        
    else:
        print("❌ Network connectivity issues detected!")
        print()
        print("🔧 **TROUBLESHOOTING:**")
        print("   1. Check if server is running:")
        print("      ps aux | grep start_network_server")
        print("   2. Check firewall settings")
        print("   3. Verify WiFi network")
        print("   4. Try restarting the server")
        
    print()
    print("🔍 **MANUAL TESTING:**")
    print(f"   Open browser and visit: http://{local_ip}:5000/health")
    print("   You should see a JSON response if working correctly")

if __name__ == '__main__':
    main()