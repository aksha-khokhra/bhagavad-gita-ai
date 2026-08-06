from src.knowledge_base.config import SYSTEM_PROMPT_PATH


class PromptBuilder:
    def __init__(self):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as prompt_file:
            self.system_prompt = prompt_file.read()

    def build_prompt(self, user_query, retrieved_documents):
        verses = retrieved_documents.get("verses", [])
        commentaries = retrieved_documents.get("commentaries", [])
        chapters = retrieved_documents.get("chapters", [])

        sections = [self.system_prompt]

        if chapters:
            chapter_parts = [
                self._format_chapter(result) for result in chapters
            ]
            chapter_context = "\n\n----------------------------------------\n\n".join(
                chapter_parts
            )
            sections.append(
                "========================\n"
                "Chapter Summaries\n"
                "========================\n\n"
                f"{chapter_context}"
            )

        verse_parts = [self._format_verse(result) for result in verses]
        verse_context = "\n\n----------------------------------------\n\n".join(
            verse_parts
        ) if verse_parts else "No relevant verses were retrieved."

        commentary_parts = [
            self._format_commentary(result) for result in commentaries
        ]
        commentary_context = "\n\n----------------------------------------\n\n".join(
            commentary_parts
        ) if commentary_parts else "No relevant commentary was retrieved."

        sections.append(
            "========================\n"
            "Relevant Verses\n"
            "========================\n\n"
            f"{verse_context}"
        )
        sections.append(
            "========================\n"
            "Commentary (Explanation)\n"
            "========================\n\n"
            f"{commentary_context}"
        )
        sections.append(
            "========================\n"
            "Question\n"
            "========================\n\n"
            f"{user_query}"
        )
        sections.append(
            "========================\n"
            "Response\n"
            "========================\n"
        )

        return "\n\n".join(sections)

    def _format_verse(self, result):
        return f"""Verse {result["metadata"]["reference"]} ({result["metadata"]["chapter_title"]})

Translation:
{result["metadata"]["english_translation"]}"""

    def _format_commentary(self, result):
        return f"""Chapter {result["metadata"]["chapter_number"]}

Section:
{result["metadata"]["section_title"]}

Commentary:
{result["metadata"]["content"]}"""

    def _format_chapter(self, result):
        metadata = result["metadata"]
        return f"""Chapter {metadata["chapter_number"]}: {metadata["chapter_title"]}
Meaning: {metadata["chapter_title_meaning"]}

Summary:
{metadata["summary"]}"""
