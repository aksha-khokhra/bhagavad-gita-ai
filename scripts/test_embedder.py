import _bootstrap  # noqa: F401
from src.knowledge_base.builders.embedder import Embedder

embedder = Embedder()

# Single embedding
embedding = embedder.embed("Krishna taught Arjuna.")

print(type(embedding))
print(embedding.shape)

# Batch embedding
embeddings = embedder.embed_batch(
    [
        "Krishna taught Arjuna.",
        "The soul is eternal.",
        "Perform your duty."
    ]
)

print(type(embeddings))
print(embeddings.shape)