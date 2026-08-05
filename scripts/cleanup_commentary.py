import json
import re

INPUT_FILE = "data/intermediate/commentary.json"
OUTPUT_FILE = "data/processed/commentary.json"


TEXT_FIXES = {
    "P a ndavas": "Pandavas",
}

EDITORIAL_NOTE = (
    "NOTE : Some non-essential verses from Chapters 1 and 2 only have been omitted "
    "for ease of understanding the teachings of the Gita by the first time readers."
)


def clean_commentary_text(text):
    """
    Cleans extracted commentary text.
    """
    if isinstance(text, list):
        text = " ".join(text)

    # ---------------------------------
    # Known text fixes
    # ---------------------------------
    for old, new in TEXT_FIXES.items():
        text = text.replace(old, new)

    # ---------------------------------
    # Remove editorial note
    # ---------------------------------
    text = text.replace(EDITORIAL_NOTE, "")

    # ---------------------------------
    # Remove PDF page headers
    # Examples:
    # Bhagavad-Gita 5
    # Bhagavad-Gita 23
    # ---------------------------------
    text = re.sub(
        r"Bhagavad-Gita\s+\d+",
        "",
        text,
        flags=re.IGNORECASE
    )

    # ---------------------------------
    # Remove URLs
    # ---------------------------------
    text = re.sub(
        r"https?://\S+",
        "",
        text
    )

    text = re.sub(
        r"www\.\S+",
        "",
        text
    )

    # ---------------------------------
    # Remove promotional section
    # Everything after these phrases
    # ---------------------------------
    STOP_PATTERNS = [
        "Glossary of Sanskrit words",
        "References used",
        "Premier Modi",
        "Star Reviews",
        "Chinese Gita",
    ]

    for pattern in STOP_PATTERNS:

        if pattern in text:
            text = text.split(pattern)[0]

    # ---------------------------------
    # Fix words broken across lines
    # righteous -> right- eous
    # ---------------------------------
    text = re.sub(
        r"-\s+",
        "",
        text
    )

    # ---------------------------------
    # Remove repeated whitespace
    # ---------------------------------
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        sections = json.load(f)

    cleaned_sections = []

    for section in sections:

        section["content"] = clean_commentary_text(
            section["content"]
        )

        # Skip empty sections
        if not section["content"]:
            continue

        # Skip sections that only contain page headers
        if re.fullmatch(
            r"Bhagavad-Gita\s+\d+",
            section["content"],
            flags=re.IGNORECASE
        ):
            continue

        # Skip promotional sections
        BAD_SECTION_TITLES = {
            "Over 14,702",
            "Twelfth print",
        }

        if section["section_title"] in BAD_SECTION_TITLES:
            continue

        cleaned_sections.append(section)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cleaned_sections,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Successfully cleaned {len(cleaned_sections)} sections."
    )


if __name__ == "__main__":
    main()