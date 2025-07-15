"""
🎨 Color Analysis for Clothing
Advanced color analysis using OpenCV and scikit-learn
"""

import cv2
import numpy as np
from PIL import Image
import webcolors
from sklearn.cluster import KMeans
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ColorAnalyzer:
    def __init__(self):
        """Initialize color analyzer"""
        self.color_thresholds = {
            'dominant_colors': 5,  # Number of dominant colors to extract
            'min_percentage': 5.0,  # Minimum percentage to consider a color significant
        }
    
    def analyze_colors(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze colors in an image"""
        try:
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Get dominant colors
            dominant_colors = self._get_dominant_colors(opencv_image)
            
            # Generate description
            description = self._generate_color_description(dominant_colors)
            
            return {
                'dominant_colors': dominant_colors,
                'description': description,
                'total_colors': len(dominant_colors)
            }
            
        except Exception as e:
            logger.error(f"❌ Color analysis error: {e}")
            return {
                'dominant_colors': [],
                'description': 'Color analysis failed',
                'total_colors': 0
            }
    
    def _get_dominant_colors(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """Extract dominant colors using K-means clustering"""
        try:
            # Resize image for faster processing
            height, width = image.shape[:2]
            if height > 300 or width > 300:
                scale = min(300/height, 300/width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height))
            
            # Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Reshape for clustering
            pixels = image_rgb.reshape(-1, 3)
            
            # Filter out very dark and very light pixels (often noise)
            mask = np.all(pixels > 20, axis=1) & np.all(pixels < 235, axis=1)
            filtered_pixels = pixels[mask]
            
            if len(filtered_pixels) == 0:
                filtered_pixels = pixels
            
            # Perform K-means clustering
            n_clusters = min(self.color_thresholds['dominant_colors'], len(np.unique(filtered_pixels.reshape(-1, filtered_pixels.shape[-1]))))
            if n_clusters < 1:
                return []
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            kmeans.fit(filtered_pixels)
            
            # Calculate color information
            colors = []
            total_pixels = len(filtered_pixels)
            
            for i, center in enumerate(kmeans.cluster_centers_):
                # Calculate percentage
                cluster_size = np.sum(kmeans.labels_ == i)
                percentage = (cluster_size / total_pixels) * 100
                
                # Skip colors with very low percentage
                if percentage < self.color_thresholds['min_percentage']:
                    continue
                
                # Get color information
                rgb = center.astype(int)
                color_name = self._get_color_name(rgb)
                
                colors.append({
                    'name': color_name,
                    'rgb': rgb.tolist(),
                    'percentage': round(percentage, 1)
                })
            
            # Sort by percentage (descending)
            colors.sort(key=lambda x: x['percentage'], reverse=True)
            
            return colors
            
        except Exception as e:
            logger.error(f"❌ Dominant colors extraction error: {e}")
            return []
    
    def _get_color_name(self, rgb: np.ndarray) -> str:
        """Get the closest color name for RGB values"""
        try:
            # Try to get closest named color from webcolors
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
            # Fallback to basic color classification
            return self._classify_basic_color(rgb)
    
    def _classify_basic_color(self, rgb: np.ndarray) -> str:
        """Classify color into basic categories"""
        r, g, b = rgb
        
        # White/Light colors
        if r > 200 and g > 200 and b > 200:
            return "white"
        
        # Black/Dark colors
        if r < 50 and g < 50 and b < 50:
            return "black"
        
        # Gray
        if abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30:
            if r > 150:
                return "lightgray"
            elif r > 100:
                return "gray"
            else:
                return "darkgray"
        
        # Primary colors
        if r > g + 50 and r > b + 50:
            if r > 200:
                return "red"
            else:
                return "darkred"
        
        if g > r + 50 and g > b + 50:
            if g > 200:
                return "lime"
            else:
                return "green"
        
        if b > r + 50 and b > g + 50:
            if b > 200:
                return "blue"
            else:
                return "darkblue"
        
        # Secondary colors
        if r > 150 and g > 150 and b < 100:
            return "yellow"
        
        if r > 150 and b > 150 and g < 100:
            return "magenta"
        
        if g > 150 and b > 150 and r < 100:
            return "cyan"
        
        # Brown/Orange
        if r > 100 and g > 50 and b < 50:
            return "brown"
        
        if r > 200 and g > 100 and b < 50:
            return "orange"
        
        # Purple/Pink
        if r > 150 and b > 100 and g < 100:
            return "purple"
        
        if r > 200 and g > 150 and b > 150:
            return "pink"
        
        # Default
        return "mixed"
    
    def _generate_color_description(self, colors: List[Dict[str, Any]]) -> str:
        """Generate a human-readable description of the colors"""
        if not colors:
            return "No significant colors detected."
        
        # Create description
        if len(colors) == 1:
            color = colors[0]
            return f"The clothing item is primarily {color['name']} ({color['percentage']}%)."
        
        # Multiple colors
        descriptions = []
        for color in colors[:3]:  # Top 3 colors
            descriptions.append(f"{color['percentage']}% {color['name']}")
        
        if len(colors) > 3:
            description = f"The clothing item contains: {', '.join(descriptions)}, and other colors."
        else:
            description = f"The clothing item contains: {', '.join(descriptions)}."
        
        return description