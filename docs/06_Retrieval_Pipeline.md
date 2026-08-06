# Project Tattva Documentation

**Document:** 06 — Retrieval Pipeline  
**Version:** 1.3  
**Status:** Completed

---

# 1. Purpose

This document describes the online retrieval workflow used by Project Tattva to find relevant Bhagavad Gita verses, commentary, and chapter summaries for a user question.

Retrieval is evaluated independently from generation because a language model cannot produce a grounded answer when the required evidence was not retrieved.

---

# 2. Retrieval Objectives

The Retriever was designed to:

- Classify chapter-level questions before search.
- Embed each user query once.
- Search multiple vector collections.
- Preserve source separation.
- Return application-friendly result objects.
- Hide collection details from the Chatbot.
- Support future reranking and adaptive routing.

---

# 3. Retrieval Architecture

```text
User Query
    │
    ▼
Query Classification
    │
    ├── general
    ├── chapter_reference
    └── chapter_overview
    │
    ▼
Query Embedding
    │
    ├──────────────┬────────────────┬─────────────────┐
    ▼              ▼                ▼                 ▼
Verse Vector   Verse Lexical   Commentary Store   Chapter Store
    │              │                │                 │
    └──────┬───────┘                │                 │
           ▼                        │                 │
    Exact Ref Lookup                │                 │
           │                        │                 │
           ▼                        │                 │
     RRF Verse Fusion               │                 │
           └───────────────┬────────┴─────────────────┘
                           ▼
                Structured Result Dictionary
```

Verse retrieval is hybrid: exact reference lookup, dense vector search, and BM25 lexical search are fused with Reciprocal Rank Fusion.
---

# 4. Query Routing

The Retriever classifies each question before searching.

| Mode | Trigger examples | Behavior |
|------|------------------|----------|
| `chapter_reference` | `Summarize Chapter 6`, `What is Chapter 3 about?` | Retrieve that chapter summary and filter verses/commentary to the same chapter |
| `chapter_overview` | `Which chapter discusses meditation?`, `Give an overview of Karma Yoga` | Retrieve top chapter summaries plus normal verse/commentary search |
| `general` | `What is devotion?` | Verse and commentary search only |

Routing keeps ordinary verse questions compact while improving chapter-level and thematic overview answers.

---

# 5. Query Embedding

The user question is embedded with the same model used during indexing.

```python
query_embedding = self.embedder.embed(user_query)
```

Expected shape:

```text
(384,)
```

Using the same model ensures the query and stored documents are represented in the same vector space.

---

# 6. Collection Search

Commentary and chapter collections use vector search. Verse retrieval uses a hybrid path.

```python
verse_results = self._hybrid_verse_results(
    user_query,
    query_embedding,
    verse_n_results,
)

commentary_results = self.commentary_store.query(
    query_embedding,
    n_results=5
)
```

## Hybrid Verse Retrieval

1. Parse direct references such as `2.47` or `BG 2.47` and fetch matching verse metadata.
2. Run dense vector search for a larger candidate pool.
3. Run BM25 lexical search over verse translations.
4. Fuse candidates with Reciprocal Rank Fusion.
5. Keep exact matches and the strongest lexical hit near the front of the final list.

For explicit chapter references, metadata filters constrain results:

```python
where={"chapter_number": chapter_number}
```

---

# 7. VectorStore Query Output

ChromaDB returns nested result structures because it supports multiple query embeddings in one request.

The VectorStore converts the raw response into a list of dictionaries.

```python
[
    {
        "id": "...",
        "document": "...",
        "metadata": {...},
        "distance": 1.23
    }
]
```

Lower distance values represent closer vector matches within the current collection configuration.

---

# 8. Retriever Output Contract

The Retriever preserves source separation.

```python
{
    "verses": verse_results,
    "commentaries": commentary_results,
    "chapters": chapter_results,
    "route": {
        "mode": "chapter_reference",
        "chapter_number": 6
    }
}
```

A dictionary was selected instead of a positional list because named keys are clearer and easier to extend.

---

# 9. Why Source Results Remain Separate

Verses, commentary, and chapter summaries play different roles.

## Verses

- Primary source
- Used for direct scriptural grounding
- Formatted with reference and chapter title

## Commentaries

- Explanatory source
- Used to clarify concepts and vocabulary
- Formatted with chapter and section title

## Chapters

- Thematic overview source
- Used for chapter summaries and “which chapter” questions
- Formatted with title, meaning, and summary text

Returning separate groups prevents the Prompt Builder from having to rediscover the source type by filtering a mixed list.

---

# 10. Retrieval Evolution

## Initial Version

The first Retriever searched only the verse collection.

## Commentary-Supported Version

Commentary retrieval was introduced after evaluation showed vocabulary mismatch between classical translations and modern paraphrases.

## Chapter-Supported Version

Chapter summaries were indexed and routed after the documents were already constructed. Chapter routing targets overview and chapter-reference questions without changing general verse/commentary retrieval.

## Hybrid Verse Version

Exact verse-reference lookup and BM25 lexical search were added after evaluation showed two failure modes:

- Users asking for `2.47` / `BG 2.47` needed deterministic metadata lookup.
- Shared wording such as “fruit of action” was sometimes outranked by dense neighbors.

Hybrid fusion improved those cases while leaving commentary as the bridge for modern paraphrases that share little wording with the verse translation.

---

# 11. Retrieval Evaluation Method

A dedicated evaluation script runs a labeled query set and reports:

- Per-query hits and misses
- Recall@K
- Mean Reciprocal Rank
- Top commentary sections for inspection

Questions include conceptual prompts such as Karma Yoga, meditation, devotion, action and inaction, and selfless duty.

---

# 12. Observed Strengths

The verse retriever performed strongly for:

- Chapter 3 queries about Karma Yoga
- Chapter 6 queries about meditation and mind control
- Chapter 12 queries about devotion
- Chapter 4 queries about action and inaction

The commentary retriever improved conceptual explanation for selfless action and attachment to results.

Chapter routing correctly returns Chapter 6 for meditation overviews and filters to a named chapter when the user asks for a specific chapter summary.

Hybrid verse retrieval returns exact references such as `BG 2.47` and recovers translation-aligned phrases such as “fruit of action.”

---

# 13. Observed Limitations

- Verse 2.47 did not appear in the top 20 for a modern paraphrase of its teaching.
- Some broad concepts, such as steady wisdom, retrieved less relevant chapters.
- Fixed retrieval counts do not fully adapt to question type.
- Commentary sections can be long.
- Results from different collections are not reranked together.
- There is no score threshold for rejecting weak context.
- Chapter intent detection is rule-based rather than model-based.
- Modern paraphrases with little lexical overlap (for example, “expecting results”) can still miss Verse 2.47 in verse-only ranking.
- Results from different source types are not jointly reranked with a cross-encoder.

---

# 14. Future Retrieval Improvements

- Dynamic `top_k`
- Cross-encoder reranking
- Broader metadata filtering
- Commentary-to-verse linking
- Similarity thresholds
- Query rewriting and expansion
- Model-based query routing

---

# 15. Summary

Project Tattva's Retriever classifies chapter-level intent, embeds the user query once, searches the relevant collections, fuses hybrid verse candidates, and returns structured results grouped by source type.

The retrieval design was improved through direct evaluation rather than assumption. Commentary support bridged vocabulary gaps, chapter routing improved overview questions, and hybrid verse search improved exact references and translation-aligned wording.

---

**Next Document:** `07_Prompt_Engineering.md`
