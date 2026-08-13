import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/models/research_analysis_result.dart';
import 'package:hemovision_capture/widgets/hb_gauge.dart';

class HbResultCard extends StatelessWidget {
  final ResearchAnalysisResult result;

  const HbResultCard({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    Color statusColor;
    String statusText;
    String statusExplanation;

    switch (result.status) {
      case ResearchResultStatus.withinRange:
        statusColor = HemoVisionTheme.greenAccent;
        statusText = 'WITHIN STUDY REFERENCE RANGE';
        statusExplanation =
            'The research model estimate falls within the reference range (${result.referenceRange.formattedRange}) configured for this study.';
        break;
      case ResearchResultStatus.belowRange:
        statusColor = HemoVisionTheme.yellowAccent;
        statusText = 'BELOW STUDY REFERENCE RANGE';
        statusExplanation =
            'The research model estimate is below the reference range (${result.referenceRange.formattedRange}) configured for this study.';
        break;
      case ResearchResultStatus.aboveRange:
        statusColor = HemoVisionTheme.redAccent;
        statusText = 'ABOVE STUDY REFERENCE RANGE';
        statusExplanation =
            'The research model estimate is above the reference range (${result.referenceRange.formattedRange}) configured for this study.';
        break;
      case ResearchResultStatus.unableToDetermine:
        statusColor = HemoVisionTheme.textMuted;
        statusText = 'UNABLE TO DETERMINE';
        statusExplanation = 'Image quality was not sufficient to generate a research estimate. Please recapture.';
        break;
    }

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            if (result.isDemo) ...[
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                decoration: BoxDecoration(
                  color: HemoVisionTheme.tealAccent.withValues(alpha:0.15),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: HemoVisionTheme.tealAccent.withValues(alpha:0.4)),
                ),
                child: Text(
                  result.demoName ?? 'DEMO MODE • SYNTHETIC SAMPLE',
                  style: const TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w800,
                    color: HemoVisionTheme.tealAccent,
                    letterSpacing: 0.05,
                  ),
                ),
              ),
              const SizedBox(height: 16),
            ],
            Text(
              result.isDemo ? 'Simulated Hb (Demo Mode)' : 'Research Hb Estimate',
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w700,
                color: HemoVisionTheme.textMuted,
                letterSpacing: 0.05,
              ),
            ),
            const SizedBox(height: 12),
            if (result.estimatedHb != null) ...[
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.baseline,
                textBaseline: TextBaseline.alphabetic,
                children: [
                  Text(
                    result.estimatedHb!.toStringAsFixed(1),
                    style: const TextStyle(
                      fontSize: 56,
                      fontWeight: FontWeight.w800,
                      color: HemoVisionTheme.textMain,
                      height: 1.0,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    result.unit,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w600,
                      color: HemoVisionTheme.textMuted,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                decoration: BoxDecoration(
                  color: statusColor.withValues(alpha:0.15),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: statusColor, width: 1.2),
                ),
                child: Text(
                  statusText,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w800,
                    color: statusColor,
                    letterSpacing: 0.03,
                  ),
                ),
              ),
              const SizedBox(height: 24),
              HbGauge(
                estimatedHb: result.estimatedHb,
                lowerBound: result.referenceRange.lowerBound,
                upperBound: result.referenceRange.upperBound,
              ),
            ] else ...[
              const Icon(Icons.blur_off, size: 48, color: HemoVisionTheme.yellowAccent),
              const SizedBox(height: 12),
              const Text(
                'Quality Failure',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: HemoVisionTheme.textMain),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                decoration: BoxDecoration(
                  color: HemoVisionTheme.redAccent.withValues(alpha:0.15),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: HemoVisionTheme.redAccent),
                ),
                child: const Text(
                  'RECAPTURE RECOMMENDED',
                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.w800, color: HemoVisionTheme.redAccent),
                ),
              ),
            ],
            const SizedBox(height: 16),
            Text(
              statusExplanation,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 13, color: HemoVisionTheme.textMuted, height: 1.4),
            ),
            const SizedBox(height: 16),
            const Divider(color: HemoVisionTheme.darkCardBorder),
            const SizedBox(height: 8),
            Text(
              result.disclaimer,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 11, fontStyle: FontStyle.italic, color: HemoVisionTheme.textMuted),
            ),
          ],
        ),
      ),
    );
  }
}
