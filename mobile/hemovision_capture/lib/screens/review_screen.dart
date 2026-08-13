import 'package:flutter/material.dart';
import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/models/quality_result.dart';
import 'package:hemovision_capture/widgets/quality_indicator.dart';

class ReviewScreen extends StatelessWidget {
  final List<String> framePaths;
  final List<QualityResult> qualityResults;
  final int bestFrameIndex;
  final EyeSide eyeSide;

  const ReviewScreen({
    super.key,
    required this.framePaths,
    required this.qualityResults,
    required this.bestFrameIndex,
    required this.eyeSide,
  });

  String _getIndicatorStatus(ImageQualityStatus status) {
    switch (status) {
      case ImageQualityStatus.usable:
        return 'GOOD';
      case ImageQualityStatus.pendingReview:
      case ImageQualityStatus.unknown:
        return 'WARNING';
      default:
        return 'REJECTED';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Review ${eyeSide == EyeSide.left ? 'Left' : 'Right'} Eye',
        ),
        automaticallyImplyLeading: false,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: framePaths.length,
              itemBuilder: (context, index) {
                final isBest = index == bestFrameIndex;
                final quality = qualityResults[index];

                return Container(
                  color: isBest
                      ? Theme.of(context)
                            .colorScheme
                            .primaryContainer
                            .withAlpha(77)
                      : null,
                  child: ListTile(
                    leading: isBest
                        ? const Icon(Icons.star, color: Colors.amber)
                        : const Icon(Icons.image),
                    title: Text('Frame ${index + 1}${isBest ? ' (Best)' : ''}'),
                    subtitle: Text(
                      'Focus: ${quality.focusScore.toStringAsFixed(1)}\n'
                      'Exposure: ${quality.exposureInfo.exposureStatus.toJsonValue}',
                    ),
                    trailing: QualityIndicator(
                      status: _getIndicatorStatus(quality.qualityStatus),
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                OutlinedButton(
                  onPressed: () => Navigator.pop(context, false),
                  child: const Text('RETAKE'),
                ),
                ElevatedButton(
                  onPressed: () => Navigator.pop(context, true),
                  child: const Text('ACCEPT'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
