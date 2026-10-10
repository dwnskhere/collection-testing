"""Regression tests for TV-series metadata matching false positives."""

from Backend.helper.metadata.common import SERIES_TITLE_THRESHOLD, title_similarity


def test_partial_doctor_title_overlap_is_rejected():
    # Previously this partial overlap exceeded the global 0.55 TVDB threshold
    # and could attach a Doctor X episode to the unrelated Doctor White record.
    assert title_similarity("Doctor X Mafia in White", "Doctor White") < SERIES_TITLE_THRESHOLD


def test_exact_doctor_x_title_is_accepted():
    assert title_similarity("Doctor X Mafia in White", "Doctor X: Mafia in White") >= SERIES_TITLE_THRESHOLD
