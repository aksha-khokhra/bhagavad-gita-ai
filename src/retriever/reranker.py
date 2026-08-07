"""Cross-encoder reranking for retrieved candidates."""

from __future__ import annotations

from sentence_transformers import CrossEncoder

from src.knowledge_base.config import RERANKER_MODEL


class CrossEncoderReranker:
    """Score query-document pairs and reorder candidates."""

    def __init__(self, model_name: str = RERANKER_MODEL):
        self.model_name = model_name
        self.model = CrossEncoder(model_name)

    def _candidate_text(self, result: dict) -> str:
        metadata = result.get("metadata") or {}
        translation = metadata.get("english_translation")
        if translation:
            return translation

        content = metadata.get("content")
        if content:
            section = metadata.get("section_title", "")
            return f"{section}\n{content}".strip()

        summary = metadata.get("summary")
        if summary:
            title = metadata.get("chapter_title", "")
            return f"{title}\n{summary}".strip()

        return result.get("document", "")

    def rerank(self, query: str, candidates: list[dict], top_k: int | None = None):
        if not candidates:
            return []

        pairs = [
            (query, self._candidate_text(candidate))
            for candidate in candidates
        ]
        scores = self.model.predict(pairs)

        ranked = []
        for candidate, score in zip(candidates, scores):
            result = dict(candidate)
            result["rerank_score"] = float(score)
            ranked.append(result)

        ranked.sort(key=lambda item: item["rerank_score"], reverse=True)

        if top_k is not None:
            return ranked[:top_k]
        return ranked
