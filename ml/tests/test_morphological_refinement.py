"""
Tests for MorphologicalRefiner
"""

import pytest
import numpy as np
from ml.src.segmentation.morphological_refinement import MorphologicalRefiner


def test_morphological_refining():
    refiner = MorphologicalRefiner(kernel_size=5, min_component_area=50)
    raw_mask = np.zeros((200, 200), dtype=np.uint8)

    # Salt & pepper noise (single pixels)
    raw_mask[10, 10] = 255
    raw_mask[12, 12] = 255

    # Main valid component
    raw_mask[50:100, 50:120] = 255

    refined = refiner.refine(raw_mask)
    # Noise should be removed
    assert refined[10, 10] == 0
    # Main component preserved
    assert np.sum(refined > 0) > 0
