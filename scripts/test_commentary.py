import _bootstrap  # noqa: F401
from src.knowledge_base.vector_store import VectorStore
from src.knowledge_base.builders.embedder import Embedder

embedder = Embedder()
commentary_store = VectorStore("commentaries")

user_query = "Why should we perform actions without expecting results?"

query_embedding = embedder.embed(user_query)

results = commentary_store.query(query_embedding)

print(results)