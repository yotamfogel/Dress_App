import 'dart:convert';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart' as path_util;

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
      name: json['name'] ?? json['color'] ?? 'unknown',
      rgb: (json['rgb'] as List<dynamic>?)
              ?.map((value) => value as int)
              .toList() ??
          [0, 0, 0],
      percentage: (json['percentage'] as num?)?.toDouble() ?? 0.0,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'rgb': rgb,
      'percentage': percentage,
    };
  }
}

class AIAnalysisData {
  final String? clothingType;
  final List<String> applicableStyles;
  final List<ColorInfo> colors;
  final String? colorDescription;
  final double confidence;
  final String detectionMethod;
  final DateTime? analyzedAt;

  AIAnalysisData({
    this.clothingType,
    this.applicableStyles = const [],
    this.colors = const [],
    this.colorDescription,
    this.confidence = 0.0,
    this.detectionMethod = 'Fashion Classification System',
    this.analyzedAt,
  });

  factory AIAnalysisData.fromJson(Map<String, dynamic> json) {
    return AIAnalysisData(
      clothingType: json['clothing_type'] as String?,
      applicableStyles: (json['applicable_styles'] as List<dynamic>?)
              ?.map((style) => style.toString())
              .toList() ??
          [],
      colors: (json['colors'] as List<dynamic>?)
              ?.map((color) => ColorInfo.fromJson(color))
              .toList() ??
          [],
      colorDescription: json['color_description'] as String?,
      confidence: ((json['detection_details'] as Map<String, dynamic>?)?['confidence'] as num?)?.toDouble() ?? 0.0,
      detectionMethod: ((json['detection_details'] as Map<String, dynamic>?)?['method'] as String?) ?? 'Fashion Classification System',
      analyzedAt: DateTime.now(),
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'clothingType': clothingType,
      'applicableStyles': applicableStyles,
      'colors': colors.map((c) => c.toMap()).toList(),
      'colorDescription': colorDescription,
      'confidence': confidence,
      'detectionMethod': detectionMethod,
      'analyzedAt': analyzedAt?.millisecondsSinceEpoch,
    };
  }
}

class ClosetItemModel {
  final int? id;
  final String imagePath;
  final AIAnalysisData? aiAnalysis;
  final List<String> patterns; // Keep for backward compatibility
  final Map<String, dynamic> features; // Keep for backward compatibility
  final DateTime? createdAt;
  final DateTime? updatedAt;

  ClosetItemModel({
    this.id,
    required this.imagePath,
    this.aiAnalysis,
    this.patterns = const [],
    this.features = const {},
    this.createdAt,
    this.updatedAt,
  });

