import 'package:hemovision_capture/core/constants.dart';

class ExposureInfo {
  final double meanIntensity;
  final double? overexposedPixelRatio;
  final double? underexposedPixelRatio;
  final ExposureStatus exposureStatus;

  ExposureInfo({
    required this.meanIntensity,
    this.overexposedPixelRatio,
    this.underexposedPixelRatio,
    required this.exposureStatus,
  });

  Map<String, dynamic> toJson() {
    return {
      'mean_intensity': meanIntensity,
      if (overexposedPixelRatio != null) 'overexposed_pixel_ratio': overexposedPixelRatio,
      if (underexposedPixelRatio != null) 'underexposed_pixel_ratio': underexposedPixelRatio,
      'exposure_status': exposureStatus.toJsonValue,
    };
  }

  factory ExposureInfo.fromJson(Map<String, dynamic> json) {
    return ExposureInfo(
      meanIntensity: (json['mean_intensity'] as num).toDouble(),
      overexposedPixelRatio: json['overexposed_pixel_ratio'] != null ? (json['overexposed_pixel_ratio'] as num).toDouble() : null,
      underexposedPixelRatio: json['underexposed_pixel_ratio'] != null ? (json['underexposed_pixel_ratio'] as num).toDouble() : null,
      exposureStatus: ExposureStatusExtension.fromJsonValue(json['exposure_status'] as String),
    );
  }
}
