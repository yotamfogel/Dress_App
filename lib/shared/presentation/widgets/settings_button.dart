import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../features/auth/presentation/providers/auth_provider.dart';

class SettingsButton extends ConsumerWidget {
  final bool showSignOut;
  final VoidCallback? onSettingsTap;

  const SettingsButton({
    super.key,
    this.showSignOut = true,
    this.onSettingsTap,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final theme = Theme.of(context);

    return Container(
      width: 48,
      height: 48,
      decoration: BoxDecoration(
        color: theme.colorScheme.primaryContainer,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(24),
          onTap: () {
            if (onSettingsTap != null) {
              onSettingsTap!();
            } else {
              context.push('/settings');
            }
          },
          child: Icon(
            Icons.settings,
            color: theme.colorScheme.onPrimaryContainer,
          ),
        ),
      ),
    );
  }
} 