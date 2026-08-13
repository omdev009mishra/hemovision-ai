class TimestampUtils {
  static String nowIso8601() {
    return DateTime.now().toUtc().toIso8601String();
  }

  static String formatTimestamp(DateTime dt) {
    return dt.toUtc().toIso8601String();
  }
}
