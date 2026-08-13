import 'dart:async';
import 'package:sensors_plus/sensors_plus.dart';

class SensorService {
  StreamSubscription? _accelSubscription;
  double _lastMagnitude = 0;
  bool _isStable = true;
  
  static const double _stabilityThreshold = 0.5;
  
  /// Start monitoring device stability.
  void startMonitoring() {
    try {
      _accelSubscription = accelerometerEventStream().listen((AccelerometerEvent event) {
        double magnitude = event.x * event.x + event.y * event.y + event.z * event.z;
        double diff = (magnitude - _lastMagnitude).abs();
        
        if (_lastMagnitude != 0) {
          _isStable = diff < _stabilityThreshold;
        }
        _lastMagnitude = magnitude;
      }, onError: (error) {
        _isStable = true;
      });
    } catch (e) {
      _isStable = true;
    }
  }
  
  /// Stop monitoring.
  void stopMonitoring() {
    _accelSubscription?.cancel();
    _accelSubscription = null;
  }
  
  /// Get current stability assessment.
  /// Returns null if sensor unavailable.
  bool? get isStable => _accelSubscription != null ? _isStable : null;
  
  /// Get ambient lux if available.
  /// NOTE: sensors_plus may not support light sensor directly.
  /// If not available, return null gracefully.
  double? get ambientLux => null;
  
  void dispose() {
    stopMonitoring();
  }
}
