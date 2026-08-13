"""
HemoVision Participant-Level Dataset Splitter
Splits dataset by participant_id to prevent data leakage across TRAIN, VALIDATION, and TEST sets.
"""

from typing import Dict, List, Set, Tuple
import random

from ml.src.data.dataset_loader import DatasetRecord


class DatasetSplitter:
    """Participant-grouped dataset splitter guaranteeing zero participant overlap across splits."""

    def __init__(self, train_ratio: float = 0.70, val_ratio: float = 0.15, test_ratio: float = 0.15, random_seed: int = 42):
        assert abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-5, "Ratios must sum to 1.0"
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.random_seed = random_seed

    def is_sufficient_for_ml_eval(self, participant_ids: List[str]) -> bool:
        unique_participants = set(participant_ids)
        return len(unique_participants) >= 3

    def split_participants(self, participant_ids: List[str]) -> Dict[str, Set[str]]:
        unique_participants = sorted(list(set(participant_ids)))
        rng = random.Random(self.random_seed)
        rng.shuffle(unique_participants)

        n_total = len(unique_participants)
        if n_total == 0:
            return {"train": set(), "val": set(), "test": set()}

        # For datasets with fewer than 3 participants, do NOT duplicate participants across sets.
        # Place available participant(s) in train set, leaving val and test empty.
        if n_total < 3:
            return {
                "train": set(unique_participants),
                "val": set(),
                "test": set(),
            }

        n_train = max(1, int(round(n_total * self.train_ratio)))
        n_val = max(1, int(round(n_total * self.val_ratio)))

        train_pts = set(unique_participants[:n_train])
        val_pts = set(unique_participants[n_train:n_train + n_val])
        test_pts = set(unique_participants[n_train + n_val:])

        if not test_pts and len(val_pts) > 1:
            test_pts.add(val_pts.pop())

        # Validate zero overlap strictly
        assert len(train_pts.intersection(val_pts)) == 0, "Leakage between TRAIN and VAL!"
        assert len(train_pts.intersection(test_pts)) == 0, "Leakage between TRAIN and TEST!"
        assert len(val_pts.intersection(test_pts)) == 0, "Leakage between VAL and TEST!"

        return {
            "train": train_pts,
            "val": val_pts,
            "test": test_pts,
        }

    def split_records(self, records: List[DatasetRecord]) -> Dict[str, List[DatasetRecord]]:
        p_ids = [r.participant_id for r in records]
        splits = self.split_participants(p_ids)

        train_recs = [r for r in records if r.participant_id in splits["train"]]
        val_recs = [r for r in records if r.participant_id in splits["val"]]
        test_recs = [r for r in records if r.participant_id in splits["test"]]

        return {
            "train": train_recs,
            "val": val_recs,
            "test": test_recs,
        }
