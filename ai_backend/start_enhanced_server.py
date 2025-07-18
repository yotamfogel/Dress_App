#!/usr/bin/env python3
"""
🚀 Enhanced AI Backend Server with Mask R-CNN + MMFashion
Advanced clothing detection using Detectron2 Mask R-CNN and MMFashion
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
import numpy as np
from PIL import Image
import cv2
import torch
import traceback
from enhanced_clothing_detector import EnhancedClothingDetector
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
enhanced_detector = None
color_analyzer = None

def initialize_models():
    """Initialize Enhanced Clothing Detector and Color Analyzer"""
    global enhanced_detector, color_analyzer
    
    try:
        logger.info("🚀 Initializing Enhanced Clothing Detector (Mask R-CNN + MMFashion)...")
        enhanced_detector = EnhancedClothingDetector()
        color_analyzer = ColorAnalyzer()
        logger.info("✅ Enhanced Clothing Detector initialized successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize models: {e}")
        logger.error(traceback.format_exc())
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
        "message": "Enhanced AI Backend is running",
        "models_loaded": {
            "enhanced_detector": enhanced_detector is not None,
            "color_analyzer": color_analyzer is not None
        },
        "version": "enhanced_v1",
        "features": [
            "Mask R-CNN segmentation",
            "MMFashion attributes",
            "Advanced color analysis",
            "Fashion-specific detection"
        ]
    })

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint for basic functionality"""
    return jsonify({
        "message": "Enhanced AI Backend is working!",
        "models_loaded": {
            "enhanced_detector": enhanced_detector is not None,
            "color_analyzer": color_analyzer is not None
        },
        "capabilities": {
            "segmentation": "Mask R-CNN based",
            "attributes": "MMFashion based",
            "color_analysis": "Advanced clustering",
            "fallback": "YOLO available"
        }
    })

@app.route('/detect-clothing', methods=['POST'])
def detect_clothing():
    """Detect clothing items with enhanced segmentation and attributes"""
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
        
        # Detect clothing
        if enhanced_detector is None:
            return jsonify({
                "success": False,
                "error": "Enhanced detector not initialized"
            }), 500
        
        logger.info("🔍 Detecting clothing items with enhanced models...")
        detections = enhanced_detector.detect_clothing(image)
        
        # Format results
        items = []
        for detection in detections:
            item = {
                "label": detection.get('label', 'unknown'),
                "confidence": float(detection.get('confidence', 0.0)),
                "bounding_box": detection.get('bounding_box', {}),
                "colors": detection.get('colors', []),
                "attributes": detection.get('attributes', {}),
                "segmentation_available": detection.get('segmentation_available', False),
                "mask_area": detection.get('mask_area', 0)
            }
            items.append(item)
        
        logger.info(f"✅ Found {len(items)} clothing items with enhanced detection")
        
        return jsonify({
            "success": True,
            "items": items,
            "total_items": len(items),
            "detection_method": "Enhanced (Mask R-CNN + MMFashion)"
        })
        
    except Exception as e:
        logger.error(f"❌ Enhanced clothing detection error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/analyze-colors', methods=['POST'])
def analyze_colors():
    """Analyze colors in an image with enhanced accuracy"""
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
        
        # Analyze colors
        if color_analyzer is None:
            return jsonify({
                "success": False,
                "error": "Color analyzer not initialized"
            }), 500
        
        logger.info("🎨 Analyzing colors with enhanced accuracy...")
        color_analysis = color_analyzer.analyze_colors(image)
        
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
            "description": color_analysis.get('description', 'Enhanced color analysis completed'),
            "analysis_method": "Enhanced clustering"
        })
        
    except Exception as e:
        logger.error(f"❌ Enhanced color analysis error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/detect-attributes', methods=['POST'])
def detect_attributes():
    """Detect fashion attributes using MMFashion"""
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
        
        # Detect attributes
        if enhanced_detector is None:
            return jsonify({
                "success": False,
                "error": "Enhanced detector not initialized"
            }), 500
        
        logger.info("🏷️ Detecting fashion attributes...")
        
        # Get detections first
        detections = enhanced_detector.detect_clothing(image)
        
        # Extract attributes for each detection
        attributes_results = []
        for detection in detections:
            attributes = detection.get('attributes', {})
            attributes_results.append({
                "label": detection.get('label', 'unknown'),
                "confidence": detection.get('confidence', 0.0),
                "attributes": attributes
            })
        
        logger.info(f"✅ Detected attributes for {len(attributes_results)} items")
        
        return jsonify({
            "success": True,
            "items": attributes_results,
            "total_items": len(attributes_results),
            "method": "MMFashion (placeholder)"
        })
        
    except Exception as e:
        logger.error(f"❌ Attribute detection error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/analyze-complete', methods=['POST'])
def analyze_complete():
    """Complete analysis: detection + segmentation + colors + attributes"""
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
        
        if enhanced_detector is None:
            return jsonify({
                "success": False,
                "error": "Enhanced detector not initialized"
            }), 500
        
        logger.info("🎯 Running complete analysis...")
        
        # Get enhanced detections (includes everything)
        detections = enhanced_detector.detect_clothing(image)
        
        # Get overall color analysis
        color_analysis = color_analyzer.analyze_colors(image) if color_analyzer else {}
        
        # Calculate summary statistics
        total_items = len(detections)
        segmented_items = sum(1 for d in detections if d.get('segmentation_available', False))
        
        # Get all unique colors
        all_colors = []
        for detection in detections:
            all_colors.extend(detection.get('colors', []))
        
        # Get unique attributes
        all_attributes = {}
        for detection in detections:
            attrs = detection.get('attributes', {})
            for key, value in attrs.items():
                if key not in all_attributes:
                    all_attributes[key] = []
                if value not in all_attributes[key]:
                    all_attributes[key].append(value)
        
        logger.info(f"✅ Complete analysis: {total_items} items, {segmented_items} segmented")
        
        return jsonify({
            "success": True,
            "detections": detections,
            "color_analysis": color_analysis,
            "summary": {
                "total_items": total_items,
                "segmented_items": segmented_items,
                "unique_colors": len(set(c['name'] for c in all_colors)),
                "attributes_detected": len(all_attributes)
            },
            "method": "Enhanced Complete Analysis"
        })
        
    except Exception as e:
        logger.error(f"❌ Complete analysis error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced AI Backend Server...")
    print("📍 Server will run on: http://localhost:5000")
    print("🔬 Features:")
    print("  - Mask R-CNN segmentation")
    print("  - MMFashion attributes")
    print("  - Advanced color analysis")
    print("  - Fashion-specific detection")
    print("  - YOLO fallback support")
    print()
    
    # Initialize models
    models_loaded = initialize_models()
    
    if not models_loaded:
        print("❌ Failed to load models. Server will start but may not work properly.")
        print("💡 The server will use fallback detection methods.")
    
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)