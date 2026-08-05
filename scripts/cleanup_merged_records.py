import json
import re

INPUT_FILE = "data/intermediate/merged_records.json"
OUTPUT_FILE = "data/processed/merged_records.json"

REQUIRED_FIELDS = [
    "id",
    "chapter_number",
    "verse_number",
    "sanskrit_text",
    "english_translation",
    "chapter_title",
    "chapter_title_meaning",
]


# --------------------------------------------------
# Text Cleaning
# --------------------------------------------------

def clean_text(text):
    if text is None:
        return ""

    if not isinstance(text, str):
        return text

    # Remove invisible unicode characters
    text = (
        text.replace("\u200b", "")
            .replace("\u200c", "")
            .replace("\u200d", "")
            .replace("\ufeff", "")
    )

    # Fix hyphenated words
    text = re.sub(r"(\w+)-\s+(\w+)", r"\1\2", text)

    # Replace newlines/tabs with spaces
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------------------------------
# Clean One Record
# --------------------------------------------------

def clean_record(record):

    cleaned = {}

    for key, value in record.items():

        # Remove chapter summary
        if key == "chapter_summary":
            continue

        if isinstance(value, str):
            cleaned[key] = clean_text(value)

        elif value is None:
            cleaned[key] = ""

        else:
            cleaned[key] = value

    return cleaned


# --------------------------------------------------
# Validation
# --------------------------------------------------

def validate(records):

    seen_ids = set()

    for record in records:

        for field in REQUIRED_FIELDS:
            if field not in record:
                print(f"Missing '{field}' in record {record.get('id')}")

        record_id = record.get("id")

        if record_id in seen_ids:
            print(f"Duplicate ID found: {record_id}")

        seen_ids.add(record_id)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = json.load(f)

    cleaned_records = [
        clean_record(record)
        for record in records
    ]

    validate(cleaned_records)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            cleaned_records,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved {len(cleaned_records)} cleaned records.")


if __name__ == "__main__":
    main()