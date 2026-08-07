import _bootstrap  # noqa: F401
from src.knowledge_base.builders.embedder import Embedder
from src.knowledge_base.vector_store import VectorStore


def main():
    embedder = Embedder()
    commentary_store = VectorStore("commentaries")

    user_query = "Why should we perform actions without expecting results?"
    query_embedding = embedder.embed(user_query)
    results = commentary_store.query(query_embedding)

    for index, result in enumerate(results[:5], start=1):
        metadata = result["metadata"]
        print("=" * 80)
        print(f"{index}. Ch.{metadata['chapter_number']} - {metadata['section_title']}")
        print(f"Distance: {result['distance']:.4f}")


if __name__ == "__main__":
    main()
