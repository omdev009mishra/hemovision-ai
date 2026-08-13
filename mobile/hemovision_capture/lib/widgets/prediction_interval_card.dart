import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';

class PredictionIntervalCard extends StatelessWidget {
  final List<double>? interval;

  const PredictionIntervalCard({super.key, this.interval});

  @override
  Widget build(BuildContext context) {
    final bool hasInterval = interval != null && interval!.length == 2;
    final String rangeText = hasInterval
        ? '${interval![0].toStringAsFixed(1)} – ${interval![1].toStringAsFixed(1)} g/dL'
        : 'Prediction interval not validated';

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
              child: const Icon(Icons.show_chart, color: HemoVisionTheme.tealAccent, size: 24),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Conformal Estimated Range (95% CI)',
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMuted),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    rangeText,
                    style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: HemoVisionTheme.textMain),
                  ),
                  const SizedBox(height: 2),
                  const Text(
                    'Empirical research prediction bound',
                    style: TextStyle(fontSize: 11, color: HemoVisionTheme.textMuted),
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
