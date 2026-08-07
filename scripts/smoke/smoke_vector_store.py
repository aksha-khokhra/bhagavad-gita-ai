import _bootstrap  # noqa: F401
from src.knowledge_base.config import VERSE_COLLECTION
from src.knowledge_base.vector_store import VectorStore


def main():
    vector_store = VectorStore(VERSE_COLLECTION)
    count = vector_store.collection.count()
    print("Vector store initialized successfully.")
    print(f"Connected to collection '{VERSE_COLLECTION}' with {count} documents.")


if __name__ == "__main__":
    main()
