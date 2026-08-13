import 'package:flutter/material.dart';

class QualityIndicator extends StatelessWidget {
  final String status; // 'GOOD', 'WARNING', 'REJECTED', 'UNKNOWN'
  
  const QualityIndicator({super.key, required this.status});

  @override
  Widget build(BuildContext context) {
    Color color;
    String message;
    IconData icon;

    switch (status.toUpperCase()) {
      case 'GOOD':
        color = Colors.green;
        message = 'Image quality acceptable';
        icon = Icons.check_circle;
        break;
      case 'WARNING':
        color = Colors.amber;
        message = 'Review image';
        icon = Icons.warning;
        break;
      case 'REJECTED':
        color = Colors.red;
        message = 'Retake recommended';
        icon = Icons.error;
        break;
      default:
        color = Colors.grey;
        message = 'Quality assessment unavailable';
        icon = Icons.help_outline;
        break;
    }

    return Chip(
      avatar: Icon(icon, color: Colors.white, size: 18),
      label: Text(
        message,
        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
      ),
      backgroundColor: color,
    );
  }
}
