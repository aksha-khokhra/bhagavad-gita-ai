# Project Tattva Documentation

**Document:** 01 — Project Overview  
**Version:** 1.1  
**Status:** MVP Completed

---

# 1. Introduction

Project Tattva is an end-to-end Retrieval-Augmented Generation (RAG) system designed to answer questions about the Bhagavad Gita using grounded, explainable, and context-aware responses.

The Bhagavad Gita contains 18 chapters and 701 verses. The verses provide the primary teachings, while commentary explains philosophical meaning in more direct and modern language. Project Tattva combines these sources so that the generated response is based on retrieved evidence rather than on the language model's internal knowledge alone.

The current MVP accepts an English-language question, generates a query embedding, retrieves relevant verses and commentary from independent ChromaDB collections, constructs a grounded prompt, and sends that prompt to a locally hosted Ollama model.

---

# 2. Project Motivation

The project was created to explore the practical implementation of Retrieval-Augmented Generation in a domain where accuracy, source traceability, and interpretation are important.

General-purpose Large Language Models can produce fluent answers about the Bhagavad Gita, but they may:

- Hallucinate verse references.
- Mix interpretations from unrelated sources.
- Answer without showing the supporting text.
- Use outside knowledge that cannot be verified.
- Miss the distinction between scripture and commentary.

Project Tattva addresses these limitations by retrieving curated source material before generation. The project also demonstrates the complete engineering workflow behind a modular RAG application, including data processing, embedding generation, vector storage, multi-source retrieval, prompt construction, local LLM integration, and evaluation.

---

# 3. Problem Statement

Large Language Models are generative systems, not authoritative retrieval systems. When they are asked domain-specific questions, they may produce plausible but unsupported answers.

For the Bhagavad Gita, this creates several challenges:

- A response may not be grounded in the source text.
- Relevant verses may be missed because user wording differs from the translation.
- Philosophical questions may require explanation beyond a literal verse translation.
- Users may be unable to verify the origin of an answer.

Project Tattva solves this problem by combining semantic retrieval with a Large Language Model. Relevant verses and commentary are retrieved first, then injected into a controlled prompt used for response generation.

---

# 4. Project Objectives

The primary objectives of Project Tattva are to:

- Design and implement an end-to-end RAG system.
- Build structured, embedding-ready documents from Bhagavad Gita data.
- Store different knowledge types in independent vector collections.
- Retrieve relevant verses and commentary using semantic search.
- Generate grounded responses using only retrieved context.
- Preserve the distinction between primary verses and explanatory commentary.
- Provide verse references where supported by the retrieved context.
- Evaluate retrieval separately from generation.
- Maintain a modular architecture that can be extended without major redesign.

---

# 5. Current Scope

The current release focuses on English-language question answering through a command-line interface.

The active retrieval pipeline uses:

- Verse Knowledge Base
- Commentary Knowledge Base

The Chapter Summary documents have been constructed but are not yet integrated into the active retriever.

The current assistant supports questions related to:

- Karma Yoga
- Meditation
- Devotion
- Action and inaction
- Duties and selfless work
- The Self
- Philosophical concepts represented in the available knowledge base

The following features remain outside the current MVP:

- FastAPI backend
- Web interface
- Conversation memory
- Chapter-summary routing
- Hybrid search
- Reranking
- Multilingual support
- Production deployment

---

# 6. Functional Requirements

The current system shall be capable of:

- Accepting a natural-language question through the CLI.
- Generating an embedding for the question.
- Searching the verse vector collection.
- Searching the commentary vector collection.
- Returning separate verse and commentary result groups.
- Formatting each knowledge type independently.
- Constructing a grounded prompt.
- Sending the prompt to a local Ollama model.
- Returning the generated response to the user.
- Exiting the CLI when the user enters `exit` or `quit`.

---

# 7. Non-Functional Requirements

## Accuracy

Responses should be based on retrieved Bhagavad Gita context rather than unrestricted model knowledge.

## Explainability

Retrieved verse references and commentary sections should make the response easier to trace and inspect.

## Maintainability

Embedding, vector storage, retrieval, prompt construction, LLM communication, and orchestration should remain separate components.

## Extensibility

Additional collections, models, rerankers, APIs, and interfaces should be addable without rewriting the complete system.

## Local Execution

The system should run locally using Ollama, avoiding mandatory paid API dependencies for the MVP.

---

# 8. High-Level Features

Project Tattva v1.1 includes:

- Structured Bhagavad Gita data processing
- Embedding-ready document construction
- Batch embedding generation
- Persistent ChromaDB storage
- Separate verse and commentary collections
- Multi-source semantic retrieval
- Source-aware prompt formatting
- Local LLM response generation with Ollama
- CLI-based interaction
- Retrieval evaluation scripts
- Modular object-oriented architecture

---

