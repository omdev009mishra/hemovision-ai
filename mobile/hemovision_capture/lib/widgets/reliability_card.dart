import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';

class ReliabilityCard extends StatelessWidget {
  final double? score;

  const ReliabilityCard({super.key, this.score});

  @override
  Widget build(BuildContext context) {
    final bool hasValue = score != null;
    final String label = hasValue ? '${(score! * 100).toInt()}%' : 'Experimental';
    final String subtext = hasValue
        ? 'Research model reliability indicator'
        : 'Reliability calibration pending study validation';

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: HemoVisionTheme.tealAccent.withValues(alpha:0.12),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Icon(Icons.verified_outlined, color: HemoVisionTheme.tealAccent, size: 24),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Analysis Reliability',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMuted),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    label,
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: HemoVisionTheme.textMain),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    subtext,
                    style: const TextStyle(fontSize: 11, color: HemoVisionTheme.textMuted),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
