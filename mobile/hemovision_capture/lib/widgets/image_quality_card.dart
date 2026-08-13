import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/core/constants.dart';

class ImageQualityCard extends StatelessWidget {
  final ImageQualityStatus status;
  final List<String> rejectionReasons;

  const ImageQualityCard({
    super.key,
    required this.status,
    this.rejectionReasons = const [],
  });

  @override
  Widget build(BuildContext context) {
    final bool isGood = status == ImageQualityStatus.usable;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Image Quality Gating',
                  style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMain),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: (isGood ? HemoVisionTheme.greenAccent : HemoVisionTheme.redAccent).withValues(alpha:0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: isGood ? HemoVisionTheme.greenAccent : HemoVisionTheme.redAccent),
                  ),
                  child: Text(
                    isGood ? '✓ GOOD' : '✕ REJECTED',
                    style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w800,
                      color: isGood ? HemoVisionTheme.greenAccent : HemoVisionTheme.redAccent,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildMetricItem('Focus', isGood || !rejectionReasons.contains('rejected_blur')),
                _buildMetricItem('Exposure', isGood || !rejectionReasons.contains('rejected_exposure')),
                _buildMetricItem('Motion', isGood || !rejectionReasons.contains('rejected_motion')),
                _buildMetricItem('Framing', isGood || !rejectionReasons.contains('rejected_framing')),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricItem(String label, bool passed) {
    return Column(
      children: [
        Icon(
          passed ? Icons.check_circle_outline : Icons.cancel_outlined,
          color: passed ? HemoVisionTheme.greenAccent : HemoVisionTheme.redAccent,
          size: 20,
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: HemoVisionTheme.textMuted),
        ),
        Text(
          passed ? 'Pass' : 'Fail',
          style: TextStyle(
            fontSize: 11,
            fontWeight: FontWeight.w700,
            color: passed ? HemoVisionTheme.greenAccent : HemoVisionTheme.redAccent,
          ),
        ),
      ],
    );
  }
}
