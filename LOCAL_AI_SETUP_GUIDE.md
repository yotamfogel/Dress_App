# 🏠 Local AI Backend Setup Guide

## 📋 Overview
This guide will help you run the AI backend locally with SAM for testing your Flutter app on the emulator.

## 🚀 Quick Start

### Step 1: Start the Local AI Backend

**Option A: Using the Batch File (Windows)**
```bash
cd ai_backend
start_local.bat
```

**Option B: Using PowerShell**
```bash
cd ai_backend
.\start_local.ps1
```

**Option C: Manual Start**
```bash
cd ai_backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python start_local_server.py
```

### Step 2: Verify the Backend is Running

Open your browser and go to: `http://192.168.1.172:8080/health`

You should see:
```json
{
  "status": "healthy",
  "message": "AI Backend is running locally",
  "sam_loaded": true
}
```

### Step 3: Test with Flutter App

1. **Run your Flutter app** on the emulator
2. **Navigate to the AI Test Widget**
3. **Check connection status** - should show "AI Backend Available"
4. **Test image analysis** - upload a photo and analyze it

## 🔧 Detailed Setup

### Prerequisites

1. **Python 3.8+** installed
2. **Git** for version control
3. **Flutter** development environment
4. **Android/iOS emulator** running

### Installation Steps

1. **Clone/Setup Repository**
   ```bash
   cd ai_backend
   git status  # Verify you're in the right directory
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Download AI Models** (automatic on first run)
   - YOLOv8 model will be downloaded automatically
   - SAM model will be downloaded automatically

### Starting the Server

```bash
python start_local_server.py
```

**Expected Output:**
```
🤖 Starting Local AI Backend Server...
📍 Server will run on: http://192.168.1.172:8080
📱 For Android emulator, use: http://10.0.2.2:5000
🍎 For iOS simulator, use: http://192.168.1.172:8080

🚀 Initializing Clothing Detector with SAM...
✅ YOLO model loaded
✅ SAM model loaded
✅ Clothing Detector initialized successfully!
🚀 Starting Flask server...
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.100:5000
```

## 📱 Flutter App Configuration

### Automatic Configuration
The Flutter app is already configured to use localhost when running in debug mode:

- **Debug Mode**: Uses `http://10.0.2.2:5000` (Android emulator)
- **Release Mode**: Uses cloud URL (when deployed)

### Manual Testing
You can test the connection manually:

1. **Open AI Test Widget** in your Flutter app
2. **Check the status card** - shows connection info
3. **Use refresh button** to test connection
4. **Upload an image** and test analysis

## 🧪 Testing the AI Backend

### Test Endpoints

1. **Health Check**
   ```
   GET http://192.168.1.172:8080/health
   ```

2. **Test Endpoint**
   ```
   GET http://192.168.1.172:8080/test
   ```

3. **Clothing Detection**
   ```
   POST http://192.168.1.172:8080/detect-clothing
   Content-Type: application/json
   Body: {"image": "base64_encoded_image"}
   ```

4. **Color Analysis**
   ```
   POST http://192.168.1.172:8080/analyze-colors
   Content-Type: application/json
   Body: {"image": "base64_encoded_image"}
   ```

### Using the AI Test Widget

1. **Launch the widget** from your Flutter app
2. **Check connection status** - should be green
3. **Pick an image** from gallery
4. **Analyze with AI** - should show results
5. **View detailed analysis** - clothing detection + colors

## 🔍 Troubleshooting

### Backend Won't Start

**Error: "Module not found"**
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

**Error: "Port already in use"**
```bash
# Find and kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Error: "SAM model not found"**
```bash
# The model will be downloaded automatically on first run
# If it fails, check your internet connection
```

### Flutter App Can't Connect

**Check URL Configuration**
- Android emulator: `http://10.0.2.2:5000`
- iOS simulator: `http://192.168.1.172:8080`
- Physical device: Use your computer's IP address

**Check Network**
```bash
# Test from Flutter app
curl http://10.0.2.2:5000/health
```

**Check Firewall**
- Ensure port 5000 is not blocked
- Allow Python/Flask through firewall

### Performance Issues

**Slow Model Loading**
- First run downloads models (~1GB)
- Subsequent runs are faster
- Models are cached locally

**Memory Issues**
- Close other applications
- Restart the server if needed
- Check available RAM (recommend 8GB+)

## 📊 Monitoring

### Server Logs
The server provides detailed logs:
```
INFO:__main__:🚀 Initializing Clothing Detector with SAM...
INFO:__main__:✅ YOLO model loaded
INFO:__main__:✅ SAM model loaded
INFO:__main__:✅ Clothing Detector initialized successfully!
```

### Health Monitoring
```bash
# Check server health
curl http://192.168.1.172:8080/health

# Check from Flutter
await AIClothingService.isAvailable()
```

## 🚀 Next Steps

1. **Test with different images** - clothing, people, objects
2. **Integrate AI features** into your main app flow
3. **Optimize performance** if needed
4. **Deploy to cloud** when ready for production

## 📞 Support

If you encounter issues:

1. **Check server logs** for error messages
2. **Verify network connectivity**
3. **Test endpoints manually** with curl/Postman
4. **Restart the server** if needed
5. **Check Flutter console** for connection errors

---

**🎉 You're all set!** Your local AI backend with SAM is ready to use with your Flutter app! 