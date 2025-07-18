"""
🚀 Enhanced Clothing Detection with Mask R-CNN + MMFashion
Advanced clothing detection using Detectron2 Mask R-CNN and MMFashion for attributes
"""

import cv2
import numpy as np
import torch
from PIL import Image
import logging
from typing import List, Dict, Any, Optional
import webcolors
from sklearn.cluster import KMeans
import requests
import os

# Detectron2 imports
try:
    import detectron2
    from detectron2.engine import DefaultPredictor
    from detectron2.config import get_cfg
    from detectron2 import model_zoo
    from detectron2.utils.visualizer import Visualizer
    from detectron2.data import MetadataCatalog
    DETECTRON2_AVAILABLE = True
    print("✅ Detectron2 available")
except ImportError:
    DETECTRON2_AVAILABLE = False
    print("⚠️ Detectron2 not available, using fallback")

# YOLO fallback imports
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

logger = logging.getLogger(__name__)

class EnhancedClothingDetector:
    def __init__(self):
        """Initialize Mask R-CNN and MMFashion models"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Initialize Mask R-CNN
        self.mask_rcnn_predictor = None
        self.mmfashion_model = None
        
        # Fashion-specific classes mapping
        self.fashion_classes = {
            'person': 0,
            'shirt': 1,
            'pants': 2,
            'dress': 3,
            'jacket': 4,
            'shoes': 5,
            'bag': 6,
            'hat': 7,
            'skirt': 8,
            'shorts': 9,
            'coat': 10,
            'hoodie': 11,
            'sweater': 12,
            'jeans': 13,
            'boots': 14,
            'sneakers': 15,
            'sandals': 16,
            't-shirt': 17,
            'blouse': 18,
            'blazer': 19
        }
        
        # Color analysis thresholds
        self.color_threshold = 0.05  # 5% minimum for color consideration
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize Mask R-CNN and MMFashion models"""
        try:
            # Initialize Mask R-CNN
            if DETECTRON2_AVAILABLE:
                self._setup_mask_rcnn()
            else:
                logger.warning("Detectron2 not available, falling back to YOLO")
                self._setup_fallback_detector()
                
            # Initialize MMFashion (will implement after Mask R-CNN is working)
            self._setup_mmfashion()
            
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
            raise
    
    def _setup_mask_rcnn(self):
        """Setup Mask R-CNN with fashion-optimized config"""
        try:
            logger.info("Setting up Mask R-CNN...")
            
            # Get configuration
            cfg = get_cfg()
            cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
            
            # Use COCO pretrained weights (we'll fine-tune for fashion later)
            cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
            
            # Set device
            cfg.MODEL.DEVICE = str(self.device)
            
            # Adjust for fashion detection
            cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.3  # Lower threshold for fashion items
            cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST = 0.4   # Non-maximum suppression threshold
            
            # Create predictor
            self.mask_rcnn_predictor = DefaultPredictor(cfg)
            logger.info("✅ Mask R-CNN initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error setting up Mask R-CNN: {e}")
            raise
    
    def _setup_fallback_detector(self):
        """Setup fallback detector if Detectron2 is not available"""
        try:
            logger.info("Setting up fallback detector...")
            from ultralytics import YOLO
            self.fallback_model = YOLO('yolov8n.pt')
            logger.info("✅ Fallback YOLO detector initialized")
        except Exception as e:
            logger.error(f"❌ Error setting up fallback detector: {e}")
            raise
    
    def _setup_mmfashion(self):
        """Setup MMFashion for attribute parsing"""
        try:
            logger.info("Setting up MMFashion...")
            # TODO: Implement MMFashion setup
            # For now, we'll use a placeholder
            self.mmfashion_model = None
            logger.info("✅ MMFashion placeholder initialized")
        except Exception as e:
            logger.error(f"❌ Error setting up MMFashion: {e}")
            # Non-fatal error, continue without MMFashion
    
    def detect_clothing(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Detect clothing items with enhanced segmentation"""
        try:
            if self.mask_rcnn_predictor is not None:
                return self._detect_with_mask_rcnn(image)
            else:
                return self._detect_with_fallback(image)
        except Exception as e:
            logger.error(f"❌ Detection error: {e}")
            return []
    
    def _detect_with_mask_rcnn(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Detect clothing using Mask R-CNN"""
        try:
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Run Mask R-CNN detection
            outputs = self.mask_rcnn_predictor(opencv_image)
            
            # Extract instances
            instances = outputs["instances"]
            
            detections = []
            for i in range(len(instances)):
                # Get basic info
                score = float(instances.scores[i])
                class_id = int(instances.pred_classes[i])
                class_name = self._get_class_name(class_id)
                
                # Filter for fashion-related items
                if not self._is_fashion_item(class_name):
                    continue
                    
                # Get bounding box
                bbox = instances.pred_boxes[i].tensor[0].cpu().numpy()
                x1, y1, x2, y2 = map(int, bbox)
                
                # Get segmentation mask
                mask = instances.pred_masks[i].cpu().numpy()
                
                # Calculate mask area and color analysis
                mask_area = np.sum(mask)
                if mask_area < 100:  # Skip very small masks
                    continue
                
                # Extract colors using mask
                colors = self._analyze_masked_colors(opencv_image, mask)
                
                # Get attributes (placeholder for now)
                attributes = self._get_fashion_attributes(opencv_image, mask, class_name)
                
                detection = {
                    'label': class_name,
                    'confidence': score,
                    'bounding_box': {
                        'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                        'width': x2 - x1, 'height': y2 - y1
                    },
                    'mask_area': int(mask_area),
                    'colors': colors,
                    'attributes': attributes,
                    'segmentation_available': True
                }
                detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"❌ Mask R-CNN detection error: {e}")
            return []
    
    def _detect_with_fallback(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Fallback detection using YOLO"""
        try:
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Run YOLO detection
            results = self.fallback_model(opencv_image, conf=0.3, iou=0.5, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        conf = float(box.conf)
                        cls = int(box.cls)
                        class_name = self.fallback_model.names[cls]
                        
                        # Filter for fashion items
                        if not self._is_fashion_item(class_name):
                            continue
                        
                        # Get bounding box
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
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
                            'colors': colors,
                            'attributes': {},
                            'segmentation_available': False
                        }
                        detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"❌ Fallback detection error: {e}")
            return []
    
    def _analyze_masked_colors(self, image: np.ndarray, mask: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze colors within a segmentation mask"""
        try:
            # Apply mask to image
            masked_image = image.copy()
            masked_image[~mask] = 0
            
            # Get only the pixels within the mask
            mask_pixels = image[mask]
            
            if len(mask_pixels) == 0:
                return []
            
            # Convert to RGB
            mask_pixels_rgb = cv2.cvtColor(mask_pixels.reshape(-1, 1, 3), cv2.COLOR_BGR2RGB).reshape(-1, 3)
            
            # Perform color clustering
            n_clusters = min(5, len(np.unique(mask_pixels_rgb.reshape(-1, mask_pixels_rgb.shape[-1]))))
            if n_clusters < 1:
                return []
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(mask_pixels_rgb)
            
            colors = []
            total_pixels = len(mask_pixels_rgb)
            
            for i, center in enumerate(kmeans.cluster_centers_):
                # Calculate percentage
                cluster_size = np.sum(kmeans.labels_ == i)
                percentage = (cluster_size / total_pixels) * 100
                
                # Skip very small color regions
                if percentage < 5:
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
            logger.error(f"❌ Masked color analysis error: {e}")
            return []
    
    def _analyze_region_colors(self, region: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze colors in a region (fallback method)"""
        try:
            if region.size == 0:
                return []
            
            # Convert to RGB
            region_rgb = cv2.cvtColor(region, cv2.COLOR_BGR2RGB)
            
            # Reshape for clustering
            pixels = region_rgb.reshape(-1, 3)
            
            # Sample pixels for faster processing
            if len(pixels) > 1000:
                indices = np.random.choice(len(pixels), 1000, replace=False)
                pixels = pixels[indices]
            
            # Perform clustering
            n_clusters = min(3, len(np.unique(pixels.reshape(-1, pixels.shape[-1]))))
            if n_clusters < 1:
                return []
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = []
            total_pixels = len(pixels)
            
            for i, center in enumerate(kmeans.cluster_centers_):
                cluster_size = np.sum(kmeans.labels_ == i)
                percentage = (cluster_size / total_pixels) * 100
                
                if percentage < 10:
                    continue
                
                rgb = center.astype(int)
                color_name = self._get_color_name(rgb)
                
                colors.append({
                    'name': color_name,
                    'rgb': rgb.tolist(),
                    'percentage': round(percentage, 1)
                })
            
            colors.sort(key=lambda x: x['percentage'], reverse=True)
            return colors
            
        except Exception as e:
            logger.error(f"❌ Region color analysis error: {e}")
            return []
    
    def _get_fashion_attributes(self, image: np.ndarray, mask: np.ndarray, class_name: str) -> Dict[str, Any]:
        """Get fashion attributes using MMFashion (placeholder)"""
        try:
            # TODO: Implement MMFashion attribute detection
            # For now, return basic attributes based on class
            attributes = {
                'category': class_name,
                'style': 'casual',  # placeholder
                'season': 'all-season',  # placeholder
                'material': 'unknown',  # placeholder
                'pattern': 'solid',  # placeholder
                'fit': 'regular'  # placeholder
            }
            
            return attributes
            
        except Exception as e:
            logger.error(f"❌ Attribute detection error: {e}")
            return {}
    
    def _is_fashion_item(self, class_name: str) -> bool:
        """Check if detected item is fashion-related"""
        fashion_keywords = [
            'person', 'shirt', 'pants', 'dress', 'jacket', 'shoes', 'bag', 'hat',
            'skirt', 'shorts', 'coat', 'hoodie', 'sweater', 'jeans', 'boots',
            'sneakers', 'sandals', 't-shirt', 'blouse', 'blazer', 'tie', 'socks',
            'gloves', 'scarf', 'belt', 'backpack', 'handbag', 'sunglasses'
        ]
        
        return any(keyword in class_name.lower() for keyword in fashion_keywords)
    
    def _get_class_name(self, class_id: int) -> str:
        """Get class name from COCO class ID"""
        # COCO class names (relevant to fashion)
        coco_classes = {
            0: 'person',
            26: 'handbag',
            27: 'tie',
            28: 'suitcase',
            32: 'sports ball',
            67: 'dining table',
            # Add more relevant mappings
        }
        
        return coco_classes.get(class_id, f'class_{class_id}')
    
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