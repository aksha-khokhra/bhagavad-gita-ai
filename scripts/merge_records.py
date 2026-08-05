import json

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

chapters = load_json("data/raw/chapters.json")
verses = load_json("data/raw/verse.json")
translations = load_json("data/raw/translation.json")

filtered_translations = {}

for translation in translations:
    if translation["author_id"] == 21:
        filtered_translations[translation["verse_id"]] = translation["description"]


chapter_lookup = {}

for chapter in chapters:
    chapter_lookup[chapter["chapter_number"]] = chapter

merged_records = []

for verse in verses:
    translation = filtered_translations[verse["id"]]
    chapter = chapter_lookup[verse["chapter_number"]]

    merged_record = {
        "id": verse["id"],
        "chapter_number": verse["chapter_number"],
        "verse_number": verse["verse_number"],
        "sanskrit_text": verse["text"],
        "english_translation": translation,
        "chapter_title": chapter["name_translation"],
        "chapter_title_meaning": chapter["name_meaning"],
        "chapter_summary": chapter["chapter_summary"],
    }

    merged_records.append(merged_record)

with open("data/intermediate/merged_records.json", "w", encoding="utf-8") as file:
    json.dump(merged_records, file, indent=4, ensure_ascii=False)