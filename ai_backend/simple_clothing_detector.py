"""
👕 Simple Clothing Detection with YOLO only
Faster initialization without SAM for testing
"""

import cv2
import numpy as np
import torch
from ultralytics import YOLO
import logging
from typing import List, Dict, Any
from PIL import Image
import webcolors
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)

class SimpleClothingDetector:
    def __init__(self):
        """Initialize YOLO model only"""
        self.yolo_model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Clothing categories that YOLO can detect
        self.clothing_categories = [
            'person', 'shirt', 'pants', 'shoes', 'dress', 'jacket', 'coat',
            'hat', 'bag', 'tie', 'socks', 'gloves', 'scarf', 'belt',
            'skirt', 'shorts', 'sweater', 'hoodie', 'jeans', 'sneakers',
            'boots', 'sandals', 'backpack', 'handbag', 'sunglasses'
        ]
        
        self._load_yolo_model()
    
    def _load_yolo_model(self):
        """Load YOLO model"""
        try:
            logger.info("📦 Loading YOLO model...")
            self.yolo_model = YOLO('yolov8n.pt')  # nano version for faster inference
            logger.info("✅ YOLO model loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error loading YOLO model: {e}")
            raise
    
    def detect_clothing(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Detect clothing items in an image"""
        try:
            # Resize image for faster processing
            max_size = 640
            if image.width > max_size or image.height > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Run YOLO detection with optimized settings
            results = self.yolo_model(opencv_image, conf=0.3, iou=0.5, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get detection info
                        conf = float(box.conf)
                        cls = int(box.cls)
                        class_name = self.yolo_model.names[cls]
                        
                        # Filter for clothing/person items with confidence > 0.3
                        if conf > 0.3 and class_name.lower() in [cat.lower() for cat in self.clothing_categories]:
                            # Get bounding box
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            
                            # Skip very small detections
                            if (x2 - x1) < 20 or (y2 - y1) < 20:
                                continue
                            
                            # Extract region for color analysis (optimized)
                            region = opencv_image[y1:y2, x1:x2]
                            colors = self._analyze_region_colors(region)
                            
                            detection = {
                                'label': class_name,
                                'confidence': conf,
                                'bounding_box': {
                                    'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                                    'width': x2 - x1, 'height': y2 - y1
                                },
                                'colors': colors
                            }
                            detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"❌ Detection error: {e}")
            return []
    
    def _analyze_region_colors(self, region: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze colors in a specific region (optimized)"""
        try:
            if region.size == 0:
                return []
            
            # Resize region for faster processing
            height, width = region.shape[:2]
            if height > 100 or width > 100:
                scale = min(100/height, 100/width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                region = cv2.resize(region, (new_width, new_height))
            
            # Convert to RGB
            region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
            
            # Reshape for clustering
            pixels = region_rgb.reshape(-1, 3)
            
            # Sample pixels for faster processing
            if len(pixels) > 1000:
                indices = np.random.choice(len(pixels), 1000, replace=False)
                pixels = pixels[indices]
            
            # Simple color analysis - get dominant colors
            n_clusters = min(3, len(np.unique(pixels.reshape(-1, pixels.shape[-1]))))
            if n_clusters < 1:
                return []
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=3, max_iter=100)
            kmeans.fit(pixels)
            
            colors = []
            total_pixels = len(pixels)
            
            for i, center in enumerate(kmeans.cluster_centers_):
                # Calculate percentage
                cluster_size = np.sum(kmeans.labels_ == i)
                percentage = (cluster_size / total_pixels) * 100
                
                # Skip very small color regions
                if percentage < 15:
                    continue
                
                # Get color info
                rgb = center.astype(int)
                color_name = self._get_color_name(rgb)
                
                colors.append({
                    'name': color_name,
                    'rgb': rgb.tolist(),
                    'percentage': round(percentage, 1)
                })
            
            # Sort by percentage
            colors.sort(key=lambda x: x['percentage'], reverse=True)
            
            return colors
            
        except Exception as e:
            logger.error(f"❌ Color analysis error: {e}")
            return []
    
    def _get_color_name(self, rgb: np.ndarray) -> str:
        """Get color name from RGB values"""
        try:
            # Convert to closest named color
            min_colours = {}
            for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
                r_c, g_c, b_c = webcolors.hex_to_rgb(key)
                rd = (r_c - rgb[0]) ** 2
                gd = (g_c - rgb[1]) ** 2
                bd = (b_c - rgb[2]) ** 2
                min_colours[(rd + gd + bd)] = name
            
            closest_name = min_colours[min(min_colours.keys())]
            return closest_name
            
        except Exception as e:
            # Fallback to basic color names
            r, g, b = rgb
            if r > 200 and g > 200 and b > 200:
                return "white"
            elif r < 50 and g < 50 and b < 50:
                return "black"
            elif r > g and r > b:
                return "red"
            elif g > r and g > b:
                return "green"
            elif b > r and b > g:
                return "blue"
            else:
                return "mixed"