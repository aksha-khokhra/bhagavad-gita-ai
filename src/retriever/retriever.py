from src.knowledge_base.builders.embedder import Embedder
from src.knowledge_base.vector_store import VectorStore
from src.knowledge_base.config import (
    VERSE_COLLECTION,
    COMMENTARY_COLLECTION
)


class Retriever:

    def __init__(self):

        self.embedder = Embedder()

        self.verse_store = VectorStore(VERSE_COLLECTION)

        self.commentary_store = VectorStore(COMMENTARY_COLLECTION)

    def retrieve(self, user_query, verse_n_results=3, commentary_n_results=5):

        query_embedding = self.embedder.embed(user_query)

        verse_results = self.verse_store.query(
            query_embedding,
            n_results=verse_n_results
        )

        commentary_results = self.commentary_store.query(
            query_embedding,
            n_results=commentary_n_results
        )

        return {
            "verses": verse_results,
            "commentaries": commentary_results
        }