# Project Tattva Documentation

**Document:** 04 — Knowledge Base Design  
**Version:** 1.2  
**Status:** Completed

---

# 1. Purpose

This document describes the design of the knowledge layer used by Project Tattva.

The project separates different forms of Bhagavad Gita knowledge instead of storing everything in one collection. This allows verses, commentary, and chapter summaries to retain their individual meaning, metadata, and retrieval role.

---

# 2. Design Objectives

The knowledge layer was designed to:

- Preserve natural semantic units.
- Separate primary sources from interpretation.
- Support source-aware prompt construction.
- Allow independent retrieval counts.
- Improve maintainability.
- Support future routing and reranking.
- Preserve citations and traceability.

---

# 3. Knowledge Base Architecture

```text
                         Knowledge Layer

        ┌────────────────────────────────────┐
        │ Verse Knowledge Base               │
        │ Status: Active                     │
        └────────────────────────────────────┘

        ┌────────────────────────────────────┐
        │ Commentary Knowledge Base          │
        │ Status: Active                     │
        └────────────────────────────────────┘

        ┌────────────────────────────────────┐
        │ Chapter Summary Knowledge Base     │
        │ Status: Documents Built            │
        └────────────────────────────────────┘
```

The active Retriever currently searches the verse and commentary collections.

---

# 4. Verse Knowledge Base

## Purpose

The Verse Knowledge Base provides the primary scriptural evidence used by the system.

It answers:

> What does the Bhagavad Gita say?

---

## Retrieval Unit

One verse is stored as one independent document.

This preserves the smallest complete unit of meaning without combining unrelated verses or splitting a verse into fragments.

---

## Embedded Content

The embedding text includes:

- Chapter title
- Chapter title meaning
- English translation

Example:

```text
Chapter: Sankhya Yoga
Meaning: Transcendental Knowledge
Translation: But you have only the right to work...
```

---

## Metadata

Verse metadata includes:

- record_id
- source
- reference
- chapter_number
- verse_number
- chapter_title
- chapter_title_meaning
- english_translation
- sanskrit_text

Metadata supports prompt formatting, display, filtering, and evaluation.

---

## Design Decisions

### One Verse = One Document

Reason:

Verses are natural semantic boundaries.

### English Translation is Embedded

Reason:

The current system accepts English-language queries.

### Chapter Context is Embedded

Reason:

Chapter title and meaning provide additional semantic cues.

### Sanskrit is Preserved

Reason:

The original text remains available without dominating English retrieval.

---

# 5. Commentary Knowledge Base

## Purpose

The Commentary Knowledge Base provides explanations and philosophical interpretation.

It answers:

> What does the teaching mean, and how is it explained?

Commentary is especially useful when user wording differs from the wording of the verse translation.

---

## Retrieval Unit

One commentary section is stored as one document.

A section may explain one verse, several verses, or one broader concept.

---

## Embedded Content

The embedding text includes:

- Chapter number
- Section title
- Commentary content

Example:

```text
Chapter: 3
Section: Leaders should set an example
Commentary: Therefore, always perform your duty efficiently...
```

---

## Metadata

Commentary metadata includes:

- source
- chapter_number
- section_number
- section_title
- content

Verse references remain present inside the content. Normalized verse-range metadata is planned for a future version.

---

## Design Decisions

### One Section = One Document

Reason:

Section boundaries preserve philosophical continuity.

### Commentary Stored Separately from Verses

Reason:

Commentary is interpretation, not primary scripture. The separation prevents the two source types from becoming indistinguishable.

### Section Title is Embedded

Reason:

Titles provide strong thematic retrieval cues.

---

# 6. Chapter Summary Knowledge Base

## Purpose

The Chapter Summary Knowledge Base supports broad chapter-level and overview questions.

It is intended to answer questions such as:

- What is Chapter 3 about?
- Which chapter discusses meditation?
- Summarize Karma Yoga.

---

## Retrieval Unit

One chapter summary is stored as one document.

---

## Embedded Content

The document includes:

- Chapter title
- Chapter title meaning
- Chapter summary

---

## Metadata

Chapter metadata includes:

- source
- chapter_number
- chapter_title
- chapter_title_meaning
- summary

---

## Current Status

The 18 chapter documents are indexed in the `chapters` ChromaDB collection and connected to the active Retriever through chapter-level query routing.

---

# 7. Why Multiple Knowledge Bases?

The three knowledge sources represent different levels of information.

| Knowledge Source | Primary Role |
|------------------|--------------|
| Verse | Authoritative scriptural evidence |
| Commentary | Interpretation and conceptual explanation |
| Chapter Summary | Broad thematic understanding |

Keeping them separate allows the system to:

- Retrieve different counts from each source.
- Format each source differently.
- Evaluate each source independently.
- Add query routing later.
- Preserve the distinction between scripture and interpretation.

---

# 8. Evidence Supporting Commentary Retrieval

During evaluation, the verse-only retriever failed to return Verse 2.47 for the query:

```text
Why should we perform actions without expecting results?
```

The verse translation uses the phrase “fruit of action,” while the user used “expecting results.” A relevant commentary section used the more direct phrase “without attachment to the results.”

This experiment demonstrated that commentary can bridge the vocabulary gap between classical translation language and modern user phrasing.

---

# 9. Alternatives Considered

## Single Knowledge Base

Rejected because source types would be mixed and harder to control.

## Commentary-Only Retrieval

Rejected because the system should retain the original verses as the primary source.

## Verse-Only Retrieval

Used in the first MVP, but expanded after evaluation showed limitations for paraphrased philosophical questions.

## Fixed-Size Chunks

Rejected because they could split natural semantic sections.

---

# 10. Design Principles

## Semantic Integrity

Documents follow natural boundaries.

## Source Separation

Primary scripture and commentary remain distinct.

## Explainability

References and metadata remain available after retrieval.

## Extensibility

New collections can be introduced without changing the VectorStore interface.

## Evaluation Independence

Each collection can be queried and inspected separately.

---

# 11. Future Improvements

- Add normalized commentary verse ranges.
- Link commentary sections to related verse records.
- Add metadata filtering beyond chapter routing.
- Add reranking across sources.
- Add hybrid semantic and keyword retrieval.
- Add multilingual collections.

---

# 12. Summary

Project Tattva uses separate knowledge bases for verses, commentary, and chapter summaries because each source represents a different level of understanding.

The current release actively combines verse, commentary, and chapter-summary retrieval. This provides primary evidence, explanatory context, and chapter-level grounding while preserving a clear distinction between the sources.

---

**Next Document:** `05_Knowledge_Base_Construction.md`
