"""
👕 Clothing Detection with YOLO and SAM
Advanced clothing detection using YOLOv8 and Segment Anything Model
"""

import cv2
import numpy as np
import torch
from ultralytics import YOLO
from segment_anything import sam_model_registry, SamPredictor
import requests
import os
import logging
from typing import List, Dict, Any
from PIL import Image
import webcolors

logger = logging.getLogger(__name__)

class ClothingDetector:
    def __init__(self):
        """Initialize YOLO and SAM models"""
        self.yolo_model = None
        self.sam_model = None
        self.sam_predictor = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Clothing categories that YOLO can detect
        self.clothing_categories = [
            'person', 'shirt', 'pants', 'shoes', 'dress', 'jacket', 'coat',
            'hat', 'bag', 'tie', 'socks', 'gloves', 'scarf', 'belt',
            'skirt', 'shorts', 'sweater', 'hoodie', 'jeans', 'sneakers',
            'boots', 'sandals', 'backpack', 'handbag', 'sunglasses'
        ]
        
        self._load_models()
    
    def _load_models(self):
        """Load YOLO and SAM models"""
        try:
            # Load YOLO model
            logger.info("📦 Loading YOLO model...")
            self.yolo_model = YOLO('yolov8n.pt')  # nano version for faster inference
            logger.info("✅ YOLO model loaded")
            
            # Load SAM model
            logger.info("📦 Loading SAM model...")
            self._load_sam_model()
            logger.info("✅ SAM model loaded")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            raise
    
    def _load_sam_model(self):
        """Load SAM model"""
        try:
            # Download SAM model if not exists
            sam_checkpoint = "sam_vit_h_4b8939.pth"
            if not os.path.exists(sam_checkpoint):
                logger.info("📥 Downloading SAM model...")
                url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
                response = requests.get(url)
                with open(sam_checkpoint, 'wb') as f:
                    f.write(response.content)
                logger.info("✅ SAM model downloaded")
            
            # Load SAM model
            model_type = "vit_h"
            self.sam_model = sam_model_registry[model_type](checkpoint=sam_checkpoint)
            self.sam_model.to(device=self.device)
            self.sam_predictor = SamPredictor(self.sam_model)
            
        except Exception as e:
            logger.warning(f"⚠️ SAM model loading failed: {e}")
            # Continue without SAM - use YOLO only
            self.sam_model = None
            self.sam_predictor = None
    
    def detect_clothing(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Detect clothing items in an image"""
        try:
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Run YOLO detection
            results = self.yolo_model(opencv_image)
            
            detections = []
            person_detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        # Get detection info
                        conf = float(box.conf)
                        cls = int(box.cls)
                        class_name = self.yolo_model.names[cls]
                        
                        # Get bounding box
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        # Separate person detections from clothing detections
                        if class_name.lower() == 'person' and conf > 0.3:
                            person_detections.append({
                                'box': (x1, y1, x2, y2),
                                'confidence': conf
                            })
                        elif class_name.lower() in [cat.lower() for cat in self.clothing_categories] and class_name.lower() != 'person':
                            # Extract region for color analysis
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
            
            # If no specific clothing items detected but person detected, analyze person regions
            if not detections and person_detections:
                for person in person_detections:
                    x1, y1, x2, y2 = person['box']
                    
                    # Analyze different regions of the person for clothing
                    height = y2 - y1
                    width = x2 - x1
                    
                    # Upper body region (shirt/top)
                    upper_y1 = y1
                    upper_y2 = y1 + int(height * 0.6)
                    upper_region = opencv_image[upper_y1:upper_y2, x1:x2]
                    upper_colors = self._analyze_region_colors(upper_region)
                    
                    if upper_colors:
                        detections.append({
                            'label': 'shirt',  # Default to shirt for upper body
                            'confidence': person['confidence'] * 0.8,  # Slightly lower confidence
                            'bounding_box': {
                                'x1': x1, 'y1': upper_y1, 'x2': x2, 'y2': upper_y2,
                                'width': width, 'height': upper_y2 - upper_y1
                            },
                            'colors': upper_colors
                        })
                    
                    # Lower body region (pants/bottom)
                    lower_y1 = y1 + int(height * 0.4)
                    lower_y2 = y2
                    lower_region = opencv_image[lower_y1:lower_y2, x1:x2]
                    lower_colors = self._analyze_region_colors(lower_region)
                    
                    if lower_colors:
                        detections.append({
                            'label': 'pants',  # Default to pants for lower body
                            'confidence': person['confidence'] * 0.8,  # Slightly lower confidence
                            'bounding_box': {
                                'x1': x1, 'y1': lower_y1, 'x2': x2, 'y2': lower_y2,
                                'width': width, 'height': lower_y2 - lower_y1
                            },
                            'colors': lower_colors
                        })
            
            return detections
            
        except Exception as e:
            logger.error(f"❌ Detection error: {e}")
            return []
    
    def _analyze_region_colors(self, region: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze colors in a specific region"""
        try:
            if region.size == 0:
                return []
            
            # Convert to RGB
            region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
            
            # Reshape for clustering
            pixels = region_rgb.reshape(-1, 3)
            
            # Simple color analysis - get dominant colors
            from sklearn.cluster import KMeans
            
            # Use fewer clusters for clothing items
            n_clusters = min(3, len(np.unique(pixels.reshape(-1, pixels.shape[-1]))))
            if n_clusters < 1:
                return []
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = []
            total_pixels = len(pixels)
            
            for i, center in enumerate(kmeans.cluster_centers_):
                # Calculate percentage
                cluster_size = np.sum(kmeans.labels_ == i)
                percentage = (cluster_size / total_pixels) * 100
                
                # Get color info
                rgb = center.astype(int)
                color_name = self._get_color_name(rgb)
                
                colors.append({
                    'name': color_name,
                    'rgb': rgb.tolist(),
                    'percentage': percentage
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
            elif r > 150 and g > 150 and b < 100:
                return "yellow"
            elif r > 150 and g < 100 and b > 150:
                return "magenta"
            elif r < 100 and g > 150 and b > 150:
                return "cyan"
            elif r > 150 and g < 150 and b < 150:
                return "orange"
            elif r < 150 and g > 150 and b < 150:
                return "lime"
            elif r < 150 and g < 150 and b > 150:
                return "navy"
            else:
                # Instead of "mixed", return a more specific color based on dominant channel
                if r > g and r > b:
                    return "red"
                elif g > r and g > b:
                    return "green"
                elif b > r and b > g:
                    return "blue"
                else:
                    return "gray"