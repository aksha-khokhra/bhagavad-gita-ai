# Project Tattva Documentation

**Document:** 03 — Data Engineering  
**Version:** 1.1  
**Status:** Completed

---

# 1. Purpose

This document describes the data engineering workflow used to transform raw Bhagavad Gita resources into clean, structured, and retrieval-ready datasets.

The quality of a RAG system depends heavily on the quality and structure of its source documents. Project Tattva therefore preserves natural semantic boundaries instead of relying on arbitrary fixed-length chunks.

---

# 2. Data Engineering Objectives

The data pipeline was designed to:

- Preserve verse-level meaning.
- Preserve commentary section boundaries.
- Create one summary document per chapter.
- Retain source references and metadata.
- Produce consistent JSON structures.
- Support independent document builders.
- Prepare all sources for embedding and vector storage.

---

# 3. Data Sources

Project Tattva uses three knowledge sources.

| Dataset | Purpose |
|---------|---------|
| Verse data | Primary Bhagavad Gita verses and translations |
| Commentary source | Explanatory chapter sections and philosophical discussion |
| Chapter summaries | High-level chapter understanding |

Each source is processed independently because its structure and retrieval role are different.

---

# 4. Data Pipeline Overview

```text
Raw Data Sources
      │
      ├── Verse JSON data
      ├── Commentary PDF
      └── Chapter-level content
      │
      ▼
Parsing and Extraction
      │
      ▼
Cleaning and Normalization
      │
      ▼
Validation
      │
      ▼
Structured Processed Data
      │
      ▼
Embedding-Ready Document Builders
```

---

# 5. Verse Dataset Processing

## 5.1 Source Data

The verse data includes:

- Chapter number
- Verse number
- Chapter title
- Chapter title meaning
- Sanskrit text
- English translation
- Record identifier

---

## 5.2 Transformation

The verse pipeline:

- Merged records into one unified dataset.
- Preserved all 18 chapters.
- Preserved all 701 verses.
- Assigned stable identifiers.
- Standardized field names.
- Retained both source text and English translation.

---

## 5.3 Processed Output

Primary processed file:

```text
data/processed/merged_records.json
```

Each record contains the information required by the verse document builder.

---

# 6. Commentary Dataset Processing

## 6.1 Source Data

The commentary source was a PDF containing:

- Chapter introductions
- Section headings
- Philosophical explanations
- Verse references
- Page headers and footers

The PDF was unstructured compared with the verse JSON data.

---

## 6.2 Extraction Strategy

The parser used PyMuPDF to extract text and layout information.

The processing logic identified:

- Chapter boundaries
- Section titles
- Section content
- Repeated headers and footers
- Non-content artifacts

Each meaningful commentary section was preserved as one semantic unit.

---

## 6.3 Cleaning Operations

The cleaning stage included:

- Removing repeated page headers and footers.
- Removing irrelevant publication artifacts.
- Standardizing whitespace.
- Preserving section headings.
- Preserving embedded verse references.
- Removing malformed trailing records.

---

## 6.4 Processed Output

The finalized commentary data contains 136 semantic sections.

Each section includes:

- chapter_number
- section_number
- section_title
- content

The data is later converted into `commentary_documents.json` by the commentary document builder.

---

# 7. Chapter Summary Processing

## 7.1 Source Data

Chapter-level content was processed into one summary for each Bhagavad Gita chapter.

---

## 7.2 Transformation

The chapter summary pipeline:

- Preserved chapter number.
- Preserved chapter title.
- Preserved chapter title meaning.
- Stored one summary per chapter.
- Produced 18 chapter-level records.

---

## 7.3 Processed Output

The final chapter data is converted into:

```text
data/processed/chapter_documents.json
```

These documents are available for future chapter-summary retrieval.

---

# 8. Data Validation

Validation was performed before document construction.

Checks included:

- Required keys are present.
- Chapter numbers are within the valid range.
- Verse numbers are present for verse records.
- IDs are unique.
- Empty content is rejected.
- JSON structure is valid.
- Trailing artifacts are removed.
- The expected verse count is preserved.

---

# 9. Encoding Considerations

The datasets contain Sanskrit and special punctuation. Files are therefore read explicitly using UTF-8.

Example:

```python
with open(path, "r", encoding="utf-8") as file:
    data = json.load(file)
```

This avoids Windows default-encoding errors when processing multilingual text.

---

# 10. Data Quality Principles

## Semantic Integrity

Natural units such as verses, commentary sections, and full chapter summaries are preserved.

## Traceability

References, chapter numbers, and source types remain available as metadata.

## Consistency

Every embedding-ready document follows the same high-level structure:

```json
{
    "id": "...",
    "document": "...",
    "metadata": {}
}
```

## Maintainability

Each source has an independent builder and can be regenerated without rebuilding unrelated raw data.

---

# 11. Design Decisions

## Decision 1 — Preserve One Verse Per Record

Reason:

A verse is already a complete semantic unit.

---

## Decision 2 — Preserve Commentary Sections

Reason:

Fixed-size splitting could break a philosophical explanation across chunks.

---

## Decision 3 — Preserve Sanskrit as Metadata

Reason:

The current retrieval language is English, while Sanskrit remains useful for display and traceability.

---

## Decision 4 — Use UTF-8 Explicitly

Reason:

The data contains Sanskrit and non-ASCII characters that may fail under platform-default encodings.

---

# 12. Alternatives Considered

## Fixed-Length Chunking

Rejected because it could split verses or commentary sections at arbitrary boundaries.

## Sentence-Level Commentary Chunks

Rejected because individual sentences may lose the surrounding philosophical explanation.

## One Combined Dataset

Rejected because verses, commentary, and summaries require different metadata and retrieval behavior.

---

# 13. Outputs of the Data Engineering Phase

| Output | Record Count | Status |
|--------|--------------|--------|
| `merged_records.json` | 701 verse records | Completed |
| Commentary section data | 136 sections | Completed |
| Chapter summary data | 18 chapters | Completed |
| `verse_documents.json` | 701 documents | Completed |
| `commentary_documents.json` | 136 documents | Completed |
| `chapter_documents.json` | 18 documents | Completed |

---

# 14. Summary

The Data Engineering phase transformed raw Bhagavad Gita resources into clean, structured, and validated data optimized for semantic retrieval.

By preserving natural semantic boundaries and source metadata, the pipeline created reliable inputs for the knowledge base construction phase.

---

**Next Document:** `04_Knowledge_Base_Design.md`
