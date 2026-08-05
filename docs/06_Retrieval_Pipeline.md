# Project Tattva Documentation

**Document:** 06 — Retrieval Pipeline  
**Version:** 1.1  
**Status:** Completed

---

# 1. Purpose

This document describes the online retrieval workflow used by Project Tattva to find relevant Bhagavad Gita verses and commentary for a user question.

Retrieval is evaluated independently from generation because a language model cannot produce a grounded answer when the required evidence was not retrieved.

---

# 2. Retrieval Objectives

The Retriever was designed to:

- Embed each user query once.
- Search multiple vector collections.
- Preserve source separation.
- Return application-friendly result objects.
- Hide collection details from the Chatbot.
- Support future routing and reranking.

---

# 3. Retrieval Architecture

```text
User Query
    │
    ▼
Retriever
    │
    ▼
Query Embedding
    │
    ├─────────────────────────┐
    ▼                         ▼
Verse Collection       Commentary Collection
    │                         │
    ▼                         ▼
Top 3 Verses           Top 2 Commentaries
    └──────────────┬──────────┘
                   ▼
          Structured Result Dictionary
```

---

# 4. Query Embedding

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

# 5. Collection Search

The query embedding is sent independently to both active vector stores.

```python
verse_results = self.verse_store.query(
    query_embedding,
    n_results=3
)

commentary_results = self.commentary_store.query(
    query_embedding,
    n_results=2
)
```

The current fixed allocation keeps the prompt compact while providing both primary and explanatory evidence.

---

# 6. VectorStore Query Output

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

# 7. Retriever Output Contract

The Retriever preserves source separation.

```python
{
    "verses": verse_results,
    "commentaries": commentary_results
}
```

A dictionary was selected instead of a positional list because named keys are clearer and easier to extend.

---

# 8. Why Verse and Commentary Results Remain Separate

Verses and commentary play different roles.

## Verses

- Primary source
- Used for direct scriptural grounding
- Formatted with reference and chapter title

## Commentaries

- Explanatory source
- Used to clarify concepts and vocabulary
- Formatted with chapter and section title

Returning separate groups prevents the Prompt Builder from having to rediscover the source type by filtering a mixed list.

---

# 9. Retrieval Evolution

## Initial Version

The first Retriever searched only the verse collection.

This worked well for direct concepts such as:

- Karma Yoga
- Meditation
- Devotion
- Controlling the mind

However, it struggled when the user's wording differed from the translation.

---

## Commentary-Supported Version

Commentary retrieval was introduced after evaluation of the query:

```text
Why should we perform actions without expecting results?
```

Verse 2.47 uses wording related to the “fruit” of action, while relevant commentary uses the modern phrase “without attachment to the results.”

Adding commentary improved the final answer by supplying a closer semantic match and a clearer explanation.

---

# 10. Retrieval Evaluation Method

A dedicated evaluation script runs representative questions and prints:

- Retrieved verse reference
- Chapter title
- Distance

Questions included:

- What is Karma Yoga?
- What is meditation?
- What is devotion?
- How can I control my mind?
- What is the difference between action and inaction?
- Who is a person of steady wisdom?

This made retrieval failures visible before LLM generation was involved.

---

# 11. Observed Strengths

The verse retriever performed strongly for:

- Chapter 3 queries about Karma Yoga
- Chapter 6 queries about meditation and mind control
- Chapter 12 queries about devotion
- Chapter 4 queries about action and inaction

The commentary retriever improved conceptual explanation for selfless action and attachment to results.

---

# 12. Observed Limitations

- Verse 2.47 did not appear in the top 20 for a modern paraphrase of its teaching.
- Some broad concepts, such as steady wisdom, retrieved less relevant chapters.
- Fixed retrieval counts do not adapt to question type.
- Commentary sections can be long.
- Results from different collections are not reranked together.
- There is no score threshold for rejecting weak context.

---

# 13. Future Retrieval Improvements

- Query routing by question type
- Chapter summary retrieval
- Dynamic `top_k`
- Cross-encoder reranking
- Hybrid keyword and vector search
- Metadata filtering
- Commentary-to-verse linking
- Reciprocal Rank Fusion
- Similarity thresholds
- Query rewriting and expansion

---

# 14. Summary

Project Tattva's Retriever embeds the user query once, searches verse and commentary collections independently, and returns structured results grouped by source type.

The retrieval design was improved through direct evaluation rather than assumption. Commentary support was introduced because it successfully bridged vocabulary differences between classical translations and modern user questions.

---

**Next Document:** `07_Prompt_Engineering.md`
