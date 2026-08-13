import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/models/exposure_info.dart';

class QualityResult {
  final double focusScore;
  final ExposureInfo exposureInfo;
  final bool? motionStable;
  final ImageQualityStatus qualityStatus;

  QualityResult({
    required this.focusScore,
    required this.exposureInfo,
    this.motionStable,
    required this.qualityStatus,
  });

  Map<String, dynamic> toJson() {
    return {
      'focus_score': focusScore,
      'exposure_info': exposureInfo.toJson(),
      if (motionStable != null) 'motion_stable': motionStable,
      'quality_status': qualityStatus.toJsonValue,
    };
  }

  factory QualityResult.fromJson(Map<String, dynamic> json) {
    return QualityResult(
      focusScore: (json['focus_score'] as num).toDouble(),
      exposureInfo: ExposureInfo.fromJson(json['exposure_info'] as Map<String, dynamic>),
      motionStable: json['motion_stable'] as bool?,
      qualityStatus: ImageQualityStatusExtension.fromJsonValue(json['quality_status'] as String),
    );
  }
}
