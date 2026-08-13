# HemoVision Conjunctiva Segmentation Benchmark Report

## Governance Declaration
- **Dataset Type**: `SYNTHETIC`
- **Clinical Validation**: `NOT PERFORMED`
- **Notice**: Software validation only. Synthetic fixture performance does not establish clinical accuracy.

## Benchmark Summary
- **Total Images Evaluated**: 7
- **Successful Segmentations**: 1
- **Failed Segmentations**: 6
- **Success Rate**: 14.29%
- **Mean IoU**: 0.9983
- **Mean Dice Score**: 0.9991
- **Mean Precision**: 1.0
- **Mean Recall**: 0.9983
- **Median Processing Time**: 1.98 ms

## Image Level Evaluation
- **`blurry_eye.png`**: Success=False | Area=0px (0.00%) | Runtime=2.58ms | IoU=None | Dice=None
- **`dark_eye.png`**: Success=False | Area=0px (0.00%) | Runtime=1.19ms | IoU=None | Dice=None
- **`incorrect_framing.png`**: Success=False | Area=0px (0.00%) | Runtime=1.82ms | IoU=None | Dice=None
- **`no_eye.png`**: Success=False | Area=0px (0.00%) | Runtime=0.96ms | IoU=None | Dice=None
- **`occluded_eye.png`**: Success=False | Area=0px (0.00%) | Runtime=83.99ms | IoU=None | Dice=None
- **`overexposed_eye.png`**: Success=False | Area=0px (0.00%) | Runtime=1.98ms | IoU=None | Dice=None
- **`synthetic_eye_001.png`**: Success=True | Area=5873px (2.24%) | Runtime=4.5ms | IoU=0.9983 | Dice=0.9991