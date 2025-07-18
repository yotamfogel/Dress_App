import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

class AIBackendManager {
  // Set the advanced server IP here
  static const String _advancedServerUrl = 'http://192.168.1.172:8080';

  static String get _baseUrl {
    return _advancedServerUrl;
  }
  
  // Health check endpoint
  static const String _healthEndpoint = '/health';
  
  // Fashion analysis endpoint (new main endpoint)
  static const String _fashionAnalysisEndpoint = '/analyze-fashion';
  
  // Legacy endpoints for compatibility
  static const String _detectEndpoint = '/detect-clothing';
  static const String _analyzeColorsEndpoint = '/analyze-colors';

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

  /// Analyze fashion item with advanced classification
  static Future<Map<String, dynamic>?> analyzeFashion(File imageFile) async {
    try {
      // Convert image to base64
      final bytes = await imageFile.readAsBytes();
      final base64Image = base64Encode(bytes);
      
      final response = await http.post(
        Uri.parse('$_baseUrl$_fashionAnalysisEndpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'image': base64Image,
        }),
      ).timeout(const Duration(seconds: 30));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        if (kDebugMode) {
          print('Fashion analysis failed: ${response.statusCode} - ${response.body}');
        }
        return null;
      }
    } catch (e) {
      if (kDebugMode) {
        print('Fashion analysis error: $e');
      }
      return null;
    }
  }

  /// Handle multiple items selection
  static Future<Map<String, dynamic>?> selectFashionItem(File imageFile, int itemSelection) async {
    try {
      // Convert image to base64
      final bytes = await imageFile.readAsBytes();
      final base64Image = base64Encode(bytes);
      
      final response = await http.post(
        Uri.parse('$_baseUrl$_fashionAnalysisEndpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'image': base64Image,
          'item_selection': itemSelection,
        }),
      ).timeout(const Duration(seconds: 30));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        if (kDebugMode) {
          print('Fashion item selection failed: ${response.statusCode} - ${response.body}');
        }
        return null;
      }
    } catch (e) {
      if (kDebugMode) {
        print('Fashion item selection error: $e');
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
  static String get localUrl => _advancedServerUrl;
  
  /// Get cloud URL for production
  static String get cloudUrl => _advancedServerUrl;
} 