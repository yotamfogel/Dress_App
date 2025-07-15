#!/usr/bin/env python3
"""
📱 AI Backend Server - Port 8010 (Container Accessible)
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
CORS(app, origins="*")

# Global variables for models
clothing_detector = None
color_analyzer = None

def initialize_models():
    """Initialize YOLO model"""
    global clothing_detector, color_analyzer
    
    try:
        logger.info("🚀 Initializing AI Models...")
        clothing_detector = SimpleClothingDetector()
        color_analyzer = ColorAnalyzer()
        logger.info("✅ AI Models initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize models: {e}")
        return False

def decode_base64_image(base64_string):
    """Decode base64 image to PIL Image"""
    try:
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        logger.error(f"Error decoding image: {e}")
        return None

@app.route('/ai/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Backend is running for Android",
        "yolo_loaded": clothing_detector is not None,
        "version": "android-accessible",
        "port": "8010"
    })

@app.route('/ai/test', methods=['GET'])
def test_endpoint():
    """Test endpoint"""
    return jsonify({
        "message": "Android AI Backend is working!",
        "models_loaded": {
            "yolo": clothing_detector is not None,
            "color_analyzer": color_analyzer is not None
        },
        "status": "ready"
    })

@app.route('/ai/detect-clothing', methods=['POST'])
def detect_clothing():
    """Detect clothing items in an image"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"success": False, "error": "No image data provided"}), 400
        
        image = decode_base64_image(data['image'])
        if image is None:
            return jsonify({"success": False, "error": "Invalid image data"}), 400
        
        if image.width > 2000 or image.height > 2000:
            return jsonify({"success": False, "error": "Image too large"}), 400
        
        if clothing_detector is None:
            return jsonify({"success": False, "error": "Detector not ready"}), 500
        
        logger.info("🔍 Detecting clothing items...")
        
        try:
            detections = clothing_detector.detect_clothing(image)
            
            items = []
            for detection in detections:
                items.append({
                    "label": detection.get('label', 'unknown'),
                    "confidence": float(detection.get('confidence', 0.0)),
                    "bounding_box": detection.get('bounding_box', {}),
                    "colors": detection.get('colors', [])
                })
            
            logger.info(f"✅ Found {len(items)} clothing items")
            
            return jsonify({
                "success": True,
                "items": items,
                "total_items": len(items)
            })
            
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return jsonify({"success": False, "error": "Detection failed"}), 500
        
    except Exception as e:
        logger.error(f"❌ Clothing detection error: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

@app.route('/ai/analyze-colors', methods=['POST'])
def analyze_colors():
    """Analyze colors in an image"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"success": False, "error": "No image data provided"}), 400
        
        image = decode_base64_image(data['image'])
        if image is None:
            return jsonify({"success": False, "error": "Invalid image data"}), 400
        
        if image.width > 2000 or image.height > 2000:
            return jsonify({"success": False, "error": "Image too large"}), 400
        
        if color_analyzer is None:
            return jsonify({"success": False, "error": "Analyzer not ready"}), 500
        
        logger.info("🎨 Analyzing colors...")
        
        try:
            color_analysis = color_analyzer.analyze_colors(image)
            
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
            logger.error(f"Color analysis error: {e}")
            return jsonify({"success": False, "error": "Analysis failed"}), 500
        
    except Exception as e:
        logger.error(f"❌ Color analysis error: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500

if __name__ == '__main__':
    print("📱 Starting AI Backend Server on Port 7000...")
    print("=" * 60)
    print("🔧 **Server will be accessible at:**")
    print(f"   http://192.168.1.172:7000/ai/health")
    print("📱 **Android testing URL:**")
    print(f"   http://192.168.1.172:7000")
    print("⚡ Using optimized YOLO for fast processing")
    print()
    
    # Initialize models
    models_loaded = initialize_models()
    
    if not models_loaded:
        print("❌ Failed to load AI models")
        sys.exit(1)
    
    print("🚀 Starting server on port 7000...")
    print("✅ AI models loaded and ready!")
    print()
    
    # Start server on port 7000 (should be accessible)
    try:
        app.run(
            host='0.0.0.0',
            port=7000,
            debug=False,
            threaded=True
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)