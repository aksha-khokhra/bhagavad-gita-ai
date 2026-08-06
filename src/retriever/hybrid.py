"""Hybrid retrieval helpers: verse-ref parsing, lexical search, and RRF fusion."""

from __future__ import annotations

import math
import re
from collections import Counter

VERSE_REF_PATTERN = re.compile(
    r"\b(?:bg\.?\s*|bhagavad\s+gita\s+)?(\d{1,2})\.(\d{1,3})\b",
    re.IGNORECASE,
)

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "in", "on", "at", "to", "for",
    "of", "is", "are", "was", "were", "be", "been", "being", "by", "with",
    "from", "as", "that", "this", "these", "those", "it", "its", "into",
    "what", "which", "who", "whom", "how", "why", "when", "where", "do",
    "does", "did", "can", "could", "should", "would", "may", "might", "must",
    "i", "we", "you", "he", "she", "they", "me", "my", "our", "your", "their",
}


def tokenize(text: str) -> list[str]:
    tokens = TOKEN_PATTERN.findall(text.lower())
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def parse_verse_references(user_query: str) -> list[str]:
    references = []
    seen = set()

    for match in VERSE_REF_PATTERN.finditer(user_query):
        chapter = int(match.group(1))
        verse = int(match.group(2))
        if not (1 <= chapter <= 18 and verse >= 1):
            continue
        reference = f"{chapter}.{verse}"
        if reference not in seen:
            seen.add(reference)
            references.append(reference)

    return references


def reciprocal_rank_fusion(result_lists, limit=3, k=60, weights=None):
    """Merge ranked result lists with Reciprocal Rank Fusion."""
    if weights is None:
        weights = [1.0] * len(result_lists)
    if len(weights) != len(result_lists):
        raise ValueError("weights must match the number of result lists")

    scores = {}
    documents = {}

    for weight, results in zip(weights, result_lists):
        for rank, result in enumerate(results, start=1):
            doc_id = result["id"]
            scores[doc_id] = scores.get(doc_id, 0.0) + weight * (
                1.0 / (k + rank)
            )
            if doc_id not in documents:
                documents[doc_id] = result

    ranked_ids = sorted(scores, key=scores.get, reverse=True)[:limit]
    fused = []
    for doc_id in ranked_ids:
        result = dict(documents[doc_id])
        result["rrf_score"] = scores[doc_id]
        fused.append(result)
    return fused


class LexicalVerseIndex:
    """In-memory BM25 index over verse translations."""

    def __init__(self, verse_documents, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = []
        self.doc_tokens = []
        self.doc_freqs = []
        self.doc_lengths = []

        for document in verse_documents:
            text = (
                f"{document['metadata'].get('english_translation', '')} "
                f"{document['metadata'].get('chapter_title', '')} "
                f"{document['metadata'].get('chapter_title_meaning', '')}"
            )
            tokens = tokenize(text)
            self.documents.append(document)
            self.doc_tokens.append(tokens)
            self.doc_freqs.append(Counter(tokens))
            self.doc_lengths.append(len(tokens))

        self.doc_count = len(self.documents)
        self.avgdl = (
            sum(self.doc_lengths) / self.doc_count if self.doc_count else 0.0
        )
        self.df = Counter()
        for tokens in self.doc_tokens:
            for token in set(tokens):
                self.df[token] += 1

    def _idf(self, token: str) -> float:
        df = self.df.get(token, 0)
        return math.log(1 + (self.doc_count - df + 0.5) / (df + 0.5))

    def search(self, query: str, n_results=10, chapter_number=None):
        query_tokens = tokenize(query)
        if not query_tokens or self.doc_count == 0:
            return []

        scores = []
        for index, document in enumerate(self.documents):
            metadata = document["metadata"]
            if (
                chapter_number is not None
                and metadata.get("chapter_number") != chapter_number
            ):
                continue

            freq = self.doc_freqs[index]
            doc_len = self.doc_lengths[index] or 1
            score = 0.0

            for token in query_tokens:
                if token not in freq:
                    continue
                tf = freq[token]
                denom = tf + self.k1 * (
                    1 - self.b + self.b * doc_len / (self.avgdl or 1)
                )
                score += self._idf(token) * (tf * (self.k1 + 1)) / denom

            if score > 0:
                scores.append((score, index))

        scores.sort(key=lambda item: item[0], reverse=True)

        results = []
        for score, index in scores[:n_results]:
            document = self.documents[index]
            results.append({
                "id": document["id"],
                "document": document["document"],
                "metadata": document["metadata"],
                "distance": 1.0 / (1.0 + score),
                "lexical_score": score,
            })
        return results
