from src.knowledge_base.config import SYSTEM_PROMPT_PATH


class PromptBuilder:
    def __init__(self):
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as prompt_file:
            self.system_prompt = prompt_file.read()

    def build_prompt(self, user_query, retrieved_documents):

        verses = retrieved_documents["verses"]
        commentaries = retrieved_documents["commentaries"]

        verse_parts = []
        commentary_parts = []
        
        for result in verses:
            verse_parts.append(self._format_verse(result))

        for result in commentaries:
            commentary_parts.append(self._format_commentary(result))

        verse_context = "\n\n----------------------------------------\n\n".join(verse_parts)
        commentary_context = "\n\n----------------------------------------\n\n".join(commentary_parts)

        prompt = f"""{self.system_prompt}
========================
Relevant Verses
========================

{verse_context}

========================
Commentary (Explanation)
========================

{commentary_context}

========================
Question
========================

{user_query}

========================
Response
========================
"""    

        return prompt

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
