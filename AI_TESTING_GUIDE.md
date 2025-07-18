# 🧪 AI Clothing Detector Testing Guide

## 🚀 Quick Start

### Step 1: Start the AI Backend
```bash
cd ai_backend
venv\Scripts\activate
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
```

### Step 2: Run Your Flutter App
```bash
flutter run
```

### Step 3: Access the AI Test Widget
1. **Look for the brain icon** 🧠 in the top-right corner of your app
2. **Tap the brain icon** to open the AI Test Widget
3. **Check the connection status** - should show "AI Backend Available" in green

## 🧪 Testing the AI

### Test 1: Connection Check
- **Expected**: Green checkmark with "AI Backend Available"
- **If Red**: Check that the backend server is running

### Test 2: Image Upload
1. **Tap "Pick Image"** button
2. **Select a photo** from your gallery
3. **Choose a photo** with clothing/people in it

### Test 3: AI Analysis
1. **Tap "Analyze with AI"** button
2. **Wait for processing** (10-30 seconds)
3. **View results**:
   - Detected clothing items
   - Color analysis with percentages
   - Named colors (e.g., "70% red, 30% black")

## 📱 What You Should See

### Connection Status Card
```
✅ AI Backend Available
Mode: Local Development
URL: http://10.0.2.2:5000
```

### Analysis Results
```
Analysis Results:

Detected Clothing:
• person (95.2%)

Color Analysis:
The clothing item contains: 45% blue, 35% white, 20% black.
```

## 🔍 Troubleshooting

### Backend Not Available
1. **Check if server is running** - look for Flask server output
2. **Check URL** - should be `http://10.0.2.2:5000` for Android emulator
3. **Restart server** if needed

### No Results
1. **Try different images** - photos with clear clothing
2. **Check image size** - not too large (>5MB)
3. **Wait longer** - first analysis takes time to load models

### Errors
1. **Check Flutter console** for error messages
2. **Check server logs** for backend errors
3. **Restart both** Flutter app and backend server

## 🎯 Test Scenarios

### Good Test Images
- ✅ Person wearing colorful clothing
- ✅ Clear, well-lit photos
- ✅ Single person in frame
- ✅ Clothing clearly visible

### Challenging Images
- ⚠️ Multiple people
- ⚠️ Dark/blurry photos
- ⚠️ Very small clothing items
- ⚠️ Complex backgrounds

## 📊 Expected Performance

### First Run
- **Model loading**: 30-60 seconds
- **Analysis time**: 10-30 seconds
- **Memory usage**: High (loading models)

### Subsequent Runs
- **Model loading**: 5-10 seconds
- **Analysis time**: 5-15 seconds
- **Memory usage**: Normal

## 🎉 Success Indicators

✅ **Green connection status**
✅ **Image uploads successfully**
✅ **Analysis completes without errors**
✅ **Results show clothing detection**
✅ **Color analysis with percentages**
✅ **Named colors displayed**

---

**🎯 You're ready to test!** Follow these steps and let me know how it goes! 