  // Convenience getters for easy access
  String? get clothingType => aiAnalysis?.clothingType;
  List<String> get applicableStyles => aiAnalysis?.applicableStyles ?? [];
  List<ColorInfo> get colors => aiAnalysis?.colors ?? [];
  String? get colorDescription => aiAnalysis?.colorDescription;
  double get confidence => aiAnalysis?.confidence ?? 0.0;

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'imagePath': imagePath,
      'aiAnalysis': aiAnalysis?.toMap(),
      'patterns': patterns,
      'features': features,
      'createdAt': createdAt?.millisecondsSinceEpoch,
      'updatedAt': updatedAt?.millisecondsSinceEpoch,
    };
  }

  factory ClosetItemModel.fromMap(Map<String, dynamic> map) {
    return ClosetItemModel(
      id: map['id'] as int?,
      imagePath: map['imagePath'] as String,
      aiAnalysis: map['aiAnalysis'] != null 
          ? _parseAIAnalysis(map['aiAnalysis'] as String?)
          : _legacyToAIAnalysis(map), // Convert legacy data
      patterns: (map['patterns'] as List<dynamic>?)
              ?.map((pattern) => pattern as String)
              .toList() ??
          [],
      features: (map['features'] as Map<String, dynamic>?) ?? {},
      createdAt: map['createdAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['createdAt'] as int)
          : null,
      updatedAt: map['updatedAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['updatedAt'] as int)
          : null,
    );
  }

  static AIAnalysisData? _parseAIAnalysis(String? aiAnalysisJson) {
    if (aiAnalysisJson == null) return null;
    try {
      final Map<String, dynamic> data = jsonDecode(aiAnalysisJson);
      return AIAnalysisData(
        clothingType: data['clothingType'] as String?,
        applicableStyles: (data['applicableStyles'] as List<dynamic>?)
                ?.map((style) => style.toString())
                .toList() ??
            [],
        colors: (data['colors'] as List<dynamic>?)
                ?.map((color) => ColorInfo.fromJson(color))
                .toList() ??
            [],
        colorDescription: data['colorDescription'] as String?,
        confidence: (data['confidence'] as num?)?.toDouble() ?? 0.0,
        detectionMethod: data['detectionMethod'] as String? ?? 'Fashion Classification System',
        analyzedAt: data['analyzedAt'] != null
            ? DateTime.fromMillisecondsSinceEpoch(data['analyzedAt'] as int)
            : null,
      );
    } catch (e) {
      return null;
    }
  }

  // Convert legacy data format to new AI analysis format
  static AIAnalysisData? _legacyToAIAnalysis(Map<String, dynamic> map) {
    final clothingType = map['clothingType'] as String?;
    final colorsData = _parseColors(map['colors'] as String?);
    
    if (clothingType == null && colorsData.isEmpty) return null;
    
    return AIAnalysisData(
      clothingType: clothingType,
      applicableStyles: [], // Legacy data doesn't have styles
      colors: colorsData,
      colorDescription: colorsData.isNotEmpty 
          ? colorsData.map((c) => '${c.percentage.toStringAsFixed(1)}% ${c.name}').join(', ')
          : null,
      confidence: (map['confidence'] as num?)?.toDouble() ?? 0.0,
      detectionMethod: 'Legacy System',
      analyzedAt: map['createdAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['createdAt'] as int)
          : null,
    );
  }

  ClosetItemModel copyWith({
    int? id,
    String? imagePath,
    AIAnalysisData? aiAnalysis,
    List<String>? patterns,
    Map<String, dynamic>? features,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return ClosetItemModel(
      id: id ?? this.id,
      imagePath: imagePath ?? this.imagePath,
      aiAnalysis: aiAnalysis ?? this.aiAnalysis,
      patterns: patterns ?? this.patterns,
      features: features ?? this.features,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  static List<ColorInfo> _parseColors(String? colorsJson) {
    if (colorsJson == null) return [];
    try {
      final List<dynamic> colorsList = jsonDecode(colorsJson);
      return colorsList.map((color) => ColorInfo.fromJson(color)).toList();
    } catch (e) {
      return [];
    }
  }
}

class ClosetDatabaseHelper {
  static Database? _database;

  static Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  static Future<Database> _initDatabase() async {
    final dbPath = await getDatabasesPath();
    final dbPathJoined = path_util.join(dbPath, 'closet.db');

    return await openDatabase(
      dbPathJoined,
      version: 3, // Updated version for new AI analysis schema
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE closet_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imagePath TEXT NOT NULL,
            aiAnalysis TEXT,
            clothingType TEXT,
            colors TEXT,
            patterns TEXT,
            confidence REAL DEFAULT 0.0,
            features TEXT,
            createdAt INTEGER,
            updatedAt INTEGER
          )
        ''');
      },
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          // Add columns for basic AI detection data
          await db.execute('ALTER TABLE closet_items ADD COLUMN clothingType TEXT');
          await db.execute('ALTER TABLE closet_items ADD COLUMN colors TEXT');
          await db.execute('ALTER TABLE closet_items ADD COLUMN patterns TEXT');
          await db.execute('ALTER TABLE closet_items ADD COLUMN confidence REAL DEFAULT 0.0');
          await db.execute('ALTER TABLE closet_items ADD COLUMN features TEXT');
          await db.execute('ALTER TABLE closet_items ADD COLUMN createdAt INTEGER');
          await db.execute('ALTER TABLE closet_items ADD COLUMN updatedAt INTEGER');
        }
        if (oldVersion < 3) {
          // Add new AI analysis column
          await db.execute('ALTER TABLE closet_items ADD COLUMN aiAnalysis TEXT');
        }
      },
    );
  }

  static Future<int> insertItem(ClosetItemModel item) async {
    final db = await database;
    return await db.insert('closet_items', {
      'imagePath': item.imagePath,
      'aiAnalysis': item.aiAnalysis != null ? jsonEncode(item.aiAnalysis!.toMap()) : null,
      'clothingType': item.aiAnalysis?.clothingType,
      'colors': jsonEncode(item.colors.map((c) => c.toMap()).toList()),
      'patterns': jsonEncode(item.patterns),
      'confidence': item.confidence,
      'features': jsonEncode(item.features),
      'createdAt': item.createdAt?.millisecondsSinceEpoch,
      'updatedAt': item.updatedAt?.millisecondsSinceEpoch,
    });
  }

  static Future<List<ClosetItemModel>> getAllItems() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('closet_items', orderBy: 'createdAt DESC');
    
    return List.generate(maps.length, (i) {
      return ClosetItemModel.fromMap(maps[i]);
    });
  }

  static Future<List<ClosetItemModel>> getFilteredItems({
    List<String>? clothingTypes,
    List<String>? styles,
    List<String>? colors,
  }) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('closet_items', orderBy: 'createdAt DESC');
    
    List<ClosetItemModel> items = List.generate(maps.length, (i) {
      return ClosetItemModel.fromMap(maps[i]);
    });

    // Apply filters
    if (clothingTypes != null && clothingTypes.isNotEmpty) {
      items = items.where((item) => 
          item.clothingType != null && 
          clothingTypes.any((type) => 
              item.clothingType!.toLowerCase().contains(type.toLowerCase()))).toList();
    }

    if (styles != null && styles.isNotEmpty) {
      items = items.where((item) => 
          item.applicableStyles.any((style) => 
              styles.contains(style))).toList();
    }

    if (colors != null && colors.isNotEmpty) {
      items = items.where((item) => 
          item.colors.any((color) => 
              colors.any((filterColor) => 
                  color.name.toLowerCase().contains(filterColor.toLowerCase())))).toList();
    }

    return items;
  }

  static Future<int> updateItem(ClosetItemModel item) async {
    final db = await database;
    return await db.update(
      'closet_items',
      {
        'imagePath': item.imagePath,
        'aiAnalysis': item.aiAnalysis != null ? jsonEncode(item.aiAnalysis!.toMap()) : null,
        'clothingType': item.aiAnalysis?.clothingType,
        'colors': jsonEncode(item.colors.map((c) => c.toMap()).toList()),
        'patterns': jsonEncode(item.patterns),
        'confidence': item.confidence,
        'features': jsonEncode(item.features),
        'updatedAt': DateTime.now().millisecondsSinceEpoch,
      },
      where: 'id = ?',
      whereArgs: [item.id],
    );
  }

  static Future<int> deleteItem(int id) async {
    final db = await database;
    return await db.delete(
      'closet_items',
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  static Future<List<String>> getUniqueClothingTypes() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'closet_items',
      columns: ['clothingType'],
      distinct: true,
      where: 'clothingType IS NOT NULL',
    );
    
    return maps.map((map) => map['clothingType'] as String).toList();
  }

  static Future<List<String>> getUniqueColors() async {
    final items = await getAllItems();
    final Set<String> uniqueColors = {};
    
    for (final item in items) {
      for (final color in item.colors) {
        uniqueColors.add(color.name);
      }
    }
    
    return uniqueColors.toList()..sort();
  }

  static Future<List<String>> getUniqueStyles() async {
    final items = await getAllItems();
    final Set<String> uniqueStyles = {};
    
    for (final item in items) {
      uniqueStyles.addAll(item.applicableStyles);
    }
    
    return uniqueStyles.toList()..sort();
  }

  static List<ColorInfo> _parseColors(String? colorsJson) {
    if (colorsJson == null) return [];
    try {
      final List<dynamic> colorsList = jsonDecode(colorsJson);
      return colorsList.map((color) => ColorInfo.fromJson(color)).toList();
    } catch (e) {
      return [];
    }
  }

  static List<String> _parsePatterns(String? patternsJson) {
    if (patternsJson == null) return [];
    try {
      final List<dynamic> patternsList = jsonDecode(patternsJson);
      return patternsList.map((pattern) => pattern.toString()).toList();
    } catch (e) {
      return [];
    }
  }

  static Map<String, dynamic> _parseFeatures(String? featuresJson) {
    if (featuresJson == null) return {};
    try {
      final Map<String, dynamic> features = jsonDecode(featuresJson);
      return features;
    } catch (e) {
      return {};
    }
  }
} 