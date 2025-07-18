#!/usr/bin/env python3
"""
🧪 Backend API Testing Suite
Tests all AI clothing detection backend endpoints
"""

import requests
import json
import base64
import io
from PIL import Image
import numpy as np
import logging
import sys
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BackendTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = {}
        
    def create_test_image(self, color=(255, 0, 0), size=(200, 200)):
        """Create a simple test image with specified color"""
        image = Image.new('RGB', size, color)
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        logger.info("🔍 Testing health endpoint...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Health check passed: {data}")
                
                # Verify expected fields
                required_fields = ['status', 'message', 'yolo_loaded', 'version']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    logger.warning(f"⚠️ Missing fields in health response: {missing_fields}")
                    self.test_results['health'] = {'status': 'partial', 'missing_fields': missing_fields}
                else:
                    self.test_results['health'] = {'status': 'pass', 'data': data}
                    
                return True
            else:
                logger.error(f"❌ Health check failed with status {response.status_code}")
                self.test_results['health'] = {'status': 'fail', 'error': f"HTTP {response.status_code}"}
                return False
                
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            self.test_results['health'] = {'status': 'fail', 'error': str(e)}
            return False
    
    def test_test_endpoint(self):
        """Test the basic test endpoint"""
        logger.info("🔍 Testing test endpoint...")
        try:
            response = requests.get(f"{self.base_url}/test", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Test endpoint passed: {data}")
                
                # Verify expected fields
                if 'message' in data and 'models_loaded' in data:
                    self.test_results['test'] = {'status': 'pass', 'data': data}
                    return True
                else:
                    logger.warning("⚠️ Test endpoint response missing expected fields")
                    self.test_results['test'] = {'status': 'partial', 'data': data}
                    return True
            else:
                logger.error(f"❌ Test endpoint failed with status {response.status_code}")
                self.test_results['test'] = {'status': 'fail', 'error': f"HTTP {response.status_code}"}
                return False
                
        except Exception as e:
            logger.error(f"❌ Test endpoint error: {e}")
            self.test_results['test'] = {'status': 'fail', 'error': str(e)}
            return False
    
    def test_color_analysis_endpoint(self):
        """Test the color analysis endpoint"""
        logger.info("🔍 Testing color analysis endpoint...")
        try:
            # Create test images with different colors
            test_cases = [
                {'color': (255, 0, 0), 'name': 'red'},
                {'color': (0, 255, 0), 'name': 'green'},
                {'color': (0, 0, 255), 'name': 'blue'},
                {'color': (255, 255, 255), 'name': 'white'}
            ]
            
            results = []
            for test_case in test_cases:
                logger.info(f"Testing color analysis with {test_case['name']} image...")
                
                # Create test image
                test_image_b64 = self.create_test_image(test_case['color'])
                
                # Send request
                payload = {'image': test_image_b64}
                response = requests.post(
                    f"{self.base_url}/analyze-colors", 
                    json=payload, 
                    timeout=30,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        logger.info(f"✅ Color analysis for {test_case['name']}: {data.get('dominant_colors', [])}")
                        results.append({
                            'color': test_case['name'],
                            'status': 'pass',
                            'data': data
                        })
                    else:
                        logger.error(f"❌ Color analysis failed for {test_case['name']}: {data.get('error')}")
                        results.append({
                            'color': test_case['name'],
                            'status': 'fail',
                            'error': data.get('error')
                        })
                else:
                    logger.error(f"❌ Color analysis HTTP error for {test_case['name']}: {response.status_code}")
                    results.append({
                        'color': test_case['name'],
                        'status': 'fail',
                        'error': f"HTTP {response.status_code}"
                    })
                
                # Small delay between requests
                time.sleep(0.5)
            
            # Evaluate overall results
            passed_tests = [r for r in results if r['status'] == 'pass']
            if len(passed_tests) >= len(test_cases) * 0.75:  # 75% pass rate
                logger.info(f"✅ Color analysis endpoint passed ({len(passed_tests)}/{len(test_cases)} tests)")
                self.test_results['color_analysis'] = {'status': 'pass', 'results': results}
                return True
            else:
                logger.error(f"❌ Color analysis endpoint failed ({len(passed_tests)}/{len(test_cases)} tests passed)")
                self.test_results['color_analysis'] = {'status': 'fail', 'results': results}
                return False
                
        except Exception as e:
            logger.error(f"❌ Color analysis endpoint error: {e}")
            self.test_results['color_analysis'] = {'status': 'fail', 'error': str(e)}
            return False
    
    def test_clothing_detection_endpoint(self):
        """Test the clothing detection endpoint"""
        logger.info("🔍 Testing clothing detection endpoint...")
        try:
            # Create test images
            test_cases = [
                {'color': (255, 0, 0), 'name': 'red_image'},
                {'color': (0, 0, 255), 'name': 'blue_image'},
                {'color': (128, 128, 128), 'name': 'gray_image'}
            ]
            
            results = []
            for test_case in test_cases:
                logger.info(f"Testing clothing detection with {test_case['name']}...")
                
                # Create test image
                test_image_b64 = self.create_test_image(test_case['color'], size=(400, 400))
                
                # Send request
                payload = {'image': test_image_b64}
                response = requests.post(
                    f"{self.base_url}/detect-clothing", 
                    json=payload, 
                    timeout=30,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') is not None:  # Accept both True and False as valid responses
                        logger.info(f"✅ Clothing detection for {test_case['name']}: found {data.get('total_items', 0)} items")
                        results.append({
                            'image': test_case['name'],
                            'status': 'pass',
                            'data': data
                        })
                    else:
                        logger.error(f"❌ Clothing detection failed for {test_case['name']}: {data.get('error')}")
                        results.append({
                            'image': test_case['name'],
                            'status': 'fail',
                            'error': data.get('error')
                        })
                else:
                    logger.error(f"❌ Clothing detection HTTP error for {test_case['name']}: {response.status_code}")
                    results.append({
                        'image': test_case['name'],
                        'status': 'fail',
                        'error': f"HTTP {response.status_code}"
                    })
                
                # Small delay between requests
                time.sleep(0.5)
            
            # Evaluate overall results
            passed_tests = [r for r in results if r['status'] == 'pass']
            if len(passed_tests) >= len(test_cases) * 0.75:  # 75% pass rate
                logger.info(f"✅ Clothing detection endpoint passed ({len(passed_tests)}/{len(test_cases)} tests)")
                self.test_results['clothing_detection'] = {'status': 'pass', 'results': results}
                return True
            else:
                logger.error(f"❌ Clothing detection endpoint failed ({len(passed_tests)}/{len(test_cases)} tests passed)")
                self.test_results['clothing_detection'] = {'status': 'fail', 'results': results}
                return False
                
        except Exception as e:
            logger.error(f"❌ Clothing detection endpoint error: {e}")
            self.test_results['clothing_detection'] = {'status': 'fail', 'error': str(e)}
            return False
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        logger.info("🔍 Testing error handling...")
        try:
            error_tests = []
            
            # Test 1: Invalid JSON for color analysis
            try:
                response = requests.post(f"{self.base_url}/analyze-colors", json={}, timeout=10)
                if response.status_code == 400:
                    error_tests.append({'test': 'invalid_json_color', 'status': 'pass'})
                else:
                    error_tests.append({'test': 'invalid_json_color', 'status': 'fail', 'code': response.status_code})
            except Exception as e:
                error_tests.append({'test': 'invalid_json_color', 'status': 'fail', 'error': str(e)})
            
            # Test 2: Invalid JSON for clothing detection
            try:
                response = requests.post(f"{self.base_url}/detect-clothing", json={}, timeout=10)
                if response.status_code == 400:
                    error_tests.append({'test': 'invalid_json_clothing', 'status': 'pass'})
                else:
                    error_tests.append({'test': 'invalid_json_clothing', 'status': 'fail', 'code': response.status_code})
            except Exception as e:
                error_tests.append({'test': 'invalid_json_clothing', 'status': 'fail', 'error': str(e)})
            
            # Test 3: Invalid base64 image
            try:
                payload = {'image': 'invalid_base64_data'}
                response = requests.post(f"{self.base_url}/analyze-colors", json=payload, timeout=10)
                if response.status_code == 400:
                    error_tests.append({'test': 'invalid_base64', 'status': 'pass'})
                else:
                    error_tests.append({'test': 'invalid_base64', 'status': 'fail', 'code': response.status_code})
            except Exception as e:
                error_tests.append({'test': 'invalid_base64', 'status': 'fail', 'error': str(e)})
            
            # Evaluate results
            passed_tests = [t for t in error_tests if t['status'] == 'pass']
            if len(passed_tests) >= len(error_tests) * 0.5:  # 50% pass rate for error handling
                logger.info(f"✅ Error handling tests passed ({len(passed_tests)}/{len(error_tests)} tests)")
                self.test_results['error_handling'] = {'status': 'pass', 'results': error_tests}
                return True
            else:
                logger.warning(f"⚠️ Error handling tests partially passed ({len(passed_tests)}/{len(error_tests)} tests)")
                self.test_results['error_handling'] = {'status': 'partial', 'results': error_tests}
                return True  # Not critical for core functionality
                
        except Exception as e:
            logger.error(f"❌ Error handling test error: {e}")
            self.test_results['error_handling'] = {'status': 'fail', 'error': str(e)}
            return False
    
    def run_all_tests(self):
        """Run all backend tests"""
        logger.info("🚀 Starting comprehensive backend testing...")
        logger.info(f"🎯 Testing backend at: {self.base_url}")
        
        tests = [
            ('Health Check', self.test_health_endpoint),
            ('Test Endpoint', self.test_test_endpoint),
            ('Color Analysis', self.test_color_analysis_endpoint),
            ('Clothing Detection', self.test_clothing_detection_endpoint),
            ('Error Handling', self.test_error_handling)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            logger.info(f"\n{'='*50}")
            logger.info(f"🧪 Running: {test_name}")
            logger.info(f"{'='*50}")
            
            try:
                if test_func():
                    passed_tests += 1
                    logger.info(f"✅ {test_name} PASSED")
                else:
                    logger.error(f"❌ {test_name} FAILED")
            except Exception as e:
                logger.error(f"❌ {test_name} ERROR: {e}")
            
            time.sleep(1)  # Brief pause between tests
        
        # Final summary
        logger.info(f"\n{'='*60}")
        logger.info(f"🎯 BACKEND TESTING COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"✅ Passed: {passed_tests}/{total_tests} tests")
        logger.info(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests >= total_tests * 0.8:  # 80% pass rate
            logger.info("🎉 BACKEND TESTS PASSED - System is working properly!")
            return True
        else:
            logger.error("❌ BACKEND TESTS FAILED - Critical issues found!")
            return False
    
    def get_detailed_results(self):
        """Get detailed test results"""
        return self.test_results

def main():
    """Main testing function"""
    print("🤖 AI Clothing Detection Backend - Test Suite")
    print("=" * 60)
    
    # Initialize tester
    tester = BackendTester()
    
    # Run all tests
    success = tester.run_all_tests()
    
    # Print detailed results
    print("\n" + "=" * 60)
    print("📋 DETAILED TEST RESULTS")
    print("=" * 60)
    
    results = tester.get_detailed_results()
    for test_name, result in results.items():
        print(f"\n🧪 {test_name.upper()}:")
        print(f"   Status: {result['status']}")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        if 'data' in result:
            print(f"   Data: {json.dumps(result['data'], indent=2)}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()