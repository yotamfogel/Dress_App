class SettingsModel {
  final String userId;
  final Map<String, dynamic> preferences;
  final Map<String, dynamic> appSettings;
  final DateTime lastUpdated;

  const SettingsModel({
    required this.userId,
    this.preferences = const {},
    this.appSettings = const {},
    required this.lastUpdated,
  });

  SettingsModel copyWith({
    String? userId,
    Map<String, dynamic>? preferences,
    Map<String, dynamic>? appSettings,
    DateTime? lastUpdated,
  }) {
    return SettingsModel(
      userId: userId ?? this.userId,
      preferences: preferences ?? this.preferences,
      appSettings: appSettings ?? this.appSettings,
      lastUpdated: lastUpdated ?? this.lastUpdated,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'userId': userId,
      'preferences': preferences,
      'appSettings': appSettings,
      'lastUpdated': lastUpdated.toIso8601String(),
    };
  }

  factory SettingsModel.fromJson(Map<String, dynamic> json) {
    return SettingsModel(
      userId: json['userId'] as String,
      preferences: Map<String, dynamic>.from(json['preferences'] ?? {}),
      appSettings: Map<String, dynamic>.from(json['appSettings'] ?? {}),
      lastUpdated: DateTime.parse(json['lastUpdated'] as String),
    );
  }
} 