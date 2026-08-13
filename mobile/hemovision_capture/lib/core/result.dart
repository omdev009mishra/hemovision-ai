/// Generic Result type for operation outcomes.
sealed class Result<T> {
  const Result();

  /// Create a successful result.
  static Result<T> success<T>(T value) => Success<T>(value);

  /// Create a failure result.
  static Result<T> failure<T>(String message, [Object? error]) =>
      Failure<T>(message, error);
}

class Success<T> extends Result<T> {
  final T value;
  const Success(this.value);
}

class Failure<T> extends Result<T> {
  final String message;
  final Object? error;
  const Failure(this.message, [this.error]);
}
