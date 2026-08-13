class ReferenceRangeConfig {
  final double lowerBound;
  final double upperBound;
  final String population;
  final String protocolVersion;
  final String source;
  final String status;

  const ReferenceRangeConfig({
    this.lowerBound = 12.0,
    this.upperBound = 17.5,
    this.population = 'Adult General Population',
    this.protocolVersion = 'HV-STUDY-PROP-V1',
    this.source = 'Study Reference Config',
    this.status = 'Configured for research prototype',
  });

  String get formattedRange => '${lowerBound.toStringAsFixed(1)} – ${upperBound.toStringAsFixed(1)} g/dL';

  bool isWithin(double hb) => hb >= lowerBound && hb <= upperBound;
  bool isBelow(double hb) => hb < lowerBound;
  bool isAbove(double hb) => hb > upperBound;
}
