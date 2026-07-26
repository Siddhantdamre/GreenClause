"""
data/submittals.py — synthetic contractor submittal values with a hand-labeled
ground truth of which are real (planted) deviations vs. compliant vs.
deliberately missing.

This is a SYNTHETIC test set, not real project data — say so anywhere these
numbers are reported. It exists to let the deviation checker's precision/
recall be computed against a known answer key, the same way DhvaniShield and
Holup report real numbers on their own frozen eval sets rather than an
unverified round number.

Each site has all 7 requirement keys. `ground_truth[site][key]` is one of:
  "compliant"       - value is genuinely within spec
  "deviation"       - value is a planted violation
  "cannot_verify"   - value deliberately omitted (tests the CANNOT_VERIFY path,
                       excluded from precision/recall since it's not a
                       deviation-detection decision)
"""

SUBMITTALS = {
    "SITE-01-Mumbai": {
        "ups_runtime": 18.0,           # compliant
        "ups_efficiency": 97.5,        # compliant
        "wue": 0.15,                   # compliant
        "cooling_cycles": 4.0,         # compliant
        "waste_heat_recovery": 14.0,   # compliant
        "generator_load": 60.0,        # compliant
        "ggbs": 35.0,                  # compliant
    },
    "SITE-02-Pune": {
        "ups_runtime": 10.0,           # DEVIATION (< 15)
        "ups_efficiency": 94.0,        # DEVIATION (< 96)
        "wue": 0.18,                   # compliant
        "cooling_cycles": 4.2,         # compliant
        "waste_heat_recovery": 12.0,   # compliant
        "generator_load": 50.0,        # compliant
        "ggbs": 40.0,                  # compliant
    },
    "SITE-03-Chennai": {
        "ups_runtime": 20.0,           # compliant
        "ups_efficiency": 96.5,        # compliant
        "wue": 0.42,                   # DEVIATION (> 0.20)
        "cooling_cycles": 7.0,         # DEVIATION (> 6)
        "waste_heat_recovery": 5.0,    # DEVIATION (< 10)
        "generator_load": 88.0,        # DEVIATION (> 80)
        "ggbs": 22.0,                  # DEVIATION (< 30)
    },
    "SITE-04-Hyderabad": {
        "ups_runtime": 16.5,           # compliant
        "ups_efficiency": 96.1,        # compliant
        "wue": None,                   # cannot_verify
        "cooling_cycles": 3.5,         # compliant
        "waste_heat_recovery": None,   # cannot_verify
        "generator_load": 65.0,        # compliant
        "ggbs": 45.0,                  # compliant
    },
    "SITE-05-Noida": {
        "ups_runtime": 15.0,           # compliant (boundary, inclusive)
        "ups_efficiency": 95.9,        # DEVIATION (< 96, just below boundary)
        "wue": 0.20,                   # compliant (boundary, inclusive)
        "cooling_cycles": 2.5,         # DEVIATION (< 3)
        "waste_heat_recovery": 10.0,   # compliant (boundary, inclusive)
        "generator_load": 30.0,        # compliant (boundary, inclusive)
        "ggbs": 50.0,                  # compliant (boundary, inclusive)
    },
}

GROUND_TRUTH = {
    "SITE-01-Mumbai": {
        "ups_runtime": "compliant", "ups_efficiency": "compliant", "wue": "compliant",
        "cooling_cycles": "compliant", "waste_heat_recovery": "compliant",
        "generator_load": "compliant", "ggbs": "compliant",
    },
    "SITE-02-Pune": {
        "ups_runtime": "deviation", "ups_efficiency": "deviation", "wue": "compliant",
        "cooling_cycles": "compliant", "waste_heat_recovery": "compliant",
        "generator_load": "compliant", "ggbs": "compliant",
    },
    "SITE-03-Chennai": {
        "ups_runtime": "compliant", "ups_efficiency": "compliant", "wue": "deviation",
        "cooling_cycles": "deviation", "waste_heat_recovery": "deviation",
        "generator_load": "deviation", "ggbs": "deviation",
    },
    "SITE-04-Hyderabad": {
        "ups_runtime": "compliant", "ups_efficiency": "compliant", "wue": "cannot_verify",
        "cooling_cycles": "compliant", "waste_heat_recovery": "cannot_verify",
        "generator_load": "compliant", "ggbs": "compliant",
    },
    "SITE-05-Noida": {
        "ups_runtime": "compliant", "ups_efficiency": "deviation", "wue": "compliant",
        "cooling_cycles": "deviation", "waste_heat_recovery": "compliant",
        "generator_load": "compliant", "ggbs": "compliant",
    },
}
