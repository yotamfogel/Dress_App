# DressApp Build Guide

This guide provides comprehensive instructions for building and running the DressApp with AI-powered clothing detection.

## 🚀 Quick Start

### Option 1: Cloud Deployment (Recommended for Mobile)

**Deploy AI to Cloud:**
```bash
# Deploy to Railway (Free tier)
python scripts/deploy_ai_cloud.py

# Or follow manual steps in ai_backend/deploy_railway.md
```

**Build Flutter App:**
```bash
flutter build apk --release
flutter install
```

### Option 2: Automatic AI Backend (Local Development)

**Windows:**
```powershell
# Using PowerShell
.\scripts\build_with_ai.ps1 -Platform debug

# Using Batch file
.\scripts\build_with_ai.bat
```

**macOS/Linux:**
```bash
# Using Python script
python scripts/start_ai_backend.py --start
flutter run
```

### Option 2: Manual Setup

1. **Start AI Backend:**
   ```bash
   cd ai_backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python start_server.py
   ```

2. **Run Flutter App:**
   ```bash
   flutter run
   ```

### Option 3: Docker (Advanced)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t dressapp-ai ./ai_backend
docker run -p 5000:5000 dressapp-ai
```

### Option 4: Cloud Deployment (Production)

**Railway (Recommended - Free):**
```bash
# Automatic deployment
python scripts/deploy_ai_cloud.py

# Manual deployment
cd ai_backend
railway init
railway up
```

**Render (Free Tier):**
```bash
# Follow steps in ai_backend/deploy_render.md
# Or use deployment script
python scripts/deploy_ai_cloud.py
```

**Google Cloud Run:**
```bash
# Deploy to Google Cloud
gcloud run deploy dressapp-ai --source .
```

## 🤖 AI Backend Features

The AI backend provides advanced clothing detection capabilities:

- **YOLOv8 Object Detection**: Detects people and clothing items
- **SAM Segmentation**: Precise clothing segmentation
- **Color Analysis**: Extracts dominant colors with percentages
- **Named Color Mapping**: Converts RGB to human-readable names
- **REST API**: Easy integration with Flutter app

### API Endpoints

- `GET /health` - Health check
- `POST /detect-clothing` - Single image analysis
- `POST /analyze-closet` - Multiple images analysis
- `GET /test` - Test endpoint

### Example Response

```json
{
  "success": true,
  "detections": [
    {
      "index": 0,
      "success": true,
      "description": "The clothing item contains: 70% red, 30% black.",
      "colors": [
        {
          "name": "red",
          "rgb": [255, 0, 0],
          "percentage": 70.0
        },
        {
          "name": "black",
          "rgb": [0, 0, 0],
          "percentage": 30.0
        }
      ],
      "clothing_type": "person",
      "confidence": 0.8
    }
  ]
}
```

## 📋 Prerequisites

### System Requirements

- **Flutter**: 3.0.0 or higher
- **Python**: 3.8+ (for AI backend)
- **RAM**: 4GB+ (8GB+ recommended for AI)
- **Storage**: 2GB+ free space
- **GPU**: CUDA-compatible (optional, for faster AI processing)

### Required Software

1. **Flutter SDK**
   ```bash
   # Install Flutter
   git clone https://github.com/flutter/flutter.git
   export PATH="$PATH:`pwd`/flutter/bin"
   flutter doctor
   ```

2. **Python 3.8+**
   ```bash
   # Download from python.org or use package manager
   python --version
   ```

3. **Android Studio / Xcode** (for mobile builds)
   - Android Studio for Android development
   - Xcode for iOS development (macOS only)

## 🛠️ Detailed Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd dressapp
```

### 2. Flutter Setup

```bash
# Get dependencies
flutter pub get

# Check setup
flutter doctor
```

### 3. AI Backend Setup

```bash
cd ai_backend

# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download SAM model (optional)
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -O sam_vit_b.pth
```

### 4. Test AI Backend

```bash
# Run test suite
python test_ai.py

# Start server
python start_server.py
```

### 5. Verify Setup

```bash
# Test API
curl http://192.168.1.172:8080/health

# Test detection
curl -X POST http://192.168.1.172:8080/test
```

## 📱 Building for Different Platforms

### Android

```bash
# Debug build
flutter build apk --debug

# Release build
flutter build apk --release

# Install on connected device
flutter install
```

### iOS (macOS only)

```bash
# Debug build
flutter build ios --debug

# Release build
flutter build ios --release

# Open in Xcode
open ios/Runner.xcworkspace
```

### Web

```bash
# Build for web
flutter build web

# Serve locally
flutter run -d chrome
```

## 🔧 Configuration

### Environment Variables

Create `.env` file in `ai_backend/`:

```env
PORT=5000
FLASK_ENV=development
FLASK_DEBUG=1
```

### Flutter Configuration

Update `lib/core/services/ai_backend_manager.dart`:

```dart
class AIBackendManager {
  static const String baseUrl = 'http://192.168.1.172:8080';
  // ... rest of configuration
}
```

## 🐛 Troubleshooting

### Common Issues

1. **AI Backend Won't Start**
   ```bash
   # Check Python version
   python --version
   
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   
   # Check port availability
   netstat -an | grep 5000
   ```

2. **Flutter Build Fails**
   ```bash
   # Clean and rebuild
   flutter clean
   flutter pub get
   flutter build apk
   ```

3. **Model Download Issues**
   ```bash
   # Manual model download
   wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
   mv sam_vit_b_01ec64.pth ai_backend/sam_vit_b.pth
   ```

4. **CUDA Issues**
   ```bash
   # Use CPU-only mode
   export CUDA_VISIBLE_DEVICES=""
   python start_server.py
   ```

### Performance Optimization

1. **Reduce Image Size**
   - Resize images before sending to AI
   - Use compression for faster processing

2. **Model Optimization**
   - Use smaller YOLO model (yolov8n)
   - Disable SAM for faster processing

3. **Caching**
   - Cache detection results
   - Use local storage for processed images

## 📊 Performance Metrics

- **YOLO Detection**: ~100-200ms per image
- **SAM Segmentation**: ~500-1000ms per image
- **Color Analysis**: ~50-100ms per image
- **Total Pipeline**: ~1-2 seconds per image

## 🔄 Development Workflow

1. **Start AI Backend**
   ```bash
   cd ai_backend
   python start_server.py
   ```

2. **Run Flutter App**
   ```bash
   flutter run
   ```

3. **Test Features**
   - Take photos of clothing
   - Verify color detection
   - Check API responses

4. **Debug Issues**
   - Check AI backend logs
   - Monitor API responses
   - Test with sample images

## 📝 Testing

### AI Backend Tests

```bash
cd ai_backend
python test_ai.py
```

### Flutter Tests

```bash
flutter test
```

### Integration Tests

```bash
# Test API endpoints
curl -X POST http://192.168.1.172:8080/detect-clothing \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "..."}'
```

## 🚀 Deployment

### Production Build

```bash
# Build release APK
flutter build apk --release

# Build for web
flutter build web --release

# Build for iOS
flutter build ios --release
```

### AI Backend Deployment

```bash
# Using Docker
docker build -t dressapp-ai ./ai_backend
docker run -p 5000:5000 dressapp-ai

# Using Docker Compose
docker-compose up -d
```

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review error logs
3. Test with sample images
4. Open an issue on GitHub

## 📄 License

This project is licensed under the MIT License. 