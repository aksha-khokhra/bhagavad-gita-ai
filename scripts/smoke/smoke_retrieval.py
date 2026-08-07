import _bootstrap  # noqa: F401
from src.knowledge_base.builders.embedder import Embedder
from src.knowledge_base.vector_store import VectorStore


def main():
    embedder = Embedder()
    verse_store = VectorStore("verses")

    user_query = "Why should we perform actions without expecting results?"
    query_embedding = embedder.embed(user_query)
    results = verse_store.query(query_embedding)

    for result in results:
        print("=" * 80)
        print(f"Reference : {result['metadata']['reference']}")
        print(f"Distance  : {result['distance']:.4f}")
        print(f"Document  : {result['document']}")


if __name__ == "__main__":
    main()
