#!/usr/bin/env python3
"""
🌐 Network-Optimized AI Backend Server
Fixed network binding and firewall configuration
"""

import os
import sys
import logging
import socket
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import numpy as np
from PIL import Image
import cv2
import torch
from simple_clothing_detector import SimpleClothingDetector
from color_analyzer import ColorAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins="*")  # Allow all origins for testing

# Global variables for models
clothing_detector = None
color_analyzer = None

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def test_network_connectivity():
    """Test if the server is accessible from network"""
    local_ip = get_local_ip()
    try:
        # Test if we can bind to the network interface
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        test_socket.bind((local_ip, 5001))  # Test with different port
        test_socket.close()
        return True
    except Exception as e:
        logger.error(f"Network binding test failed: {e}")
        return False

def initialize_models():
    """Initialize YOLO model (without SAM for faster startup)"""
    global clothing_detector, color_analyzer
    
    try:
        logger.info("🚀 Initializing Simple Clothing Detector...")
        clothing_detector = SimpleClothingDetector()
        color_analyzer = ColorAnalyzer()
        logger.info("✅ Clothing Detector initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize models: {e}")
        return False

def decode_base64_image(base64_string):
    """Decode base64 image to PIL Image"""
    try:
        # Remove data URL prefix if present
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        logger.error(f"Error decoding image: {e}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Backend is running on network",
        "yolo_loaded": clothing_detector is not None,
        "version": "network-optimized",
        "server_ip": get_local_ip(),
        "timestamp": str(int(time.time()))
    })

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint for basic functionality"""
    return jsonify({
        "message": "Network AI Backend is working!",
        "server_ip": get_local_ip(),
        "models_loaded": {
            "yolo": clothing_detector is not None,
            "color_analyzer": color_analyzer is not None
        },
        "network_accessible": True
    })

@app.route('/detect-clothing', methods=['POST'])
def detect_clothing():
    """Detect clothing items in an image"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({
                "success": False,
                "error": "No image data provided"
            }), 400
        
        # Decode image
        image = decode_base64_image(data['image'])
        if image is None:
            return jsonify({
                "success": False,
                "error": "Invalid image data"
            }), 400
        
        # Check image size
        if image.width > 2000 or image.height > 2000:
            return jsonify({
                "success": False,
                "error": "Image too large. Please use images smaller than 2000x2000 pixels."
            }), 400
        
        # Detect clothing
        if clothing_detector is None:
            return jsonify({
                "success": False,
                "error": "Clothing detector not initialized"
            }), 500
        
        logger.info("🔍 Detecting clothing items...")
        
        try:
            detections = clothing_detector.detect_clothing(image)
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return jsonify({
                "success": False,
                "error": "Detection failed. Please try again."
            }), 500
        
        # Format results
        items = []
        for detection in detections:
            item = {
                "label": detection.get('label', 'unknown'),
                "confidence": float(detection.get('confidence', 0.0)),
                "bounding_box": detection.get('bounding_box', {}),
                "colors": detection.get('colors', [])
            }
            items.append(item)
        
        logger.info(f"✅ Found {len(items)} clothing items")
        
        return jsonify({
            "success": True,
            "items": items,
            "total_items": len(items)
        })
        
    except Exception as e:
        logger.error(f"❌ Clothing detection error: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error. Please try again."
        }), 500

@app.route('/analyze-colors', methods=['POST'])
def analyze_colors():
    """Analyze colors in an image"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({
                "success": False,
                "error": "No image data provided"
            }), 400
        
        # Decode image
        image = decode_base64_image(data['image'])
        if image is None:
            return jsonify({
                "success": False,
                "error": "Invalid image data"
            }), 400
        
        # Check image size
        if image.width > 2000 or image.height > 2000:
            return jsonify({
                "success": False,
                "error": "Image too large. Please use images smaller than 2000x2000 pixels."
            }), 400
        
        # Analyze colors
        if color_analyzer is None:
            return jsonify({
                "success": False,
                "error": "Color analyzer not initialized"
            }), 500
        
        logger.info("🎨 Analyzing colors...")
        
        try:
            color_analysis = color_analyzer.analyze_colors(image)
        except Exception as e:
            logger.error(f"Color analysis error: {e}")
            return jsonify({
                "success": False,
                "error": "Analysis failed. Please try again."
            }), 500
        
        # Format results
        dominant_colors = []
        for color in color_analysis.get('dominant_colors', []):
            dominant_colors.append({
                "name": color.get('name', 'unknown'),
                "rgb": color.get('rgb', [0, 0, 0]),
                "percentage": float(color.get('percentage', 0.0))
            })
        
        logger.info(f"✅ Analyzed {len(dominant_colors)} dominant colors")
        
        return jsonify({
            "success": True,
            "dominant_colors": dominant_colors,
            "description": color_analysis.get('description', 'Color analysis completed')
        })
        
    except Exception as e:
        logger.error(f"❌ Color analysis error: {e}")
        return jsonify({
            "success": False,
            "error": "Internal server error. Please try again."
        }), 500

if __name__ == '__main__':
    import time
    
    local_ip = get_local_ip()
    
    print("🌐 Starting Network-Optimized AI Backend Server...")
    print("=" * 70)
    print(f"📱 **FOR ANDROID PHONE, USE THIS URL:**")
    print(f"   http://{local_ip}:5000")
    print("=" * 70)
    print(f"💻 Local computer access: http://localhost:5000")
    print(f"🌐 Network IP: {local_ip}")
    print(f"📱 Make sure your phone is on the same WiFi network!")
    print("⚡ Using YOLO only for faster startup")
    print()
    
    # Test network connectivity
    if test_network_connectivity():
        print("✅ Network connectivity test passed!")
    else:
        print("⚠️ Network connectivity test failed, but continuing anyway...")
    
    print()
    
    # Initialize models
    models_loaded = initialize_models()
    
    if not models_loaded:
        print("❌ Failed to load models. Server will start but may not work properly.")
        print()
    
    print("🚀 Starting Flask server...")
    print(f"✅ Server will be accessible at: http://{local_ip}:5000")
    print("📲 Use this URL in your Flutter app configuration!")
    print()
    print("🔍 Testing URLs:")
    print(f"   Health: http://{local_ip}:5000/health")
    print(f"   Test: http://{local_ip}:5000/test")
    print()
    
    # Start server with explicit network binding
    try:
        app.run(
            host='0.0.0.0',  # Bind to all interfaces
            port=5000,
            debug=True,
            use_reloader=False,  # Disable reloader for better network stability
            threaded=True  # Enable threading for better performance
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        print("🔧 Trying alternative configuration...")
        
        # Try with different configuration
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )