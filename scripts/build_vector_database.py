import _bootstrap  # noqa: F401
from src.knowledge_base.builders.embedder import Embedder
from src.knowledge_base.vector_store import VectorStore
from src.knowledge_base.config import (
    VERSE_DOCUMENTS,
    COMMENTARY_DOCUMENTS,
    CHAPTER_DOCUMENTS,
    VERSE_COLLECTION,
    COMMENTARY_COLLECTION,
    CHAPTER_COLLECTION,
)
from src.knowledge_base.utils import load_json


def build_collection(embedder: Embedder, collection_name: str, json_file):
    vector_store = VectorStore(collection_name)
    documents = load_json(json_file)

    ids = [doc["id"] for doc in documents]
    texts = [doc["document"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]

    embeddings = embedder.embed_batch(texts)
    vector_store.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )

    print(f"Successfully indexed {len(ids)} documents into '{collection_name}'.")


if __name__ == "__main__":
    embedder = Embedder()
    build_collection(embedder, VERSE_COLLECTION, VERSE_DOCUMENTS)
    build_collection(embedder, COMMENTARY_COLLECTION, COMMENTARY_DOCUMENTS)
    build_collection(embedder, CHAPTER_COLLECTION, CHAPTER_DOCUMENTS)
