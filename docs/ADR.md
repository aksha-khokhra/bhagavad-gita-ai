# Project Tattva Documentation

**Document:** Architecture Decision Records  
**Version:** 1.1  
**Status:** Active

---

# ADR-001 — Use Retrieval-Augmented Generation

**Status:** Accepted

## Context

A general LLM can answer questions about the Bhagavad Gita but may hallucinate, omit references, or mix unsupported interpretations.

## Decision

Use Retrieval-Augmented Generation so that relevant source material is retrieved before generation.

## Consequences

- Responses can be grounded in curated data.
- Retrieval quality becomes a critical dependency.
- The system requires document processing, embeddings, and vector storage.

---

# ADR-002 — Preserve Natural Semantic Units

**Status:** Accepted

## Context

Fixed-size chunks can break verses and commentary sections at arbitrary boundaries.

## Decision

Use one verse, one commentary section, and one chapter summary as the primary document units.

## Consequences

- Semantic integrity is preserved.
- Chunk sizes vary.
- Long commentary sections may require future compression or sub-sectioning.

---

# ADR-003 — Use Separate Knowledge Collections

**Status:** Accepted

## Context

Verses, commentary, and chapter summaries serve different purposes.

## Decision

Store each knowledge type in an independent ChromaDB collection.

## Consequences

- Source-specific retrieval and formatting are possible.
- The Retriever must coordinate multiple stores.
- Future routing can select collections independently.

---

# ADR-004 — Use Sentence Transformers

**Status:** Accepted

## Context

The project requires a local, lightweight embedding model for semantic search.

## Decision

Use `all-MiniLM-L6-v2` through Sentence Transformers.

## Consequences

- Embeddings are generated locally.
- Vectors contain 384 dimensions.
- Domain-specific paraphrases may not always rank ideally.

---

# ADR-005 — Use Persistent ChromaDB

**Status:** Accepted

## Context

Regenerating embeddings whenever the application starts would be inefficient.

## Decision

Use `chromadb.PersistentClient` and store collections under `data/chroma_db`.

## Consequences

- Embeddings persist across sessions.
- Collection rebuilds require careful handling.
- Local storage must be excluded or managed appropriately in Git.

---

# ADR-006 — Wrap ChromaDB Behind VectorStore

**Status:** Accepted

## Context

Raw ChromaDB response structures should not spread through the application.

## Decision

Create a VectorStore class that handles collection access and returns clean result dictionaries.

## Consequences

- The rest of the application is less coupled to ChromaDB.
- Replacing the vector database would primarily affect one component.

---

# ADR-007 — Introduce a Retriever Service

**Status:** Accepted

## Context

The Chatbot initially performed query embedding and verse retrieval directly. Commentary support made retrieval more complex.

## Decision

Move embedding and multi-collection search into a dedicated Retriever class.

## Consequences

- The Chatbot remains a simple orchestrator.
- New stores and ranking logic can be added inside the Retriever.
- Retrieval can be tested independently.

---

# ADR-008 — Preserve Verse and Commentary Separation in Retriever Output

**Status:** Accepted

## Context

A mixed result list would require the PromptBuilder to filter source types again.

## Decision

Return a dictionary with named `verses` and `commentaries` keys.

## Consequences

- The output contract is self-documenting.
- Prompt formatting remains simple.
- Additional source keys can be added later.

---

# ADR-009 — Store Prompt Instructions Outside Python Code

**Status:** Accepted

## Context

Prompt wording may change frequently during testing.

## Decision

Store the system prompt in a Markdown file and load it once in PromptBuilder.

## Consequences

- Prompt changes do not require Python edits.
- Multiple prompt templates can be added later.

---

# ADR-010 — Use Ollama for the MVP

**Status:** Accepted

## Context

The project requires a no-cost local LLM option for development and demonstrations.

## Decision

Use Ollama with `phi3:mini` for the initial release.

## Consequences

- The system can run locally.
- Response quality depends on local model capability.
- The LLMClient abstraction allows a future provider change.

---

# ADR-011 — Evaluate Retrieval Before Generation

**Status:** Accepted

## Context

A poor answer may be caused by retrieval, prompt construction, or generation.

## Decision

Create a dedicated retrieval evaluation script that inspects references and distances without calling the LLM.

## Consequences

- Retrieval failures can be isolated.
- Architecture improvements can be evidence-driven.
- Quantitative metrics can be added later.

---

# ADR-012 — Add Commentary After Evaluation

**Status:** Accepted

## Context

The dense-only baseline Retriever failed to retrieve Verse 2.47 in the top 20 for a modern paraphrase about performing actions without expecting results.

