from .config import (
    VERSE_DOCUMENTS,
    COMMENTARY_DOCUMENTS,
    CHAPTER_DOCUMENTS
)

from .utils import load_json

def validate_ids(documents, dataset_name):
    ids = [doc["id"] for doc in documents]

    if len(ids) != len(set(ids)):
        raise ValueError(f"Duplicate document IDs found in {dataset_name}.")

    print(f"✓ {dataset_name}: Document IDs are unique.")

def validate_document_text(documents, dataset_name):
    for doc in documents:
        if not doc["document"].strip():
            raise ValueError(
                f"Empty document found in {dataset_name}: {doc['id']}"
            )

    print(f"✓ {dataset_name}: All documents contain text.")

def validate_metadata(documents, dataset_name):
    for doc in documents:
        metadata = doc.get("metadata")

        if not metadata:
            raise ValueError(
                f"Missing metadata in {dataset_name}: {doc['id']}"
            )

    print(f"✓ {dataset_name}: All documents contain metadata.")

def validate_documents(documents, dataset_name):
    print(f"\nValidating {dataset_name}...")

    validate_ids(documents, dataset_name)
    validate_document_text(documents, dataset_name)
    validate_metadata(documents, dataset_name)

    print(f"✓ {dataset_name} validation completed.")

def main():
    verse_documents = load_json(VERSE_DOCUMENTS)
    commentary_documents = load_json(COMMENTARY_DOCUMENTS)
    chapter_documents = load_json(CHAPTER_DOCUMENTS)

    validate_documents(verse_documents, "Verse Documents")
    validate_documents(commentary_documents, "Commentary Documents")
    validate_documents(chapter_documents, "Chapter Documents")

    print("\nAll document collections passed validation!")


if __name__ == "__main__":
    main()