import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../data/models/settings_model.dart';
import '../../../../core/providers/app_providers.dart';

class SettingsState {
  final SettingsModel? settings;
  final bool isLoading;
  final String? error;

  const SettingsState({
    this.settings,
    this.isLoading = false,
    this.error,
  });

  SettingsState copyWith({
    SettingsModel? settings,
    bool? isLoading,
    String? error,
  }) {
    return SettingsState(
      settings: settings ?? this.settings,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }
}

class SettingsNotifier extends StateNotifier<SettingsState> {
  final SharedPreferences _prefs;
  static const String _settingsKey = 'user_settings';

  SettingsNotifier(this._prefs) : super(const SettingsState()) {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    state = state.copyWith(isLoading: true);

    try {
      final settingsJson = _prefs.getString(_settingsKey);
      if (settingsJson != null) {
        final Map<String, dynamic> settingsMap = jsonDecode(settingsJson);
        final settings = SettingsModel.fromJson(settingsMap);
        state = state.copyWith(
          settings: settings,
          isLoading: false,
        );
      } else {
        // Create default settings
        final defaultSettings = SettingsModel(
          userId: 'default_user',
          preferences: {},
          appSettings: {
            'notifications': true,
            'darkMode': false,
            'autoSave': true,
          },
          lastUpdated: DateTime.now(),
        );
        await _saveSettings(defaultSettings);
        state = state.copyWith(
          settings: defaultSettings,
          isLoading: false,
        );
      }
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  Future<void> _saveSettings(SettingsModel settings) async {
    final settingsJson = jsonEncode(settings.toJson());
    await _prefs.setString(_settingsKey, settingsJson);
  }

  Future<void> updatePreference(String key, dynamic value) async {
    if (state.settings == null) return;

    try {
      final updatedPreferences = Map<String, dynamic>.from(state.settings!.preferences);
      updatedPreferences[key] = value;

      final updatedSettings = state.settings!.copyWith(
        preferences: updatedPreferences,
        lastUpdated: DateTime.now(),
      );

      await _saveSettings(updatedSettings);
      state = state.copyWith(settings: updatedSettings);
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  Future<void> updateAppSetting(String key, dynamic value) async {
    if (state.settings == null) return;

    try {
      final updatedAppSettings = Map<String, dynamic>.from(state.settings!.appSettings);
      updatedAppSettings[key] = value;

      final updatedSettings = state.settings!.copyWith(
        appSettings: updatedAppSettings,
        lastUpdated: DateTime.now(),
      );

      await _saveSettings(updatedSettings);
      state = state.copyWith(settings: updatedSettings);
    } catch (e) {
      state = state.copyWith(error: e.toString());
    }
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}

final settingsProvider = StateNotifierProvider<SettingsNotifier, SettingsState>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return SettingsNotifier(prefs);
}); 