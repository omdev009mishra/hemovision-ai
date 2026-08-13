import 'package:flutter/material.dart';

enum AlignmentStatus { none, poor, ok, good }

class AlignmentReticle extends StatelessWidget {
  final AlignmentStatus status;
  final String guidanceText;

  const AlignmentReticle({
    super.key,
    this.status = AlignmentStatus.none,
    this.guidanceText = 'Center the eye',
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        CustomPaint(
          size: const Size(200, 100),
          painter: _ReticlePainter(status: status),
        ),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: Colors.black54,
            borderRadius: BorderRadius.circular(16),
          ),
          child: Text(
            guidanceText,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ],
    );
  }
}

class _ReticlePainter extends CustomPainter {
  final AlignmentStatus status;

  _ReticlePainter({required this.status});

  @override
  void paint(Canvas canvas, Size size) {
    Color color;
    switch (status) {
      case AlignmentStatus.good:
        color = Colors.green;
        break;
      case AlignmentStatus.ok:
        color = Colors.amber;
        break;
      case AlignmentStatus.poor:
        color = Colors.red;
        break;
      case AlignmentStatus.none:
        color = Colors.white70;
        break;
    }

    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final center = Offset(size.width / 2, size.height / 2);
    final rect = Rect.fromCenter(center: center, width: size.width, height: size.height);

    // Draw eye-shaped ellipse
    canvas.drawOval(rect, paint);

    // Draw crosshair
    final crosshairSize = 10.0;
    canvas.drawLine(
      Offset(center.dx - crosshairSize, center.dy),
      Offset(center.dx + crosshairSize, center.dy),
      paint,
    );
    canvas.drawLine(
      Offset(center.dx, center.dy - crosshairSize),
      Offset(center.dx, center.dy + crosshairSize),
      paint,
    );
  }

  @override
  bool shouldRepaint(covariant _ReticlePainter oldDelegate) {
    return oldDelegate.status != status;
  }
}
