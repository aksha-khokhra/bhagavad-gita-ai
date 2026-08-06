from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data Directories
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"
EVAL_DIR = DATA_DIR / "evaluation"

# Input Files
VERSE_DATASET = PROCESSED_DIR / "merged_records.json"
COMMENTARY_DATASET = PROCESSED_DIR / "commentary.json"
CHAPTER_DATASET = PROCESSED_DIR / "chapter_summaries.json"

# Output Files
VERSE_DOCUMENTS = PROCESSED_DIR / "verse_documents.json"
COMMENTARY_DOCUMENTS = PROCESSED_DIR / "commentary_documents.json"
CHAPTER_DOCUMENTS = PROCESSED_DIR / "chapter_documents.json"
RETRIEVAL_EVAL_DATASET = EVAL_DIR / "retrieval_eval.json"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

SYSTEM_PROMPT_PATH = PROJECT_ROOT / "src" / "prompts" / "system_prompt.md"

OLLAMA_MODEL = "phi3:mini"

VERSE_COLLECTION = "verses"
COMMENTARY_COLLECTION = "commentaries"
CHAPTER_COLLECTION = "chapters"