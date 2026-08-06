# Project Tattva Documentation

**Document:** 10 — Future Development  
**Version:** 1.2  
**Status:** Planned

---

# 1. Purpose

This document records planned improvements beyond Project Tattva v1.2.

The current version includes verse, commentary, and chapter-summary retrieval with chapter-level routing. Future work should be prioritized based on measured retrieval or usability limitations rather than feature count alone.

---

# 2. Current Baseline

Project Tattva v1.2 currently includes:

- Verse, commentary, and chapter document builders
- Persistent ChromaDB collections for all three sources
- Sentence Transformer embeddings
- Multi-source Retriever with chapter routing
- Source-aware PromptBuilder
- Local Ollama LLM integration
- Interactive CLI
- Labeled retrieval evaluation (Recall@K / MRR)

---

# 3. Version 1.3 — Retrieval Improvements

Planned improvements:

- Add normalized verse ranges to commentary metadata.
- Add source-specific distance inspection.
- Add dynamic retrieval counts.
- Add similarity thresholds.
- Improve evaluation data coverage.

Goal:

Improve retrieval precision without changing the overall architecture.

---

# 4. Version 1.4 — Reranking

Planned improvements:

- Retrieve a larger candidate set.
- Apply a reranker to the candidates.
- Select the final context after reranking.

Possible approaches:

- Cross-encoder reranking
- Source-aware weighted ranking
- Reciprocal Rank Fusion

---

# 5. Version 1.5 — Hybrid Retrieval

Planned improvements:

- Combine vector retrieval with lexical search.
- Improve exact phrase and verse-reference matching.
- Support direct reference queries such as `2.47`.

Hybrid search may help when semantic retrieval misses domain-specific synonyms or exact terms.

---

# 6. Version 1.6 — Conversation Memory

Planned improvements:

- Store recent user and assistant turns.
- Support follow-up questions.
- Prevent unrelated history from polluting retrieval.
- Separate conversational context from Bhagavad Gita evidence.

---

# 7. Version 1.7 — API and Interface

Planned improvements:

- FastAPI backend
- Request and response schemas
- Error handling
- Health endpoint
- Streaming support
- Web chat interface

The existing Chatbot class can be called directly from the API layer.

---

# 8. Version 2.0 — Intelligent Query Routing

Version 2.0 is expected to replace rule-based chapter detection with richer query-aware retrieval.

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

# 9. Evaluation Improvements

Future evaluation should include:

- Broader labeled query coverage
- Precision@K
- Groundedness scoring
- Citation verification
- Response relevance scoring
- Model comparison
- Retrieval latency
- Generation latency

---

# 10. Production Readiness

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

# 11. Prioritization Principle

Future features should be added only when they address a demonstrated limitation.

Commentary was added because evaluation showed a vocabulary gap in verse-only retrieval. Chapter routing was added because chapter documents were ready and overview questions needed a dedicated source. Future changes should follow the same evidence-driven process.

---

# 12. Summary

Project Tattva v1.2 provides a stable foundation for more advanced retrieval and user-interface features.

The next technical milestones are reranking and hybrid retrieval, followed by conversation memory and an API/UI layer. Version 2.0 will focus on intelligent query routing and adaptive evidence selection rather than simply searching every collection with fixed settings.

---

**Next Document:** `ADR.md`
