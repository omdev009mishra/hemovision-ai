import 'package:flutter/material.dart';
import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/models/research_analysis_result.dart';
import 'package:hemovision_capture/screens/prep_screen.dart';
import 'package:hemovision_capture/screens/how_it_works_screen.dart';
import 'package:hemovision_capture/screens/research_details_screen.dart';
import 'package:hemovision_capture/screens/analyzing_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              width: 32,
              height: 32,
              decoration: BoxDecoration(
                color: HemoVisionTheme.redAccent,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Center(
                child: Text('HV', style: TextStyle(fontWeight: FontWeight.w900, color: Colors.white, fontSize: 14)),
              ),
            ),
            const SizedBox(width: 10),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text('HemoVision', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: HemoVisionTheme.textMain)),
                Text('Conjunctival Imaging Research', style: TextStyle(fontSize: 11, color: HemoVisionTheme.textMuted)),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.more_vert),
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
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Hero Section Card
              Card(
                child: Container(
                  padding: const EdgeInsets.all(24.0),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    gradient: LinearGradient(
                      colors: [
                        const Color(0xFF1E293B),
                        HemoVisionTheme.darkCardBg,
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: HemoVisionTheme.tealAccent.withValues(alpha:0.15),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: HemoVisionTheme.tealAccent.withValues(alpha:0.3)),
                        ),
                        child: const Text(
                          'AI-POWERED HEALTH RESEARCH',
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w800,
                            color: HemoVisionTheme.tealAccent,
                            letterSpacing: 0.05,
                          ),
                        ),
                      ),
                      const SizedBox(height: 16),
                      const Text(
                        'Check your blood health\nwith a quick eye scan',
                        style: TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.w800,
                          color: HemoVisionTheme.textMain,
                          height: 1.2,
                        ),
                      ),
                      const SizedBox(height: 10),
                      const Text(
                        'Research estimate from non-invasive smartphone conjunctival imaging.',
                        style: TextStyle(fontSize: 13, color: HemoVisionTheme.textMuted, height: 1.4),
                      ),
                      const SizedBox(height: 20),
                      // Visual Eye Illustration Icon Box
                      Center(
                        child: Container(
                          width: 100,
                          height: 100,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            color: const Color(0xFF0F172A),
                            border: Border.all(color: HemoVisionTheme.tealAccent.withValues(alpha:0.5), width: 2),
                            boxShadow: [
                              BoxShadow(
                                color: HemoVisionTheme.tealAccent.withValues(alpha:0.2),
                                blurRadius: 20,
                                spreadRadius: 5,
                              ),
                            ],
                          ),
                          child: const Icon(
                            Icons.remove_red_eye_outlined,
                            size: 52,
                            color: HemoVisionTheme.tealAccent,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 20),

              // Quick Info Chips
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    _buildChip(Icons.remove_red_eye, '2-Eye Scan'),
                    _buildChip(Icons.timer_outlined, '~30 Seconds'),
                    _buildChip(Icons.memory_outlined, 'On-Device Quality'),
                    _buildChip(Icons.science_outlined, 'Research Prototype'),
                  ],
                ),
              ),

              const SizedBox(height: 24),

              // Primary CTA: SCAN MY EYES
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const PrepScreen()),
                    );
                  },
                  icon: const Icon(Icons.camera_alt, color: Colors.black),
                  label: const Text('SCAN MY EYES'),
                ),
              ),

              const SizedBox(height: 12),

              // Secondary Actions Row
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const HowItWorksScreen()),
                        );
                      },
                      icon: const Icon(Icons.help_outline, size: 18),
                      label: const Text('How It Works'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: () => _showDemoPresetsModal(context),
                      icon: const Icon(Icons.play_circle_outline, size: 18, color: HemoVisionTheme.tealAccent),
                      label: const Text('1-Click Presets', style: TextStyle(color: HemoVisionTheme.tealAccent)),
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 28),

              // Bottom Research Disclaimer
              Center(
                child: Column(
                  children: const [
                    Text(
                      'Research Prototype • Not a Medical Diagnostic Device',
                      style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMuted),
                    ),
                    SizedBox(height: 4),
                    Text(
                      'AI predictions generated by HemoVision must not be used for clinical decisions.',
                      style: TextStyle(fontSize: 11, fontStyle: FontStyle.italic, color: HemoVisionTheme.textMuted),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildChip(IconData icon, String label) {
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        decoration: BoxDecoration(
          color: HemoVisionTheme.darkCardBg,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: HemoVisionTheme.darkCardBorder),
        ),
        child: Row(
          children: [
            Icon(icon, size: 14, color: HemoVisionTheme.tealAccent),
            const SizedBox(width: 6),
            Text(label, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: HemoVisionTheme.textMain)),
          ],
        ),
      ),
    );
  }

  void _showDemoPresetsModal(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: HemoVisionTheme.darkCardBg,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                '⚡ 1-Click Judge Presets (Demo Mode)',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: HemoVisionTheme.textMain),
              ),
              const SizedBox(height: 6),
              const Text(
                'Instantly trigger synthetic sample evaluation for live judge demonstration:',
                style: TextStyle(fontSize: 12, color: HemoVisionTheme.textMuted),
              ),
              const SizedBox(height: 16),
              _buildPresetOption(
                context,
                title: 'Normal Preset (~13.5 g/dL)',
                subtitle: 'Simulated normal palpebral conjunctiva redness',
                onTap: () {
                  Navigator.pop(context);
                  final res = ResearchAnalysisResult.createDemo(simulatedHb: 13.5, demoName: 'DEMO: Normal Hb (~13.5 g/dL)');
                  Navigator.push(context, MaterialPageRoute(builder: (context) => AnalyzingScreen(result: res)));
                },
              ),
              _buildPresetOption(
                context,
                title: 'Mild Anemia Preset (~11.2 g/dL)',
                subtitle: 'Simulated mild conjunctival pallor',
                onTap: () {
                  Navigator.pop(context);
                  final res = ResearchAnalysisResult.createDemo(simulatedHb: 11.2, demoName: 'DEMO: Mild Anemia (~11.2 g/dL)');
                  Navigator.push(context, MaterialPageRoute(builder: (context) => AnalyzingScreen(result: res)));
                },
              ),
              _buildPresetOption(
                context,
                title: 'Severe Anemia Preset (~7.5 g/dL)',
                subtitle: 'Simulated severe conjunctival pallor',
                onTap: () {
                  Navigator.pop(context);
                  final res = ResearchAnalysisResult.createDemo(simulatedHb: 7.5, demoName: 'DEMO: Severe Anemia (~7.5 g/dL)');
                  Navigator.push(context, MaterialPageRoute(builder: (context) => AnalyzingScreen(result: res)));
                },
              ),
              _buildPresetOption(
                context,
                title: 'Quality Failure Preset (Blurry)',
                subtitle: 'Simulated out-of-focus blur quality rejection',
                onTap: () {
                  Navigator.pop(context);
                  final res = ResearchAnalysisResult.createDemo(simulatedHb: 0.0, demoName: 'DEMO: Quality Failure (Blurry)', isQualityFailure: true);
                  Navigator.push(context, MaterialPageRoute(builder: (context) => AnalyzingScreen(result: res)));
                },
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildPresetOption(
    BuildContext context, {
    required String title,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10.0),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: const Color(0xFF1F2937),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: HemoVisionTheme.darkCardBorder),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: HemoVisionTheme.textMain)),
                  const SizedBox(height: 2),
                  Text(subtitle, style: const TextStyle(fontSize: 11, color: HemoVisionTheme.textMuted)),
                ],
              ),
              const Icon(Icons.arrow_forward_ios, size: 14, color: HemoVisionTheme.tealAccent),
            ],
          ),
        ),
      ),
    );
  }
}
