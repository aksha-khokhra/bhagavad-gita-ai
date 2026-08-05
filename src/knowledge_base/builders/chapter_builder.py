from ..config import (
    CHAPTER_DATASET,
    VERSE_DATASET,
    CHAPTER_DOCUMENTS
)

from ..utils import load_json, save_json


def build_chapter_lookup(verses):
    lookup = {}

    for verse in verses:
        chapter_number = verse["chapter_number"]

        if chapter_number not in lookup:
            lookup[chapter_number] = {
                "chapter_title": verse["chapter_title"],
                "chapter_title_meaning": verse["chapter_title_meaning"]
            }

    return lookup

def create_chapter_document(summary, chapter_info):
    document = (
        f"Chapter: {summary['chapter_number']}\n"
        f"Title: {chapter_info['chapter_title']}\n"
        f"Meaning: {chapter_info['chapter_title_meaning']}\n\n"
        f"Summary:\n{summary['summary']}"
    )

    return {
        "id": f"chapter_{summary['chapter_number']}",
        "document": document,
        "metadata": {
            "source": "chapter",
            "reference": str(summary["chapter_number"]),
            "chapter_number": summary["chapter_number"],
            "chapter_title": chapter_info["chapter_title"],
            "chapter_title_meaning": chapter_info["chapter_title_meaning"],
            "summary": summary["summary"]
        }
    }


def build_chapter_documents():
    summaries = load_json(CHAPTER_DATASET)
    verses = load_json(VERSE_DATASET)

    chapter_lookup = build_chapter_lookup(verses)

    documents = []

    for summary in summaries:
        chapter_number = summary["chapter_number"]
        chapter_info = chapter_lookup[chapter_number]

        document = create_chapter_document(summary, chapter_info)
        documents.append(document)

    save_json(documents, CHAPTER_DOCUMENTS)

    print(f"Generated {len(documents)} chapter documents.")