import 'package:camera/camera.dart' hide CameraLensDirection, CameraLensType;
import 'package:camera/camera.dart' as cam show CameraLensDirection;
import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/core/result.dart';

class CameraService {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  CameraDescription? _selectedCamera;

  List<CameraDescription> get availableCamerasList => _cameras ?? [];
  CameraDescription? get selectedCamera => _selectedCamera;

  CameraLensDirection get currentLensDirection {
    if (_selectedCamera == null) return CameraLensDirection.unknown;
    return _selectedCamera!.lensDirection == cam.CameraLensDirection.front
        ? CameraLensDirection.front
        : CameraLensDirection.back;
  }

  CameraLensType get currentLensType {
    if (_selectedCamera == null) return CameraLensType.unknown;
    if (_selectedCamera!.lensDirection == cam.CameraLensDirection.front) {
      return CameraLensType.frontFacing;
    }
    final name = _selectedCamera!.name.toLowerCase();
    if (name.contains('ultra') || name.contains('wide_angle')) {
      return CameraLensType.ultraWide;
    } else if (name.contains('tele') || name.contains('zoom')) {
      return CameraLensType.telephoto;
    }
    return CameraLensType.mainWide;
  }

  Future<Result<void>> initialize({CameraLensDirection targetDirection = CameraLensDirection.front}) async {
    try {
      _cameras = await availableCameras();
      if (_cameras == null || _cameras!.isEmpty) {
        return Result.failure('No cameras available on device', null);
      }

      CameraDescription? targetCam;
      final targetCamDirection = targetDirection == CameraLensDirection.front
          ? cam.CameraLensDirection.front
          : cam.CameraLensDirection.back;

      for (var c in _cameras!) {
        if (c.lensDirection == targetCamDirection) {
          targetCam = c;
          break;
        }
      }

      targetCam ??= _cameras!.first;
      _selectedCamera = targetCam;

      return await _setupController(_selectedCamera!);
    } catch (e) {
      return Result.failure('Failed to initialize camera', e);
    }
  }

  Future<Result<void>> switchCamera() async {
    if (_cameras == null || _cameras!.isEmpty) {
      return Result.failure('No cameras available to switch', null);
    }

    final targetDirection = currentLensDirection == CameraLensDirection.front
        ? CameraLensDirection.back
        : CameraLensDirection.front;

    final targetCamDirection = targetDirection == CameraLensDirection.front
        ? cam.CameraLensDirection.front
        : cam.CameraLensDirection.back;

    CameraDescription? nextCamera;
    for (var c in _cameras!) {
      if (c.lensDirection == targetCamDirection) {
        nextCamera = c;
        break;
      }
    }

    if (nextCamera == null || nextCamera == _selectedCamera) {
      return Result.failure('No alternative camera lens available on this device', null);
    }

    await _controller?.dispose();
    _controller = null;
    _selectedCamera = nextCamera;

    return await _setupController(_selectedCamera!);
  }

  Future<Result<void>> _setupController(CameraDescription camera) async {
    try {
      _controller = CameraController(
        camera,
        ResolutionPreset.high,
        enableAudio: false,
      );
      await _controller!.initialize();
    } catch (_) {
      try {
        _controller = CameraController(
          camera,
          ResolutionPreset.medium,
          enableAudio: false,
        );
        await _controller!.initialize();
      } catch (e) {
        return Result.failure('Failed to setup camera controller', e);
      }
    }

    if (_controller!.value.flashMode != FlashMode.off) {
      try {
        await _controller!.setFlashMode(FlashMode.off);
      } catch (_) {}
    }

    return Result.success(null);
  }

  Future<Result<String>> captureFrame() async {
    if (_controller == null || !_controller!.value.isInitialized) {
      return Result.failure('Camera not initialized', null);
    }

    try {
      final XFile file = await _controller!.takePicture();
      return Result.success(file.path);
    } catch (e) {
      return Result.failure('Failed to capture frame', e);
    }
  }

  Future<Result<List<String>>> captureBurst(int frameCount) async {
    if (_controller == null || !_controller!.value.isInitialized) {
      return Result.failure('Camera not initialized', null);
    }

    try {
      List<String> paths = [];
      for (int i = 0; i < frameCount; i++) {
        final XFile file = await _controller!.takePicture();
        paths.add(file.path);
        if (i < frameCount - 1) {
          await Future.delayed(const Duration(milliseconds: 100));
        }
      }
      return Result.success(paths);
    } catch (e) {
      return Result.failure('Failed to capture burst', e);
    }
  }

  CameraController? get controller => _controller;
  bool get isInitialized => _controller?.value.isInitialized ?? false;

  void dispose() {
    _controller?.dispose();
    _controller = null;
  }
}
