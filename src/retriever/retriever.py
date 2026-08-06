import re

from src.knowledge_base.builders.embedder import Embedder
from src.knowledge_base.vector_store import VectorStore
from src.knowledge_base.config import (
    VERSE_COLLECTION,
    COMMENTARY_COLLECTION,
    CHAPTER_COLLECTION,
    VERSE_DOCUMENTS,
)
from src.knowledge_base.utils import load_json
from src.retriever.hybrid import (
    LexicalVerseIndex,
    parse_verse_references,
    reciprocal_rank_fusion,
)


CHAPTER_NUMBER_PATTERN = re.compile(
    r"\b(?:chapter|ch\.?)\s*(\d{1,2})\b",
    re.IGNORECASE,
)

CHAPTER_INTENT_PATTERN = re.compile(
    r"\b("
    r"summarize|summary|overview|"
    r"which\s+chapter|what\s+(?:is|are)\s+chapter|"
    r"chapter\s+(?:about|discuss|cover)|"
    r"chapters?\s+discuss|"
    r"chapter\s+\d{1,2}|ch\.?\s*\d{1,2}"
    r")\b",
    re.IGNORECASE,
)

VECTOR_CANDIDATE_MULTIPLIER = 3
LEXICAL_CANDIDATE_MULTIPLIER = 3


class Retriever:

    def __init__(self):
        self.embedder = Embedder()
        self.verse_store = VectorStore(VERSE_COLLECTION)
        self.commentary_store = VectorStore(COMMENTARY_COLLECTION)
        self.chapter_store = VectorStore(CHAPTER_COLLECTION)
        self.lexical_index = LexicalVerseIndex(load_json(VERSE_DOCUMENTS))

    def classify_query(self, user_query):
        chapter_match = CHAPTER_NUMBER_PATTERN.search(user_query)
        if chapter_match:
            chapter_number = int(chapter_match.group(1))
            if 1 <= chapter_number <= 18:
                return {
                    "mode": "chapter_reference",
                    "chapter_number": chapter_number,
                }

        if CHAPTER_INTENT_PATTERN.search(user_query):
            return {
                "mode": "chapter_overview",
                "chapter_number": None,
            }

        return {
            "mode": "general",
            "chapter_number": None,
        }

    def _exact_verse_results(self, user_query, chapter_number=None):
        references = parse_verse_references(user_query)
        results = []
        seen = set()

        for reference in references:
            matches = self.verse_store.get_by_metadata(
                where={"reference": reference}
            )
            for match in matches:
                if (
                    chapter_number is not None
                    and match["metadata"].get("chapter_number") != chapter_number
                ):
                    continue
                if match["id"] in seen:
                    continue
                seen.add(match["id"])
                match = dict(match)
                match["match_type"] = "exact_reference"
                results.append(match)

        return results

    def _hybrid_verse_results(
        self,
        user_query,
        query_embedding,
        verse_n_results,
        chapter_number=None,
    ):
        exact_results = self._exact_verse_results(
            user_query,
            chapter_number=chapter_number,
        )

        vector_n = max(verse_n_results * VECTOR_CANDIDATE_MULTIPLIER, 10)
        lexical_n = max(verse_n_results * LEXICAL_CANDIDATE_MULTIPLIER, 10)

        where = None
        if chapter_number is not None:
            where = {"chapter_number": chapter_number}

        vector_results = self.verse_store.query(
            query_embedding,
            n_results=vector_n,
            where=where,
        )
        lexical_results = self.lexical_index.search(
            user_query,
            n_results=lexical_n,
            chapter_number=chapter_number,
        )

        fused = reciprocal_rank_fusion(
            [exact_results, vector_results, lexical_results],
            limit=max(verse_n_results * 2, verse_n_results),
            k=20,
            weights=[3.0, 1.0, 2.0],
        )

        ordered = []
        seen = set()

        # Exact verse references always win.
        for result in exact_results:
            if result["id"] not in seen:
                ordered.append(result)
                seen.add(result["id"])

        # Keep the strongest lexical hit so shared wording is not drowned by vectors.
        if lexical_results:
            best_lexical = lexical_results[0]
            if best_lexical["id"] not in seen:
                ordered.append(best_lexical)
                seen.add(best_lexical["id"])

        for result in fused:
            if result["id"] not in seen:
                ordered.append(result)
                seen.add(result["id"])
            if len(ordered) >= verse_n_results:
                break

        return ordered[:verse_n_results]
    def retrieve(
        self,
        user_query,
        verse_n_results=3,
        commentary_n_results=5,
        chapter_n_results=2,
    ):
        query_embedding = self.embedder.embed(user_query)
        route = self.classify_query(user_query)

        if route["mode"] == "chapter_reference":
            chapter_results = self.chapter_store.query(
                query_embedding,
                n_results=1,
                where={"chapter_number": route["chapter_number"]},
            )
            verse_results = self._hybrid_verse_results(
                user_query,
                query_embedding,
                verse_n_results,
                chapter_number=route["chapter_number"],
            )
            commentary_results = self.commentary_store.query(
                query_embedding,
                n_results=commentary_n_results,
                where={"chapter_number": route["chapter_number"]},
            )
        elif route["mode"] == "chapter_overview":
            chapter_results = self.chapter_store.query(
                query_embedding,
                n_results=max(chapter_n_results, 3),
            )
            verse_results = self._hybrid_verse_results(
                user_query,
                query_embedding,
                verse_n_results,
            )
            commentary_results = self.commentary_store.query(
                query_embedding,
                n_results=commentary_n_results,
            )
        else:
            chapter_results = []
            verse_results = self._hybrid_verse_results(
                user_query,
                query_embedding,
                verse_n_results,
            )
            commentary_results = self.commentary_store.query(
                query_embedding,
                n_results=commentary_n_results,
            )

        return {
            "verses": verse_results,
            "commentaries": commentary_results,
            "chapters": chapter_results,
            "route": route,
        }
