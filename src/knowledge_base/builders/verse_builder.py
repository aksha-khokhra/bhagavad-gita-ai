from ..config import (
    VERSE_DATASET,
    VERSE_DOCUMENTS
)

from ..utils import load_json, save_json

def create_verse_document(record: dict) -> dict:
    """
    Convert a verse record into an embedding-ready document.
    """

    document = (
        f"Chapter: {record['chapter_title']}\n"
        f"Meaning: {record['chapter_title_meaning']}\n"
        f"Translation: {record['english_translation']}"
    )

    metadata = {
        "record_id": record["id"],
        "source": "verse",
        "reference": f"{record['chapter_number']}.{record['verse_number']}",
        "chapter_number": record["chapter_number"],
        "verse_number": record["verse_number"],
        "chapter_title": record["chapter_title"],
        "chapter_title_meaning": record["chapter_title_meaning"],
        "english_translation": record["english_translation"],
        "sanskrit_text": record["sanskrit_text"]
    }

    return {
        "id": f"verse_{record['chapter_number']}_{record['verse_number']}",
        "document": document,
        "metadata": metadata
    }

def build_verse_documents():

    verses = load_json(VERSE_DATASET)

    documents = [
        create_verse_document(record)
        for record in verses
    ]

    save_json(documents, VERSE_DOCUMENTS)

    print(f"Generated {len(documents)} verse documents.")

    