import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/models/exposure_info.dart';

class ImageMetadata {
  final String imageId;
  final String sessionId;
  final String participantId;
  final EyeSide eyeSide;
  final int frameIndex;
  final String imagePath;
  final String captureTimestamp;
  final String phoneManufacturer;
  final String phoneModel;
  final CameraLensDirection cameraLensDirection;
  final CameraLensType cameraLensType;
  final int imageWidth;
  final int imageHeight;
  final double focusScore;
  final ExposureInfo exposureInfo;
  final ImageQualityStatus imageQualityStatus;
  final AnnotationStatus annotationStatus;

  ImageMetadata({
    required this.imageId,
    required this.sessionId,
    required this.participantId,
    required this.eyeSide,
    required this.frameIndex,
    required this.imagePath,
    required this.captureTimestamp,
    required this.phoneManufacturer,
    required this.phoneModel,
    this.cameraLensDirection = CameraLensDirection.front,
    required this.cameraLensType,
    required this.imageWidth,
    required this.imageHeight,
    required this.focusScore,
    required this.exposureInfo,
    required this.imageQualityStatus,
    this.annotationStatus = AnnotationStatus.unannotated,
  });

  Map<String, dynamic> toJson() {
    return {
      'image_id': imageId,
      'session_id': sessionId,
      'participant_id': participantId,
      'eye_side': eyeSide.toJsonValue,
      'frame_index': frameIndex,
      'image_path': imagePath,
      'capture_timestamp': captureTimestamp,
      'phone_manufacturer': phoneManufacturer,
      'phone_model': phoneModel,
      'camera_lens_direction': cameraLensDirection.toJsonValue,
      'camera_lens_type': cameraLensType.toJsonValue,
      'image_width': imageWidth,
      'image_height': imageHeight,
      'focus_score': focusScore,
      'exposure_info': exposureInfo.toJson(),
      'image_quality_status': imageQualityStatus.toJsonValue,
      'annotation_status': annotationStatus.toJsonValue,
    };
  }

  factory ImageMetadata.fromJson(Map<String, dynamic> json) {
    return ImageMetadata(
      imageId: json['image_id'] as String,
      sessionId: json['session_id'] as String,
      participantId: json['participant_id'] as String,
      eyeSide: EyeSideExtension.fromJsonValue(json['eye_side'] as String),
      frameIndex: json['frame_index'] as int,
      imagePath: json['image_path'] as String,
      captureTimestamp: json['capture_timestamp'] as String,
      phoneManufacturer: json['phone_manufacturer'] as String,
      phoneModel: json['phone_model'] as String,
      cameraLensDirection: json['camera_lens_direction'] != null
          ? CameraLensDirectionExtension.fromJsonValue(json['camera_lens_direction'] as String)
          : CameraLensDirection.front,
      cameraLensType: CameraLensTypeExtension.fromJsonValue(json['camera_lens_type'] as String),
      imageWidth: json['image_width'] as int,
      imageHeight: json['image_height'] as int,
      focusScore: (json['focus_score'] as num).toDouble(),
      exposureInfo: ExposureInfo.fromJson(json['exposure_info'] as Map<String, dynamic>),
      imageQualityStatus: ImageQualityStatusExtension.fromJsonValue(json['image_quality_status'] as String),
      annotationStatus: json['annotation_status'] != null 
          ? AnnotationStatusExtension.fromJsonValue(json['annotation_status'] as String) 
          : AnnotationStatus.unannotated,
    );
  }
}
