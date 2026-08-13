import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/screens/capture_screen.dart';

class PrepScreen extends StatelessWidget {
  const PrepScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Capture Preparation'),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Let's get a clear scan",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.w800, color: HemoVisionTheme.textMain),
              ),
              const SizedBox(height: 8),
              const Text(
                'Follow these simple steps to ensure optimal image quality for the research algorithm.',
                style: TextStyle(fontSize: 14, color: HemoVisionTheme.textMuted),
              ),
              const SizedBox(height: 24),
              _buildCheckItem('Clean your front camera lens'),
              _buildCheckItem('Find a well-lit area (avoid harsh glare)'),
              _buildCheckItem('Hold the phone steady at eye level'),
              _buildCheckItem('Gently pull down your lower eyelid'),
              _buildCheckItem('Align your eye inside the reticle frame'),
              const Spacer(),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(builder: (context) => const CaptureScreen()),
                    );
                  },
                  child: const Text('START SCAN'),
                ),
              ),
              const SizedBox(height: 12),
              const Center(
                child: Text(
                  'This research prototype does not replace a laboratory blood test.',
                  style: TextStyle(fontSize: 11, fontStyle: FontStyle.italic, color: HemoVisionTheme.textMuted),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCheckItem(String text) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10.0),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: HemoVisionTheme.tealAccent.withValues(alpha:0.15),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.check, color: HemoVisionTheme.tealAccent, size: 18),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: HemoVisionTheme.textMain),
            ),
          ),
        ],
      ),
    );
  }
}
