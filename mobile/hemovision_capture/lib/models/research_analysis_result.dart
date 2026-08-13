import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/models/reference_range_config.dart';

enum ResearchResultStatus {
  withinRange,
  belowRange,
  aboveRange,
  unableToDetermine,
}

class ResearchAnalysisResult {
  final double? estimatedHb;
  final String unit;
  final ResearchResultStatus status;
  final ReferenceRangeConfig referenceRange;
  final ImageQualityStatus qualityStatus;
  final double? reliabilityScore; // e.g. 0.92
  final List<double>? predictionInterval; // [lower, upper]
  final bool isDemo;
  final String? demoName;
  final String pipelineVersion;
  final String modelVersion;
  final String? imagePath;
  final String? roiMaskB64;
  final List<String> rejectionReasons;
  final String disclaimer;

  const ResearchAnalysisResult({
    this.estimatedHb,
    this.unit = 'g/dL',
    required this.status,
    required this.referenceRange,
    required this.qualityStatus,
    this.reliabilityScore,
    this.predictionInterval,
    this.isDemo = false,
    this.demoName,
    this.pipelineVersion = 'hv-pipe-v1.0.0',
    this.modelVersion = 'hb-ridge-v1.0.0',
    this.imagePath,
    this.roiMaskB64,
    this.rejectionReasons = const [],
    this.disclaimer = 'HemoVision is an investigational research prototype. Not a medical diagnostic device.',
  });

  factory ResearchAnalysisResult.fromApiJson(Map<String, dynamic> json, {String? imagePath}) {
    final bool isUsable = json['is_usable'] ?? false;
    final pred = json['prediction'] ?? {};
    final quality = json['quality'] ?? {};
    final double? hb = (pred['estimated_hb_g_dl'] as num?)?.toDouble();

    final config = const ReferenceRangeConfig();
    ResearchResultStatus resStatus = ResearchResultStatus.unableToDetermine;

    if (isUsable && hb != null) {
      if (config.isWithin(hb)) {
        resStatus = ResearchResultStatus.withinRange;
      } else if (config.isBelow(hb)) {
        resStatus = ResearchResultStatus.belowRange;
      } else {
        resStatus = ResearchResultStatus.aboveRange;
      }
    }

    List<double>? interval;
    if (pred['prediction_interval'] != null && pred['prediction_interval'] is List) {
      interval = (pred['prediction_interval'] as List)
          .map((e) => (e as num).toDouble())
          .toList();
    }

    List<String> rejections = [];
    if (quality['rejection_reasons'] != null && quality['rejection_reasons'] is List) {
      rejections = (quality['rejection_reasons'] as List).map((e) => e.toString()).toList();
    }

    return ResearchAnalysisResult(
      estimatedHb: hb,
      status: resStatus,
      referenceRange: config,
      qualityStatus: isUsable ? ImageQualityStatus.usable : ImageQualityStatus.rejectedBlur,
      reliabilityScore: (pred['reliability_score'] as num?)?.toDouble(),
      predictionInterval: interval,
      isDemo: false,
      imagePath: imagePath,
      roiMaskB64: json['visual_overlay_b64'],
      rejectionReasons: rejections,
      disclaimer: json['disclaimer'] ?? 'Research estimate from smartphone conjunctival imaging.',
    );
  }

  factory ResearchAnalysisResult.createDemo({
    required double simulatedHb,
    required String demoName,
    bool isQualityFailure = false,
  }) {
    final config = const ReferenceRangeConfig();
    ResearchResultStatus resStatus = ResearchResultStatus.unableToDetermine;

    if (!isQualityFailure) {
      if (config.isWithin(simulatedHb)) {
        resStatus = ResearchResultStatus.withinRange;
      } else if (config.isBelow(simulatedHb)) {
        resStatus = ResearchResultStatus.belowRange;
      } else {
        resStatus = ResearchResultStatus.aboveRange;
      }
    }

    return ResearchAnalysisResult(
      estimatedHb: isQualityFailure ? null : simulatedHb,
      status: resStatus,
      referenceRange: config,
      qualityStatus: isQualityFailure ? ImageQualityStatus.rejectedBlur : ImageQualityStatus.usable,
      reliabilityScore: isQualityFailure ? null : 0.92,
      predictionInterval: isQualityFailure ? null : [simulatedHb - 0.8, simulatedHb + 0.8],
      isDemo: true,
      demoName: demoName,
      rejectionReasons: isQualityFailure ? ['rejected_blur', 'rejected_exposure'] : [],
      disclaimer: 'DEMO MODE • SYNTHETIC SAMPLE • NOT A REAL PATIENT • NOT A MEDICAL MEASUREMENT',
    );
  }
}
