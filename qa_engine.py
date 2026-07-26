"""
qa_engine.py — TF-IDF citation-or-silence Q&A over spec documents.

Design principle (same family as deviation_checker.py's CANNOT_VERIFY and
DhvaniShield's "never say safe"): this is retrieval, not generation. It never
composes a free-text answer. It either points at the specific spec clause
that answers the question (citation) or says plainly that nothing in the
corpus answers it (silence) — it does not blend, summarize, or guess at an
answer that isn't directly grounded in a retrieved passage.

Pure Python, no numpy/sklearn dependency, matching the rest of this
portfolio's "runs anywhere, nothing hidden in a library" style.
"""

import math
import re
from dataclasses import dataclass

_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "on", "for", "and", "or", "at", "by", "with", "this",
    "that", "it", "as", "what", "which", "does", "do", "must", "should",
    "can", "will", "shall", "has", "have", "had",
}

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list:
    return [t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]


@dataclass
class Document:
    doc_id: str
    title: str
    text: str


@dataclass
class Answer:
    answered: bool
    doc_id: str | None
    title: str | None
    excerpt: str | None
    score: float
    reason: str


class TfidfIndex:
    """A minimal TF-IDF index with cosine-similarity retrieval."""

    def __init__(self, documents: list, silence_threshold: float = 0.12):
        self.documents = {d.doc_id: d for d in documents}
        self.silence_threshold = silence_threshold
        self._doc_tokens = {d.doc_id: tokenize(d.text) for d in documents}
        self._df = self._document_frequencies()
        self._n_docs = len(documents)
        self._doc_vectors = {
            doc_id: self._tfidf_vector(tokens)
            for doc_id, tokens in self._doc_tokens.items()
        }

    def _document_frequencies(self) -> dict:
        df: dict = {}
        for tokens in self._doc_tokens.values():
            for term in set(tokens):
                df[term] = df.get(term, 0) + 1
        return df

    def _idf(self, term: str) -> float:
        df = self._df.get(term, 0)
        if df == 0:
            return 0.0
        # smoothed idf, always >= 0
        return math.log((1 + self._n_docs) / (1 + df)) + 1.0

    def _tfidf_vector(self, tokens: list) -> dict:
        if not tokens:
            return {}
        tf: dict = {}
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1
        n = len(tokens)
        vec = {term: (count / n) * self._idf(term) for term, count in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        return {term: v / norm for term, v in vec.items()}

    @staticmethod
    def _cosine(vec_a: dict, vec_b: dict) -> float:
        if not vec_a or not vec_b:
            return 0.0
        # iterate the smaller vector for efficiency
        if len(vec_a) > len(vec_b):
            vec_a, vec_b = vec_b, vec_a
        return sum(v * vec_b.get(term, 0.0) for term, v in vec_a.items())

    def query(self, question: str) -> Answer:
        q_tokens = tokenize(question)
        q_vector = self._tfidf_vector(q_tokens)

        if not q_vector:
            return Answer(
                answered=False, doc_id=None, title=None, excerpt=None, score=0.0,
                reason="Question contained no indexable terms after stopword removal.",
            )

        scored = [
            (doc_id, self._cosine(q_vector, doc_vec))
            for doc_id, doc_vec in self._doc_vectors.items()
        ]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        best_doc_id, best_score = scored[0]

        if best_score < self.silence_threshold:
            return Answer(
                answered=False, doc_id=None, title=None, excerpt=None,
                score=best_score,
                reason=(
                    f"Best match score {best_score:.3f} is below the "
                    f"silence threshold {self.silence_threshold:.2f} -- "
                    "no spec clause is a confident enough match to cite. "
                    "Staying silent rather than guessing."
                ),
            )

        doc = self.documents[best_doc_id]
        return Answer(
            answered=True,
            doc_id=doc.doc_id,
            title=doc.title,
            excerpt=doc.text.strip(),
            score=best_score,
            reason=f"Matched '{doc.title}' with cosine similarity {best_score:.3f}.",
        )


if __name__ == "__main__":
    from data.spec_documents import SPEC_DOCUMENTS

    index = TfidfIndex(SPEC_DOCUMENTS)
    for q in [
        "What is the minimum UPS runtime required?",
        "What GGBS percentage range does the spec require?",
        "What color should the server racks be painted?",  # out of scope -> silence
    ]:
        ans = index.query(q)
        print(f"Q: {q}")
        if ans.answered:
            print(f"  -> [{ans.title}] {ans.excerpt}  (score={ans.score:.3f})")
        else:
            print(f"  -> SILENCE: {ans.reason}")
        print()