## Decision

Add a commentary collection and retrieve explanatory sections alongside verses.

## Consequences

- Conceptual retrieval and generation improved.
- Prompt context became longer.
- Future ranking and token-budget controls may be required.

---

# ADR-013 — Defer Chapter Summary Retrieval

**Status:** Superseded by ADR-014

## Context

Chapter documents are available, but the current MVP focuses on verse and commentary questions.

## Decision

Keep chapter summaries prepared but outside the active Retriever until query routing is introduced.

## Consequences

- The MVP remains focused.
- Broad chapter questions are not yet optimized.
- Chapter integration remains a clear next milestone.

---

# ADR-014 — Integrate Chapter Summary Retrieval with Routing

**Status:** Accepted

## Context

Chapter documents were already constructed. Overview and chapter-reference questions were poorly served by verse and commentary retrieval alone.

## Decision

Index the `chapters` collection and add rule-based query routing:

- `chapter_reference` for explicit chapter numbers
- `chapter_overview` for summary / which-chapter style questions
- `general` for ordinary verse and commentary questions

Format chapter summaries as a separate prompt section when routed.

## Consequences

- Chapter overviews and thematic chapter discovery improve.
- Explicit chapter questions can filter verses and commentary to that chapter.
- Routing remains rule-based and may miss some nuanced intents.
- Prompt length increases for chapter-routed questions.

---

# ADR-015 — Hybrid Verse Retrieval with RRF

**Status:** Accepted

## Context

Dense verse retrieval missed exact reference queries such as `BG 2.47` and under-ranked translation-aligned phrases such as “fruit of action.” Evaluation also showed that modern paraphrases with little lexical overlap still need commentary support.

Dense similarity scores and BM25 scores are not on a compatible scale, so a naive weighted sum is unreliable.

## Decision

Retrieve verses with three channels and fuse them:

1. Exact metadata lookup for parsed verse references
2. Dense vector search
3. In-memory BM25 lexical search over verse translations

Merge candidates with Reciprocal Rank Fusion, preferring exact matches and preserving the strongest lexical hit. Then apply cross-encoder reranking.

## Alternatives considered

- Dense-only retrieval
- BM25-only retrieval
- Weighted raw-score combination across dense and lexical scores

RRF was selected because it combines ranks without requiring calibrated score fusion.

## Consequences

- Exact verse references become deterministic.
- Shared wording with translations improves verse recall.
- Modern paraphrases with weak lexical overlap can still miss; commentary remains important.
- Retriever startup loads an in-memory lexical index from verse documents.

---

# ADR-016 — Cross-Encoder Reranking

**Status:** Accepted

## Context

Hybrid fusion improved candidate recall, but final ordering still depended on vector distance and BM25 rank. A larger candidate pool needs pairwise relevance scoring before prompt construction.

## Decision

After hybrid verse fusion and commentary vector retrieval, rerank candidates with `cross-encoder/ms-marco-MiniLM-L-6-v2`.

Preserve exact verse references and the strongest BM25 hit so reranking cannot undo those rescues.

## Consequences

- Final context ordering better reflects query-document relevance.
- Startup and per-query latency increase because a second model is loaded and scored.
- General-purpose reranker scores are not domain-tuned to Bhagavad Gita translations.
- Aggregate Recall@K may stay similar when the right verse was already present; gains appear mainly as better ranking and commentary selection.

---

# ADR-017 — Out-of-Scope Rejection via Rerank Score

**Status:** Accepted

## Context

Vector search always returns nearest neighbors. Out-of-domain questions such as “Who built the Taj Mahal?” could still retrieve Gita verses and reach the LLM.

Probe runs showed a clear score gap for `cross-encoder/ms-marco-MiniLM-L-6-v2`:

- In-scope top scores were typically above about `-4`
- Out-of-scope top scores were typically below about `-8`

## Decision

After retrieval and reranking, reject a query when the best verse/commentary `rerank_score` is below `MIN_RELEVANCE_SCORE = -6.5`.

Exact verse references and successful `chapter_reference` routes are never rejected. Overview-style chapter queries still pass through the rerank-score check. The Chatbot returns a deterministic fallback without calling Ollama.

## Consequences

- Out-of-scope rejection becomes measurable and deterministic.
- Thresholds are model-specific and may need retuning if the reranker changes.
- Borderline weak in-scope questions could be rejected if scores fall near the cutoff.

---

# Summary

These records document the major architectural choices made during Project Tattva v1.

The decisions emphasize semantic integrity, source separation, modularity, local execution, and evidence-driven iteration.
