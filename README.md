# Project Tattva

An end-to-end Retrieval-Augmented Generation (RAG) system for the Bhagavad Gita.

Project Tattva answers English questions by retrieving relevant verses, commentary, and chapter summaries from ChromaDB, building a grounded prompt, and generating a response with a local Ollama model.

---

## Demo

```text
$ python scripts/chat.py

You: What does Krishna say about attachment to results?

Project Tattva: According to the retrieved verses and commentary,
one should perform duty without attachment to the fruit of action
(see Verse 2.47 and related commentary on selfless work)...

You: Who built the Taj Mahal?

Project Tattva: I don't have enough information in the Bhagavad Gita
knowledge base to answer that.

You: exit
Goodbye!
```

---

## Architecture

```text
User Query
     │
     ▼
Query Analysis / Routing
     │
     ├──── Exact Reference Retrieval
     │
     ├──── Dense Vector Retrieval
     │
     └──── BM25 Lexical Retrieval
                    │
                    ▼
           Reciprocal Rank Fusion
                    │
                    ▼
          Cross-Encoder Reranking
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
       Verses   Commentary   Chapter
         └──────────┼──────────┘
                    ▼
         Relevance Check (rerank score)
              │           │
           in-scope    out-of-scope
              │           │
              ▼           ▼
        Prompt Builder  Deterministic fallback
              │
              ▼
           Ollama
              │
              ▼
       Grounded Answer
```

---

## What it does

1. Embeds the user question with `all-MiniLM-L6-v2`
2. Routes chapter-level questions to the chapter collection when needed
3. Retrieves verses with hybrid search (exact reference + vector + BM25, fused with RRF)
4. Reranks verse and commentary candidates with a cross-encoder
5. Rejects out-of-scope questions when the best rerank score is too weak
6. Formats retrieved evidence into a grounded prompt
7. Generates an answer with Ollama (`phi3:mini` by default)

---

## Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.12+ |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Reranker | Cross-encoder (`ms-marco-MiniLM-L-6-v2`) |
| Vector DB | ChromaDB (persistent) |
| LLM | Ollama (`phi3:mini`) |
| Interface | CLI |

---

## Project structure

```text
bhagavad-gita-ai/
├── data/
│   ├── raw/                 # Source verse, translation, chapter data
│   ├── processed/           # Merged records and embedding-ready documents
│   ├── evaluation/          # Labeled retrieval eval set
│   └── chroma_db/           # Persistent vector store (local, gitignored)
├── docs/                    # Engineering documentation and ADRs
├── scripts/
│   ├── smoke/               # Manual smoke checks
│   ├── build_vector_database.py
│   ├── chat.py
│   └── evaluate_retriever.py
└── src/
    ├── chatbot/             # Orchestrator, prompt builder, LLM client
    ├── knowledge_base/      # Document builders, embedder, vector store
    ├── prompts/             # System prompt
    └── retriever/           # Hybrid retrieval, reranking, routing
```

---

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

`sentence-transformers` provides both the embedding model and the cross-encoder. On first run, Hugging Face will download:

- `sentence-transformers/all-MiniLM-L6-v2`
- `cross-encoder/ms-marco-MiniLM-L-6-v2`

### 3. Install and start Ollama

Install from [https://ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull phi3:mini
```

### 4. Build the vector database (first time)

Processed documents are already in `data/processed/`. Index them into ChromaDB from the repository root:

```bash
python scripts/build_vector_database.py
```

This creates `data/chroma_db/` with `verses`, `commentaries`, and `chapters` collections. Re-running the script upserts documents safely.

---

## Usage

Run all commands from the repository root.

### Chat

```bash
python scripts/chat.py
```

Type a question, or `exit` / `quit` to leave.

### Evaluate retrieval

```bash
python scripts/evaluate_retriever.py
```

### Smoke checks

```bash
python scripts/smoke/smoke_vector_store.py
python scripts/smoke/smoke_embedder.py
python scripts/smoke/smoke_retrieval.py
```

---

## Evaluation

The retrieval pipeline is evaluated with a manually labeled set containing exact-reference, semantic, conceptual, chapter-level, and out-of-scope queries.

| Metric | Result |
|--------|-------:|
| Verse-reference Recall@3 (semantic/conceptual) | 0.307 |
| Verse-reference MRR@3 (semantic/conceptual) | 0.487 |
| Exact Reference Accuracy | 10/10 (1.000) |
| Chapter Query Accuracy | 6/6 (1.000) |
| Out-of-Scope Rejection Accuracy | 7/7 (1.000) |

Verse-reference Recall@3 remains challenging for highly paraphrased queries, which is why the system also uses commentary retrieval, lexical search, reranking, and out-of-scope rejection. Details are in `docs/09_Evaluation.md`.

---

## Current scope (v1)

**Included**

- Verse + commentary + chapter document construction
- Persistent ChromaDB indexing for all three collections
- Hybrid verse retrieval (exact reference + BM25 + vector RRF)
- Cross-encoder reranking for verses and commentary
- Chapter-level query routing
- Out-of-scope rejection based on rerank score
- Grounded prompt construction
- Local Ollama generation
- CLI chat
- Typed labeled retrieval evaluation

**Not included**

- FastAPI backend or web UI
- Conversation memory
- Multilingual support

See `docs/10_Future_Development.md` for the roadmap.

---

## Documentation

| Document | Description |
|----------|-------------|
| [01_Project_Overview.md](docs/01_Project_Overview.md) | Motivation, objectives, scope |
| [02_System_Architecture.md](docs/02_System_Architecture.md) | Components and data flow |
| [03_Data_Engineering.md](docs/03_Data_Engineering.md) | Parsing and preprocessing |
| [04_Knowledge_Base_Design.md](docs/04_Knowledge_Base_Design.md) | Verse / commentary / chapter design |
| [05_Knowledge_Base_Construction.md](docs/05_Knowledge_Base_Construction.md) | Builders, embeddings, indexing |
| [06_Retrieval_Pipeline.md](docs/06_Retrieval_Pipeline.md) | Hybrid retrieval, reranking, routing |
| [07_Prompt_Engineering.md](docs/07_Prompt_Engineering.md) | Grounding rules and formatting |
| [08_Application_Integration.md](docs/08_Application_Integration.md) | Chatbot + Ollama CLI |
| [09_Evaluation.md](docs/09_Evaluation.md) | Retrieval findings and limits |
| [10_Future_Development.md](docs/10_Future_Development.md) | Planned improvements |
| [ADR.md](docs/ADR.md) | Architecture Decision Records |

---

## Design notes

- Verses, commentary, and chapter summaries stay in **separate collections** so prompts can treat each source differently.
- Documents keep natural units (one verse / one commentary section / one chapter summary) instead of fixed-size chunks.
- Chapter-level questions are routed before retrieval.
- Verse search combines exact reference lookup, dense vectors, and BM25 before Reciprocal Rank Fusion.
- A cross-encoder reranks candidates; weak top scores trigger a deterministic out-of-scope fallback.
- Retrieval is evaluated independently of generation so failures can be isolated.

---

## License

Educational, research, and portfolio use.
