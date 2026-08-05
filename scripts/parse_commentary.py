import pymupdf
import re
import json

RED = 16711680
ITALIC_FLAG_VALUE = 6

HEADERS_AND_FOOTERS = {
    "International Gita Society",
    "The Bhagavad Gita"
}


def extract_pages_from_pdf(filename):
    """
    Extracts the layout information from a PDF.
    Returns a list of page dictionaries.
    """
    document = pymupdf.open(filename)
    pages = []

    for page in document:
        pages.append(page.get_text("dict"))

    document.close()
    return pages


def is_section_heading(text):
    """
    Returns True if the given text is a valid section heading.
    """

    if text.isupper():
        return False

    if re.match(r"^\d+\.\s+", text):
        return False

    if text == "Chapter Summary":
        return False

    return True


def is_italic(span):
    return span["flags"] == ITALIC_FLAG_VALUE


def is_header_or_footer(text):
    return any(header in text for header in HEADERS_AND_FOOTERS)


def is_decorative_text(text):
    return "Teachings of the Gita begins" in text


def append_current_section_to_sections(sections, current_section):
    if current_section is not None:
        sections.append(current_section)


def parse_sections(pages):
    """
    Parses section headings and their content from the PDF.
    Returns a list of section dictionaries.
    """

    sections = []

    current_chapter_number = None
    current_section = None

    for page in pages:

        for block in page["blocks"]:

            if "lines" not in block:
                continue

            for line in block["lines"]:

                for span in line["spans"]:

                    text = span["text"].strip()

                    if not text:
                        continue

                    if is_header_or_footer(text):
                        continue

                    if is_italic(span):
                        continue

                    if is_decorative_text(text):
                        continue

                    color = span["color"]

                    # ---------------------------------
                    # Chapter Number
                    # ---------------------------------
                    chapter_match = re.match(
                        r"CHAPTER\s+(\d+)",
                        text
                    )

                    if chapter_match:

                        append_current_section_to_sections(
                            sections,
                            current_section
                        )

                        current_section = None

                        current_chapter_number = int(
                            chapter_match.group(1)
                        )

                        continue

                    # ---------------------------------
                    # Ignore Chapter Title
                    # Example:
                    # 2. Spiritual Knowledge
                    # ---------------------------------
                    if re.match(r"^\d+\.\s+.+", text):
                        continue

                    # ---------------------------------
                    # Section Heading
                    # ---------------------------------
                    if color == RED:

                        if not is_section_heading(text):
                            continue

                        append_current_section_to_sections(
                            sections,
                            current_section
                        )

                        current_section = {
                            "chapter_number": current_chapter_number,
                            "section_title": text,
                            "content": []
                        }

                    # ---------------------------------
                    # Body Text
                    # ---------------------------------
                    else:

                        if current_section is None:

                            if current_chapter_number is None:
                                continue

                            current_section = {
                                "chapter_number": current_chapter_number,
                                "section_title": "Chapter Introduction",
                                "content": []
                            }

                        current_section["content"].append(text)

    # Save final section
    append_current_section_to_sections(
        sections,
        current_section
    )

    return sections


def main():

    pages = extract_pages_from_pdf(
        "data/raw/commentary.pdf"
    )

    sections = parse_sections(pages)

    for section in sections:
        section["content"] = " ".join(
            section["content"]
        ).strip()

    with open(
        "data/intermediate/commentary.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            sections,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Successfully saved {len(sections)} sections."
    )


if __name__ == "__main__":
    main()