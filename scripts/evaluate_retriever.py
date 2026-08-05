"""
Evaluate verse retrieval with a labeled query set.

Prints per-query hits and aggregate Recall@K / MRR.
Run from the project root:

    python scripts/evaluate_retriever.py
"""

import _bootstrap  # noqa: F401

from src.knowledge_base.config import RETRIEVAL_EVAL_DATASET
from src.knowledge_base.utils import load_json
from src.retriever.retriever import Retriever

K = 3


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


def main():
    dataset = load_json(RETRIEVAL_EVAL_DATASET)
    retriever = Retriever()

    recall_scores = []
    mrr_scores = []

    print(f"Evaluating {len(dataset)} queries (verse Recall@{K})\n")

    for item in dataset:
        query = item["query"]
        expected = item["expected_references"]

        results = retriever.retrieve(
            query,
            verse_n_results=max(K, 10),
            commentary_n_results=5,
        )

        top_k = retrieved_references(results, K)
        recall = recall_at_k(expected, top_k)
        mrr = reciprocal_rank(expected, top_k)

        recall_scores.append(recall)
        mrr_scores.append(mrr)

        hits = set(expected).intersection(top_k)
        missed = set(expected) - set(top_k)

        print("=" * 80)
        print(f"Query: {query}")
        print(f"Expected: {expected}")
        print(f"Top-{K}:  {top_k}")
        print(f"Hits:     {sorted(hits) if hits else 'none'}")
        if missed:
            print(f"Missed:   {sorted(missed)}")
        print(f"Recall@{K}: {recall:.2f} | RR: {mrr:.2f}")

        print("\nCommentaries:")
        for index, result in enumerate(results["commentaries"][:3], start=1):
            metadata = result["metadata"]
            print(
                f"  {index}. Ch.{metadata['chapter_number']} - "
                f"{metadata['section_title']} "
                f"(distance={result['distance']:.4f})"
            )

    mean_recall = sum(recall_scores) / len(recall_scores)
    mean_mrr = sum(mrr_scores) / len(mrr_scores)

    print("\n" + "=" * 80)
    print(f"Mean Recall@{K}: {mean_recall:.3f}")
    print(f"Mean MRR@{K}:    {mean_mrr:.3f}")
    print("=" * 80)


if __name__ == "__main__":
    main()
