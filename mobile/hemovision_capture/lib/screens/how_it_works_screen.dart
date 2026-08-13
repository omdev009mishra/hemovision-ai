import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';

class HowItWorksScreen extends StatelessWidget {
  const HowItWorksScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('How HemoVision Works'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              '5-Step AI Research Pipeline',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: HemoVisionTheme.textMain),
            ),
            const SizedBox(height: 6),
            const Text(
              'Understand how palpebral conjunctiva optical reflection is processed for non-invasive health screening.',
              style: TextStyle(fontSize: 13, color: HemoVisionTheme.textMuted),
            ),
            const SizedBox(height: 24),
            _buildStepCard(
              stepNumber: '1',
              title: 'Guided Eye Capture',
              description: 'Your smartphone camera captures high-resolution burst images of the lower eyelid palpebral conjunctiva.',
              icon: Icons.camera_alt_outlined,
            ),
            _buildStepCard(
              stepNumber: '2',
              title: 'Quality Gating',
              description: 'On-device algorithms check focus blur (Laplacian variance), luminance over/underexposure, and motion stability.',
              icon: Icons.high_quality_outlined,
            ),
            _buildStepCard(
              stepNumber: '3',
              title: 'Conjunctiva ROI Localization',
              description: 'Color-space segmentation (HSV + LAB a*) isolates the inner mucosal tissue from sclera and skin.',
              icon: Icons.crop_free_outlined,
            ),
            _buildStepCard(
              stepNumber: '4',
              title: 'Color & Spectral Analysis',
              description: 'Extracts 28 chromaticity, redness (a*), yellowness (b*), and spectral reflectance proxy features.',
              icon: Icons.palette_outlined,
            ),
            _buildStepCard(
              stepNumber: '5',
              title: 'Research Model & Conformal Interval',
              description: 'Generates a continuous Hb estimate (g/dL) with a 95% conformal prediction interval and reliability score.',
              icon: Icons.analytics_outlined,
            ),
            const SizedBox(height: 16),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  children: const [
                    Icon(Icons.info_outline, color: HemoVisionTheme.tealAccent, size: 28),
                    SizedBox(height: 8),
                    Text(
                      'Research Disclaimer',
                      style: TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMain),
                    ),
                    SizedBox(height: 4),
                    Text(
                      'This prototype is an investigational research project. It is not clinically validated and must not be used for medical diagnosis.',
                      textAlign: TextAlign.center,
                      style: TextStyle(fontSize: 12, color: HemoVisionTheme.textMuted),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStepCard({
    required String stepNumber,
    required String title,
    required String description,
    required IconData icon,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16.0),
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: HemoVisionTheme.tealAccent.withValues(alpha:0.15),
                  shape: BoxShape.circle,
                ),
                child: Center(
                  child: Text(
                    stepNumber,
                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: HemoVisionTheme.tealAccent),
                  ),
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMain)),
                    const SizedBox(height: 4),
                    Text(description, style: const TextStyle(fontSize: 13, color: HemoVisionTheme.textMuted, height: 1.35)),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
