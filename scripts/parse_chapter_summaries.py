import re
import json


INPUT_FILE = "data/raw/summary.md"
OUTPUT_FILE = "data/processed/chapter_summaries.json"


def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def parse_chapters(text):

    chapters = []

    # Find every chapter heading
    pattern = re.compile(
        r"<h3>\s*Chapter\s+(\d+):.*?</h3>",
        re.IGNORECASE | re.DOTALL
    )

    matches = list(pattern.finditer(text))

    for i, match in enumerate(matches):

        chapter_number = int(match.group(1))

        start = match.end()

        if i < len(matches) - 1:
            end = matches[i + 1].start()
        else:
            end = len(text)

        summary = text[start:end].strip()

        chapters.append({
            "chapter_number": chapter_number,
            "summary": summary
        })

    return chapters


def main():

    text = read_file(INPUT_FILE)

    chapters = parse_chapters(text)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chapters,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"Successfully saved {len(chapters)} chapter summaries."
    )


if __name__ == "__main__":
    main()