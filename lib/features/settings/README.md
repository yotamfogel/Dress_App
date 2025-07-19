# Settings Feature

This feature provides a comprehensive settings page with tabs for managing user preferences and app settings.

## Features

### 🎯 **Profile Tab**
- Display user information (name, email)
- Edit profile functionality (placeholder)
- Sign out functionality

### ❤️ **Preferences Tab**
- View all questionnaire responses
- Edit individual preferences
- Reset all preferences
- Automatic saving of changes
- Visual indicators for answered questions

### ⚙️ **App Settings Tab**
- Notifications settings (placeholder)
- Privacy settings (placeholder)
- Help & Support (placeholder)
- About section (placeholder)

## Architecture

### Models
- `SettingsModel` - Main settings data model
- `PreferenceQuestionModel` - Questionnaire question model (from preferences feature)

### Providers
- `SettingsProvider` - Manages app settings state
- `PreferencesProvider` - Manages questionnaire preferences (from preferences feature)

### Pages
- `SettingsPage` - Main settings page with tabbed interface

## Usage

### Navigation
```dart
// Navigate to settings
context.push('/settings');

// Or use the settings button
const SettingsButton();
```

### Accessing Settings Data
```dart
// Watch settings state
final settingsState = ref.watch(settingsProvider);

// Update app setting
ref.read(settingsProvider.notifier).updateAppSetting('notifications', false);

// Update preference
ref.read(settingsProvider.notifier).updatePreference('theme', 'dark');
```

### Accessing Preferences Data
```dart
// Watch preferences state
final preferencesState = ref.watch(preferencesProvider);

// Answer a question
ref.read(preferencesProvider.notifier).answerQuestion('Casual');

// Reset all preferences
ref.read(preferencesProvider.notifier).resetAllPreferences();
```

## Data Persistence

- **Settings**: Stored in SharedPreferences as JSON
- **Preferences**: Stored in SharedPreferences as JSON (from preferences feature)
- **Automatic Saving**: Changes are saved immediately when made

## UI Components

### Settings Tiles
Reusable card-based list tiles for settings options:
```dart
_buildSettingsTile(
  context,
  icon: Icons.notifications,
  title: 'Notifications',
  subtitle: 'Manage notification preferences',
  onTap: () { /* action */ },
)
```

### Preference Cards
Display questionnaire questions with current answers:
```dart
_buildPreferenceCard(context, question)
```

### Edit Dialogs
Modal dialogs for editing preferences:
```dart
_showEditPreferenceDialog(context, question)
```

## Future Enhancements

1. **Profile Management**: Complete profile editing functionality
2. **Theme Settings**: Dark/light mode toggle
3. **Notification Settings**: Push notification preferences
4. **Privacy Settings**: Data usage and privacy controls
5. **Export/Import**: Backup and restore settings
6. **Sync**: Cloud synchronization of settings
7. **Advanced Preferences**: More detailed fashion preferences

## Integration

The settings feature integrates with:
- **Auth Provider**: For user information and sign out
- **Preferences Provider**: For questionnaire data
- **Shared Preferences**: For data persistence
- **Go Router**: For navigation
- **Riverpod**: For state management 