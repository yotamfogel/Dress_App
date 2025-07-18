"""
🎯 Enhanced Fashion Classification System
Advanced clothing type and style classification with color analysis
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

# Import existing modules
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

logger = logging.getLogger(__name__)

class FashionClassificationSystem:
    def __init__(self):
        """Initialize the Fashion Classification System"""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Initialize YOLO model
        self.yolo_model = None
        if YOLO_AVAILABLE:
            self._setup_yolo()
        
        # Define clothing type mappings
        self.clothing_types = {
            # Tops
            't-shirt': ['t-shirt', 'tee', 'tank', 'tank top', 'basic tee'],
            'button-shirt': ['button-up', 'dress shirt', 'button shirt', 'formal shirt'],
            'polo': ['polo shirt', 'polo', 'collared shirt'],
            'hoodie': ['hoodie', 'sweatshirt', 'pullover'],
            'sweater': ['sweater', 'jumper', 'cardigan', 'knitwear'],
            'blazer': ['blazer', 'sport coat', 'suit jacket'],
            'jacket': ['jacket', 'coat', 'outerwear'],
            'blouse': ['blouse', 'silk shirt', 'dressy top'],
            'crop-top': ['crop top', 'cropped shirt', 'belly shirt'],
            'tube-top': ['tube top', 'bandeau', 'strapless top'],
            
            # Bottoms
            'jeans': ['jeans', 'denim pants', 'blue jeans'],
            'cargo-pants': ['cargo pants', 'utility pants', 'tactical pants'],
            'dress-pants': ['dress pants', 'slacks', 'trousers', 'formal pants'],
            'chinos': ['chinos', 'khakis', 'casual pants'],
            'shorts': ['shorts', 'short pants'],
            'cargo-shorts': ['cargo shorts', 'utility shorts'],
            'skirt': ['skirt', 'mini skirt', 'maxi skirt', 'pencil skirt'],
            'leggings': ['leggings', 'tights', 'yoga pants'],
            'joggers': ['joggers', 'track pants', 'sweatpants'],
            
            # Dresses
            'dress': ['dress', 'gown', 'frock'],
            'maxi-dress': ['maxi dress', 'long dress'],
            'mini-dress': ['mini dress', 'short dress'],
            'cocktail-dress': ['cocktail dress', 'party dress'],
            
            # Footwear
            'sneakers': ['sneakers', 'trainers', 'athletic shoes'],
            'boots': ['boots', 'ankle boots', 'combat boots'],
            'loafers': ['loafers', 'slip-on shoes', 'moccasins'],
            'heels': ['high heels', 'pumps', 'stilettos'],
            'sandals': ['sandals', 'flip-flops', 'slides'],
            
            # Accessories
            'hat': ['hat', 'cap', 'beanie', 'baseball cap'],
            'bag': ['bag', 'handbag', 'purse', 'backpack'],
            'belt': ['belt', 'waist belt', 'leather belt']
        }
        
        # Define style classifications
        self.style_mappings = {
            'casual': [
                't-shirt', 'jeans', 'hoodie', 'sneakers', 'shorts', 'cargo-shorts',
                'joggers', 'tank-top', 'polo', 'chinos', 'sandals', 'cap'
            ],
            'classy-elegant': [
                'blazer', 'dress-pants', 'button-shirt', 'blouse', 'pencil-skirt',
                'cocktail-dress', 'heels', 'loafers', 'silk-blouse', 'tailored-pants'
            ],
            'business-office': [
                'blazer', 'dress-pants', 'button-shirt', 'blouse', 'suit-jacket',
                'formal-shirt', 'pencil-skirt', 'dress-shoes', 'briefcase'
            ],
            'business-casual': [
                'chinos', 'loafers', 'cardigan', 'polo', 'blouse', 'khakis',
                'casual-blazer', 'dress-pants', 'button-shirt'
            ],
            'streetwear': [
                't-shirt', 'hoodie', 'sneakers', 'cap', 'graphic-tee', 'joggers',
                'track-jacket', 'oversized-hoodie', 'basketball-shorts'
            ],
            'athleisure': [
                'leggings', 'joggers', 'track-jacket', 'athletic-shoes', 'sports-bra',
                'tank-top', 'sweatshirt', 'running-shoes', 'yoga-pants'
            ],
            'bohemian': [
                'maxi-dress', 'flowy-dress', 'peasant-blouse', 'fringe-jacket',
                'sandals', 'wide-leg-pants', 'crochet-top', 'earthy-tones'
            ],
            'minimalist': [
                'simple-tee', 'straight-pants', 'clean-blazer', 'white-shirt',
                'black-pants', 'neutral-dress', 'simple-sneakers'
            ],
            'preppy': [
                'polo', 'pleated-skirt', 'loafers', 'cardigan', 'khakis',
                'button-down', 'tennis-shoes', 'blazer'
            ],
            'grunge': [
                'flannel', 'ripped-jeans', 'band-tee', 'combat-boots',
                'leather-jacket', 'torn-pants', 'oversized-shirt'
            ],
            'vintage-retro': [
                'vintage-dress', 'flare-jeans', 'retro-tee', 'vintage-jacket',
                'classic-sneakers', 'mom-jeans', 'vintage-blouse'
            ],
            'y2k': [
                'baby-tee', 'low-rise-jeans', 'platform-shoes', 'metallic-top',
                'mini-skirt', 'sparkly-accessories', 'crop-top'
            ],
            'edgy-punk': [
                'leather-jacket', 'ripped-jeans', 'studded-belt', 'combat-boots',
                'band-tee', 'plaid-pants', 'spiked-accessories'
            ],
            'goth': [
                'black-dress', 'corset', 'platform-boots', 'black-lace',
                'dark-makeup', 'black-jacket', 'gothic-accessories'
            ],
            'chic': [
                'tailored-blazer', 'high-quality-jeans', 'silk-blouse', 'designer-bag',
                'stylish-heels', 'trendy-dress', 'fashion-forward-pieces'
            ],
            'romantic': [
                'floral-dress', 'ruffled-blouse', 'pastel-colors', 'lace-top',
                'flowing-skirt', 'delicate-jewelry', 'soft-cardigan'
            ],
            'cottagecore': [
                'flowy-dress', 'puff-sleeves', 'apron', 'peasant-blouse',
                'midi-skirt', 'cardigans', 'vintage-inspired'
            ],
            'artsy-eclectic': [
                'colorful-prints', 'unusual-silhouettes', 'bold-patterns',
                'artistic-pieces', 'unique-combinations', 'statement-pieces'
            ],
            'avant-garde': [
                'architectural-shapes', 'asymmetrical-pieces', 'experimental-design',
                'unconventional-silhouettes', 'futuristic-elements'
            ],
            'resort-cruise': [
                'linen-sets', 'kaftans', 'straw-hats', 'flowy-pants',
                'beach-dress', 'sandals', 'light-fabrics'
            ],
            'evening-formal': [
                'gown', 'tuxedo', 'cocktail-dress', 'formal-suit',
                'dress-shoes', 'elegant-heels', 'formal-accessories'
            ]
        }
        
        # Initialize color analyzer
        self.color_threshold = 0.05  # 5% minimum for color consideration
        
    def _setup_yolo(self):
        """Setup YOLO model for clothing detection"""
        try:
            logger.info("Setting up YOLO model...")
            self.yolo_model = YOLO('yolov8n.pt')
            logger.info("✅ YOLO model loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Error loading YOLO model: {e}")
            self.yolo_model = None
    
    def analyze_clothing_image(self, image: Image.Image) -> Dict[str, Any]:
        """
        Complete clothing analysis including type, style, and colors
        """
        try:
            # Convert PIL to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Step 1: Detect clothing items
            detected_items = self._detect_clothing_items(opencv_image)
            
            # Step 2: Check for multiple items
            if len(detected_items) > 1:
                return {
                    'success': True,
                    'multiple_items': True,
                    'items': detected_items,
                    'message': 'Multiple clothing items detected. Please specify which item you want to analyze.',
                    'instruction': 'Please respond with the number of the item you want to analyze.'
                }
            
            # Step 3: Single item analysis
            if len(detected_items) == 1:
                item = detected_items[0]
                detailed_analysis = self._analyze_single_item(opencv_image, item)
                return {
                    'success': True,
                    'multiple_items': False,
                    'analysis': detailed_analysis
                }
            
            # Step 4: No specific items detected, analyze whole image
            whole_image_analysis = self._analyze_whole_image(opencv_image)
            return {
                'success': True,
                'multiple_items': False,
                'analysis': whole_image_analysis
            }
            
        except Exception as e:
            logger.error(f"❌ Clothing analysis error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _detect_clothing_items(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Detect clothing items in the image"""
        detected_items = []
        
        if self.yolo_model is not None:
            try:
                # Run YOLO detection
                results = self.yolo_model(image, conf=0.3, iou=0.5, verbose=False)
                
                item_count = 0
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            conf = float(box.conf)
                            cls = int(box.cls)
                            class_name = self.yolo_model.names[cls]
                            
                            # Filter for clothing items
                            if self._is_clothing_item(class_name) and conf > 0.3:
                                x1, y1, x2, y2 = map(int, box.xyxy[0])
                                
                                # Skip very small detections
                                if (x2 - x1) < 30 or (y2 - y1) < 30:
                                    continue
                                
                                item_count += 1
                                detected_items.append({
                                    'id': item_count,
                                    'label': class_name,
                                    'confidence': conf,
                                    'bounding_box': {
                                        'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                                        'width': x2 - x1, 'height': y2 - y1
                                    }
                                })
                
            except Exception as e:
                logger.error(f"❌ YOLO detection error: {e}")
        
        return detected_items
    
    def _analyze_single_item(self, image: np.ndarray, item: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single clothing item"""
        try:
            # Extract item region
            bbox = item['bounding_box']
            x1, y1, x2, y2 = bbox['x1'], bbox['y1'], bbox['x2'], bbox['y2']
            item_region = image[y1:y2, x1:x2]
            
            # Classify clothing type
            clothing_type = self._classify_clothing_type(item['label'])
            
            # Determine applicable styles
            applicable_styles = self._get_applicable_styles(clothing_type)
            
            # Analyze colors
            colors = self._analyze_colors(item_region)
            
            return {
                'clothing_type': clothing_type,
                'detected_as': item['label'],
                'confidence': item['confidence'],
                'applicable_styles': applicable_styles,
                'colors': colors,
                'color_description': self._generate_color_description(colors)
            }
            
        except Exception as e:
            logger.error(f"❌ Single item analysis error: {e}")
            return {
                'clothing_type': 'unknown',
                'applicable_styles': [],
                'colors': [],
                'error': str(e)
            }
    
    def _analyze_whole_image(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze the whole image when no specific items are detected"""
        try:
            # Analyze colors of the whole image
            colors = self._analyze_colors(image)
            
            # Try to infer clothing type from image characteristics
            inferred_type = self._infer_clothing_type(image)
            
            # Get applicable styles
            applicable_styles = self._get_applicable_styles(inferred_type)
            
            return {
                'clothing_type': inferred_type,
                'detected_as': 'whole_image_analysis',
                'confidence': 0.5,
                'applicable_styles': applicable_styles,
                'colors': colors,
                'color_description': self._generate_color_description(colors),
                'note': 'Analysis based on whole image as no specific clothing items were detected'
            }
            
        except Exception as e:
            logger.error(f"❌ Whole image analysis error: {e}")
            return {
                'clothing_type': 'unknown',
                'applicable_styles': [],
                'colors': [],
                'error': str(e)
            }
    
    def _classify_clothing_type(self, detected_label: str) -> str:
        """Classify the detected label into our clothing type system"""
        detected_lower = detected_label.lower()
        
        # Direct matching
        for clothing_type, variations in self.clothing_types.items():
            if detected_lower in [v.lower() for v in variations]:
                return clothing_type
        
        # Fuzzy matching
        for clothing_type, variations in self.clothing_types.items():
            for variation in variations:
                if variation.lower() in detected_lower or detected_lower in variation.lower():
                    return clothing_type
        
        # Default classification based on common terms
        if any(term in detected_lower for term in ['shirt', 'top', 'blouse']):
            return 't-shirt'
        elif any(term in detected_lower for term in ['pants', 'jeans', 'trouser']):
            return 'jeans'
        elif any(term in detected_lower for term in ['dress', 'gown']):
            return 'dress'
        elif any(term in detected_lower for term in ['shoe', 'boot', 'sneaker']):
            return 'sneakers'
        elif any(term in detected_lower for term in ['jacket', 'coat']):
            return 'jacket'
        
        return detected_label  # Return original if no match found
    
    def _get_applicable_styles(self, clothing_type: str) -> List[str]:
        """Get applicable styles for a clothing type"""
        applicable_styles = []
        
        # Check each style to see if the clothing type fits
        for style, items in self.style_mappings.items():
            if clothing_type in items:
                applicable_styles.append(style)
        
        # If no direct match, infer based on clothing type
        if not applicable_styles:
            applicable_styles = self._infer_styles_from_type(clothing_type)
        
        return applicable_styles
    
    def _infer_styles_from_type(self, clothing_type: str) -> List[str]:
        """Infer styles when no direct mapping exists"""
        type_lower = clothing_type.lower()
        
        # Basic inference rules
        if any(term in type_lower for term in ['t-shirt', 'jeans', 'hoodie', 'sneakers']):
            return ['casual', 'streetwear']
        elif any(term in type_lower for term in ['blazer', 'dress-pants', 'button-shirt']):
            return ['business-office', 'classy-elegant']
        elif any(term in type_lower for term in ['dress', 'gown', 'heels']):
            return ['classy-elegant', 'evening-formal']
        elif any(term in type_lower for term in ['athletic', 'sports', 'gym']):
            return ['athleisure']
        elif any(term in type_lower for term in ['vintage', 'retro']):
            return ['vintage-retro']
        else:
            return ['casual']  # Default to casual
    
    def _analyze_colors(self, image_region: np.ndarray) -> List[Dict[str, Any]]:
        """Analyze colors in the image region"""
        try:
            if image_region.size == 0:
                return []
            
            # Convert to RGB
            if len(image_region.shape) == 3:
                rgb_image = cv2.cvtColor(image_region, cv2.COLOR_BGR2RGB)
            else:
                rgb_image = image_region
            
            # Reshape for clustering
            pixels = rgb_image.reshape(-1, 3)
            
            # Filter out very dark and very light pixels (noise)
            mask = np.all(pixels > 15, axis=1) & np.all(pixels < 240, axis=1)
            filtered_pixels = pixels[mask]
            
            if len(filtered_pixels) < 10:
                filtered_pixels = pixels
            
            # Sample pixels for faster processing
            if len(filtered_pixels) > 2000:
                indices = np.random.choice(len(filtered_pixels), 2000, replace=False)
                filtered_pixels = filtered_pixels[indices]
            
            # Perform K-means clustering
            n_clusters = min(5, len(np.unique(filtered_pixels.reshape(-1, filtered_pixels.shape[-1]))))
            if n_clusters < 1:
                return []
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(filtered_pixels)
            
            # Calculate color information
            colors = []
            total_pixels = len(filtered_pixels)
            
            for i, center in enumerate(kmeans.cluster_centers_):
                cluster_size = np.sum(kmeans.labels_ == i)
                percentage = (cluster_size / total_pixels) * 100
                
                # Skip very small color regions
                if percentage < 5:
                    continue
                
                rgb = center.astype(int)
                color_name = self._get_color_name(rgb)
                
                colors.append({
                    'color': color_name,
                    'percentage': round(percentage, 1),
                    'rgb': rgb.tolist()
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
            
            return min_colours[min(min_colours.keys())]
            
        except Exception as e:
            # Fallback to basic color names
            r, g, b = rgb
            if r > 200 and g > 200 and b > 200:
                return "white"
            elif r < 50 and g < 50 and b < 50:
                return "black"
            elif r > g + 30 and r > b + 30:
                return "red"
            elif g > r + 30 and g > b + 30:
                return "green"
            elif b > r + 30 and b > g + 30:
                return "blue"
            elif r > 150 and g > 150 and b < 100:
                return "yellow"
            elif r > 100 and g > 50 and b < 50:
                return "brown"
            else:
                return "mixed"
    
    def _generate_color_description(self, colors: List[Dict[str, Any]]) -> str:
        """Generate a human-readable color description"""
        if not colors:
            return "No colors detected"
        
        if len(colors) == 1:
            return f"{colors[0]['percentage']}% {colors[0]['color']}"
        
        color_parts = []
        for color in colors:
            color_parts.append(f"{color['percentage']}% {color['color']}")
        
        return ", ".join(color_parts)
    
    def _is_clothing_item(self, class_name: str) -> bool:
        """Check if the detected class is a clothing item"""
        clothing_keywords = [
            'person', 'shirt', 'pants', 'dress', 'jacket', 'shoes', 'bag', 'hat',
            'skirt', 'shorts', 'coat', 'hoodie', 'sweater', 'jeans', 'boots',
            'sneakers', 'sandals', 'tie', 'belt', 'backpack', 'handbag'
        ]
        
        return any(keyword in class_name.lower() for keyword in clothing_keywords)
    
    def _infer_clothing_type(self, image: np.ndarray) -> str:
        """Infer clothing type from image characteristics"""
        # Basic inference based on image shape and color distribution
        height, width = image.shape[:2]
        aspect_ratio = height / width
        
        # Simple heuristics
        if aspect_ratio > 1.5:
            return 'dress'  # Tall images might be dresses
        elif aspect_ratio < 0.8:
            return 'pants'  # Wide images might be pants
        else:
            return 't-shirt'  # Default to t-shirt
    
    def analyze_selected_item(self, image: Image.Image, item_id: int, detected_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a specific item selected by the user"""
        try:
            if item_id < 1 or item_id > len(detected_items):
                return {
                    'success': False,
                    'error': 'Invalid item selection'
                }
            
            selected_item = detected_items[item_id - 1]
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            detailed_analysis = self._analyze_single_item(opencv_image, selected_item)
            
            return {
                'success': True,
                'analysis': detailed_analysis
            }
            
        except Exception as e:
            logger.error(f"❌ Selected item analysis error: {e}")
            return {
                'success': False,
                'error': str(e)
            }