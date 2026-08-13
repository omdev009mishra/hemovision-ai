import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/models/research_analysis_result.dart';
import 'package:hemovision_capture/screens/result_screen.dart';

class AnalyzingScreen extends StatefulWidget {
  final ResearchAnalysisResult result;

  const AnalyzingScreen({super.key, required this.result});

  @override
  State<AnalyzingScreen> createState() => _AnalyzingScreenState();
}

class _AnalyzingScreenState extends State<AnalyzingScreen> {
  int _step = 0;

  @override
  void initState() {
    super.initState();
    _startAnimationSequence();
  }

  void _startAnimationSequence() async {
    await Future.delayed(const Duration(milliseconds: 600));
    if (mounted) setState(() => _step = 1);
    await Future.delayed(const Duration(milliseconds: 600));
    if (mounted) setState(() => _step = 2);
    await Future.delayed(const Duration(milliseconds: 600));
    if (mounted) setState(() => _step = 3);
    await Future.delayed(const Duration(milliseconds: 600));

    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => ResultScreen(result: widget.result)),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const SizedBox(
                width: 64,
                height: 64,
                child: CircularProgressIndicator(
                  strokeWidth: 4,
                  valueColor: AlwaysStoppedAnimation<Color>(HemoVisionTheme.tealAccent),
                ),
              ),
              const SizedBox(height: 32),
              const Text(
                'Analyzing your scan',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: HemoVisionTheme.textMain),
              ),
              const SizedBox(height: 8),
              const Text(
                'Processing image through the 5-stage research pipeline...',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 13, color: HemoVisionTheme.textMuted),
              ),
              const SizedBox(height: 36),
              _buildStepTile(0, 'Image quality gating (focus/exposure)'),
              _buildStepTile(1, 'Palpebral conjunctiva ROI localization'),
              _buildStepTile(2, 'Color calibration & chromaticity transform'),
              _buildStepTile(3, 'Research model & conformal interval'),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStepTile(int index, String label) {
    final bool isDone = _step > index;
    final bool isCurrent = _step == index;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Icon(
            isDone
                ? Icons.check_circle
                : (isCurrent ? Icons.hourglass_top : Icons.radio_button_unchecked),
            color: isDone
                ? HemoVisionTheme.greenAccent
                : (isCurrent ? HemoVisionTheme.tealAccent : HemoVisionTheme.darkCardBorder),
            size: 22,
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Text(
              label,
              style: TextStyle(
                fontSize: 14,
                fontWeight: isCurrent || isDone ? FontWeight.w700 : FontWeight.w500,
                color: isDone || isCurrent ? HemoVisionTheme.textMain : HemoVisionTheme.textMuted,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
