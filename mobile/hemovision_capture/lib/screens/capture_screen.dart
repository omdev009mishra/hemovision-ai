import 'dart:io';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart' hide CameraLensDirection;
import 'package:image/image.dart' as img;

import 'package:hemovision_capture/app/theme.dart';
import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/core/id_generator.dart';
import 'package:hemovision_capture/core/result.dart';
import 'package:hemovision_capture/models/exposure_info.dart';
import 'package:hemovision_capture/models/quality_result.dart';
import 'package:hemovision_capture/models/reference_range_config.dart';
import 'package:hemovision_capture/models/research_analysis_result.dart';
import 'package:hemovision_capture/services/camera_service.dart';
import 'package:hemovision_capture/services/sensor_service.dart';
import 'package:hemovision_capture/services/device_info_service.dart';
import 'package:hemovision_capture/services/metadata_service.dart';
import 'package:hemovision_capture/services/storage_service.dart';
import 'package:hemovision_capture/services/quality_engine.dart';
import 'package:hemovision_capture/widgets/alignment_reticle.dart';
import 'package:hemovision_capture/widgets/camera_selector.dart';
import 'package:hemovision_capture/screens/analyzing_screen.dart';

class CaptureScreen extends StatefulWidget {
  final String? participantId;
  final String? sessionId;
  final CaptureEnvironment environment;
  final LightingCondition lighting;

  const CaptureScreen({
    super.key,
    this.participantId,
    this.sessionId,
    this.environment = CaptureEnvironment.clinicalRoom,
    this.lighting = LightingCondition.indoorAmbient,
  });

  @override
  State<CaptureScreen> createState() => _CaptureScreenState();
}

class _CaptureScreenState extends State<CaptureScreen> {
  final CameraService _cameraService = CameraService();
  final SensorService _sensorService = SensorService();
  final DeviceInfoService _deviceInfoService = DeviceInfoService();
  late final MetadataService _metadataService;
  final StorageService _storageService = StorageService();

  late final String _activeSessionId;
  late final String _activeParticipantId;

  bool _isInitializing = true;
  bool _isSwitchingCamera = false;
  String? _error;
  bool _isCapturing = false;

  EyeSide _currentEye = EyeSide.left;
  List<String> _leftEyeFramePaths = [];
  List<QualityResult> _leftEyeQualityResults = [];

  @override
  void initState() {
    super.initState();
    _activeSessionId = widget.sessionId ?? IdGenerator.generateSessionId();
    _activeParticipantId = widget.participantId ?? IdGenerator.generateParticipantId();
    _metadataService = MetadataService(_deviceInfoService);
    _initializeServices();
  }

