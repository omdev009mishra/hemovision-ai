import 'package:flutter/material.dart';

class SessionSummaryScreen extends StatelessWidget {
  final String sessionId;
  final int leftEyeFrames;
  final int leftEyeUsable;
  final int rightEyeFrames;
  final int rightEyeUsable;

  const SessionSummaryScreen({
    super.key,
    required this.sessionId,
    required this.leftEyeFrames,
    required this.leftEyeUsable,
    required this.rightEyeFrames,
    required this.rightEyeUsable,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Session Complete'),
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Session ID: $sessionId', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 24),
            const Text('Left Eye', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Text('Total Frames: $leftEyeFrames'),
            Text('Usable Frames: $leftEyeUsable'),
            const SizedBox(height: 16),
            const Text('Right Eye', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Text('Total Frames: $rightEyeFrames'),
            Text('Usable Frames: $rightEyeUsable'),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () {
                  Navigator.of(context).popUntil((route) => route.isFirst);
                },
                child: const Text('NEW SESSION'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
