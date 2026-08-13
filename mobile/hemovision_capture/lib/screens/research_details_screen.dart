import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/core/id_generator.dart';
import 'package:hemovision_capture/models/session_metadata.dart';

class ResearchDetailsScreen extends StatelessWidget {
  final SessionMetadata? sessionMetadata;
  final String cameraLensDirection;
  final String cameraLensType;

  const ResearchDetailsScreen({
    super.key,
    this.sessionMetadata,
    this.cameraLensDirection = 'front',
    this.cameraLensType = 'front_facing',
  });

  @override
  Widget build(BuildContext context) {
    final String sessId = sessionMetadata?.sessionId ?? IdGenerator.generateSessionId();
    final String partId = sessionMetadata?.participantId ?? IdGenerator.generateParticipantId();
    final String devId = sessionMetadata?.deviceId ?? IdGenerator.generateDeviceId();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Research & Technical Details'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Technical Metadata & Schema Attributes',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMain),
            ),
            const SizedBox(height: 6),
            const Text(
              'This screen exposes developer and study protocol metadata required for Phase 1/Phase 2 dataset schema alignment.',
              style: TextStyle(fontSize: 13, color: HemoVisionTheme.textMuted),
            ),
            const SizedBox(height: 20),
            _buildDetailCard([
              _buildRow('Session ID (UUID v4)', sessId),
              _buildRow('Synthetic Participant ID', partId),
              _buildRow('Device ID', devId),
              _buildRow('Camera Direction', cameraLensDirection.toUpperCase()),
              _buildRow('Camera Lens Type', cameraLensType),
              _buildRow('Consent Status', 'development_testing'),
              _buildRow('Environment', sessionMetadata?.captureEnvironment.name ?? 'clinical_room'),
              _buildRow('Lighting Condition', sessionMetadata?.lightingCondition.name ?? 'indoor_ambient'),
            ]),
            const SizedBox(height: 20),
            const Text(
              'Pipeline & Model Schema Specs',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMain),
            ),
            const SizedBox(height: 12),
            _buildDetailCard([
              _buildRow('Dataset Schema Draft', 'Draft 2020-12'),
              _buildRow('ML Pipeline Version', 'hv-pipe-v1.0.0'),
              _buildRow('Hb Estimator Architecture', 'Ridge Regression (28 features)'),
              _buildRow('Conformal Coverage Target', '95% Empirical Interval'),
              _buildRow('Laplacian Focus Threshold', 'kFocusScoreThreshold = 100.0'),
              _buildRow('Overexposure Ratio Threshold', '0.15 max'),
            ]),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailCard(List<Widget> children) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(children: children),
      ),
    );
  }

  Widget _buildRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 13, color: HemoVisionTheme.textMuted, fontWeight: FontWeight.w600)),
          Flexible(
            child: Text(
              value,
              textAlign: TextAlign.right,
              style: const TextStyle(fontSize: 13, fontFamily: 'monospace', fontWeight: FontWeight.w700, color: HemoVisionTheme.tealAccent),
            ),
          ),
        ],
      ),
    );
  }
}
