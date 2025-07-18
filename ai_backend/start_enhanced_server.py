#!/usr/bin/env python3
"""
🚀 Enhanced AI Backend Server with Fashion Classification System
Advanced clothing detection, style classification, and color analysis
"""

import os
import sys
import logging
from flask import Flask, request, jsonify, session
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
from fashion_classification_system import FashionClassificationSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'fashion_classification_secret_key'
CORS(app)

# Global variables for models
enhanced_detector = None
color_analyzer = None
fashion_classifier = None

def initialize_models():
    """Initialize all AI models"""
    global enhanced_detector, color_analyzer, fashion_classifier
    
    try:
        logger.info("🚀 Initializing Enhanced AI Models...")
        
        # Initialize Enhanced Clothing Detector
        enhanced_detector = EnhancedClothingDetector()
        
        # Initialize Color Analyzer
        color_analyzer = ColorAnalyzer()
        
        # Initialize Fashion Classification System
        
        fashion_classifier = FashionClassificationSystem()
        
        logger.info("✅ All AI models initialized successfully!")
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
        "message": "Enhanced AI Backend with Fashion Classification",
        "models_loaded": {
            "enhanced_detector": enhanced_detector is not None,
            "color_analyzer": color_analyzer is not None,
            "fashion_classifier": fashion_classifier is not None
        },
        "version": "fashion_v1",
        "features": [
            "Fashion Type Classification",
            "Style Category Mapping",
            "Color Percentage Analysis",
            "Multiple Item Detection",
            "User Feedback Integration"
        ]
    })

@app.route('/analyze-fashion', methods=['POST'])
def analyze_fashion():
    """
    Main endpoint for fashion analysis
    Returns: clothing type, applicable styles, and color percentages
    """
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
        
        # Check if this is a follow-up request for item selection
        if 'item_selection' in data and 'detected_items' in session:
            try:
                item_id = int(data['item_selection'])
                detected_items = session['detected_items']
                
                # Analyze the selected item
                result = fashion_classifier.analyze_selected_item(image, item_id, detected_items)
                
                # Clear session data
                session.pop('detected_items', None)
                
                return jsonify(result)
                
            except ValueError:
                return jsonify({
                    "success": False,
                    "error": "Invalid item selection. Please provide a number."
                }), 400
        
        # Perform fashion analysis
        if fashion_classifier is None:
            return jsonify({
                "success": False,
                "error": "Fashion classifier not initialized"
            }), 500
        
        logger.info("🔍 Analyzing fashion image...")
        analysis_result = fashion_classifier.analyze_clothing_image(image)
        
        # Handle multiple items case
        if analysis_result.get('multiple_items', False):
            # Store detected items in session for follow-up
            session['detected_items'] = analysis_result['items']
            
            # Format the response for multiple items
            items_list = []
            for item in analysis_result['items']:
                items_list.append({
                    'id': item['id'],
                    'description': f"{item['label']} (confidence: {item['confidence']:.1%})"
                })
            
            return jsonify({
                "success": True,
                "multiple_items": True,
                "message": "Multiple clothing items detected. Please select which item to analyze:",
                "items": items_list,
                "instruction": "Send another request with 'item_selection': [item_id] to analyze the specific item."
            })
        
        # Single item or whole image analysis
        if 'analysis' in analysis_result:
            analysis = analysis_result['analysis']
            
            # Format the response according to user requirements
            response = {
                "success": True,
                "clothing_type": analysis.get('clothing_type', 'unknown'),
                "applicable_styles": analysis.get('applicable_styles', []),
                "colors": analysis.get('colors', []),
                "color_description": analysis.get('color_description', 'No colors detected'),
                "detection_details": {
                    "detected_as": analysis.get('detected_as', 'unknown'),
                    "confidence": analysis.get('confidence', 0),
                    "method": "Fashion Classification System"
                }
            }
            
            # Add note if present
            if 'note' in analysis:
                response['note'] = analysis['note']
            
            return jsonify(response)
        
        logger.error("❌ Unexpected analysis result format")
        return jsonify({
            "success": False,
            "error": "Unexpected analysis result format"
        }), 500
        
    except Exception as e:
        logger.error(f"❌ Fashion analysis error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Legacy endpoints for backward compatibility
@app.route('/detect-clothing', methods=['POST'])
def detect_clothing():
    """Legacy endpoint - redirects to fashion analysis"""
    return analyze_fashion()

@app.route('/analyze-colors', methods=['POST'])
def analyze_colors():
    """Enhanced color analysis endpoint"""
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
        
        logger.info("🎨 Analyzing colors...")
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

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint for basic functionality"""
    return jsonify({
        "message": "Enhanced AI Backend with Fashion Classification is working!",
        "models_loaded": {
            "enhanced_detector": enhanced_detector is not None,
            "color_analyzer": color_analyzer is not None,
            "fashion_classifier": fashion_classifier is not None
        },
        "capabilities": {
            "fashion_classification": "Clothing type identification",
            "style_mapping": "21 style categories",
            "color_analysis": "Percentage-based color detection",
            "multiple_items": "Handle multiple clothing items",
            "user_feedback": "Interactive item selection"
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Enhanced AI Backend Server with Fashion Classification...")
    print("📍 Server will run on: http://localhost:5000")
    print("🔬 Features:")
    print("  - Fashion Type Classification")
    print("  - Style Category Mapping (21 styles)")
    print("  - Color Percentage Analysis")
    print("  - Multiple Item Detection")
    print("  - User Feedback Integration")
    print()
    
    # Initialize models
    models_loaded = initialize_models()
    
    if not models_loaded:
        print("❌ Failed to load models. Server will start but may not work properly.")
    
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)