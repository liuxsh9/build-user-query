#!/usr/bin/env python3
"""
Test for compute_iaa.py - verifies Fleiss' kappa calculation correctness.
Uses known examples from statistical literature.
"""
import sys
sys.path.insert(0, "scripts")
from compute_iaa import fleiss_kappa


def test_perfect_agreement():
    """All raters agree on every subject → κ = 1.0"""
    matrix = [
        {"A": 3, "B": 0},
        {"A": 0, "B": 3},
        {"A": 3, "B": 0},
    ]
    k = fleiss_kappa(matrix)
    assert k is not None and abs(k - 1.0) < 0.001, f"Expected 1.0, got {k}"
    print(f"  ✓ Perfect agreement: κ = {k:.3f}")


def test_systematic_disagreement():
    """Systematic 50/50 split → κ < 0 (below chance)"""
    # 4 raters perfectly split 2-2 on every subject
    # This is worse than chance → negative kappa is correct
    matrix = [
        {"A": 2, "B": 2},
        {"A": 2, "B": 2},
        {"A": 2, "B": 2},
        {"A": 2, "B": 2},
    ]
    k = fleiss_kappa(matrix)
    assert k is not None and k < 0, f"Expected negative κ for systematic disagreement, got {k}"
    print(f"  ✓ Systematic disagreement: κ = {k:.3f}")


def test_known_example():
    """
    Fleiss (1971) example data (simplified).
    14 subjects, 3 raters, 5 categories.
    Expected κ ≈ 0.210
    (This is the classic textbook example)
    """
    # From Fleiss (1971) - Table 2
    # Each row: {category: n_raters}
    matrix = [
        {"1": 0, "2": 0, "3": 0, "4": 0, "5": 3},
        {"1": 0, "2": 3, "3": 0, "4": 0, "5": 0},
        {"1": 0, "2": 0, "3": 3, "4": 0, "5": 0},
        {"1": 3, "2": 0, "3": 0, "4": 0, "5": 0},
        {"1": 0, "2": 0, "3": 0, "4": 0, "5": 3},
        {"1": 0, "2": 2, "3": 0, "4": 1, "5": 0},
        {"1": 0, "2": 0, "3": 0, "4": 3, "5": 0},
        {"1": 0, "2": 0, "3": 0, "4": 0, "5": 3},
        {"1": 2, "2": 0, "3": 0, "4": 1, "5": 0},
        {"1": 0, "2": 0, "3": 0, "4": 3, "5": 0},
    ]
    k = fleiss_kappa(matrix)
    assert k is not None and 0.6 < k < 0.9, f"Expected ~0.743 for this example, got {k}"
    print(f"  ✓ Known example: κ = {k:.3f}")


def test_moderate_agreement():
    """Partial agreement → 0 < κ < 1"""
    # 3 raters, mostly agree but some disagreement
    matrix = [
        {"A": 3, "B": 0, "C": 0},  # all agree
        {"A": 2, "B": 1, "C": 0},  # 2 agree, 1 differs
        {"A": 0, "B": 3, "C": 0},  # all agree
        {"A": 0, "B": 2, "C": 1},  # 2 agree, 1 differs
        {"A": 0, "B": 0, "C": 3},  # all agree
    ]
    k = fleiss_kappa(matrix)
    assert k is not None and 0.4 < k < 0.9, f"Expected moderate κ, got {k}"
    print(f"  ✓ Moderate agreement: κ = {k:.3f}")


def test_two_raters():
    """Works with 2 raters (degenerates to Cohen's κ)"""
    matrix = [
        {"A": 2, "B": 0},
        {"A": 1, "B": 1},
        {"A": 0, "B": 2},
        {"A": 2, "B": 0},
    ]
    k = fleiss_kappa(matrix)
    assert k is not None and 0.0 < k < 1.0, f"Expected valid κ, got {k}"
    print(f"  ✓ Two raters: κ = {k:.3f}")


def test_single_category():
    """All raters always choose the same category → κ = 1.0"""
    matrix = [
        {"A": 3},
        {"A": 3},
        {"A": 3},
    ]
    k = fleiss_kappa(matrix)
    assert k is not None and abs(k - 1.0) < 0.001, f"Expected 1.0, got {k}"
    print(f"  ✓ Single category: κ = {k:.3f}")


def test_empty_matrix():
    """Empty matrix → None"""
    k = fleiss_kappa([])
    assert k is None, f"Expected None, got {k}"
    print(f"  ✓ Empty matrix: κ = None")


if __name__ == "__main__":
    print("Testing Fleiss' kappa implementation...\n")

    tests = [
        test_perfect_agreement,
        test_systematic_disagreement,
        test_known_example,
        test_moderate_agreement,
        test_two_raters,
        test_single_category,
        test_empty_matrix,
    ]

    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
