import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hemovision_capture/models/research_analysis_result.dart';
import 'package:hemovision_capture/screens/result_screen.dart';

void main() {
  group('ResultScreen Widget Tests', () {
    testWidgets('ResultScreen renders Analysis Result and action buttons', (WidgetTester tester) async {
      final result = ResearchAnalysisResult.createDemo(simulatedHb: 13.5, demoName: 'Normal Demo');
      await tester.pumpWidget(MaterialApp(home: ResultScreen(result: result)));

      expect(find.text('Analysis Result'), findsOneWidget);
      expect(find.text('SCAN AGAIN'), findsOneWidget);
      expect(find.text('VIEW DETAILS'), findsOneWidget);
    });
  });
}
