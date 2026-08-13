import 'package:hemovision_capture/core/constants.dart';

class CaptureSettings {
  final CaptureEnvironment environment;
  final LightingCondition lightingCondition;
  final double? ambientLux;
  final double? colorTemperatureKelvin;

  CaptureSettings({
    required this.environment,
    required this.lightingCondition,
    this.ambientLux,
    this.colorTemperatureKelvin,
  });

  Map<String, dynamic> toJson() {
    return {
      'environment': environment.toJsonValue,
      'lighting_condition': lightingCondition.toJsonValue,
      if (ambientLux != null) 'ambient_lux': ambientLux,
      if (colorTemperatureKelvin != null) 'color_temperature_kelvin': colorTemperatureKelvin,
    };
  }

  factory CaptureSettings.fromJson(Map<String, dynamic> json) {
    return CaptureSettings(
      environment: CaptureEnvironmentExtension.fromJsonValue(json['environment'] as String),
      lightingCondition: LightingConditionExtension.fromJsonValue(json['lighting_condition'] as String),
      ambientLux: json['ambient_lux'] != null ? (json['ambient_lux'] as num).toDouble() : null,
      colorTemperatureKelvin: json['color_temperature_kelvin'] != null ? (json['color_temperature_kelvin'] as num).toDouble() : null,
    );
  }
}
