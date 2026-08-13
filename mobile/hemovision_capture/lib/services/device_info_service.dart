import 'package:device_info_plus/device_info_plus.dart';
import 'dart:io';

class DeviceInfoService {
  String manufacturer = 'unknown';
  String model = 'unknown';
  
  Future<void> initialize() async {
    final DeviceInfoPlugin deviceInfoPlugin = DeviceInfoPlugin();
    try {
      if (Platform.isAndroid) {
        final androidInfo = await deviceInfoPlugin.androidInfo;
        manufacturer = androidInfo.manufacturer;
        model = androidInfo.model;
      } else if (Platform.isIOS) {
        final iosInfo = await deviceInfoPlugin.iosInfo;
        manufacturer = 'Apple';
        model = iosInfo.model;
      }
    } catch (e) {
      // Handle gracefully
    }
  }
}
