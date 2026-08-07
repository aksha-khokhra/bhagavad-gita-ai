"""
Evaluate retrieval with a typed labeled query set.

Reports:
- Verse Recall@3 / MRR@3 for semantic and conceptual queries
- Exact Reference Accuracy
- Chapter Query Accuracy
- Out-of-Scope Rejection Accuracy

Run from the project root:

    python scripts/evaluate_retriever.py
"""

import _bootstrap  # noqa: F401

from src.knowledge_base.config import RETRIEVAL_EVAL_DATASET
from src.knowledge_base.utils import load_json
from src.retriever.retriever import Retriever

K = 3
VERSE_METRIC_TYPES = {"semantic", "conceptual"}


def retrieved_references(results, k):
    return [
        result["metadata"]["reference"]
        for result in results["verses"][:k]
    ]


def recall_at_k(expected, retrieved):
    if not expected:
        return 0.0

    expected_set = set(expected)
    hits = expected_set.intersection(retrieved)
    return len(hits) / len(expected_set)


def reciprocal_rank(expected, retrieved):
    expected_set = set(expected)

    for index, reference in enumerate(retrieved, start=1):
        if reference in expected_set:
            return 1.0 / index

    return 0.0


def chapter_hit(results, expected_chapters):
    expected = set(expected_chapters)
    routed = results.get("route", {})
    if (
        routed.get("mode") == "chapter_reference"
        and routed.get("chapter_number") in expected
    ):
        return True

    retrieved_chapters = {
        result["metadata"]["chapter_number"]
        for result in results.get("chapters", [])
    }
    return bool(expected.intersection(retrieved_chapters))


def mean(values):
    if not values:
        return 0.0
    return sum(values) / len(values)


def main():
    dataset = load_json(RETRIEVAL_EVAL_DATASET)
    retriever = Retriever()

    recall_scores = []
    mrr_scores = []
    exact_hits = 0
    exact_total = 0
    chapter_hits = 0
    chapter_total = 0
    out_of_scope_hits = 0
    out_of_scope_total = 0

    print(f"Evaluating {len(dataset)} typed queries\n")

    for item in dataset:
        query = item["query"]
        query_type = item.get("type", "semantic")
        expected = item.get("expected_references", [])
        expected_chapters = item.get("expected_chapters", [])

        results = retriever.retrieve(
            query,
            verse_n_results=max(K, 10),
            commentary_n_results=5,
        )
        route_mode = results.get("route", {}).get("mode")
        top_k = retrieved_references(results, K)

        print("=" * 80)
        print(f"Type:  {query_type}")
        print(f"Query: {query}")
        print(f"Route: {results.get('route')}")

        if query_type in VERSE_METRIC_TYPES:
            recall = recall_at_k(expected, top_k)
            mrr = reciprocal_rank(expected, top_k)
            recall_scores.append(recall)
            mrr_scores.append(mrr)
            hits = set(expected).intersection(top_k)
            missed = set(expected) - set(top_k)
            print(f"Expected: {expected}")
            print(f"Top-{K}:  {top_k}")
            print(f"Hits:     {sorted(hits) if hits else 'none'}")
            if missed:
                print(f"Missed:   {sorted(missed)}")
            print(f"Recall@{K}: {recall:.2f} | RR: {mrr:.2f}")

        elif query_type == "exact_reference":
            exact_total += 1
            hit = bool(expected) and expected[0] in top_k
            exact_hits += int(hit)
            print(f"Expected: {expected}")
            print(f"Top-{K}:  {top_k}")
            print(f"Exact hit: {hit}")

        elif query_type == "chapter":
            chapter_total += 1
            hit = chapter_hit(results, expected_chapters)
            chapter_hits += int(hit)
            retrieved_chapters = [
                result["metadata"]["chapter_number"]
                for result in results.get("chapters", [])
            ]
            print(f"Expected chapters: {expected_chapters}")
            print(f"Retrieved chapters: {retrieved_chapters}")
            print(f"Chapter query hit: {hit}")

        elif query_type == "out_of_scope":
            out_of_scope_total += 1
            hit = route_mode == "out_of_scope"
            out_of_scope_hits += int(hit)
            print(f"Out-of-scope rejection: {hit}")

        if results.get("commentaries"):
            print("\nCommentaries:")
            for index, result in enumerate(results["commentaries"][:3], start=1):
                metadata = result["metadata"]
                score = result.get("rerank_score")
                score_text = (
                    f"rerank={score:.4f}"
                    if score is not None
                    else f"distance={result['distance']:.4f}"
                )
                print(
                    f"  {index}. Ch.{metadata['chapter_number']} - "
                    f"{metadata['section_title']} ({score_text})"
                )

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print(
        f"Verse-reference Recall@{K} "
        f"(semantic/conceptual): {mean(recall_scores):.3f}"
    )
    print(
        f"Verse-reference MRR@{K} "
        f"(semantic/conceptual): {mean(mrr_scores):.3f}"
    )
    if exact_total:
        print(
            f"Exact Reference Accuracy: "
            f"{exact_hits}/{exact_total} "
            f"({exact_hits / exact_total:.3f})"
        )
    if chapter_total:
        print(
            f"Chapter Query Accuracy: "
            f"{chapter_hits}/{chapter_total} "
            f"({chapter_hits / chapter_total:.3f})"
        )
    if out_of_scope_total:
        print(
            f"Out-of-Scope Rejection Accuracy: "
            f"{out_of_scope_hits}/{out_of_scope_total} "
            f"({out_of_scope_hits / out_of_scope_total:.3f})"
        )
    print("=" * 80)

    return {
        "recall": mean(recall_scores),
        "mrr": mean(mrr_scores),
        "exact": exact_hits / exact_total if exact_total else None,
        "chapter": chapter_hits / chapter_total if chapter_total else None,
        "out_of_scope": (
            out_of_scope_hits / out_of_scope_total
            if out_of_scope_total
            else None
        ),
        "exact_hits": exact_hits,
        "exact_total": exact_total,
        "chapter_hits": chapter_hits,
        "chapter_total": chapter_total,
        "out_of_scope_hits": out_of_scope_hits,
        "out_of_scope_total": out_of_scope_total,
    }


if __name__ == "__main__":
    main()
