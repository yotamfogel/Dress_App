# 🤖 AI Backend for Clothing Detection

This folder contains two AI backend implementations for clothing detection and color analysis:

## 🚀 Available Implementations

### 1. **Simple YOLO-Only** ⚡ (Recommended for testing)
- **Server:** `start_http_server.py`
- **Detector:** `simple_clothing_detector.py`
- **Features:** Fast YOLO detection, basic color analysis
- **Performance:** 2-5 seconds, 500MB memory
- **Best for:** Quick testing, development, emulator

### 2. **Advanced YOLO + SAM** 🎯 (Production-ready)
- **Server:** `start_advanced_server.py`
- **Detector:** `clothing_detector.py`
- **Features:** YOLO + SAM segmentation, advanced color analysis
- **Performance:** 5-15 seconds, 2-3GB memory
- **Best for:** High precision, production apps, detailed analysis

## 📋 Quick Start

### **For Flutter Emulator (Recommended):**
```bash
cd ai_backend
python start_http_server.py
```

### **For Advanced Features:**
```bash
cd ai_backend
pip install segment-anything
python start_advanced_server.py
```

## 🧪 Testing

### **Test Simple Implementation:**
```bash
python test_http_server.py
```

### **Test Advanced Implementation:**
```bash
python test_advanced_backend.py
```

## 📊 Feature Comparison

| Feature | Simple YOLO | Advanced YOLO + SAM |
|---------|-------------|---------------------|
| Clothing Detection | ✅ Good | ✅ Excellent |
| Segmentation | ❌ Bounding boxes | ✅ Pixel-perfect |
| Startup Speed | ⚡ 5-10s | 🐌 2-5min (first run) |
| Memory Usage | 💚 ~500MB | 🔴 ~2-3GB |
| Accuracy | 📊 Good | 🎯 Excellent |

## 🔧 Configuration Files

### **Core Files:**
- `requirements.txt` - Basic dependencies
- `requirements_full.txt` - Full dependencies with SAM
- `color_analyzer.py` - Color analysis (shared)

### **Server Files:**
- `start_http_server.py` - Simple YOLO server
- `start_advanced_server.py` - Advanced YOLO + SAM server
- `start_wifi_server.py` - Network server (legacy)

### **AI Models:**
- `simple_clothing_detector.py` - YOLO-only detection
- `clothing_detector.py` - YOLO + SAM detection

### **Testing:**
- `test_http_server.py` - Test simple implementation
- `test_advanced_backend.py` - Test advanced implementation
- `test_*.py` - Various network and functionality tests

## 📱 Flutter Integration

Both implementations work with the Flutter app via these endpoints:

### **Simple Implementation:**
- `GET /ai/health` - Health check
- `POST /ai/detect-clothing` - Basic clothing detection
- `POST /ai/analyze-colors` - Color analysis

### **Advanced Implementation:**
- `GET /ai/health` - Health check with SAM status
- `GET /ai/models` - Model information
- `POST /ai/detect-clothing` - Advanced detection
- `POST /ai/analyze-colors` - Advanced color analysis
- `POST /ai/segment-clothing` - Precise segmentation

## 🎯 Which to Use?

### **Use Simple YOLO-Only If:**
- Testing with Flutter emulator
- Limited hardware resources
- Need fast response times
- Basic detection is sufficient

### **Use Advanced YOLO + SAM If:**
- Building production application
- Need high precision segmentation
- Have sufficient hardware (8GB+ RAM)
- Want detailed clothing analysis

## 🚀 Current Status

- ✅ **Simple YOLO**: Ready for emulator testing
- ✅ **Advanced YOLO + SAM**: Available for production use
- ✅ **Flutter Integration**: Works with both implementations
- ✅ **Color Analysis**: Advanced clustering with hex colors

See `IMPLEMENTATION_GUIDE.md` for detailed comparison and usage instructions.