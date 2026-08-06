# Project Tattva Documentation

**Document:** 02 — System Architecture  
**Version:** 1.2  
**Status:** Completed

---

# 1. Purpose

This document describes the implemented architecture of Project Tattva v1.2, including its major components, responsibilities, interactions, and design decisions.

The system follows a modular Retrieval-Augmented Generation architecture. Retrieval is performed before generation, and each major responsibility is isolated behind a dedicated class.

---

# 2. Architectural Goals

The architecture was designed to support:

- Separation of concerns
- Independent knowledge sources
- Reusable components
- Persistent local storage
- Explainable retrieval
- Local LLM execution
- Easy testing
- Future extension without major redesign

---

# 3. Implemented High-Level Architecture

```text
                         User Question
                               │
                               ▼
                           Chatbot
                               │
                               ▼
                           Retriever
                               │
                   ┌───────────┴───────────┐
                   ▼                       ▼
             Query Embedder          Vector Stores
                                           │
                              ┌────────────┴────────────┐
                              ▼                         ▼
                       Verse Collection       Commentary Collection
                              └────────────┬────────────┘
                                           ▼
                              Structured Retrieval Result
                                           │
                                           ▼
                                    Prompt Builder
                                           │
                                           ▼
                                      LLM Client
                                           │
                                           ▼
                                      Ollama Model
                                           │
                                           ▼
                                      Final Response
```

The Chapter Summary Knowledge Base is indexed and connected through chapter-level query routing.

---

# 4. System Components

## 4.1 Chatbot

The `Chatbot` class is the application orchestrator.

Responsibilities:

- Accept the user query.
- Request relevant knowledge from the Retriever.
- Send the retrieved result to the Prompt Builder.
- Send the completed prompt to the LLM Client.
- Return the generated response.

The Chatbot intentionally does not perform embedding, vector search, prompt formatting, or model communication itself.

---

## 4.2 Retriever

The `Retriever` class owns the active retrieval workflow.

Responsibilities:

- Initialize the Embedder.
- Connect to the verse, commentary, and chapter collections.
- Classify chapter-level intent.
- Embed the user query once.
- Search the relevant collections using the same query embedding.
- Return verses, commentaries, and chapters as separate result groups.

Current return structure:

```python
{
    "verses": [...],
    "commentaries": [...],
    "chapters": [...],
    "route": {"mode": "general", "chapter_number": None}
}
```

Default retrieval counts are three verses and five commentary sections. Chapter results are included when the query is routed as a chapter overview or chapter reference.

---

## 4.3 Embedder

The `Embedder` class wraps the Sentence Transformers model.

Responsibilities:

- Load `all-MiniLM-L6-v2` once.
- Generate one embedding for a single text.
- Generate embeddings for a batch of texts.

Public methods:

```python
embed(text)
embed_batch(texts)
```

The same embedding model is used during indexing and retrieval. This is required because stored documents and incoming queries must exist in the same vector space.

---

## 4.4 VectorStore

The `VectorStore` class wraps ChromaDB collection access.

Responsibilities:

- Connect to the persistent ChromaDB directory.
- Open or create one named collection.
- Add document IDs, embeddings, text, and metadata.
- Query the collection using a query embedding.
- Convert the raw ChromaDB response into a cleaner application-level structure.

One `VectorStore` instance represents one collection.

Current active collections:

- `verses`
- `commentaries`

---

## 4.5 PromptBuilder

The `PromptBuilder` class converts structured retrieval results into one final prompt.

Responsibilities:

- Load the system prompt once during initialization.
- Format verses as primary source material.
- Format commentary as explanatory material.
- Keep verse and commentary sections separate.
- Insert the user question.
- Return one complete prompt string.

The Prompt Builder does not perform retrieval and does not communicate with Ollama.

---

## 4.6 LLMClient

The `LLMClient` class isolates communication with Ollama.

Responsibilities:

- Read the configured Ollama model name.
- Send the prompt through `ollama.chat()`.
- Return only the generated message content.

The rest of the application does not depend on Ollama's raw response structure.

---

## 4.7 Command-Line Interface

The CLI is implemented in `scripts/chat.py`.

Responsibilities:

- Initialize one Chatbot instance.
- Accept repeated user questions.
- Print the generated response.
- Exit when the user enters `exit` or `quit`.

The CLI is intentionally lightweight and contains no retrieval or generation logic.

---

