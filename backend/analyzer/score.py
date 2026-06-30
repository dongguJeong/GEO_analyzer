from typing import Dict

LLM_WEIGHTS = {
    "readability": 0.25,
    "expertise": 0.30,
    "trustworthiness": 0.25,
    "faq": 0.10,
    "summary": 0.10,
}

MAX_METRIC_SCORE = 30 

def calculate_score(
    llm_result: Dict,
    metrics: Dict
) -> float:

    # -------------------------
    # LLM Score (70점)
    # -------------------------

    llm_score = 0

    for key, weight in LLM_WEIGHTS.items():
        value = llm_result.get(key, 0)
        llm_score += (value / 10) * weight

    llm_score *= 70

    # -------------------------
    # HTML Metrics (30점)
    # -------------------------

    metric_score = 0

    # Title (5)
    if 30 <= metrics["title_length"] <= 60:
        metric_score += 5

    # Meta Description (5)
    if 120 <= metrics["meta_length"] <= 160:
        metric_score += 5

    # H1 (5)
    if metrics["h1_count"] == 1:
        metric_score += 5

    # Heading Structure (3)
    if metrics["heading_ratio"] >= 0.2:
        metric_score += 3

    # Paragraph Length (3)
    if 30 <= metrics["avg_paragraph_length"] <= 120:
        metric_score += 3

    # Image ALT (4)
    metric_score += metrics["image_alt_ratio"] * 4

    # Word Count (5)
    if metrics["word_count"] >= 800:
        metric_score += 5

    metric_score = (metric_score / MAX_METRIC_SCORE) * 30

    # -------------------------
    # Final Score
    # -------------------------

    final_score = llm_score + metric_score

    return round(final_score, 1)