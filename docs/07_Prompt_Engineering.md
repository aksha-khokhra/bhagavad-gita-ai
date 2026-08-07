# Project Tattva Documentation

**Document:** 07 — Prompt Engineering  
**Version:** 1.2  
**Status:** Completed

---

# 1. Purpose

This document describes how Project Tattva converts retrieved verses, commentary, chapter summaries, and a user question into a structured prompt for the local language model.

Prompt construction is isolated from retrieval and LLM communication so that each layer can be modified and tested independently.

---

# 2. Prompt Engineering Objectives

The prompt was designed to:

- Restrict generation to retrieved context.
- Preserve the distinction between verses, commentary, and chapter summaries.
- Provide explicit source labels.
- Encourage concise synthesis.
- Reduce hallucination.
- Provide a controlled fallback for unsupported questions.
- Keep formatting readable for both humans and the model.

---

# 3. PromptBuilder Responsibilities

The `PromptBuilder` class:

- Loads the system prompt from a Markdown file once.
- Accepts the user query.
- Accepts structured Retriever output.
- Formats verses.
- Formats commentaries.
- Formats chapter summaries when present.
- Joins each source group with separators.
- Builds one final prompt string.

It does not:

- Generate embeddings.
- Search ChromaDB.
- Call Ollama.

---

# 4. External System Prompt

The system instructions are stored separately in:

```text
src/prompts/system_prompt.md
```

This allows behavior changes without modifying Python code.

The file is loaded in `PromptBuilder.__init__()` and stored in memory.

---

# 5. Grounding Rules

The system prompt instructs the model to:

- Use only retrieved context.
- Avoid outside knowledge.
- Avoid guessing.
- Avoid inventing verses or interpretations.
- Cite supported verse references.
- Synthesize multiple relevant sources.
- Return a fixed fallback statement when the context is insufficient.
- Avoid mentioning training data.

The fallback response is:

```text
I don't have enough information in the Bhagavad Gita knowledge base to answer that.
```

---

# 6. Verse Formatting

Verses are formatted as primary source material.

Example:

```text
Verse 4.16 (Jnana Karma Sanyasa Yoga)

Translation:
What is action and what is inaction? ...
```

The formatter uses verse metadata directly instead of reusing the full embedded document. This avoids duplicated labels and gives the Prompt Builder control over presentation.

---

# 7. Commentary Formatting

Commentary is formatted as explanatory material.

Example:

```text
Chapter 3

Section:
Leaders should set an example

Commentary:
Therefore, always perform your duty efficiently...
```

The formatter uses `metadata["content"]` rather than the full embedded document to avoid repeating chapter and section labels.

---

# 8. Chapter Summary Formatting

Chapter summaries are included only when the Retriever routes a chapter-level question.

Example:

```text
Chapter 6: Dhyana Yoga
Meaning: The Yoga of Meditation

Summary:
...
```

The formatter uses chapter metadata directly so the model receives a clean overview block.

---

# 9. Prompt Structure

The final prompt follows this order:

```text
System Instructions

========================
Chapter Summaries
========================

Formatted chapter summaries (when routed)

========================
Relevant Verses
========================

Formatted verses

========================
Commentary (Explanation)
========================

Formatted commentary

========================
Question
========================

User question

========================
Response
========================
```

Chapter summaries appear first for overview questions. Verses remain the primary scriptural evidence when present.

---

# 10. Why Sources Are Separated

The prompt keeps verses, commentary, and chapter summaries under different headings because:

- Verses are authoritative source text.
- Commentary is interpretation.
- Chapter summaries are thematic overviews.
- The model should not present commentary or summaries as direct Bhagavad Gita quotations.
- Separate sections improve readability.
- Future prompts can assign different rules to each source type.

---

# 11. Context Assembly

Each formatted result is added to a list and joined once.

```python
verse_context = separator.join(verse_parts)
commentary_context = separator.join(commentary_parts)
```

This approach is clearer and more efficient than repeatedly concatenating immutable strings inside a loop.

---

# 12. Prompt Iteration

The prompt evolved during testing.

## Initial Prompt

The first prompt used one generic “Retrieved Knowledge” section.

## Improved Prompt

The revised prompt:

- Removed duplicated chapter labels.
- Removed unwanted indentation from triple-quoted strings.
- Added separate verse and commentary sections.
- Strengthened the out-of-scope instruction.
- Prevented training-data disclaimers.
- Encouraged coherent synthesis.

## Chapter Integration

Chapter summary sections were added for routed overview and chapter-reference questions.

---

# 13. Observed Result

With verse-only context, the system could not directly answer why actions should be performed without expecting results.

After commentary was added, the response correctly discussed:

- Performing work without attachment to results
- Selfless action
- Universal welfare
- Relevant commentary sections and verse ranges

This demonstrated that prompt quality depends on both formatting and retrieval quality.

---

# 14. Current Limitations

- The smaller local model may still produce awkward wording.
- Citations are generated from the context rather than validated after generation.
- Commentary can dominate the answer when verse retrieval is weak.
- There is no token-budget manager.
- Long commentary sections are not compressed.

---

# 15. Future Improvements

- Add structured citation validation.
- Add token-aware context truncation.
- Add source-specific context limits.
- Add model-specific prompt templates.
- Add conversation-history support.

---

# 16. Summary

Project Tattva uses a dedicated PromptBuilder to convert structured retrieval results into a grounded, readable prompt.

The prompt separates scripture, commentary, and chapter summaries, restricts the model to retrieved context, and provides a controlled fallback for unsupported questions. This design improves transparency and keeps prompt logic independent from retrieval and model communication.

---

**Next Document:** `08_Application_Integration.md`
