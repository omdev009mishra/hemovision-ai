import 'package:image/image.dart' as img;
import 'package:hemovision_capture/core/constants.dart';
import 'package:hemovision_capture/models/exposure_info.dart';
import 'package:hemovision_capture/models/quality_result.dart';

class QualityEngine {
  /// EXPERIMENTAL — These thresholds are engineering heuristics, NOT clinically validated.
  
  /// Calculate focus score using Laplacian variance approximation.
  /// Works on decoded image bytes.
  static double calculateFocusScore(img.Image image) {
    if (image.width < 3 || image.height < 3) return 0.0;
    
    // Convert to grayscale
    final grayscale = img.grayscale(image);
    
    int sum = 0;
    int sumSquares = 0;
    int count = 0;
    
    // Apply 3x3 Laplacian kernel: [0,1,0; 1,-4,1; 0,1,0]
    for (int y = 1; y < grayscale.height - 1; y++) {
      for (int x = 1; x < grayscale.width - 1; x++) {
        final top = grayscale.getPixel(x, y - 1).r;
        final bottom = grayscale.getPixel(x, y + 1).r;
        final left = grayscale.getPixel(x - 1, y).r;
        final right = grayscale.getPixel(x + 1, y).r;
        final center = grayscale.getPixel(x, y).r;
        
        final laplacian = top + bottom + left + right - (4 * center);
        final int val = laplacian.toInt();
        
        sum += val;
        sumSquares += val * val;
        count++;
      }
    }
    
    if (count == 0) return 0.0;
    
    double mean = sum / count;
    // Return variance of Laplacian response
    double variance = (sumSquares / count) - (mean * mean);
    return variance;
  }
  
  /// Analyze exposure from pixel histogram.
  static ExposureInfo analyzeExposure(img.Image image) {
    int totalPixels = image.width * image.height;
    if (totalPixels == 0) {
      return ExposureInfo(
        meanIntensity: 0,
        overexposedPixelRatio: 0,
        underexposedPixelRatio: 0,
        exposureStatus: ExposureStatus.optimal,
      );
    }
    
    final grayscale = img.grayscale(image);
    double sumIntensity = 0;
    int overexposedCount = 0;
    int underexposedCount = 0;
    
    for (var pixel in grayscale) {
      final intensity = pixel.r;
      sumIntensity += intensity;
      if (intensity > kOverexposedPixelThreshold) overexposedCount++;
      if (intensity < kUnderexposedPixelThreshold) underexposedCount++;
    }
    
    double meanIntensity = sumIntensity / totalPixels;
    double overexposedRatio = overexposedCount / totalPixels;
    double underexposedRatio = underexposedCount / totalPixels;
    
    ExposureStatus status = ExposureStatus.optimal;
    if (overexposedRatio > kOverexposedRatioLimit) {
      status = ExposureStatus.overexposed;
    } else if (underexposedRatio > kUnderexposedRatioLimit) {
      status = ExposureStatus.underexposed;
    }
    
    return ExposureInfo(
      meanIntensity: meanIntensity,
      overexposedPixelRatio: overexposedRatio,
      underexposedPixelRatio: underexposedRatio,
      exposureStatus: status,
    );
  }
  
  /// Determine overall quality status.
  static ImageQualityStatus classifyQuality({
    required double focusScore,
    required ExposureInfo exposure,
    bool? motionStable,
  }) {
    if (focusScore < kFocusScoreThreshold) {
      return ImageQualityStatus.rejectedBlur;
    }
    if (exposure.exposureStatus == ExposureStatus.overexposed ||
        exposure.exposureStatus == ExposureStatus.underexposed) {
      return ImageQualityStatus.rejectedExposure;
    }
    if (motionStable == false) {
      return ImageQualityStatus.rejectedMotion;
    }
    if (motionStable == null) {
      return ImageQualityStatus.unknown;
    }
    return ImageQualityStatus.usable;
  }
  
  /// Run full quality assessment on an image.
  static QualityResult assessImage(img.Image image, {bool? motionStable}) {
    final focusScore = calculateFocusScore(image);
    final exposureInfo = analyzeExposure(image);
    final qualityStatus = classifyQuality(
      focusScore: focusScore,
      exposure: exposureInfo,
      motionStable: motionStable,
    );
    
    return QualityResult(
      focusScore: focusScore,
      exposureInfo: exposureInfo,
      motionStable: motionStable,
      qualityStatus: qualityStatus,
    );
  }
  
  /// Select best frame from burst based on quality scores.
  static int selectBestFrame(List<QualityResult> results) {
    if (results.isEmpty) return -1;
    if (results.length == 1) return 0;
    
    int bestIndex = 0;
    QualityResult bestResult = results[0];
    
    for (int i = 1; i < results.length; i++) {
      final current = results[i];
      
      int currentRank = _getStatusRank(current.qualityStatus);
      int bestRank = _getStatusRank(bestResult.qualityStatus);
      
      if (currentRank > bestRank) {
        bestIndex = i;
        bestResult = current;
      } else if (currentRank == bestRank) {
        if (current.focusScore > bestResult.focusScore) {
          bestIndex = i;
          bestResult = current;
        } else if (current.focusScore == bestResult.focusScore) {
          double currentExposureDist = (current.exposureInfo.meanIntensity - 128).abs();
          double bestExposureDist = (bestResult.exposureInfo.meanIntensity - 128).abs();
          if (currentExposureDist < bestExposureDist) {
            bestIndex = i;
            bestResult = current;
          }
        }
      }
    }
    
    return bestIndex;
  }
  
  static int _getStatusRank(ImageQualityStatus status) {
    switch (status) {
      case ImageQualityStatus.usable:
        return 3;
      case ImageQualityStatus.unknown:
        return 2;
      default:
        return 1;
    }
  }
}
