// Schema-aligned enums matching Phase 1 dataset contract.
// All thresholds are EXPERIMENTAL / UNVALIDATED engineering heuristics.

const String appVersion = '0.2.0';
const String schemaVersion = '1.0.0';

// Quality thresholds — EXPERIMENTAL, NOT clinically validated
const double kFocusScoreThreshold = 100.0;
const double kOverexposedPixelThreshold = 240.0;
const double kUnderexposedPixelThreshold = 15.0;
const double kOverexposedRatioLimit = 0.15;
const double kUnderexposedRatioLimit = 0.15;
const int kDefaultBurstFrameCount = 3;
const int kMaxBurstFrameCount = 5;
const int kMinBurstFrameCount = 3;

enum EyeSide { left, right, unknown }

extension EyeSideExtension on EyeSide {
  String get toJsonValue {
    switch (this) {
      case EyeSide.left: return 'left';
      case EyeSide.right: return 'right';
      case EyeSide.unknown: return 'unknown';
    }
  }

  static EyeSide fromJsonValue(String value) {
    switch (value) {
      case 'left': return EyeSide.left;
      case 'right': return EyeSide.right;
      default: return EyeSide.unknown;
    }
  }
}

enum CaptureEnvironment { clinicalRoom, fieldClinic, household, outdoor, unknown }

extension CaptureEnvironmentExtension on CaptureEnvironment {
  String get toJsonValue {
    switch (this) {
      case CaptureEnvironment.clinicalRoom: return 'clinical_room';
      case CaptureEnvironment.fieldClinic: return 'field_clinic';
      case CaptureEnvironment.household: return 'household';
      case CaptureEnvironment.outdoor: return 'outdoor';
      case CaptureEnvironment.unknown: return 'unknown';
    }
  }

  static CaptureEnvironment fromJsonValue(String value) {
    switch (value) {
      case 'clinical_room': return CaptureEnvironment.clinicalRoom;
      case 'field_clinic': return CaptureEnvironment.fieldClinic;
      case 'household': return CaptureEnvironment.household;
      case 'outdoor': return CaptureEnvironment.outdoor;
      default: return CaptureEnvironment.unknown;
    }
  }
}

enum LightingCondition { indoorAmbient, indoorLedFlash, outdoorShade, directSunlight, controlledLightBox, unknown }

extension LightingConditionExtension on LightingCondition {
  String get toJsonValue {
    switch (this) {
      case LightingCondition.indoorAmbient: return 'indoor_ambient';
      case LightingCondition.indoorLedFlash: return 'indoor_led_flash';
      case LightingCondition.outdoorShade: return 'outdoor_shade';
      case LightingCondition.directSunlight: return 'direct_sunlight';
      case LightingCondition.controlledLightBox: return 'controlled_light_box';
      case LightingCondition.unknown: return 'unknown';
    }
  }

  static LightingCondition fromJsonValue(String value) {
    switch (value) {
      case 'indoor_ambient': return LightingCondition.indoorAmbient;
      case 'indoor_led_flash': return LightingCondition.indoorLedFlash;
      case 'outdoor_shade': return LightingCondition.outdoorShade;
      case 'direct_sunlight': return LightingCondition.directSunlight;
      case 'controlled_light_box': return LightingCondition.controlledLightBox;
      default: return LightingCondition.unknown;
    }
  }
}

enum ConsentStatus { developmentTesting }

extension ConsentStatusExtension on ConsentStatus {
  String get toJsonValue {
    switch (this) {
      case ConsentStatus.developmentTesting: return 'development_testing';
    }
  }

  static ConsentStatus fromJsonValue(String value) {
    switch (value) {
      case 'development_testing': return ConsentStatus.developmentTesting;
      default: return ConsentStatus.developmentTesting;
    }
  }
}

enum ImageQualityStatus { usable, rejectedBlur, rejectedExposure, rejectedMotion, rejectedFraming, pendingReview, unknown }