# 9. Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python 3.12 |
| Embedding Library | Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| Local LLM Runtime | Ollama |
| Initial LLM | `phi3:mini` |
| Data Format | JSON / Markdown |
| Version Control | Git and GitHub |
| Current Interface | Command-line interface |

---

# 10. Current Repository Structure

```text
bhagavad-gita-ai/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── chroma_db/
│
├── docs/
│   ├── 01_Project_Overview.md
│   ├── 02_System_Architecture.md
│   ├── 03_Data_Engineering.md
│   ├── 04_Knowledge_Base_Design.md
│   ├── 05_Knowledge_Base_Construction.md
│   ├── 06_Retrieval_Pipeline.md
│   ├── 07_Prompt_Engineering.md
│   ├── 08_Application_Integration.md
│   ├── 09_Evaluation.md
│   ├── 10_Future_Development.md
│   └── ADR.md
│
├── scripts/
│   ├── build_vector_database.py
│   ├── chat.py
│   ├── evaluate_retriever.py
│   ├── test_embedder.py
│   ├── test_vector_store.py
│   ├── test_retrieval.py
│   └── test_prompt_builder.py
│
├── src/
│   ├── chatbot/
│   │   ├── chatbot.py
│   │   ├── llm.py
│   │   └── prompt_builder.py
│   │
│   ├── knowledge_base/
│   │   ├── builders/
│   │   ├── config.py
│   │   └── vector_store.py
│   │
│   ├── prompts/
│   │   └── system_prompt.md
│   │
│   └── retriever/
│       └── retriever.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 11. Project Roadmap

## Phase 1 — Data Collection

- [x] Collect verse data
- [x] Collect commentary source
- [x] Collect chapter-level content

---

## Phase 2 — Data Engineering

- [x] Merge verse records
- [x] Parse commentary sections
- [x] Clean and validate processed data
- [x] Prepare chapter summaries

---

## Phase 3 — Knowledge Base Design

- [x] Design Verse Knowledge Base
- [x] Design Commentary Knowledge Base
- [x] Design Chapter Summary Knowledge Base

---

## Phase 4 — Knowledge Base Construction

- [x] Build verse documents
- [x] Build commentary documents
- [x] Build chapter summary documents
- [x] Generate verse embeddings
- [x] Generate commentary embeddings
- [x] Persist verse and commentary collections in ChromaDB
- [ ] Index chapter summary collection

---

## Phase 5 — Retrieval Pipeline

- [x] Generate query embeddings
- [x] Retrieve relevant verses
- [x] Retrieve relevant commentary
- [x] Return structured multi-source results
- [ ] Add chapter-summary routing
- [ ] Add reranking

---

## Phase 6 — Prompt Engineering

- [x] Store system instructions separately
- [x] Format verses and commentary independently
- [x] Construct grounded prompts
- [x] Add out-of-scope response instructions

---

## Phase 7 — Application Integration

- [x] Integrate local Ollama model
- [x] Build Chatbot orchestrator
- [x] Build interactive CLI
- [ ] Build FastAPI backend
- [ ] Build frontend interface

---

## Phase 8 — Evaluation

- [x] Create manual retrieval evaluation script
- [x] Compare verse-only and commentary-assisted retrieval
- [x] Identify vocabulary mismatch in verse retrieval
- [ ] Create labeled evaluation dataset
- [ ] Add quantitative retrieval metrics
- [ ] Add response-quality evaluation

---

## Phase 9 — Release

- [x] Complete MVP architecture
- [x] Add commentary-supported retrieval
- [ ] Final code cleanup
- [ ] Complete README
- [ ] Push interview-ready release to GitHub

---

# 12. Related Documentation

| Document | Description |
|----------|-------------|
| 02_System_Architecture.md | Current component architecture and data flow |
| 03_Data_Engineering.md | Dataset preprocessing and transformation |
| 04_Knowledge_Base_Design.md | Design of the three knowledge sources |
| 05_Knowledge_Base_Construction.md | Document builders, embeddings, and ChromaDB indexing |
| 06_Retrieval_Pipeline.md | Multi-source query retrieval workflow |
| 07_Prompt_Engineering.md | Prompt structure, grounding rules, and formatting |
| 08_Application_Integration.md | Ollama, Chatbot, and CLI integration |
| 09_Evaluation.md | Retrieval experiments, findings, and limitations |
| 10_Future_Development.md | Planned improvements beyond the MVP |
| ADR.md | Architecture Decision Records |

---

# 13. Conclusion

Project Tattva v1.1 is a functional, modular RAG application that retrieves Bhagavad Gita verses and commentary before generating a local LLM response.

The project demonstrates the complete workflow behind a practical RAG system while preserving clear separation between data engineering, retrieval, prompt construction, and generation. The current release is suitable as an interview and portfolio project, while the architecture provides a strong foundation for future improvements.

---

**Next Document:** `02_System_Architecture.md`
