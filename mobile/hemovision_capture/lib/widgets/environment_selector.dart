import 'package:flutter/material.dart';
import 'package:hemovision_capture/core/constants.dart';

class EnvironmentSelector extends StatelessWidget {
  final CaptureEnvironment currentEnvironment;
  final LightingCondition currentLighting;
  final ValueChanged<CaptureEnvironment> onEnvironmentChanged;
  final ValueChanged<LightingCondition> onLightingChanged;

  const EnvironmentSelector({
    super.key,
    required this.currentEnvironment,
    required this.currentLighting,
    required this.onEnvironmentChanged,
    required this.onLightingChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Environment', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8.0,
          children: CaptureEnvironment.values.map((env) {
            return ChoiceChip(
              label: Text(env.name.replaceAll('_', ' ').toUpperCase()),
              selected: currentEnvironment == env,
              onSelected: (selected) {
                if (selected) onEnvironmentChanged(env);
              },
            );
          }).toList(),
        ),
        const SizedBox(height: 16),
        const Text('Lighting', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8.0,
          children: LightingCondition.values.map((light) {
            return ChoiceChip(
              label: Text(light.name.replaceAll('_', ' ').toUpperCase()),
              selected: currentLighting == light,
              onSelected: (selected) {
                if (selected) onLightingChanged(light);
              },
            );
          }).toList(),
        ),
      ],
    );
  }
}