extension ImageQualityStatusExtension on ImageQualityStatus {
  String get toJsonValue {
    switch (this) {
      case ImageQualityStatus.usable: return 'usable';
      case ImageQualityStatus.rejectedBlur: return 'rejected_blur';
      case ImageQualityStatus.rejectedExposure: return 'rejected_exposure';
      case ImageQualityStatus.rejectedMotion: return 'rejected_motion';
      case ImageQualityStatus.rejectedFraming: return 'rejected_framing';
      case ImageQualityStatus.pendingReview: return 'pending_review';
      case ImageQualityStatus.unknown: return 'unknown';
    }
  }

  static ImageQualityStatus fromJsonValue(String value) {
    switch (value) {
      case 'usable': return ImageQualityStatus.usable;
      case 'rejected_blur': return ImageQualityStatus.rejectedBlur;
      case 'rejected_exposure': return ImageQualityStatus.rejectedExposure;
      case 'rejected_motion': return ImageQualityStatus.rejectedMotion;
      case 'rejected_framing': return ImageQualityStatus.rejectedFraming;
      case 'pending_review': return ImageQualityStatus.pendingReview;
      default: return ImageQualityStatus.unknown;
    }
  }
}

enum ExposureStatus { optimal, overexposed, underexposed }

extension ExposureStatusExtension on ExposureStatus {
  String get toJsonValue {
    switch (this) {
      case ExposureStatus.optimal: return 'optimal';
      case ExposureStatus.overexposed: return 'overexposed';
      case ExposureStatus.underexposed: return 'underexposed';
    }
  }

  static ExposureStatus fromJsonValue(String value) {
    switch (value) {
      case 'optimal': return ExposureStatus.optimal;
      case 'overexposed': return ExposureStatus.overexposed;
      case 'underexposed': return ExposureStatus.underexposed;
      default: return ExposureStatus.optimal;
    }
  }
}

enum AnnotationStatus { unannotated, inReview, annotated, rejectedQuality }

extension AnnotationStatusExtension on AnnotationStatus {
  String get toJsonValue {
    switch (this) {
      case AnnotationStatus.unannotated: return 'unannotated';
      case AnnotationStatus.inReview: return 'in_review';
      case AnnotationStatus.annotated: return 'annotated';
      case AnnotationStatus.rejectedQuality: return 'rejected_quality';
    }
  }

  static AnnotationStatus fromJsonValue(String value) {
    switch (value) {
      case 'unannotated': return AnnotationStatus.unannotated;
      case 'in_review': return AnnotationStatus.inReview;
      case 'annotated': return AnnotationStatus.annotated;
      case 'rejected_quality': return AnnotationStatus.rejectedQuality;
      default: return AnnotationStatus.unannotated;
    }
  }
}

enum CameraLensDirection { front, back, unknown }

extension CameraLensDirectionExtension on CameraLensDirection {
  String get toJsonValue {
    switch (this) {
      case CameraLensDirection.front: return 'front';
      case CameraLensDirection.back: return 'back';
      case CameraLensDirection.unknown: return 'unknown';
    }
  }

  static CameraLensDirection fromJsonValue(String value) {
    switch (value) {
      case 'front': return CameraLensDirection.front;
      case 'back': return CameraLensDirection.back;
      default: return CameraLensDirection.unknown;
    }
  }
}

enum CameraLensType { mainWide, telephoto, ultraWide, frontFacing, unknown }

extension CameraLensTypeExtension on CameraLensType {
  String get toJsonValue {
    switch (this) {
      case CameraLensType.mainWide: return 'main_wide';
      case CameraLensType.telephoto: return 'telephoto';
      case CameraLensType.ultraWide: return 'ultra_wide';
      case CameraLensType.frontFacing: return 'front_facing';
      case CameraLensType.unknown: return 'unknown';
    }
  }

  static CameraLensType fromJsonValue(String value) {
    switch (value) {
      case 'main_wide': return CameraLensType.mainWide;
      case 'telephoto': return CameraLensType.telephoto;
      case 'ultra_wide': return CameraLensType.ultraWide;
      case 'front_facing': return CameraLensType.frontFacing;
      default: return CameraLensType.unknown;
    }
  }
}
