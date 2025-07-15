#!/usr/bin/env python3
"""
🤖 WiFi Network AI Backend Server for Clothing Detection
Runs on local WiFi network for Android phone testing
"""

import os
import sys
import logging
import socket
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
CORS(app)

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
        "message": "AI Backend is running on WiFi network",
        "yolo_loaded": clothing_detector is not None,
        "version": "wifi-network",
        "server_ip": get_local_ip()
    })

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint for basic functionality"""
    return jsonify({
        "message": "WiFi AI Backend is working!",
        "server_ip": get_local_ip(),
        "models_loaded": {
            "yolo": clothing_detector is not None,
            "color_analyzer": color_analyzer is not None
        }
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
        
        # Set timeout for detection
        import signal
        def timeout_handler(signum, frame):
            raise TimeoutError("Detection timeout")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)  # 30 second timeout
        
        try:
            detections = clothing_detector.detect_clothing(image)
            signal.alarm(0)  # Cancel timeout
        except TimeoutError:
            signal.alarm(0)
            return jsonify({
                "success": False,
                "error": "Detection timeout. Please try with a smaller image."
            }), 408
        
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
        
        # Set timeout for analysis
        import signal
        def timeout_handler(signum, frame):
            raise TimeoutError("Analysis timeout")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(20)  # 20 second timeout
        
        try:
            color_analysis = color_analyzer.analyze_colors(image)
            signal.alarm(0)  # Cancel timeout
        except TimeoutError:
            signal.alarm(0)
            return jsonify({
                "success": False,
                "error": "Analysis timeout. Please try with a smaller image."
            }), 408
        
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
    local_ip = get_local_ip()
    
    print("🤖 Starting WiFi Network AI Backend Server...")
    print("=" * 60)
    print(f"📱 **FOR ANDROID PHONE, USE THIS URL:**")
    print(f"   http://{local_ip}:5000")
    print("=" * 60)
    print(f"💻 Local computer access: http://localhost:5000")
    print(f"🌐 Network IP: {local_ip}")
    print(f"📱 Make sure your phone is on the same WiFi network!")
    print("⚡ Using YOLO only for faster startup")
    print()
    
    # Initialize models
    models_loaded = initialize_models()
    
    if not models_loaded:
        print("❌ Failed to load models. Server will start but may not work properly.")
        print()
    
    print("🚀 Starting Flask server...")
    print(f"✅ Server accessible at: http://{local_ip}:5000")
    print("📲 Use this URL in your Flutter app configuration!")
    print()
    
    # Run server on all interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)