# 5. Offline Indexing Workflow

The vector collections are built before the chatbot is used.

```text
Processed JSON Documents
          │
          ▼
Extract IDs, Text, and Metadata
          │
          ▼
Batch Embedding Generation
          │
          ▼
VectorStore.add() / upsert()
          │
          ▼
Persistent ChromaDB Collections
```

The indexing workflow currently creates:

- 701 verse records
- 136 commentary records
- 18 chapter summary records

All three collections are indexed into persistent ChromaDB storage.

---

# 6. Online Query Workflow

## Step 1

The CLI receives a user question.

## Step 2

The Chatbot sends the question to the Retriever.

## Step 3

The Retriever classifies chapter-level intent and generates one query embedding.

## Step 4

The verse, commentary, and chapter collections are searched according to the route. Explicit chapter references also filter verse and commentary results to that chapter.

## Step 5

The Retriever returns separate verse, commentary, and chapter lists, plus the routing decision.

## Step 6

The Prompt Builder formats each source type and inserts the question.

## Step 7

The LLM Client sends the prompt to Ollama.

## Step 8

The generated response is returned to the CLI.

---

# 7. Component Interaction

```text
scripts/chat.py
      │
      ▼
Chatbot.chat(user_query)
      │
      ▼
Retriever.retrieve(user_query)
      │
      ├── classify_query(user_query)
      ├── Embedder.embed(user_query)
      ├── Verse VectorStore.query(...)
      ├── Commentary VectorStore.query(...)
      └── Chapter VectorStore.query(...) when routed
      │
      ▼
PromptBuilder.build_prompt(...)
      │
      ▼
LLMClient.generate_response(prompt)
      │
      ▼
Generated text
```

Each component exposes a small public interface and hides the implementation details of its dependency.

---

# 8. Design Principles

## Separation of Concerns

Each class has one primary responsibility.

## Encapsulation

Raw ChromaDB and Ollama response structures are converted before being returned to the rest of the application.

## Dependency Reuse

The embedding model and system prompt are loaded once per application instance.

## Semantic Source Separation

Verses and commentary are stored and formatted independently because they serve different roles.

## Incremental Evolution

The system began with verse-only retrieval. Commentary support was added through a Retriever abstraction without rewriting the Chatbot, VectorStore, or LLM Client.

---

# 9. Major Architectural Decisions

## Decision 1 — Use RAG Instead of LLM-Only Generation

Reason:

The model must answer from curated Bhagavad Gita material rather than unrestricted internal knowledge.

---

## Decision 2 — Use Separate Collections

Reason:

Verses are primary sources, while commentary provides interpretation and chapter summaries provide thematic grounding. Keeping them separate supports independent retrieval counts, formatting, evaluation, and future ranking strategies.

---

## Decision 3 — Introduce a Retriever Abstraction

Reason:

The Chatbot should not know which collections exist or how query embeddings are generated.

---

## Decision 4 — Use a Persistent Vector Database

Reason:

Embeddings should survive application restarts and should not be regenerated for every session.

---

## Decision 5 — Use a Local LLM

Reason:

Ollama allows the MVP to run locally without mandatory paid API access.

---

# 10. Alternatives Considered

## Single Vector Collection

Rejected because mixed document types make source-aware retrieval and prompt formatting more difficult.

## Keyword-Only Search

Rejected because user wording may differ from scripture wording, as demonstrated by the difference between “expecting results” and “fruit of action.”

## LLM-Only Responses

Rejected because responses would be harder to ground, evaluate, and trace.

## Loading the Embedding Model Per Query

Rejected because repeatedly loading the same model would be inefficient.

---

# 11. Current Limitations

- Chapter routing is rule-based rather than model-based.
- Retrieval counts are mostly fixed.
- Results are not reranked after vector search.
- Commentary sections may be long.
- Commentary metadata does not yet contain normalized verse ranges.
- The interface is CLI-only.
- There is no conversation memory.

---

# 12. Summary

Project Tattva v1.2 uses a modular RAG architecture built around six primary components: Embedder, VectorStore, Retriever, PromptBuilder, LLMClient, and Chatbot.

The architecture separates retrieval from generation and preserves the distinction between Bhagavad Gita verses, explanatory commentary, and chapter summaries. This design supports the current release while providing a stable foundation for reranking, API, and interface improvements.

---

**Next Document:** `03_Data_Engineering.md`
