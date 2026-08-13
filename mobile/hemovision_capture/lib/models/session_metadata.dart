import 'package:hemovision_capture/core/constants.dart';

class SessionMetadata {
  final String sessionId;
  final String participantId;
  final String sessionTimestamp;
  final String operatorId;
  final CaptureEnvironment captureEnvironment;
  final LightingCondition lightingCondition;
  final double? ambientLux;
  final double? colorTemperatureKelvin;
  final String deviceId;
  final String consentStatus;

  SessionMetadata({
    required this.sessionId,
    required this.participantId,
    required this.sessionTimestamp,
    required this.operatorId,
    required this.captureEnvironment,
    required this.lightingCondition,
    this.ambientLux,
    this.colorTemperatureKelvin,
    required this.deviceId,
    this.consentStatus = 'development_testing',
  });

  Map<String, dynamic> toJson() {
    return {
      'session_id': sessionId,
      'participant_id': participantId,
      'session_timestamp': sessionTimestamp,
      'operator_id': operatorId,
      'capture_environment': captureEnvironment.toJsonValue,
      'lighting_condition': lightingCondition.toJsonValue,
      if (ambientLux != null) 'ambient_lux': ambientLux,
      if (colorTemperatureKelvin != null) 'color_temperature_kelvin': colorTemperatureKelvin,
      'device_id': deviceId,
      'consent_status': consentStatus,
    };
  }

  factory SessionMetadata.fromJson(Map<String, dynamic> json) {
    return SessionMetadata(
      sessionId: json['session_id'] as String,
      participantId: json['participant_id'] as String,
      sessionTimestamp: json['session_timestamp'] as String,
      operatorId: json['operator_id'] as String,
      captureEnvironment: CaptureEnvironmentExtension.fromJsonValue(json['capture_environment'] as String),
      lightingCondition: LightingConditionExtension.fromJsonValue(json['lighting_condition'] as String),
      ambientLux: json['ambient_lux'] != null ? (json['ambient_lux'] as num).toDouble() : null,
      colorTemperatureKelvin: json['color_temperature_kelvin'] != null ? (json['color_temperature_kelvin'] as num).toDouble() : null,
      deviceId: json['device_id'] as String,
      consentStatus: json['consent_status'] as String? ?? 'development_testing',
    );
  }
}
