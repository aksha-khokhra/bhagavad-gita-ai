import re

from src.knowledge_base.builders.embedder import Embedder
from src.knowledge_base.vector_store import VectorStore
from src.knowledge_base.config import (
    VERSE_COLLECTION,
    COMMENTARY_COLLECTION,
    CHAPTER_COLLECTION,
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


class Retriever:

    def __init__(self):
        self.embedder = Embedder()
        self.verse_store = VectorStore(VERSE_COLLECTION)
        self.commentary_store = VectorStore(COMMENTARY_COLLECTION)
        self.chapter_store = VectorStore(CHAPTER_COLLECTION)

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
            verse_results = self.verse_store.query(
                query_embedding,
                n_results=verse_n_results,
                where={"chapter_number": route["chapter_number"]},
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
            verse_results = self.verse_store.query(
                query_embedding,
                n_results=verse_n_results,
            )
            commentary_results = self.commentary_store.query(
                query_embedding,
                n_results=commentary_n_results,
            )
        else:
            chapter_results = []
            verse_results = self.verse_store.query(
                query_embedding,
                n_results=verse_n_results,
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
