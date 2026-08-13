import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/models/research_analysis_result.dart';
import 'package:hemovision_capture/widgets/hb_result_card.dart';
import 'package:hemovision_capture/widgets/reliability_card.dart';
import 'package:hemovision_capture/widgets/prediction_interval_card.dart';
import 'package:hemovision_capture/widgets/image_quality_card.dart';
import 'package:hemovision_capture/widgets/conjunctiva_preview_card.dart';
import 'package:hemovision_capture/screens/prep_screen.dart';
import 'package:hemovision_capture/screens/research_details_screen.dart';
import 'package:hemovision_capture/screens/how_it_works_screen.dart';

class ResultScreen extends StatelessWidget {
  final ResearchAnalysisResult result;

  const ResultScreen({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Analysis Result'),
        actions: [
          IconButton(
            icon: const Icon(Icons.tune_outlined),
            tooltip: 'Research Details',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ResearchDetailsScreen()),
              );
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            HbResultCard(result: result),
            const SizedBox(height: 16),
            ReliabilityCard(score: result.reliabilityScore),
            const SizedBox(height: 16),
            PredictionIntervalCard(interval: result.predictionInterval),
            const SizedBox(height: 16),
            ImageQualityCard(
              status: result.qualityStatus,
              rejectionReasons: result.rejectionReasons,
            ),
            const SizedBox(height: 16),
            ConjunctivaPreviewCard(
              imagePath: result.imagePath,
              roiMaskB64: result.roiMaskB64,
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: () {
                      Navigator.pushAndRemoveUntil(
                        context,
                        MaterialPageRoute(builder: (context) => const PrepScreen()),
                        (route) => route.isFirst,
                      );
                    },
                    child: const Text('SCAN AGAIN'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => const ResearchDetailsScreen()),
                      );
                    },
                    child: const Text('VIEW DETAILS'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton(
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => const HowItWorksScreen()),
                      );
                    },
                    child: const Text('HOW IT WORKS'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
            const Text(
              'HemoVision is an investigational research project. Not a certified medical device or clinical diagnostic tool.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 11, fontStyle: FontStyle.italic, color: HemoVisionTheme.textMuted),
            ),
          ],
        ),
      ),
    );
  }
}
