# Project Tattva

An end-to-end Retrieval-Augmented Generation (RAG) system for the Bhagavad Gita.

Project Tattva answers English questions by retrieving relevant verses and commentary from ChromaDB, building a grounded prompt, and generating a response with a local Ollama model.

---

## What it does

1. Embeds the user question with `all-MiniLM-L6-v2`
2. Searches separate **verse** and **commentary** collections
3. Formats retrieved evidence into a grounded prompt
4. Generates an answer with Ollama (`phi3:mini` by default)

Chapter-summary documents are prepared but not yet connected to the active retriever.

---

## Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.12+ |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
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
├── scripts/                 # Build, chat, eval, and smoke scripts
└── src/
    ├── chatbot/             # Orchestrator, prompt builder, LLM client
    ├── knowledge_base/      # Document builders, embedder, vector store
    ├── prompts/             # System prompt
    └── retriever/           # Multi-collection retrieval
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

### 3. Install and start Ollama

Install from [https://ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull phi3:mini
```

### 4. Build the vector database (first time)

Processed documents are already in `data/processed/`. Index them into ChromaDB:

```bash
python scripts/build_vector_database.py
```

This creates `data/chroma_db/` with `verses` and `commentaries` collections.

---

## Usage

### Chat

```bash
python scripts/chat.py
```

Type a question, or `exit` / `quit` to leave.

Example:

```text
You: What is Karma Yoga?

Project Tattva: ...
```

### Evaluate retrieval

Runs the labeled set in `data/evaluation/retrieval_eval.json` and reports Recall@3 and MRR:

```bash
python scripts/evaluate_retriever.py
```

Verse-only Recall@3 is intentionally modest on paraphrase-heavy questions (for example, “expecting results” vs “fruit of action”). Commentary retrieval often recovers the right theme — that gap is documented in `docs/09_Evaluation.md`.

---

## Current scope (MVP)

**Included**

- Verse + commentary document construction
- Persistent ChromaDB indexing
- Multi-source semantic retrieval
- Grounded prompt construction
- Local Ollama generation
- CLI chat
- Labeled retrieval evaluation (Recall@K / MRR)

**Not included yet**

- Chapter-summary retrieval / routing
- FastAPI backend or web UI
- Conversation memory
- Hybrid search / reranking
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
| [06_Retrieval_Pipeline.md](docs/06_Retrieval_Pipeline.md) | Multi-source retrieval |
| [07_Prompt_Engineering.md](docs/07_Prompt_Engineering.md) | Grounding rules and formatting |
| [08_Application_Integration.md](docs/08_Application_Integration.md) | Chatbot + Ollama CLI |
| [09_Evaluation.md](docs/09_Evaluation.md) | Retrieval findings and limits |
| [10_Future_Development.md](docs/10_Future_Development.md) | Planned improvements |
| [ADR.md](docs/ADR.md) | Architecture Decision Records |

---

## Design notes

- Verses and commentary stay in **separate collections** so prompts can treat scripture and explanation differently.
- Documents keep natural units (one verse / one commentary section) instead of fixed-size chunks.
- Retrieval is evaluated independently of generation so failures can be isolated.

---

## License

Educational, research, and portfolio use.
