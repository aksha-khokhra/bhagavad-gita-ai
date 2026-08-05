# Project Tattva Documentation

**Document:** 05 — Knowledge Base Construction  
**Version:** 1.1  
**Status:** Completed

---

# 1. Purpose

This document describes how Project Tattva converts processed datasets into embedding-ready documents and persistent ChromaDB collections.

Knowledge base construction is an offline workflow. It is performed when source documents, document builders, or the embedding model change. The resulting vector database is then reused during user queries.

---

# 2. Construction Objectives

The construction pipeline was designed to:

- Create a standard document structure for all sources.
- Generate embeddings efficiently in batches.
- Preserve source metadata.
- Store embeddings persistently.
- Build independent collections.
- Reuse the same Embedder and VectorStore abstractions.

---

# 3. Standard Document Structure

Every document builder produces objects with the same top-level shape.

```json
{
    "id": "unique_document_id",
    "document": "text used for embedding",
    "metadata": {
        "source": "..."
    }
}
```

This common structure allows one reusable indexing function to process verses, commentary, and chapter summaries.

---

# 4. Document Builders

## 4.1 Verse Builder

The Verse Builder creates one document per verse.

Document ID format:

```text
verse_<chapter>_<verse>
```

Example:

```text
verse_2_47
```

The embedded document contains chapter context and English translation. Detailed fields remain in metadata.

Output:

```text
data/processed/verse_documents.json
```

Record count:

```text
701
```

---

## 4.2 Commentary Builder

The Commentary Builder creates one document per semantic commentary section.

Document ID format:

```text
commentary_<chapter>_<section>
```

Output:

```text
data/processed/commentary_documents.json
```

Record count:

```text
136
```

---

## 4.3 Chapter Builder

The Chapter Builder creates one document per chapter summary.

Document ID format:

```text
chapter_<chapter_number>
```

Output:

```text
data/processed/chapter_documents.json
```

Record count:

```text
18
```

---

# 5. Embedder Component

The Embedder wraps the Sentence Transformers model configured in `config.py`.

Current model:

```text
all-MiniLM-L6-v2
```

The model produces 384-dimensional vectors.

---

## 5.1 Single Embedding

```python
embedding = embedder.embed(text)
```

Expected shape:

```text
(384,)
```

---

## 5.2 Batch Embedding

```python
embeddings = embedder.embed_batch(texts)
```

For 701 verse documents, the expected shape is:

```text
(701, 384)
```

Batch embedding is used during indexing because it is more efficient than calling the model separately for every document.

---

# 6. VectorStore Component

The VectorStore wraps access to one ChromaDB collection.

During initialization, it:

- Connects to a persistent ChromaDB path.
- Opens an existing collection or creates a new one.

The `add()` method receives parallel lists:

- ids
- embeddings
- documents
- metadatas

Items at the same list index are stored as one record.

---

# 7. Persistent Storage

Project Tattva uses `chromadb.PersistentClient`.

The vector database is stored under:

```text
data/chroma_db
```

Persistence allows the chatbot to reuse indexed embeddings after the application restarts.

---

# 8. Reusable Indexing Function

The indexing script uses a reusable function similar to:

```python
def build_collection(embedder, collection_name, json_file):
    ...
```

The function performs the following operations:

1. Open the JSON file with UTF-8 encoding.
2. Load the document list.
3. Extract IDs.
4. Extract embedding text.
5. Extract metadata.
6. Generate embeddings in one batch.
7. Add all records to the requested collection.

The same Embedder instance is reused across collection builds.

---

# 9. Active Collections

| Collection | Documents | Status |
|------------|-----------|--------|
| `verses` | 701 | Indexed |
| `commentaries` | 136 | Indexed |
| `chapters` | 18 | Not yet indexed in active release |

---

# 10. Indexing Workflow

```text
Processed Document JSON
          │
          ▼
Load with UTF-8
          │
          ▼
Extract IDs, Text, Metadata
          │
          ▼
Embedder.embed_batch(texts)
          │
          ▼
VectorStore.add(...)
          │
          ▼
Persistent ChromaDB Collection
```

---

# 11. Testing

The construction layer was tested incrementally.

## Embedder Test

Verified:

- Single embedding shape
- Batch embedding shape
- Model loading

## VectorStore Test

Verified:

- Collection creation
- Persistent connection
- Record insertion
- Query response conversion

## Full Index Test

Verified:

- 701 verse documents indexed
- 136 commentary documents indexed

Modules are executed from the project root using:

```bash
python -m scripts.<module_name>
```

The `.py` extension is not included when using `-m`.

---

# 12. Error Handling and Lessons

## UTF-8 Decode Error

A Windows default-encoding error occurred while reading Sanskrit content.

Resolution:

```python
open(path, "r", encoding="utf-8")
```

## Module Import Error

Running scripts directly produced package import errors.

Resolution:

Run scripts as modules from the repository root.

## Collection Name vs Document Path

Collection names and JSON paths were separated into different configuration constants to prevent accidental misuse.

---

# 13. Current Limitations

- The chapter collection has not yet been indexed.
- Rebuilding collections is not yet fully idempotent.
- No automatic collection versioning exists.
- The embedding model is fixed through configuration.
- Indexing progress uses simple terminal output rather than structured logging.

---

# 14. Summary

The Knowledge Base Construction phase converts structured Bhagavad Gita documents into persistent vector collections.

By using reusable document builders, batch embeddings, source metadata, and a generic VectorStore abstraction, the same construction workflow supports multiple knowledge sources without duplicated indexing logic.

---

**Next Document:** `06_Retrieval_Pipeline.md`
