# GreenClause

ET AI Hackathon 2026 — Problem 4 (AI Intelligence Platform for Data Centre EPC
Project Delivery).

**One sentence:** checks contractor submittals against project spec across 7
real engineering requirement types, and answers spec questions by citing the
exact clause or admitting it doesn't know — never a silent guess either way.

## Status — first working build (2026-07-26)

Nothing existed on disk before today despite planning documents describing
this as partially built (see "Honesty note" below). This is a from-scratch,
tested, working MVP of the two capabilities those documents described:

- [x] Deterministic spec-vs-submittal deviation checker, 7 requirement types:
      UPS runtime, UPS efficiency, WUE, condenser water cycles of
      concentration, waste-heat recovery, generator load, GGBS cement
      replacement. Every threshold is a real engineering figure with a stated
      reason (`spec_registry.py`), not an arbitrary number.
- [x] Three-way verdict per requirement: COMPLIANT / DEVIATION /
      CANNOT_VERIFY. A missing or unparseable submittal value is never
      assumed compliant — same "don't guess" principle as DhvaniShield's
      no-safe-output gate and Holup's abstain option.
- [x] TF-IDF citation-or-silence Q&A over spec documents (`qa_engine.py`),
      pure Python, no ML dependency. Retrieval only — it points at the exact
      clause, it does not compose a free-text answer, and it declines rather
      than stretches a weak match.
- [x] Real synthetic test sets with hand-labeled ground truth, both engines:
      `test_deviation_checker.py` → 23/23 checks pass, precision/recall
      computed as 1.000/1.000 over 33 labeled + 2 cannot-verify instances
      (this is a deterministic rule engine, so any FP/FN would mean a real
      bug, not calibration noise — say so, don't just report the number).
      `test_qa_engine.py` → 10/10 in-corpus retrieval accuracy, 4/4
      out-of-corpus silence accuracy, on a 10-document synthetic corpus.
- [ ] Not built yet: schedule risk prediction, supply chain/shipment
      tracking, commissioning workflow support, PDF ingestion (submittals
      are Python dicts right now, not parsed from real documents), expanding
      the requirement registry beyond these 7 types to ~40 real requirements
      from public sources (UFGS, Indian DC tenders, CPCB, ECBC).

## Honesty note

Two of this portfolio's own planning documents (`weekly_schedule.md`,
`hackathon_rubric.md`) describe GreenClause as already having "a
deterministic deviation engine live... 100% recall/precision on its own
planted-deviation test set" — but no code, folder, or file for GreenClause
existed anywhere in the connected workspace before this session. That
description was aspirational, not actual. This README's checklist reflects
what was actually built and tested today, not what earlier documents assumed.

## Run it

```
python3 deviation_checker.py     # demo: one site, mixed verdicts
python3 test_deviation_checker.py
python3 qa_engine.py             # demo: 2 answerable + 1 silence
python3 test_qa_engine.py
```

Zero external dependencies — stdlib only.

## Why this scope first

Per `hackathon_rubric.md`'s own evaluation-focus notes, schedule risk
prediction is the higher-leverage gap for Innovation/Scalability scoring than
deepening the deviation engine further. That's still true — but with zero
code existing before today, there was no foundation to build schedule risk
prediction on top of. This session's job was making the core deviation +
Q&A capability real and tested first; schedule risk prediction is the next
session's target, not deprioritized, just sequenced after having something
that actually runs.

## Files

```
spec_registry.py          7 requirement definitions + real engineering rationale
deviation_checker.py      core engine: submittal values -> verdicts
qa_engine.py               TF-IDF citation-or-silence retrieval
data/submittals.py         5 synthetic sites, hand-labeled ground truth
data/spec_documents.py     10-document synthetic spec corpus (7 in-scope + 3 adjacent)
test_deviation_checker.py  23 checks: confusion matrix, boundaries, malformed input
test_qa_engine.py          17 checks: retrieval accuracy, silence accuracy, degenerate input
```
