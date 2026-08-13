import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:image/image.dart' as img;
import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/core/id_generator.dart';
import 'package:hemovision_capture/models/exposure_info.dart';
import 'package:hemovision_capture/models/quality_result.dart';
import 'package:hemovision_capture/models/reference_range_config.dart';
import 'package:hemovision_capture/models/research_analysis_result.dart';
import 'package:hemovision_capture/services/quality_engine.dart';
import 'package:hemovision_capture/widgets/hb_result_card.dart';
import 'package:hemovision_capture/app/app.dart';

void main() {
  group('IdGenerator Tests', () {
    test('generateSessionId returns valid UUID v4', () {
      final id = IdGenerator.generateSessionId();
      expect(id, isNotEmpty);
      expect(id.length, 36);
      expect(id.contains('-'), isTrue);
    });

    test('generateParticipantId format matches HV-TEST-P-XXXXXXXX', () {
      final id = IdGenerator.generateParticipantId();
      expect(id.startsWith('HV-TEST-P-'), isTrue);
      expect(id.length, 18);
    });

    test('generateDeviceId format matches HV-DEV-XXXXXXXX', () {
      final id = IdGenerator.generateDeviceId();
      expect(id.startsWith('HV-DEV-'), isTrue);
      expect(id.length, 15);
    });

    test('generateOperatorId format matches HV-OPR-XXXXXXXX', () {
      final id = IdGenerator.generateOperatorId();
      expect(id.startsWith('HV-OPR-'), isTrue);
      expect(id.length, 15);
    });
  });

  group('QualityEngine Tests', () {
    test('calculateFocusScore returns positive variance for non-uniform image', () {
      final testImage = img.Image(width: 10, height: 10);
      for (int y = 0; y < 10; y++) {
        for (int x = 0; x < 10; x++) {
          if ((x + y) % 2 == 0) {
            testImage.setPixelRgb(x, y, 255, 255, 255);
          } else {
            testImage.setPixelRgb(x, y, 0, 0, 0);
          }
        }
      }
      final score = QualityEngine.calculateFocusScore(testImage);
      expect(score, greaterThan(0.0));
    });

    test('analyzeExposure identifies optimal exposure', () {
      final testImage = img.Image(width: 10, height: 10);
      for (int y = 0; y < 10; y++) {
        for (int x = 0; x < 10; x++) {
          testImage.setPixelRgb(x, y, 128, 128, 128);
        }
      }
      final exposure = QualityEngine.analyzeExposure(testImage);
      expect(exposure.exposureStatus, ExposureStatus.optimal);
      expect(exposure.meanIntensity, closeTo(128.0, 1.0));
    });

    test('classifyQuality classifies usable image', () {
      final exposure = ExposureInfo(
        meanIntensity: 128.0,
        overexposedPixelRatio: 0.0,
        underexposedPixelRatio: 0.0,
        exposureStatus: ExposureStatus.optimal,
      );
      final status = QualityEngine.classifyQuality(
        focusScore: 150.0,
        exposure: exposure,
        motionStable: true,
      );
      expect(status, ImageQualityStatus.usable);
    });

    test('selectBestFrame selects highest focus score among usable frames', () {
      final qr1 = QualityResult(
        focusScore: 110.0,
        exposureInfo: ExposureInfo(meanIntensity: 128, exposureStatus: ExposureStatus.optimal),
        motionStable: true,
        qualityStatus: ImageQualityStatus.usable,
      );
      final qr2 = QualityResult(
        focusScore: 200.0,
        exposureInfo: ExposureInfo(meanIntensity: 128, exposureStatus: ExposureStatus.optimal),
        motionStable: true,
        qualityStatus: ImageQualityStatus.usable,
      );
      final qr3 = QualityResult(
        focusScore: 80.0,
        exposureInfo: ExposureInfo(meanIntensity: 128, exposureStatus: ExposureStatus.optimal),
        motionStable: true,
        qualityStatus: ImageQualityStatus.rejectedBlur,
      );

      final bestIdx = QualityEngine.selectBestFrame([qr1, qr2, qr3]);
      expect(bestIdx, 1);
    });
  });

  group('Reference Range & Research Analysis Result Tests', () {
    test('ReferenceRangeConfig identifies within/below/above range', () {
      final config = const ReferenceRangeConfig(lowerBound: 12.0, upperBound: 17.5);
      expect(config.isWithin(13.5), isTrue);
      expect(config.isBelow(10.5), isTrue);
      expect(config.isAbove(18.0), isTrue);
    });

    test('ResearchAnalysisResult createDemo creates valid result', () {
      final demo = ResearchAnalysisResult.createDemo(simulatedHb: 13.5, demoName: 'Normal Test');
      expect(demo.isDemo, isTrue);
      expect(demo.estimatedHb, 13.5);
      expect(demo.status, ResearchResultStatus.withinRange);
      expect(demo.disclaimer.contains('DEMO MODE'), isTrue);
    });
  });

  group('Widget Tests', () {
    testWidgets('App renders redesigned home screen UI', (WidgetTester tester) async {
      await tester.pumpWidget(const HemoVisionApp());
      expect(find.text('HemoVision'), findsOneWidget);
      expect(find.text('SCAN MY EYES'), findsOneWidget);
      expect(find.text('How It Works'), findsOneWidget);
      expect(find.text('1-Click Presets'), findsOneWidget);
    });

    testWidgets('HbResultCard renders estimated Hb and reference range status', (WidgetTester tester) async {
      final result = ResearchAnalysisResult.createDemo(simulatedHb: 13.5, demoName: 'Normal Test');
      await tester.pumpWidget(MaterialApp(home: Scaffold(body: HbResultCard(result: result))));

      expect(find.text('13.5'), findsOneWidget);
      expect(find.text('g/dL'), findsOneWidget);
      expect(find.text('WITHIN STUDY REFERENCE RANGE'), findsOneWidget);
    });
  });
}
