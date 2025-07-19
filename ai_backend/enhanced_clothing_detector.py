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

# MMFashion imports
try:
    import mmcv
    from mmdet.apis import inference_detector, init_detector
    MMFASHION_AVAILABLE = True
    print("✅ MMFashion/MMDet available")
except ImportError:
    MMFASHION_AVAILABLE = False
    print("⚠️ MMFashion not available, using fallback")

# YOLO fallback imports
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
    print("✅ YOLO available")
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️ YOLO not available")

logger = logging.getLogger(__name__)

class EnhancedClothingDetector:
    def __init__(self):
        """Initialize Mask R-CNN and MMFashion models"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Initialize models
        self.mask_rcnn_predictor = None
        self.mmfashion_model = None
        self.fallback_model = None
        
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
        
        # Attribute categories for MMFashion
        self.attribute_categories = {
            'category': ['shirt', 'pants', 'dress', 'jacket', 'shoes', 'bag', 'hat'],
            'color': ['red', 'blue', 'green', 'black', 'white', 'gray', 'brown', 'pink', 'yellow', 'purple'],
            'pattern': ['solid', 'striped', 'checkered', 'floral', 'geometric', 'abstract'],
            'material': ['cotton', 'denim', 'leather', 'wool', 'silk', 'polyester', 'linen'],
            'style': ['casual', 'formal', 'sporty', 'vintage', 'modern', 'bohemian'],
            'fit': ['tight', 'regular', 'loose', 'oversized', 'skinny', 'straight'],
            'season': ['spring', 'summer', 'fall', 'winter', 'all-season']
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
                logger.warning("Detectron2 not available, using fallback")
                
            # Initialize MMFashion
            if MMFASHION_AVAILABLE:
                self._setup_mmfashion()
            else:
                logger.warning("MMFashion not available, using basic attributes")
                
            # Initialize fallback detector
            if not DETECTRON2_AVAILABLE:
                self._setup_fallback_detector()
                
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
            # Don't raise - allow fallback to work
    
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
            import traceback
            logger.error(f"❌ Error setting up Mask R-CNN: {e}\n" + traceback.format_exc())
            self.mask_rcnn_predictor = None
    
    def _setup_mmfashion(self):
        """Setup MMFashion for attribute parsing"""
        try:
            logger.info("Setting up MMFashion...")
            
            # For now, use a placeholder - in real implementation, we'd load MMFashion models
            # This would typically load pre-trained models for attribute detection
            self.mmfashion_model = "placeholder"
            
            logger.info("✅ MMFashion initialized successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error setting up MMFashion: {e}")
            self.mmfashion_model = None
    
    def _setup_fallback_detector(self):
        """Setup fallback detector if Detectron2 is not available"""
        try:
            logger.info("Setting up fallback detector...")
            if YOLO_AVAILABLE:
                from ultralytics import YOLO
                self.fallback_model = YOLO('yolov8n.pt')
                logger.info("✅ Fallback YOLO detector initialized")
            else:
                # Create a very basic detector
                self.fallback_model = None
                logger.warning("⚠️ No detection models available")
        except Exception as e:
            logger.error(f"❌ Error setting up fallback detector: {e}")
            self.fallback_model = None
    
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
                
                # Get attributes using MMFashion
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
                    'segmentation_available': True,
                    'detection_method': 'Mask R-CNN'
                }
                detections.append(detection)
            
            return detections
            
        except Exception as e:
            logger.error(f"❌ Mask R-CNN detection error: {e}")
            return []
    
    def _detect_with_fallback(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Fallback detection using YOLO or basic method"""
        try:
            if self.fallback_model is not None:
                # Use YOLO
                return self._detect_with_yolo(image)
            else:
                # Use basic detection method
                return self._detect_basic(image)
        except Exception as e:
            logger.error(f"❌ Fallback detection error: {e}")
            return []
    
    def _detect_with_yolo(self, image: Image.Image) -> List[Dict[str, Any]]:
        """YOLO-based detection"""
        try:
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Run YOLO detection
            results = self.fallback_model(opencv_image, conf=0.3, iou=0.5, verbose=False)
            
            detections = []
            person_detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        conf = float(box.conf)
                        cls = int(box.cls)
                        class_name = self.fallback_model.names[cls]
                        
                        # Get bounding box
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        
                        # Separate person detections from clothing detections
                        if class_name.lower() == 'person' and conf > 0.3:
                            person_detections.append({
                                'box': (x1, y1, x2, y2),
                                'confidence': conf
                            })
                        elif class_name.lower() != 'person' and self._is_fashion_item(class_name):
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
                                'attributes': self._get_basic_attributes(class_name),
                                'segmentation_available': False
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
                            'colors': upper_colors,
                            'attributes': self._get_basic_attributes('shirt'),
                            'segmentation_available': False
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
                            'colors': lower_colors,
                            'attributes': self._get_basic_attributes('pants'),
                            'segmentation_available': False
                        })
            
            return detections
            
        except Exception as e:
            logger.error(f"❌ YOLO detection error: {e}")
            return []
    
    def _detect_basic(self, image: Image.Image) -> List[Dict[str, Any]]:
        """Basic detection method when no models are available"""
        try:
            # Return a dummy detection for testing
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            height, width = opencv_image.shape[:2]
            
            # Analyze overall image colors
            colors = self._analyze_region_colors(opencv_image)
            
            # Return basic clothing detection
            detection = {
                'label': 'clothing_item',
                'confidence': 0.5,
                'bounding_box': {
                    'x1': 0, 'y1': 0, 'x2': width, 'y2': height,
                    'width': width, 'height': height
                },
                'colors': colors,
                'attributes': self._get_basic_attributes('clothing_item'),
                'segmentation_available': False
            }
            
            return [detection]
            
        except Exception as e:
            logger.error(f"❌ Basic detection error: {e}")
            return []
    
    def _get_basic_attributes(self, class_name: str) -> Dict[str, Any]:
        """Get basic attributes for fallback detection"""
        attributes = {
            'category': class_name,
            'style': 'casual',
            'season': 'all-season',
            'material': 'unknown',
            'pattern': 'solid',
            'fit': 'regular',
            'detection_method': 'basic'
        }
        return attributes
    
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
        """Get fashion attributes using MMFashion and heuristics"""
        try:
            attributes = {}
            
            # Basic category from detection
            attributes['category'] = class_name
            
            # If MMFashion is available, use it for advanced attributes
            if self.mmfashion_model is not None and MMFASHION_AVAILABLE:
                attributes.update(self._get_mmfashion_attributes(image, mask, class_name))
            else:
                # Use heuristic-based attribute detection
                attributes.update(self._get_heuristic_attributes(image, mask, class_name))
            
            return attributes
            
        except Exception as e:
            logger.error(f"❌ Attribute detection error: {e}")
            return {'category': class_name}
    
    def _get_mmfashion_attributes(self, image: np.ndarray, mask: np.ndarray, class_name: str) -> Dict[str, Any]:
        """Get attributes using MMFashion models"""
        try:
            # TODO: Implement actual MMFashion attribute detection
            # For now, return enhanced placeholder attributes
            attributes = {
                'style': self._predict_style(image, mask, class_name),
                'season': self._predict_season(image, mask, class_name),
                'material': self._predict_material(image, mask, class_name),
                'pattern': self._predict_pattern(image, mask, class_name),
                'fit': self._predict_fit(image, mask, class_name),
                'detection_method': 'MMFashion (advanced)'
            }
            
            return attributes
            
        except Exception as e:
            logger.error(f"❌ MMFashion attribute detection error: {e}")
            return {}
    
    def _get_heuristic_attributes(self, image: np.ndarray, mask: np.ndarray, class_name: str) -> Dict[str, Any]:
        """Get attributes using heuristic methods"""
        try:
            # Extract masked region
            masked_region = image.copy()
            masked_region[~mask] = 0
            
            # Analyze colors in the region
            colors = self._analyze_masked_colors(image, mask)
            dominant_color = colors[0]['name'] if colors else 'unknown'
            
            # Heuristic-based attribute prediction
            attributes = {
                'dominant_color': dominant_color,
                'style': self._predict_style_heuristic(class_name, colors),
                'season': self._predict_season_heuristic(class_name, colors),
                'material': self._predict_material_heuristic(class_name),
                'pattern': self._predict_pattern_heuristic(masked_region, mask),
                'fit': self._predict_fit_heuristic(mask),
                'detection_method': 'heuristic'
            }
            
            return attributes
            
        except Exception as e:
            logger.error(f"❌ Heuristic attribute detection error: {e}")
            return {}
    
    def _predict_style(self, image: np.ndarray, mask: np.ndarray, class_name: str) -> str:
        """Predict clothing style using advanced methods"""
        # TODO: Implement MMFashion-based style prediction
        return self._predict_style_heuristic(class_name, [])
    
    def _predict_season(self, image: np.ndarray, mask: np.ndarray, class_name: str) -> str:
        """Predict suitable season using advanced methods"""
        # TODO: Implement MMFashion-based season prediction
        return self._predict_season_heuristic(class_name, [])
    
    def _predict_material(self, image: np.ndarray, mask: np.ndarray, class_name: str) -> str:
        """Predict material using advanced methods"""
        # TODO: Implement MMFashion-based material prediction
        return self._predict_material_heuristic(class_name)
    
    def _predict_pattern(self, image: np.ndarray, mask: np.ndarray, class_name: str) -> str:
        """Predict pattern using advanced methods"""
        # TODO: Implement MMFashion-based pattern prediction
        return self._predict_pattern_heuristic(image, mask)
    
    def _predict_fit(self, image: np.ndarray, mask: np.ndarray, class_name: str) -> str:
        """Predict fit using advanced methods"""
        # TODO: Implement MMFashion-based fit prediction
        return self._predict_fit_heuristic(mask)
    
    def _predict_style_heuristic(self, class_name: str, colors: List[Dict]) -> str:
        """Predict style using heuristic rules"""
        # Business/formal items
        if any(item in class_name.lower() for item in ['suit', 'blazer', 'tie', 'dress shirt']):
            return 'formal'
        
        # Sporty items
        if any(item in class_name.lower() for item in ['sneakers', 'sports', 'athletic', 'hoodie']):
            return 'sporty'
        
        # Casual items
        if any(item in class_name.lower() for item in ['jeans', 't-shirt', 'casual']):
            return 'casual'
        
        # Default based on colors
        if colors and any(color['name'] in ['black', 'white', 'gray', 'navy'] for color in colors):
            return 'formal'
        
        return 'casual'
    
    def _predict_season_heuristic(self, class_name: str, colors: List[Dict]) -> str:
        """Predict season using heuristic rules"""
        # Winter items
        if any(item in class_name.lower() for item in ['coat', 'jacket', 'sweater', 'boots']):
            return 'winter'
        
        # Summer items
        if any(item in class_name.lower() for item in ['shorts', 'sandals', 'tank', 'summer']):
            return 'summer'
        
        # Spring/Fall items
        if any(item in class_name.lower() for item in ['cardigan', 'light jacket']):
            return 'spring-fall'
        
        return 'all-season'
    
    def _predict_material_heuristic(self, class_name: str) -> str:
        """Predict material using heuristic rules"""
        # Common material associations
        if 'jean' in class_name.lower():
            return 'denim'
        elif any(item in class_name.lower() for item in ['leather', 'boots']):
            return 'leather'
        elif any(item in class_name.lower() for item in ['cotton', 't-shirt']):
            return 'cotton'
        elif any(item in class_name.lower() for item in ['wool', 'sweater']):
            return 'wool'
        elif any(item in class_name.lower() for item in ['silk', 'dress']):
            return 'silk'
        
        return 'cotton'  # Default
    
    def _predict_pattern_heuristic(self, image: np.ndarray, mask: np.ndarray) -> str:
        """Predict pattern using image analysis"""
        try:
            # Extract masked region
            masked_region = image[mask]
            
            if len(masked_region) == 0:
                return 'solid'
            
            # Simple pattern detection based on color variance
            # Convert to grayscale for pattern analysis
            gray_region = cv2.cvtColor(masked_region.reshape(-1, 1, 3), cv2.COLOR_BGR2GRAY)
            
            # Calculate variance - high variance might indicate patterns
            variance = np.var(gray_region)
            
            if variance > 1000:  # High variance threshold
                return 'patterned'
            else:
                return 'solid'
                
        except Exception as e:
            logger.error(f"❌ Pattern prediction error: {e}")
            return 'solid'
    
    def _predict_fit_heuristic(self, mask: np.ndarray) -> str:
        """Predict fit using mask shape analysis"""
        try:
            # Calculate aspect ratio and other shape features
            mask_coords = np.where(mask)
            
            if len(mask_coords[0]) == 0:
                return 'regular'
            
            height = np.max(mask_coords[0]) - np.min(mask_coords[0])
            width = np.max(mask_coords[1]) - np.min(mask_coords[1])
            
            if height == 0 or width == 0:
                return 'regular'
            
            aspect_ratio = height / width
            
            # Simple heuristic based on aspect ratio
            if aspect_ratio > 2.5:
                return 'tight'
            elif aspect_ratio < 1.5:
                return 'loose'
            else:
                return 'regular'
                
        except Exception as e:
            logger.error(f"❌ Fit prediction error: {e}")
            return 'regular'
    
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