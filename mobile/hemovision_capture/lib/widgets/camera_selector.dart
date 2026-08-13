import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/core/constants.dart';

class CameraSelector extends StatelessWidget {
  final CameraLensDirection currentDirection;
  final VoidCallback onSwitch;
  final bool isSwitching;

  const CameraSelector({
    super.key,
    required this.currentDirection,
    required this.onSwitch,
    this.isSwitching = false,
  });

  @override
  Widget build(BuildContext context) {
    final isFront = currentDirection == CameraLensDirection.front;
    final label = isFront ? 'FRONT CAMERA' : 'REAR CAMERA';

    return GestureDetector(
      onTap: isSwitching ? null : onSwitch,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: Colors.black.withValues(alpha: 0.8),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: HemoVisionTheme.darkCardBorder, width: 1.2),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (isSwitching)
              const SizedBox(
                width: 14,
                height: 14,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: HemoVisionTheme.tealAccent,
                ),
              )
            else
              const Icon(
                Icons.flip_camera_ios_rounded,
                color: HemoVisionTheme.tealAccent,
                size: 16,
              ),
            const SizedBox(width: 8),
            Text(
              label,
              style: const TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w700,
                color: Colors.white,
                letterSpacing: 0.05,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
