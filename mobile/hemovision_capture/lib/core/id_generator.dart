import 'dart:math';
import 'package:uuid/uuid.dart';

class IdGenerator {
  static const Uuid _uuid = Uuid();
  static final Random _random = Random();

  static String generateSessionId() {
    return _uuid.v4();
  }

  static String generateImageId() {
    return _uuid.v4();
  }

  static String _generateRandomHex(int length) {
    final buffer = StringBuffer();
    for (int i = 0; i < length; i++) {
      buffer.write(_random.nextInt(16).toRadixString(16).toUpperCase());
    }
    return buffer.toString();
  }

  static String generateParticipantId() {
    return 'HV-TEST-P-${_generateRandomHex(8)}';
  }

  static String generateDeviceId() {
    return 'HV-DEV-${_generateRandomHex(8)}';
  }

  static String generateOperatorId() {
    return 'HV-OPR-${_generateRandomHex(8)}';
  }
}
