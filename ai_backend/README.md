# 🤖 AI Backend for Clothing Detection

This folder contains the AI backend server that provides clothing detection and color analysis capabilities for the Flutter app.

## 🚀 Key Files

### **Main Server Files:**
- `start_http_server.py` - HTTP server for Android emulator testing
- `start_android_server.py` - Android-accessible server
- `start_wifi_server.py` - WiFi network server

### **AI Models:**
- `simple_clothing_detector.py` - YOLO-based clothing detection
- `color_analyzer.py` - Color analysis using K-means clustering
- `clothing_detector.py` - Advanced clothing detection with SAM

### **Configuration:**
- `requirements.txt` - Python dependencies
- `start_local.bat` - Windows startup script

### **Testing:**
- `test_http_server.py` - Test HTTP server functionality
- `test_android_backend.py` - Test Android connectivity
- `test_network_complete.py` - Comprehensive network tests

## 🎯 How to Use

### **For Android Emulator:**
```bash
cd ai_backend
python start_http_server.py
```
Then in Flutter app, the backend will be accessible at `http://10.0.2.2:8080`

### **For Physical Android Device:**
```bash
cd ai_backend
python start_wifi_server.py
```
Use your computer's IP address with port 8080

## 📋 Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

**Note:** The YOLO model (`yolov8n.pt`) will be downloaded automatically on first run.

## 🧪 Testing

Test the server:
```bash
python test_http_server.py
```

## 🎨 AI Capabilities

- **Clothing Detection**: Detects shirts, pants, shoes, dresses, etc.
- **Color Analysis**: Extracts dominant colors with percentages
- **Confidence Scores**: Provides accuracy ratings for detections
- **Fast Processing**: Optimized for 2-5 second response times

## 📱 Flutter Integration

The Flutter app connects to this backend via the `AIBackendManager` class for:
- Health checks
- Clothing detection
- Color analysis
- Real-time AI processing

## 🔧 Configuration

The server automatically detects the environment and configures endpoints accordingly:
- `/ai/health` - Health check
- `/ai/detect-clothing` - Clothing detection
- `/ai/analyze-colors` - Color analysis