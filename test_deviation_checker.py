"""
test_deviation_checker.py — standalone checks (no pytest dependency, run
directly via `python3 test_deviation_checker.py`), matching the style used
elsewhere in this portfolio (MetaCog-Triage, GSoC-Healing-Stones) where the
sandbox/demo environment can't assume test frameworks are installed.

Computes REAL precision/recall for deviation detection against the hand-
labeled ground truth in data/submittals.py, rather than asserting a round
number. Also checks the CANNOT_VERIFY path explicitly and a set of boundary
conditions (values exactly at a threshold).
"""

import sys

from data.submittals import SUBMITTALS, GROUND_TRUTH
from deviation_checker import check_submittal, check_requirement, Verdict

passed = 0
failed = 0


def check(condition, description):
    global passed, failed
    if condition:
        passed += 1
    else:
        failed += 1
        print(f"  FAIL: {description}")


# --- 1. Confusion matrix over every requirement instance with a real label
# (excludes cannot_verify instances -- those aren't a deviation-detection
# decision, they're an "I don't have data" decision, scored separately below)
tp = fp = tn = fn = 0
cannot_verify_correct = 0
cannot_verify_total = 0

for site_id, values in SUBMITTALS.items():
    truth_for_site = GROUND_TRUTH[site_id]
    for key, value in values.items():
        predicted = check_requirement(key, value).verdict
        truth = truth_for_site[key]

        if truth == "cannot_verify":
            cannot_verify_total += 1
            if predicted == Verdict.CANNOT_VERIFY:
                cannot_verify_correct += 1
            continue

        truth_is_deviation = (truth == "deviation")
        predicted_is_deviation = (predicted == Verdict.DEVIATION)

        if truth_is_deviation and predicted_is_deviation:
            tp += 1
        elif truth_is_deviation and not predicted_is_deviation:
            fn += 1
        elif not truth_is_deviation and predicted_is_deviation:
            fp += 1
        else:
            tn += 1

precision = tp / (tp + fp) if (tp + fp) else float("nan")
recall = tp / (tp + fn) if (tp + fn) else float("nan")
f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else float("nan")

print("=== Deviation-detection confusion matrix (over labeled, non-missing instances) ===")
print(f"TP={tp}  FP={fp}  TN={tn}  FN={fn}")
print(f"Precision = {precision:.3f}   Recall = {recall:.3f}   F1 = {f1:.3f}")
print(f"CANNOT_VERIFY correctly identified: {cannot_verify_correct}/{cannot_verify_total}")
print()

# The engine is deterministic rule application, not a learned classifier, so a
# real bug (not a calibration issue) would show up as any FP or FN here. On
# this 35-instance synthetic set (33 labeled deviation/compliant + 2
# cannot_verify), it should be perfect -- and if it's not, that's a real
# defect in the rule logic, not noise to shrug off.
check(fp == 0, f"expected 0 false positives, got {fp}")
check(fn == 0, f"expected 0 false negatives, got {fn}")
check(cannot_verify_correct == cannot_verify_total,
      f"expected all {cannot_verify_total} missing values flagged CANNOT_VERIFY, "
      f"got {cannot_verify_correct}")

# --- 2. Boundary conditions: inclusive bounds must be COMPLIANT, not DEVIATION
boundary_cases = [
    ("ups_runtime", 15.0, Verdict.COMPLIANT),   # exactly the minimum
    ("ups_runtime", 14.999, Verdict.DEVIATION), # just under
    ("wue", 0.20, Verdict.COMPLIANT),           # exactly the maximum
    ("wue", 0.201, Verdict.DEVIATION),          # just over
    ("cooling_cycles", 3.0, Verdict.COMPLIANT), # low end of range
    ("cooling_cycles", 6.0, Verdict.COMPLIANT), # high end of range
    ("cooling_cycles", 2.999, Verdict.DEVIATION),
    ("cooling_cycles", 6.001, Verdict.DEVIATION),
    ("ggbs", 30.0, Verdict.COMPLIANT),
    ("ggbs", 50.0, Verdict.COMPLIANT),
    ("ggbs", 29.999, Verdict.DEVIATION),
    ("ggbs", 50.001, Verdict.DEVIATION),
]
print("=== Boundary conditions ===")
for key, value, expected in boundary_cases:
    actual = check_requirement(key, value).verdict
    check(actual == expected, f"{key}={value}: expected {expected.value}, got {actual.value}")

# --- 3. Malformed / non-numeric submittal values must be CANNOT_VERIFY, never
# silently coerced or crashed on -- an unparseable value is not the same as
# "no value," but it's just as unsafe to guess about.
print("=== Malformed input handling ===")
malformed_cases = ["not-a-number", "", "N/A", [], {}]
for bad_value in malformed_cases:
    result = check_requirement("ups_runtime", bad_value)
    check(result.verdict == Verdict.CANNOT_VERIFY,
          f"malformed value {bad_value!r} should be CANNOT_VERIFY, got {result.verdict.value}")

# --- 4. check_submittal wiring: report object aggregates correctly
print("=== check_submittal aggregation ===")
report = check_submittal("SITE-03-Chennai", SUBMITTALS["SITE-03-Chennai"])
check(len(report.deviations) == 5, f"SITE-03-Chennai: expected 5 deviations, got {len(report.deviations)}")
check(len(report.compliant) == 2, f"SITE-03-Chennai: expected 2 compliant, got {len(report.compliant)}")
check(len(report.cannot_verify) == 0, f"SITE-03-Chennai: expected 0 cannot_verify, got {len(report.cannot_verify)}")

print()
print(f"{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
