
from metric.html_metric import extract_metrics
from crawler.download import fetch_html
from extractor.extract import extract_text

from analyzer.score import calculate_score
from report.report import grade

from database.database import SessionLocal
from database.models import Analysis

async def analyze_url(url : str , llm , db):

    html = await fetch_html(url)

    content = extract_text(html)

    metrics = extract_metrics(html, url)

    analysis = llm.analyze(content)

    score = calculate_score(
        analysis,
        metrics
    )

    grade_result = grade(score)

    try:
        result = Analysis(
            url=url,
            score=score,
            grade=grade_result
        )

        db.add(result)
        db.commit()

        # id 값을 사용하려면 갱신
        db.refresh(result)

    finally:
        db.close()

    return {
        "id": result.id,
        "url": url,
        "score": score,
        "grade": grade_result,
        "metrics": metrics,
        "analysis": analysis
    }