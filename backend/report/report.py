from typing import Dict


def check(value: bool) -> str:
    return "✔" if value else "✘"


def grade(score: float) -> str:

    if score >= 90:
        return "A"

    if score >= 80:
        return "B"

    if score >= 70:
        return "C"

    if score >= 60:
        return "D"

    return "F"


def print_report(
    url: str,
    score: float,
    metrics: Dict,
    analysis: Dict
):

    print("=" * 70)
    print("                     GEO ANALYSIS REPORT")
    print("=" * 70)

    print(f"\nURL")
    print(url)

    print(f"\nGEO Score : {score:.1f} / 100")
    print(f"Grade     : {grade(score)}")

    print("\n" + "-" * 70)
    print("HTML METRICS")
    print("-" * 70)

    print(f"Title                : {check(metrics['has_title'])}")
    print(f"Title Length         : {metrics['title_length']}")

    print(f"Meta Description     : {check(metrics['has_meta_description'])}")
    print(f"Meta Length          : {metrics['meta_length']}")

    print(f"H1                   : {check(metrics['has_h1'])}")
    print(f"H1 Count             : {metrics['h1_count']}")

    print(f"Heading Count        : {metrics['heading_count']}")
    print(f"Paragraph Count      : {metrics['paragraph_count']}")
    print(f"Average Paragraph    : {metrics['avg_paragraph_length']:.1f} words")
    print(f"Heading Ratio        : {metrics['heading_ratio']:.2f}")

    print(f"Image Count          : {metrics['image_count']}")
    print(f"Image ALT Ratio      : {metrics['image_alt_ratio']:.1%}")

    print(f"Internal Links       : {metrics['internal_links']}")
    print(f"External Links       : {metrics['external_links']}")

    print(f"Word Count           : {metrics['word_count']}")

    print("\n" + "-" * 70)
    print("LLM ANALYSIS")
    print("-" * 70)

    print(f"Readability      : {analysis['readability']}/10")
    print(f"Expertise        : {analysis['expertise']}/10")
    print(f"Trustworthiness  : {analysis['trustworthiness']}/10")
    print(f"FAQ              : {analysis['faq']}/10")
    print(f"Summary          : {analysis['summary']}/10")

    print("\nStrengths")

    for item in analysis["strengths"]:
        print(f"  + {item}")

    print("\nWeaknesses")

    for item in analysis["weaknesses"]:
        print(f"  - {item}")

    print("\nSuggestions")

    for item in analysis["suggestions"]:
        print(f"  * {item}")

    print("\n" + "=" * 70)