from ..config import (
    COMMENTARY_DATASET,
    COMMENTARY_DOCUMENTS
)

from ..utils import load_json, save_json

def create_commentary_document(
    record: dict,
    section_number: int
) -> dict:

    document = (
        f"Chapter: {record['chapter_number']}\n"
        f"Section: {record['section_title']}\n"
        f"Commentary: {record['content']}"
    )

    metadata = {
        "source": "commentary",
        "chapter_number": record["chapter_number"],
        "section_number": section_number,
        "section_title": record["section_title"],
        "content": record["content"]
    }

    return {
        "id": f"commentary_{record['chapter_number']}_{section_number}",
        "document": document,
        "metadata": metadata
    }

def build_commentary_documents():

    commentary = load_json(COMMENTARY_DATASET)

    documents = []

    chapter_counter = {}

    for record in commentary:

        chapter = record["chapter_number"]

        chapter_counter.setdefault(chapter, 0)
        chapter_counter[chapter] += 1

        documents.append(
            create_commentary_document(
                record,
                chapter_counter[chapter]
            )
        )

    save_json(documents, COMMENTARY_DOCUMENTS)

    print(f"Generated {len(documents)} commentary documents.")