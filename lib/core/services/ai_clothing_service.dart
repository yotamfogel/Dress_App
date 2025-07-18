import 'dart:io';
import 'package:flutter/foundation.dart';
import 'ai_backend_manager.dart';

class AIClothingService {
  /// Check if AI backend is available
  static Future<bool> isAvailable() async {
    return await AIBackendManager.isBackendAvailable();
  }

  /// Detect clothing items in an image
  static Future<List<ClothingItem>?> detectClothingItems(File imageFile) async {
    try {
      final result = await AIBackendManager.analyzeFashion(imageFile);
      
      if (result != null && result['success'] == true) {
        final List<dynamic> items = result['items'] ?? [];
        return items.map((item) => ClothingItem.fromJson(item)).toList();
      }
      
      return null;
    } catch (e) {
      if (kDebugMode) {
        print('Error detecting clothing items: $e');
      }
      return null;
    }
  }

  /// Analyze colors in an image
  static Future<ColorAnalysis?> analyzeImageColors(File imageFile) async {
    try {
      final result = await AIBackendManager.analyzeColors(imageFile);
      
      if (result != null && result['success'] == true) {
        return ColorAnalysis.fromJson(result);
      }
      
      return null;
    } catch (e) {
      if (kDebugMode) {
        print('Error analyzing colors: $e');
      }
      return null;
    }
  }

  /// Get comprehensive clothing analysis
  static Future<ClothingAnalysis?> analyzeClothing(File imageFile) async {
    try {
      final clothingItems = await detectClothingItems(imageFile);
      final colorAnalysis = await analyzeImageColors(imageFile);
      
      if (clothingItems != null || colorAnalysis != null) {
        return ClothingAnalysis(
          clothingItems: clothingItems ?? [],
          colorAnalysis: colorAnalysis,
        );
      }
      
      return null;
    } catch (e) {
      if (kDebugMode) {
        print('Error in comprehensive clothing analysis: $e');
      }
      return null;
    }
  }
}

/// Model for detected clothing items
class ClothingItem {
  final String label;
  final double confidence;
  final Map<String, dynamic> boundingBox;
  final List<ColorInfo>? colors;

  ClothingItem({
    required this.label,
    required this.confidence,
    required this.boundingBox,
    this.colors,
  });

  factory ClothingItem.fromJson(Map<String, dynamic> json) {
    return ClothingItem(
      label: json['label'] ?? '',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      boundingBox: json['bounding_box'] ?? {},
      colors: json['colors'] != null 
        ? (json['colors'] as List).map((c) => ColorInfo.fromJson(c)).toList()
        : null,
    );
  }
}

/// Model for color information
class ColorInfo {
  final String name;
  final List<int> rgb;
  final double percentage;

  ColorInfo({
    required this.name,
    required this.rgb,
    required this.percentage,
  });

  factory ColorInfo.fromJson(Map<String, dynamic> json) {
    return ColorInfo(
      name: json['name'] ?? '',
      rgb: List<int>.from(json['rgb'] ?? [0, 0, 0]),
      percentage: (json['percentage'] ?? 0.0).toDouble(),
    );
  }
}

/// Model for color analysis results
class ColorAnalysis {
  final List<ColorInfo> dominantColors;
  final String description;

  ColorAnalysis({
    required this.dominantColors,
    required this.description,
  });

  factory ColorAnalysis.fromJson(Map<String, dynamic> json) {
    return ColorAnalysis(
      dominantColors: (json['dominant_colors'] as List?)
        ?.map((c) => ColorInfo.fromJson(c))
        .toList() ?? [],
      description: json['description'] ?? '',
    );
  }
}

/// Comprehensive clothing analysis result
class ClothingAnalysis {
  final List<ClothingItem> clothingItems;
  final ColorAnalysis? colorAnalysis;

  ClothingAnalysis({
    required this.clothingItems,
    this.colorAnalysis,
  });
} 