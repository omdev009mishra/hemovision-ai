import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';

class HbGauge extends StatelessWidget {
  final double? estimatedHb;
  final double lowerBound;
  final double upperBound;

  const HbGauge({
    super.key,
    required this.estimatedHb,
    this.lowerBound = 12.0,
    this.upperBound = 17.5,
  });

  @override
  Widget build(BuildContext context) {
    if (estimatedHb == null) return const SizedBox.shrink();

    // Map Hb value to range fraction [0.0, 1.0] (Visual range 6.0 to 20.0)
    final double minVal = 6.0;
    final double maxVal = 20.0;
    final double clampedHb = estimatedHb!.clamp(minVal, maxVal);
    final double fraction = (clampedHb - minVal) / (maxVal - minVal);

    final double lowerFraction = (lowerBound - minVal) / (maxVal - minVal);
    final double upperFraction = (upperBound - minVal) / (maxVal - minVal);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: const [
            Text('LOW (6.0)', style: TextStyle(fontSize: 11, color: HemoVisionTheme.textMuted, fontWeight: FontWeight.w600)),
            Text('STUDY REFERENCE RANGE', style: TextStyle(fontSize: 11, color: HemoVisionTheme.tealAccent, fontWeight: FontWeight.w700)),
            Text('HIGH (20.0)', style: TextStyle(fontSize: 11, color: HemoVisionTheme.textMuted, fontWeight: FontWeight.w600)),
          ],
        ),
        const SizedBox(height: 8),
        Stack(
          children: [
            // Base track
            Container(
              height: 12,
              decoration: BoxDecoration(
                color: const Color(0xFF1F2937),
                borderRadius: BorderRadius.circular(6),
              ),
            ),
            // Reference range track highlight
            Positioned(
              left: MediaQuery.of(context).size.width * lowerFraction * 0.8,
              width: MediaQuery.of(context).size.width * (upperFraction - lowerFraction) * 0.8,
              top: 0,
              bottom: 0,
              child: Container(
                decoration: BoxDecoration(
                  color: HemoVisionTheme.tealAccent.withValues(alpha:0.25),
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: HemoVisionTheme.tealAccent.withValues(alpha:0.5), width: 1),
                ),
              ),
            ),
            // Current value indicator dot
            FractionallySizedBox(
              widthFactor: fraction.clamp(0.05, 0.95),
              child: Align(
                alignment: Alignment.centerRight,
                child: Container(
                  width: 20,
                  height: 20,
                  transform: Matrix4.translationValues(10, -4, 0),
                  decoration: BoxDecoration(
                    color: HemoVisionTheme.textMain,
                    shape: BoxShape.circle,
                    border: Border.all(color: HemoVisionTheme.tealAccent, width: 3),
                    boxShadow: [
                      BoxShadow(
                        color: HemoVisionTheme.tealAccent.withValues(alpha:0.6),
                        blurRadius: 8,
                        spreadRadius: 2,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }
}
