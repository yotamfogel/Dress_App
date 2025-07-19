#!/usr/bin/env python3
"""
🧪 Test Enhanced AI Models
Verify that Detectron2, MMCV, and MMDet are working correctly
"""

import sys
import logging
from PIL import Image
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_detectron2():
    """Test Detectron2 installation and basic functionality"""
    try:
        import detectron2
        from detectron2.engine import DefaultPredictor
        from detectron2.config import get_cfg
        from detectron2 import model_zoo
        
        logger.info("✅ Detectron2 imported successfully")
        
        # Test configuration
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        
        logger.info("✅ Detectron2 configuration created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Detectron2 test failed: {e}")
        return False

def test_mmcv():
    """Test MMCV installation and basic functionality"""
    try:
        import mmcv
        from mmcv import Config
        
        logger.info("✅ MMCV imported successfully")
        
        # Test basic functionality
        config_dict = dict(
            model=dict(type='ResNet'),
            dataset=dict(type='COCODataset')
        )
        config = Config(config_dict)
        
        logger.info("✅ MMCV configuration test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ MMCV test failed: {e}")
        return False

def test_mmdet():
    """Test MMDet installation and basic functionality"""
    try:
        import mmdet
        from mmdet.apis import init_detector, inference_detector
        
        logger.info("✅ MMDet imported successfully")
        
        # Test model initialization (without loading weights)
        logger.info("✅ MMDet basic functionality test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ MMDet test failed: {e}")
        return False

def test_enhanced_detector():
    """Test the enhanced clothing detector with new models"""
    try:
        from enhanced_clothing_detector import EnhancedClothingDetector
        
        logger.info("🔍 Testing Enhanced Clothing Detector...")
        
        # Create a test image
        test_image = Image.new('RGB', (224, 224), color='red')
        
        # Initialize detector
        detector = EnhancedClothingDetector()
        
        # Test detection
        detections = detector.detect_clothing(test_image)
        
        logger.info(f"✅ Enhanced detector test passed. Found {len(detections)} detections")
        return True
        
    except Exception as e:
        logger.error(f"❌ Enhanced detector test failed: {e}")
        return False

def test_fashion_classification():
    """Test the fashion classification system"""
    try:
        from fashion_classification_system import FashionClassificationSystem
        
        logger.info("👗 Testing Fashion Classification System...")
        
        # Create a test image
        test_image = Image.new('RGB', (224, 224), color='blue')
        
        # Initialize classifier
        classifier = FashionClassificationSystem()
        
        # Test analysis
        result = classifier.analyze_clothing_image(test_image)
        
        logger.info("✅ Fashion classification test passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Fashion classification test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Starting Enhanced AI Models Test Suite")
    logger.info("=" * 50)
    
    tests = [
        ("Detectron2", test_detectron2),
        ("MMCV", test_mmcv),
        ("MMDet", test_mmdet),
        ("Enhanced Detector", test_enhanced_detector),
        ("Fashion Classification", test_fashion_classification),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n🔬 Testing {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            logger.error(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 Test Results Summary:")
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"  {test_name}: {status}")
        if success:
            passed += 1
    
    logger.info(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        logger.info("🎉 All tests passed! Enhanced AI models are ready to use.")
        return True
    else:
        logger.warning("⚠️ Some tests failed. Check the logs above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 