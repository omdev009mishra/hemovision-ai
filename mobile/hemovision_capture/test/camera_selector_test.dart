import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/widgets/camera_selector.dart';

void main() {
  group('CameraSelector Widget Tests', () {
    testWidgets('Renders FRONT CAMERA label when currentDirection is front', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CameraSelector(
              currentDirection: CameraLensDirection.front,
              onSwitch: () {},
            ),
          ),
        ),
      );

      expect(find.text('FRONT CAMERA'), findsOneWidget);
    });

    testWidgets('Renders REAR CAMERA label when currentDirection is back', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CameraSelector(
              currentDirection: CameraLensDirection.back,
              onSwitch: () {},
            ),
          ),
        ),
      );

      expect(find.text('REAR CAMERA'), findsOneWidget);
    });

    testWidgets('Triggers onSwitch callback when tapped', (WidgetTester tester) async {
      bool tapped = false;
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CameraSelector(
              currentDirection: CameraLensDirection.front,
              onSwitch: () => tapped = true,
            ),
          ),
        ),
      );

      await tester.tap(find.byType(CameraSelector));
      expect(tapped, isTrue);
    });
  });
}
