# Project Tattva Documentation

**Document:** 10 — Future Development  
**Version:** 1.1  
**Status:** Planned

---

# 1. Purpose

This document records planned improvements beyond the Project Tattva v1.1 MVP.

The current version is complete enough for demonstration and interviews. Future work should be prioritized based on measured retrieval or usability limitations rather than feature count alone.

---

# 2. Current Baseline

Project Tattva v1.1 currently includes:

- Verse and commentary document builders
- Persistent ChromaDB collections
- Sentence Transformer embeddings
- Multi-source Retriever
- Source-aware PromptBuilder
- Local Ollama LLM integration
- Interactive CLI
- Manual retrieval evaluation

---

# 3. Version 1.2 — Retrieval Improvements

Planned improvements:

- Add normalized verse ranges to commentary metadata.
- Add source-specific distance inspection.
- Add dynamic retrieval counts.
- Add similarity thresholds.
- Improve evaluation data.

Goal:

Improve retrieval precision without changing the overall architecture.

---

# 4. Version 1.3 — Chapter Summary Integration

Planned improvements:

- Index the 18 chapter documents.
- Add a chapter summary VectorStore.
- Add chapter-level question detection.
- Format chapter summaries separately in the prompt.

Example use cases:

- Summarize Chapter 6.
- Which chapter discusses meditation?
- Give an overview of Karma Yoga.

---

# 5. Version 1.4 — Reranking

Planned improvements:

- Retrieve a larger candidate set.
- Apply a reranker to the candidates.
- Select the final context after reranking.

Possible approaches:

- Cross-encoder reranking
- Source-aware weighted ranking
- Reciprocal Rank Fusion

---

# 6. Version 1.5 — Hybrid Retrieval

Planned improvements:

- Combine vector retrieval with lexical search.
- Improve exact phrase and verse-reference matching.
- Support direct reference queries such as `2.47`.

Hybrid search may help when semantic retrieval misses domain-specific synonyms or exact terms.

---

# 7. Version 1.6 — Conversation Memory

Planned improvements:

- Store recent user and assistant turns.
- Support follow-up questions.
- Prevent unrelated history from polluting retrieval.
- Separate conversational context from Bhagavad Gita evidence.

---

# 8. Version 1.7 — API and Interface

Planned improvements:

- FastAPI backend
- Request and response schemas
- Error handling
- Health endpoint
- Streaming support
- Web chat interface

The existing Chatbot class can be called directly from the API layer.

---

# 9. Version 2.0 — Intelligent Query Routing

Version 2.0 is expected to introduce query-aware retrieval.

```text
User Query
    │
    ▼
Query Analyzer
    │
    ├── Verse question
    ├── Commentary question
    ├── Chapter overview question
    └── Multi-source question
    │
    ▼
Adaptive Retrieval Plan
    │
    ▼
Evidence Aggregation and Reranking
    │
    ▼
Grounded Response
```

Potential capabilities:

- Select relevant knowledge sources dynamically.
- Retrieve direct verse matches when references are provided.
- Use summaries for broad questions.
- Use commentary for explanation questions.
- Perform multi-step retrieval when one search is insufficient.

---

# 10. Evaluation Improvements

Future evaluation should include:

- Labeled query set
- Recall@K
- Precision@K
- Mean Reciprocal Rank
- Groundedness scoring
- Citation verification
- Response relevance scoring
- Model comparison
- Retrieval latency
- Generation latency

---

# 11. Production Readiness

Before production deployment, the project would require:

- Structured logging
- Automated tests
- Configuration validation
- Collection versioning
- Safe rebuild process
- Error boundaries
- Rate limiting
- Monitoring
- Security review
- Containerization
- Deployment documentation

---

# 12. Prioritization Principle

Future features should be added only when they address a demonstrated limitation.

The commentary collection was added because evaluation showed a vocabulary gap in verse-only retrieval. Future changes should follow the same evidence-driven process.

---

# 13. Summary

Project Tattva v1.1 provides a stable foundation for more advanced retrieval and user-interface features.

The next major technical milestone is chapter-summary integration, followed by reranking and hybrid retrieval. Version 2.0 will focus on intelligent query routing and adaptive evidence selection rather than simply searching every collection with fixed settings.

---

**Next Document:** `ADR.md`
