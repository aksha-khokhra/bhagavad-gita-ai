# Project Tattva Documentation

**Document:** 09 — Evaluation  
**Version:** 1.1  
**Status:** Initial Evaluation Completed

---

# 1. Purpose

This document describes the initial evaluation process used to inspect retrieval quality and end-to-end response behavior in Project Tattva.

The evaluation intentionally separates retrieval from generation so that failures can be traced to the correct system component.

---

# 2. Evaluation Objectives

The initial evaluation aimed to determine:

- Whether relevant chapters and verses were retrieved.
- Whether vector distance rankings were reasonable.
- Which question types performed well.
- Which concepts were missed.
- Whether commentary improved conceptual retrieval.
- Whether out-of-scope questions were handled safely.

---

# 3. Evaluation Strategy

The evaluation used three stages.

## Stage 1 — Retrieval Inspection

Questions were embedded and searched without calling the LLM.

The script printed:

- Question
- Verse reference
- Chapter title
- Distance

## Stage 2 — Ranking Investigation

Weak queries were expanded from top 5 to top 20 results to find the rank of an expected verse.

## Stage 3 — End-to-End Comparison

The same question was tested before and after commentary retrieval was introduced.

---

# 4. Evaluation Queries

Representative questions included:

- Why should we perform actions without expecting results?
- What is Karma Yoga?
- What is the difference between action and inaction?
- Who is a person of steady wisdom?
- How can I control my mind?
- What is devotion?
- What is the Self?
- Why do people suffer?
- How should a wise person perform their duties?
- What is meditation?

An out-of-scope query was also tested:

```text
Who built the Taj Mahal?
```

---

# 5. Strong Retrieval Results

## Karma Yoga

The query retrieved multiple Chapter 3 verses with low relative distances.

## Mind Control

The query retrieved Chapter 6 verses related to controlling the mind.

## Devotion

The query retrieved multiple Chapter 12 verses.

## Meditation

The query retrieved several Chapter 6 verses.

## Action and Inaction

The query retrieved Verses 4.16 and 4.17 near the top.

These results showed that the embedding model performs well when user language is close to the theme and wording of the stored documents.

---

# 6. Weak Retrieval Results

## Steady Wisdom

The query did not retrieve the expected Chapter 2 verses describing steady wisdom.

## Action Without Expected Results

The expected Verse 2.47 did not appear in the top 20 verse results.

The query used:

```text
expecting results
```

while the translation used:

```text
fruit of action
```

This vocabulary difference reduced semantic similarity under the current embedding model.

---

# 7. Commentary Experiment

A commentary-only search was performed using the same question.

Relevant commentary included language such as:

```text
without attachment to the results
```

This was much closer to the user's wording than the verse translation.

The experiment supported the hypothesis that commentary can act as a semantic bridge between classical translation vocabulary and modern user phrasing.

---

# 8. End-to-End Comparison

## Verse-Only Version

The generated answer stated that the retrieved context did not explicitly contain enough information.

## Verse + Commentary Version

The generated answer discussed:

- Performing work without attachment to results
- Selfless action
- Universal welfare
- Relevant commentary and verse ranges

This represented a clear qualitative improvement.

---

# 9. Out-of-Scope Behavior

The initial prompt allowed the model to mention its training data when it could not answer an unrelated question.

The prompt was strengthened to require one fixed fallback response and prohibit:

- Outside knowledge
- Guessing
- Training-data explanations

This demonstrates that generation safety must be tested directly rather than assumed from prompt wording.

---

# 10. Evaluation Findings

The initial evaluation produced the following conclusions:

1. Retrieval should be evaluated separately from generation.
2. The verse collection performs well for direct thematic questions.
3. General embedding models may struggle with domain-specific paraphrases.
4. Commentary improves retrieval and generation for conceptual questions.
5. Increasing `top_k` alone does not solve every retrieval failure.
6. Prompt guardrails require iterative testing.
7. The current system benefits from multiple knowledge sources.

---

# 11. Current Evaluation Limitations

- Manual inspection rather than labeled metrics
- Small query set
- No automated relevance judgments
- No Recall@K or MRR calculation
- No comparison across embedding models
- No latency benchmarks
- No hallucination scoring
- No citation correctness checker

---

# 12. Planned Quantitative Metrics

Future evaluation may include:

## Recall@K

Measures whether an expected document appears within the top K retrieved results.

## Mean Reciprocal Rank

Measures how highly the first relevant result is ranked.

## Precision@K

Measures the proportion of retrieved documents judged relevant.

## Groundedness

Measures whether the answer is supported by retrieved context.

## Citation Accuracy

Measures whether cited references are present in the retrieved evidence.

## Latency

Measures indexing, retrieval, and generation time.

---

# 13. Recommended Evaluation Dataset Structure

```json
{
    "query": "Why should we perform actions without expecting results?",
    "expected_references": ["2.47", "3.19", "3.25"],
    "expected_topics": ["detachment", "selfless action"]
}
```

A labeled dataset would allow retrieval changes to be compared objectively.

---

# 14. Summary

Project Tattva's initial evaluation successfully identified both strengths and weaknesses in the retrieval pipeline.

The most important result was evidence that commentary improves conceptual retrieval by using language closer to modern user questions. This finding directly motivated the move from verse-only retrieval to the current multi-source Retriever.

---

**Next Document:** `10_Future_Development.md`
