import 'dart:io';
import 'dart:convert';
import 'package:path_provider/path_provider.dart';
import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/models/session_metadata.dart';
import 'package:hemovision_capture/models/image_metadata.dart';

/// Application-private local storage for development research prototype.
class StorageService {
  /// Get the base directory for hemovision data.
  Future<String> getBaseDirectory() async {
    final directory = await getApplicationDocumentsDirectory();
    return '${directory.path}/hemovision_data/sessions';
  }

  /// Create session directory structure.
  Future<String> createSessionDirectory(String sessionId) async {
    final base = await getBaseDirectory();
    final sessionDir = '$base/$sessionId';

    await Directory(sessionDir).create(recursive: true);
    await Directory('$sessionDir/left_eye').create(recursive: true);
    await Directory('$sessionDir/right_eye').create(recursive: true);

    return sessionDir;
  }

  /// Get subdirectory name for an eye side.
  String _eyeSubdir(EyeSide eyeSide) {
    switch (eyeSide) {
      case EyeSide.left: return 'left_eye';
      case EyeSide.right: return 'right_eye';
      case EyeSide.unknown: return 'unknown_eye';
    }
  }

  /// Save image file to correct eye subdirectory.
  Future<String> saveImage({
    required String sessionDir,
    required String sourcePath,
    required EyeSide eyeSide,
    required int frameIndex,
  }) async {
    final eyeDir = _eyeSubdir(eyeSide);
    final fileName = 'frame_${frameIndex.toString().padLeft(3, '0')}.jpg';
    final relativePath = '$eyeDir/$fileName';
    final destinationPath = '$sessionDir/$relativePath';

    final file = File(sourcePath);
    await file.copy(destinationPath);

    return relativePath;
  }

  /// Save JSON metadata file.
  Future<void> saveMetadataJson({
    required String filePath,
    required Map<String, dynamic> json,
  }) async {
    final file = File(filePath);
    final encoder = JsonEncoder.withIndent('  ');
    await file.writeAsString(encoder.convert(json));
  }

  /// Save session metadata.
  Future<void> saveSessionMetadata(String sessionDir, SessionMetadata metadata) async {
    await saveMetadataJson(
      filePath: '$sessionDir/session_metadata.json',
      json: metadata.toJson(),
    );
  }

  /// Save image metadata sidecar file.
  Future<void> saveImageMetadata(
    String sessionDir,
    EyeSide eye,
    int frameIndex,
    ImageMetadata metadata,
  ) async {
    final eyeDir = _eyeSubdir(eye);
    final fileName = 'frame_${frameIndex.toString().padLeft(3, '0')}_metadata.json';
    await saveMetadataJson(
      filePath: '$sessionDir/$eyeDir/$fileName',
      json: metadata.toJson(),
    );
  }
}
