import 'package:flutter/material.dart';

class VersionBanner extends StatelessWidget {
  const VersionBanner({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8.0),
      child: Text(
        'v1.0.0 - Enhanced AI',
        style: TextStyle(
          fontSize: 12,
          color: Colors.grey[600],
        ),
      ),
    );
  }
}