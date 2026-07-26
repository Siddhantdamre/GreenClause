"""
deviation_checker.py — spec-vs-submittal deviation detection engine.

Core rule this engine follows (same design principle as DhvaniShield's "never
say safe" gate and Holup's abstain option): a requirement with no matching
value in the submittal is reported as CANNOT_VERIFY, never silently assumed
COMPLIANT. Assuming compliance on missing data is a worse failure mode than a
false deviation flag, because it's the one a reviewer won't catch by re-reading
the submittal — they'll just see "COMPLIANT" and move on.

Usage:
    from deviation_checker import check_submittal
    result = check_submittal(site_id, submittal_values)  # dict[str, float|None]
"""

from dataclasses import dataclass
from enum import Enum

from spec_registry import REQUIREMENTS, REQUIREMENT_ORDER


class Verdict(str, Enum):
    COMPLIANT = "COMPLIANT"
    DEVIATION = "DEVIATION"
    CANNOT_VERIFY = "CANNOT_VERIFY"  # value missing or unparseable in submittal


@dataclass
class RequirementResult:
    key: str
    label: str
    verdict: Verdict
    submittal_value: float | None
    rule_text: str
    unit: str
    reason: str


@dataclass
class SubmittalReport:
    site_id: str
    results: list  # list[RequirementResult]

    @property
    def deviations(self):
        return [r for r in self.results if r.verdict == Verdict.DEVIATION]

    @property
    def cannot_verify(self):
        return [r for r in self.results if r.verdict == Verdict.CANNOT_VERIFY]

    @property
    def compliant(self):
        return [r for r in self.results if r.verdict == Verdict.COMPLIANT]

    def summary_line(self) -> str:
        return (
            f"{self.site_id}: {len(self.compliant)} compliant, "
            f"{len(self.deviations)} deviation(s), "
            f"{len(self.cannot_verify)} cannot-verify"
        )


def check_requirement(key: str, value) -> RequirementResult:
    req = REQUIREMENTS[key]

    if value is None:
        return RequirementResult(
            key=key,
            label=req.label,
            verdict=Verdict.CANNOT_VERIFY,
            submittal_value=None,
            rule_text=req.rule_text,
            unit=req.unit,
            reason="No value for this requirement found in the submittal.",
        )

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return RequirementResult(
            key=key,
            label=req.label,
            verdict=Verdict.CANNOT_VERIFY,
            submittal_value=None,
            rule_text=req.rule_text,
            unit=req.unit,
            reason=f"Submittal value {value!r} is not a parseable number.",
        )

    if req.check(numeric_value):
        return RequirementResult(
            key=key,
            label=req.label,
            verdict=Verdict.COMPLIANT,
            submittal_value=numeric_value,
            rule_text=req.rule_text,
            unit=req.unit,
            reason=f"{numeric_value} {req.unit} satisfies '{req.rule_text}'.",
        )
    else:
        return RequirementResult(
            key=key,
            label=req.label,
            verdict=Verdict.DEVIATION,
            submittal_value=numeric_value,
            rule_text=req.rule_text,
            unit=req.unit,
            reason=f"{numeric_value} {req.unit} violates '{req.rule_text}'.",
        )


def check_submittal(site_id: str, submittal_values: dict) -> SubmittalReport:
    """submittal_values: dict mapping requirement key -> numeric value or None/missing."""
    results = [
        check_requirement(key, submittal_values.get(key))
        for key in REQUIREMENT_ORDER
    ]
    return SubmittalReport(site_id=site_id, results=results)


if __name__ == "__main__":
    demo = {
        "ups_runtime": 12.0,       # DEVIATION (< 15)
        "ups_efficiency": 97.2,    # COMPLIANT
        "wue": 0.35,               # DEVIATION (> 0.20)
        "cooling_cycles": 4.5,     # COMPLIANT
        "waste_heat_recovery": None,  # CANNOT_VERIFY
        "generator_load": 55.0,    # COMPLIANT
        "ggbs": 28.0,              # DEVIATION (< 30)
    }
    report = check_submittal("DEMO-SITE-1", demo)
    print(report.summary_line())
    for r in report.results:
        print(f"  [{r.verdict.value:14s}] {r.label}: {r.reason}")
