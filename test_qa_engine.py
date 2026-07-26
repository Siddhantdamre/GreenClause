"""
test_qa_engine.py — standalone checks for the TF-IDF citation-or-silence
engine (no pytest dependency; run via `python3 test_qa_engine.py`).

Two things are measured for real, not assumed:
  1. Retrieval accuracy on in-corpus questions: does the top match cite the
     CORRECT clause, not just "some" clause with a high score?
  2. Silence accuracy on out-of-corpus questions: does the engine correctly
     decline rather than stretch a weak match into an answer?

A retrieval system that never says "I don't know" isn't safe for a spec
compliance tool -- a wrong citation is worse than an admitted gap, because a
reviewer trusts a citation by default.
"""

import sys

from data.spec_documents import SPEC_DOCUMENTS
from qa_engine import TfidfIndex

passed = 0
failed = 0


def check(condition, description):
    global passed, failed
    if condition:
        passed += 1
    else:
        failed += 1
        print(f"  FAIL: {description}")


index = TfidfIndex(SPEC_DOCUMENTS)

# --- 1. In-corpus questions: one per document, expecting the correct doc_id
IN_CORPUS_CASES = [
    ("What is the minimum UPS runtime required?", "ups_runtime"),
    ("What electrical efficiency must the UPS achieve at rated load?", "ups_efficiency"),
    ("What is the maximum water usage effectiveness target for cooling?", "wue"),
    ("What cycles of concentration range must condenser water stay within?", "cooling_cycles"),
    ("What percentage of rejected heat must be captured for waste-heat recovery?", "waste_heat_recovery"),
    ("What load percentage range should standby generators be tested at?", "generator_load"),
    ("What percentage of GGBS cement replacement is required in structural concrete?", "ggbs"),
    ("How tall must the perimeter security fencing be?", "site_security_fencing"),
    ("Where should contractor personnel park during construction?", "employee_parking"),
    ("What is the minimum hold time for the clean agent fire suppression system?", "fire_suppression"),
]

print("=== In-corpus retrieval accuracy ===")
correct = 0
for question, expected_doc_id in IN_CORPUS_CASES:
    ans = index.query(question)
    is_correct = ans.answered and ans.doc_id == expected_doc_id
    correct += is_correct
    check(is_correct,
          f"Q={question!r} expected doc_id={expected_doc_id!r}, "
          f"got {ans.doc_id!r} (answered={ans.answered}, score={ans.score:.3f})")

retrieval_accuracy = correct / len(IN_CORPUS_CASES)
print(f"Retrieval accuracy: {correct}/{len(IN_CORPUS_CASES)} = {retrieval_accuracy:.3f}")
print()

# --- 2. Out-of-corpus questions: near-zero vocabulary overlap with any spec
# clause, so the engine must decline rather than stretch a weak match.
OUT_OF_CORPUS_CASES = [
    "What color should the server racks be painted?",
    "What is the CEO's email address?",
    "What is on the lunch menu for the site canteen?",
    "Who won the cricket match last night?",
]

print("=== Out-of-corpus silence accuracy ===")
silent_correct = 0
for question in OUT_OF_CORPUS_CASES:
    ans = index.query(question)
    is_silent = not ans.answered
    silent_correct += is_silent
    check(is_silent, f"Q={question!r} should be SILENCE, got doc_id={ans.doc_id!r} score={ans.score:.3f}")

silence_accuracy = silent_correct / len(OUT_OF_CORPUS_CASES)
print(f"Silence accuracy: {silent_correct}/{len(OUT_OF_CORPUS_CASES)} = {silence_accuracy:.3f}")
print()

# --- 3. Empty / degenerate query handling
print("=== Degenerate input handling ===")
for bad_query in ["", "the a of is", "   "]:
    ans = index.query(bad_query)
    check(not ans.answered, f"degenerate query {bad_query!r} should not be answered, got doc_id={ans.doc_id!r}")

print()
print(f"{passed} passed, {failed} failed")
print(
    "\nHonest limitation: this is a 10-document synthetic corpus with "
    "hand-written spec prose, not a real project's full specification set "
    "(which would run to hundreds of clauses with more vocabulary overlap "
    "between sections). Retrieval and silence accuracy above are real "
    "numbers on this test set -- they are not a claim about how the engine "
    "performs on a real, larger, messier spec document."
)
sys.exit(1 if failed else 0)
