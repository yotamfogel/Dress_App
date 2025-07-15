import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

class AIBackendManager {
  // Your computer's IP address with accessible port
  static const String _localUrl = 'http://192.168.1.172:8010';
  
  // Cloud deployment URL (update this when you deploy to Railway)
  static const String _cloudUrl = 'https://your-ai-backend.railway.app';
  
  // Use local URL for development, cloud URL for production
  static String get _baseUrl {
    if (kDebugMode) {
      return _localUrl; // Use your IP with port 8010
    } else {
      return _cloudUrl; // Use cloud URL in release mode
    }
  }
  
  // Health check endpoint
  static const String _healthEndpoint = '/ai/health';
  
  // Clothing detection endpoint
  static const String _detectEndpoint = '/api/detect-clothing';
  
  // Color analysis endpoint
  static const String _analyzeColorsEndpoint = '/api/analyze-colors';

  /// Check if the AI backend is available
  static Future<bool> isBackendAvailable() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl$_healthEndpoint'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 10));
      
      return response.statusCode == 200;
    } catch (e) {
      if (kDebugMode) {
        print('AI Backend health check failed: $e');
        print('Trying to connect to: $_baseUrl$_healthEndpoint');
      }
      return false;
    }
  }

  /// Detect clothing items in an image
  static Future<Map<String, dynamic>?> detectClothing(File imageFile) async {
    try {
      // Convert image to base64
      final bytes = await imageFile.readAsBytes();
      final base64Image = base64Encode(bytes);
      
      final response = await http.post(
        Uri.parse('$_baseUrl$_detectEndpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'image': base64Image,
        }),
      ).timeout(const Duration(seconds: 30));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        if (kDebugMode) {
          print('AI Backend detection failed: ${response.statusCode} - ${response.body}');
        }
        return null;
      }
    } catch (e) {
      if (kDebugMode) {
        print('AI Backend detection error: $e');
      }
      return null;
    }
  }

  /// Analyze colors in an image
  static Future<Map<String, dynamic>?> analyzeColors(File imageFile) async {
    try {
      // Convert image to base64
      final bytes = await imageFile.readAsBytes();
      final base64Image = base64Encode(bytes);
      
      final response = await http.post(
        Uri.parse('$_baseUrl$_analyzeColorsEndpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'image': base64Image,
        }),
      ).timeout(const Duration(seconds: 30));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        if (kDebugMode) {
          print('AI Backend color analysis failed: ${response.statusCode} - ${response.body}');
        }
        return null;
      }
    } catch (e) {
      if (kDebugMode) {
        print('AI Backend color analysis error: $e');
      }
      return null;
    }
  }

  /// Get the current backend URL
  static String getBackendUrl() {
    return _baseUrl;
  }

  /// Check if running locally
  static bool get isLocalMode {
    return kDebugMode;
  }

  /// Get local URL for manual testing
  static String get localUrl => _localUrl;
  
  /// Get cloud URL for production
  static String get cloudUrl => _cloudUrl;
} 