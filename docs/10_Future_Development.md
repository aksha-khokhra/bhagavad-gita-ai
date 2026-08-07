# Project Tattva Documentation

**Document:** 10 — Future Development  
**Version:** 1.0  
**Status:** Planned beyond v1

---

# 1. Purpose

This document records planned improvements beyond Project Tattva v1.

v1 is intentionally complete for portfolio and interview use. Future work should be prioritized based on measured limitations rather than feature count alone.

---

# 2. Current Baseline (v1)

Project Tattva v1 currently includes:

- Verse, commentary, and chapter document builders
- Persistent ChromaDB collections for all three sources
- Sentence Transformer embeddings
- Multi-source Retriever with chapter routing
- Hybrid verse retrieval (exact reference + BM25 + vector RRF)
- Cross-encoder reranking for verses and commentary
- Out-of-scope rejection based on rerank score
- Source-aware PromptBuilder
- Local Ollama LLM integration
- Interactive CLI
- Typed labeled retrieval evaluation

---

# 3. Next Possible Improvements

- Retrieval hardening (dynamic `top_k`, similarity thresholds, commentary verse ranges)
- Conversation memory
- FastAPI backend and web interface
- Response-quality evaluation
- Domain-adapted reranker training
- Intelligent query routing beyond rule-based chapter detection

---

# 4. Prioritization Principle

Future features should be added only when they address a demonstrated limitation.

v1 stopped after hybrid retrieval, reranking, routing, evaluation, and out-of-scope protection because those closed the measured gaps needed for a credible RAG demo.

---

**Next Document:** `ADR.md`
