import 'package:flutter_test/flutter_test.dart';
import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/models/image_metadata.dart';
import 'package:hemovision_capture/models/exposure_info.dart';

void main() {
  group('Camera Metadata & Enum Tests', () {
    test('CameraLensDirection extension toJsonValue and fromJsonValue', () {
      expect(CameraLensDirection.front.toJsonValue, 'front');
      expect(CameraLensDirection.back.toJsonValue, 'back');
      expect(CameraLensDirectionExtension.fromJsonValue('front'), CameraLensDirection.front);
      expect(CameraLensDirectionExtension.fromJsonValue('back'), CameraLensDirection.back);
    });

    test('ImageMetadata serializes camera_lens_direction and camera_lens_type', () {
      final imgMeta = ImageMetadata(
        imageId: 'img-001',
        sessionId: 'sess-001',
        participantId: 'part-001',
        eyeSide: EyeSide.left,
        frameIndex: 0,
        imagePath: 'left/frame_000.jpg',
        captureTimestamp: '2026-08-13T00:00:00Z',
        phoneManufacturer: 'Motorola',
        phoneModel: 'Edge 70',
        cameraLensDirection: CameraLensDirection.back,
        cameraLensType: CameraLensType.mainWide,
        imageWidth: 1920,
        imageHeight: 1080,
        focusScore: 180.0,
        exposureInfo: ExposureInfo(
          meanIntensity: 128.0,
          overexposedPixelRatio: 0.01,
          underexposedPixelRatio: 0.01,
          exposureStatus: ExposureStatus.optimal,
        ),
        imageQualityStatus: ImageQualityStatus.usable,
      );

      final json = imgMeta.toJson();
      expect(json['camera_lens_direction'], 'back');
      expect(json['camera_lens_type'], 'main_wide');
    });
  });
}
