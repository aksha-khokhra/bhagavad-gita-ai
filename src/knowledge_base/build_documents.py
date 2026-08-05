from .builders.verse_builder import build_verse_documents
from .builders.commentary_builder import build_commentary_documents
from .builders.chapter_builder import build_chapter_documents


def build_all_documents():

    print("=" * 50)
    print("Building Knowledge Base Documents")
    print("=" * 50)

    build_verse_documents()
    build_commentary_documents()
    build_chapter_documents()

    print("\nAll document collections generated successfully!")


if __name__ == "__main__":
    build_all_documents()