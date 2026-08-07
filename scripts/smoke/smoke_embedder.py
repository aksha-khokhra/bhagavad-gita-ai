import _bootstrap  # noqa: F401
from src.knowledge_base.builders.embedder import Embedder


def main():
    embedder = Embedder()

    embedding = embedder.embed("Krishna taught Arjuna.")
    print(type(embedding))
    print(embedding.shape)

    embeddings = embedder.embed_batch(
        [
            "Krishna taught Arjuna.",
            "The soul is eternal.",
            "Perform your duty.",
        ]
    )
    print(type(embeddings))
    print(embeddings.shape)


if __name__ == "__main__":
    main()
