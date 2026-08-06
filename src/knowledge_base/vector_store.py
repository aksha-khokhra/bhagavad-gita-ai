import chromadb

from src.knowledge_base.config import CHROMA_DB_PATH


class VectorStore:
    def __init__(self, collection_name: str):
        self.client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        ids,
        embeddings,
        documents,
        metadatas
    ):
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def query(self, query_embedding, n_results=5, where=None):
        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": n_results,
        }
        if where is not None:
            query_kwargs["where"] = where

        results = self.collection.query(**query_kwargs)

        retrieved_documents = []

        for doc_id, document, metadata, distance in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            retrieved_documents.append({
                "id": doc_id,
                "document": document,
                "metadata": metadata,
                "distance": distance
            })

        return retrieved_documents

    def get_by_metadata(self, where):
        results = self.collection.get(
            where=where,
            include=["documents", "metadatas"],
        )

        retrieved_documents = []
        for doc_id, document, metadata in zip(
            results["ids"],
            results["documents"],
            results["metadatas"],
        ):
            retrieved_documents.append({
                "id": doc_id,
                "document": document,
                "metadata": metadata,
                "distance": 0.0,
            })

        return retrieved_documents
