import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/core/id_generator.dart';
import 'package:hemovision_capture/core/timestamp_utils.dart';
import 'package:hemovision_capture/models/image_metadata.dart';
import 'package:hemovision_capture/models/session_metadata.dart';
import 'package:hemovision_capture/models/quality_result.dart';
import 'package:hemovision_capture/services/device_info_service.dart';

class MetadataService {
  final DeviceInfoService _deviceInfo;

  MetadataService(this._deviceInfo);

  /// Create session metadata.
  SessionMetadata createSessionMetadata({
    required String participantId,
    required CaptureEnvironment environment,
    required LightingCondition lighting,
    double? ambientLux,
    double? colorTemperatureKelvin,
  }) {
    return SessionMetadata(
      sessionId: IdGenerator.generateSessionId(),
      participantId: participantId,
      sessionTimestamp: TimestampUtils.nowIso8601(),
      operatorId: IdGenerator.generateOperatorId(),
      captureEnvironment: environment,
      lightingCondition: lighting,
      ambientLux: ambientLux,
      colorTemperatureKelvin: colorTemperatureKelvin,
      deviceId: IdGenerator.generateDeviceId(),
      consentStatus: 'development_testing',
    );
  }

  /// Create image metadata for a captured frame.
  ImageMetadata createImageMetadata({
    required String sessionId,
    required String participantId,
    required EyeSide eyeSide,
    required int frameIndex,
    required String imagePath,
    required int imageWidth,
    required int imageHeight,
    required QualityResult quality,
    CameraLensDirection cameraLensDirection = CameraLensDirection.front,
    CameraLensType cameraLensType = CameraLensType.frontFacing,
  }) {
    return ImageMetadata(
      imageId: IdGenerator.generateImageId(),
      sessionId: sessionId,
      participantId: participantId,
      eyeSide: eyeSide,
      frameIndex: frameIndex,
      imagePath: imagePath,
      captureTimestamp: TimestampUtils.nowIso8601(),
      phoneManufacturer: _deviceInfo.manufacturer,
      phoneModel: _deviceInfo.model,
      cameraLensDirection: cameraLensDirection,
      cameraLensType: cameraLensType,
      imageWidth: imageWidth,
      imageHeight: imageHeight,
      focusScore: quality.focusScore,
      exposureInfo: quality.exposureInfo,
      imageQualityStatus: quality.qualityStatus,
    );
  }
}
