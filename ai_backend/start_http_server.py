#!/usr/bin/env python3
"""
📱 Simple HTTP AI Server - Network Accessible
Uses Python's built-in HTTP server with threading for network access
"""

import os
import sys
import json
import base64
import threading
import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import io
from PIL import Image
import numpy as np
import cv2
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import AI modules
try:
    from simple_clothing_detector import SimpleClothingDetector
    from color_analyzer import ColorAnalyzer
    
    # Initialize AI models
    print("🚀 Initializing AI models...")
    clothing_detector = SimpleClothingDetector()
    color_analyzer = ColorAnalyzer()
    print("✅ AI models loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load AI models: {e}")
    clothing_detector = None
    color_analyzer = None

class AIRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """Custom logging to reduce noise"""
        pass
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/ai/health':
            self.send_json_response({
                "status": "healthy",
                "message": "AI Backend is running for Android",
                "yolo_loaded": clothing_detector is not None,
                "version": "http-server",
                "port": "8080"
            })
        elif self.path == '/ai/test':
            self.send_json_response({
                "message": "HTTP AI Backend is working!",
                "models_loaded": {
                    "yolo": clothing_detector is not None,
                    "color_analyzer": color_analyzer is not None
                },
                "status": "ready"
            })
        else:
            self.send_json_response({"error": "Not Found"}, status=404)
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/ai/detect-clothing':
            self.handle_detect_clothing()
        elif self.path == '/ai/analyze-colors':
            self.handle_analyze_colors()
        else:
            self.send_json_response({"error": "Not Found"}, status=404)
    
    def handle_detect_clothing(self):
        """Handle clothing detection"""
        try:
            # Get request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if not data or 'image' not in data:
                self.send_json_response({"success": False, "error": "No image data"}, status=400)
                return
            
            # Decode image
            image = self.decode_base64_image(data['image'])
            if image is None:
                self.send_json_response({"success": False, "error": "Invalid image"}, status=400)
                return
            
            # Check if models are loaded
            if clothing_detector is None:
                self.send_json_response({"success": False, "error": "AI models not loaded"}, status=500)
                return
            
            # Detect clothing
            logger.info("🔍 Detecting clothing...")
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
            
            self.send_json_response({
                "success": True,
                "items": items,
                "total_items": len(items)
            })
            
        except Exception as e:
            logger.error(f"❌ Detection error: {e}")
            self.send_json_response({"success": False, "error": str(e)}, status=500)
    
    def handle_analyze_colors(self):
        """Handle color analysis"""
        try:
            # Get request data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if not data or 'image' not in data:
                self.send_json_response({"success": False, "error": "No image data"}, status=400)
                return
            
            # Decode image
            image = self.decode_base64_image(data['image'])
            if image is None:
                self.send_json_response({"success": False, "error": "Invalid image"}, status=400)
                return
            
            # Check if models are loaded
            if color_analyzer is None:
                self.send_json_response({"success": False, "error": "AI models not loaded"}, status=500)
                return
            
            # Analyze colors
            logger.info("🎨 Analyzing colors...")
            color_analysis = color_analyzer.analyze_colors(image)
            
            dominant_colors = []
            for color in color_analysis.get('dominant_colors', []):
                dominant_colors.append({
                    "name": color.get('name', 'unknown'),
                    "rgb": color.get('rgb', [0, 0, 0]),
                    "percentage": float(color.get('percentage', 0.0))
                })
            
            logger.info(f"✅ Analyzed {len(dominant_colors)} colors")
            
            self.send_json_response({
                "success": True,
                "dominant_colors": dominant_colors,
                "description": color_analysis.get('description', 'Color analysis completed')
            })
            
        except Exception as e:
            logger.error(f"❌ Color analysis error: {e}")
            self.send_json_response({"success": False, "error": str(e)}, status=500)
    
    def decode_base64_image(self, base64_string):
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
            logger.error(f"Image decode error: {e}")
            return None
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        json_data = json.dumps(data)
        self.wfile.write(json_data.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread"""
    pass

def start_server():
    """Start the HTTP server"""
    server_address = ('0.0.0.0', 8080)
    httpd = ThreadedHTTPServer(server_address, AIRequestHandler)
    
    print("📱 AI HTTP Server Starting...")
    print("=" * 60)
    print("🔧 **Server accessible at:**")
    print(f"   http://192.168.1.172:8080/ai/health")
    print("📱 **Test this URL in your phone's browser first!**")
    print("⚡ Using threaded HTTP server for network access")
    print()
    print("✅ Server ready and waiting for connections...")
    print("🌐 Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == '__main__':
    start_server()