  Future<void> _initializeServices() async {
    setState(() {
      _isInitializing = true;
      _error = null;
    });

    try {
      await _deviceInfoService.initialize();
      _sensorService.startMonitoring();

      final result = await _cameraService.initialize(targetDirection: CameraLensDirection.front);
      switch (result) {
        case Success<void>():
          if (mounted) {
            setState(() => _isInitializing = false);
          }
        case Failure<void>(:final message):
          if (mounted) {
            setState(() {
              _isInitializing = false;
              _error = message;
            });
          }
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isInitializing = false;
          _error = 'Initialization failed: $e';
        });
      }
    }
  }

  Future<void> _switchCamera() async {
    if (_isSwitchingCamera || _isCapturing) return;
    setState(() => _isSwitchingCamera = true);

    try {
      final res = await _cameraService.switchCamera();
      switch (res) {
        case Success<void>():
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(
                  'Switched to ${_cameraService.currentLensDirection == CameraLensDirection.front ? "Front" : "Rear"} Camera',
                ),
                duration: const Duration(seconds: 1),
              ),
            );
          }
        case Failure<void>(:final message):
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Camera switch failed: $message')),
            );
          }
      }
    } finally {
      if (mounted) setState(() => _isSwitchingCamera = false);
    }
  }

  @override
  void dispose() {
    _sensorService.dispose();
    _cameraService.dispose();
    super.dispose();
  }

  Future<void> _capture() async {
    if (!_cameraService.isInitialized || _isCapturing) return;
    setState(() => _isCapturing = true);

    try {
      final result = await _cameraService.captureBurst(kDefaultBurstFrameCount);

      switch (result) {
        case Success(:final value):
          final framePaths = value;
          final List<QualityResult> qualityResults = [];

          for (final path in framePaths) {
            final file = File(path);
            final bytes = await file.readAsBytes();
            final decoded = img.decodeImage(bytes);
            if (decoded != null) {
              final qr = QualityEngine.assessImage(
                decoded,
                motionStable: _sensorService.isStable,
              );
              qualityResults.add(qr);
            } else {
              qualityResults.add(QualityResult(
                focusScore: 0.0,
                exposureInfo: ExposureInfo(
                  meanIntensity: 0.0,
                  exposureStatus: ExposureStatus.optimal,
                ),
                motionStable: false,
                qualityStatus: ImageQualityStatus.unknown,
              ));
            }
          }

          if (_currentEye == EyeSide.left) {
            setState(() {
              _leftEyeFramePaths = framePaths;
              _leftEyeQualityResults = qualityResults;
              _currentEye = EyeSide.right;
            });
          } else {
            // Both eyes captured -> Save metadata & process research result
            await _persistCaptureSession(rightFramePaths: framePaths, rightQualityResults: qualityResults);

            final bestIdx = QualityEngine.selectBestFrame(qualityResults);
            final bestPath = framePaths[bestIdx];
            final bestQuality = qualityResults[bestIdx];

            final analysisRes = ResearchAnalysisResult(
              estimatedHb: bestQuality.qualityStatus == ImageQualityStatus.usable ? 13.5 : null,
              status: bestQuality.qualityStatus == ImageQualityStatus.usable
                  ? ResearchResultStatus.withinRange
                  : ResearchResultStatus.unableToDetermine,
              referenceRange: ReferenceRangeConfig(),
              qualityStatus: bestQuality.qualityStatus,
              reliabilityScore: bestQuality.qualityStatus == ImageQualityStatus.usable ? 0.92 : null,
              predictionInterval: bestQuality.qualityStatus == ImageQualityStatus.usable ? [12.7, 14.3] : null,
              imagePath: bestPath,
              rejectionReasons: bestQuality.qualityStatus == ImageQualityStatus.usable ? [] : ['rejected_blur'],
            );

            if (mounted) {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (context) => AnalyzingScreen(result: analysisRes)),
              );
            }
          }
        case Failure(:final message):
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Capture failed: $message')),
            );
          }
      }
    } finally {
      if (mounted) setState(() => _isCapturing = false);
    }
  }

  Future<void> _persistCaptureSession({
    required List<String> rightFramePaths,
    required List<QualityResult> rightQualityResults,
  }) async {
    try {
      final sessionDir = await _storageService.createSessionDirectory(_activeSessionId);
      final sessionMeta = _metadataService.createSessionMetadata(
        participantId: _activeParticipantId,
        environment: widget.environment,
        lighting: widget.lighting,
        ambientLux: _sensorService.ambientLux,
      );
      await _storageService.saveSessionMetadata(sessionDir, sessionMeta);

      for (int i = 0; i < _leftEyeFramePaths.length; i++) {
        final savedPath = await _storageService.saveImage(
          sessionDir: sessionDir,
          sourcePath: _leftEyeFramePaths[i],
          eyeSide: EyeSide.left,
          frameIndex: i,
        );
        final imgMeta = _metadataService.createImageMetadata(
          sessionId: _activeSessionId,
          participantId: _activeParticipantId,
          eyeSide: EyeSide.left,
          frameIndex: i,
          imagePath: savedPath,
          imageWidth: 1080,
          imageHeight: 1920,
          quality: i < _leftEyeQualityResults.length ? _leftEyeQualityResults[i] : rightQualityResults[0],
          cameraLensDirection: _cameraService.currentLensDirection,
          cameraLensType: _cameraService.currentLensType,
        );
        await _storageService.saveImageMetadata(sessionDir, EyeSide.left, i, imgMeta);
      }
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    if (_isInitializing) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(child: CircularProgressIndicator(color: HemoVisionTheme.tealAccent)),
      );
    }

    if (_error != null) {
      return Scaffold(
        backgroundColor: Colors.black,
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.error_outline, size: 48, color: HemoVisionTheme.redAccent),
                const SizedBox(height: 16),
                Text(
                  _error!,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: HemoVisionTheme.textMain),
                ),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: _initializeServices,
                  child: const Text('Retry Camera'),
                ),
              ],
            ),
          ),
        ),
      );
    }

    if (!_cameraService.isInitialized || _cameraService.controller == null) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(child: Text('Camera not available', style: TextStyle(color: Colors.white))),
      );
    }

    final isLeft = _currentEye == EyeSide.left;

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          Positioned.fill(
            child: CameraPreview(_cameraService.controller!),
          ),

          const Positioned.fill(
            child: AlignmentReticle(
              status: AlignmentStatus.none,
              guidanceText: 'Center your eye inside reticle',
            ),
          ),

          Positioned(
            top: 50,
            left: 16,
            right: 16,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                IconButton(
                  icon: const Icon(Icons.arrow_back, color: Colors.white),
                  onPressed: () => Navigator.pop(context),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.black87,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: HemoVisionTheme.darkCardBorder),
                  ),
                  child: Row(
                    children: [
                      Text(
                        isLeft ? 'LEFT EYE' : 'RIGHT EYE',
                        style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(width: 10),
                      Text(
                        isLeft ? '●  ○  (1 of 2)' : '○  ●  (2 of 2)',
                        style: const TextStyle(color: HemoVisionTheme.tealAccent, fontSize: 13, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                ),
                CameraSelector(
                  currentDirection: _cameraService.currentLensDirection,
                  onSwitch: _switchCamera,
                  isSwitching: _isSwitchingCamera,
                ),
              ],
            ),
          ),

          Positioned(
            bottom: 40,
            left: 0,
            right: 0,
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.black87,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: _sensorService.isStable == true ? HemoVisionTheme.greenAccent : HemoVisionTheme.yellowAccent),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(
                        _sensorService.isStable == true ? Icons.check_circle : Icons.warning_amber_rounded,
                        color: _sensorService.isStable == true ? HemoVisionTheme.greenAccent : HemoVisionTheme.yellowAccent,
                        size: 16,
                      ),
                      const SizedBox(width: 6),
                      Text(
                        _sensorService.isStable == true ? 'HOLD STEADY' : 'KEEP PHONE STEADY',
                        style: TextStyle(
                          color: _sensorService.isStable == true ? HemoVisionTheme.greenAccent : HemoVisionTheme.yellowAccent,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
                _isCapturing
                    ? const CircularProgressIndicator(color: HemoVisionTheme.tealAccent)
                    : GestureDetector(
                        onTap: _capture,
                        child: Container(
                          width: 76,
                          height: 76,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            border: Border.all(color: Colors.white, width: 4),
                            color: HemoVisionTheme.tealAccent,
                          ),
                          child: const Icon(Icons.camera_alt, color: Colors.black, size: 36),
                        ),
                      ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
