# BM25 (Best Matching 25)

## 개요

BM25는 TF-IDF를 개선한 문서 관련도 랭킹 알고리즘으로, 현재 Elasticsearch를 포함한 대부분의 실전 검색엔진이 기본 알고리즘으로 채택하고 있습니다.

## 요약
이 단어가 희귀할수록(IDF), 이 문서에 자주 나올수록(TF 포화), 문서가 짧을수록(길이 보정) 점수를 높게 준다

---

## TF-IDF의 한계

BM25를 이해하려면 먼저 TF-IDF가 어떤 문제를 갖고 있는지 알아야 합니다.

### 1. TF 선형 증가 문제

TF-IDF에서 TF(단어 빈도)는 선형으로 점수에 반영됩니다.

```
단어가 1번 등장 → 점수 1
단어가 5번 등장 → 점수 5
단어가 10번 등장 → 점수 10
```

현실에서는 단어가 10번 나온 문서가 1번 나온 문서보다 10배 관련도가 높지 않습니다. 일정 횟수 이상 등장하면 관련도 증가폭이 줄어드는 게 자연스럽습니다.

### 2. 문서 길이 보정 부족

짧은 문서는 단어 수가 적어서 특정 단어의 TF 비중이 자동으로 높아집니다. 반대로 긴 문서는 같은 단어가 여러 번 나와도 TF가 희석됩니다. TF-IDF는 이 길이 차이를 충분히 보정하지 못합니다.

> **실험 결과**: 위 더미데이터로 `"GEO 검색 최적화"` 쿼리를 TF-IDF로 검색하면,  
> 단어 수가 적은 3번 문서("GEO와 SEO는 서로 다른 최적화 전략입니다")가  
> 더 관련도 높은 1번 문서("GEO 분석기로 콘텐츠의 검색 노출을 최적화합니다")보다 높은 점수를 받습니다.  
> BM25는 이 순위를 올바르게 역전시킵니다.

---

## BM25 공식

```
BM25(q, d) = Σ IDF(w) × [ TF(w,d) × (k1 + 1) ] / [ TF(w,d) + k1 × (1 - b + b × |d| / avgdl) ]
```

| 기호 | 의미 |
|------|------|
| `w` | 쿼리의 각 단어 |
| `TF(w, d)` | 문서 d에서 단어 w의 등장 횟수 |
| `IDF(w)` | 단어 w의 희귀도 (전체 문서 중 등장 문서가 적을수록 높음) |
| `|d|` | 현재 문서의 길이 (토큰 수) |
| `avgdl` | 전체 문서의 평균 길이 |
| `k1` | TF 포화 속도 조절 파라미터 (기본값: 1.5) |
| `b` | 문서 길이 보정 강도 (기본값: 0.75) |

---

## 핵심 개념

### TF 포화 (Saturation)

분모에 TF가 다시 등장하면서, TF가 커질수록 점수 증가폭이 줄어드는 포화 곡선이 만들어집니다.

```
TF-IDF:  1번→1점  5번→5점  10번→10점  (선형)
BM25:    1번→1점  5번→3점  10번→4점   (포화)
```

`k1` 값이 클수록 포화가 느려지고(반복 등장의 영향이 더 오래 유지), 작을수록 빨리 포화됩니다.

### 문서 길이 정규화

분모의 `(1 - b + b × |d| / avgdl)` 항이 문서 길이를 보정합니다.

- 문서가 평균보다 길면 → 분모가 커짐 → 점수가 낮아짐
- 문서가 평균보다 짧으면 → 분모가 작아짐 → 점수가 높아짐
- `b = 1.0`: 길이 보정을 완전히 적용
- `b = 0.0`: 길이 보정을 전혀 적용하지 않
- `b = 0.75`: 절충안 (기본값)

### IDF 스무딩

TF-IDF와 달리 BM25의 IDF 공식은 스무딩이 적용되어 있습니다.

```python
# TF-IDF IDF
log(total_docs / freq)

# BM25 IDF
log((total_docs - freq + 0.5) / (freq + 0.5) + 1)
```

`+0.5` 스무딩으로 모든 문서에 등장하는 단어가 0점으로 완전히 죽는 현상을 방지하고, `+1`로 음수가 나오는 엣지케이스를 막습니다.

---

## 구현

```python
import math
from collections import Counter


def compute_bm25_scores(
    query_tokens: list[str],
    documents: dict[int, list[str]],
    k1: float = 1.5,
    b: float = 0.75,
) -> dict[int, float]:

    total_docs = len(documents)

    # IDF 계산
    doc_freq = {}
    for tokens in documents.values():
        for word in set(tokens):
            doc_freq[word] = doc_freq.get(word, 0) + 1

    idf = {
        word: math.log((total_docs - freq + 0.5) / (freq + 0.5) + 1)
        for word, freq in doc_freq.items()
    }

    # 평균 문서 길이
    avgdl = sum(len(tokens) for tokens in documents.values()) / total_docs

    # 문서별 BM25 점수
    scores = {}
    for doc_id, tokens in documents.items():
        dl = len(tokens)
        tf_map = Counter(tokens)
        score = 0.0

        for word in query_tokens:
            tf = tf_map.get(word, 0)
            if tf == 0:
                continue
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * dl / avgdl)
            score += idf.get(word, 0) * (numerator / denominator)

        scores[doc_id] = score

    return scores
```

---

## TF-IDF vs BM25 비교

| 항목 | TF-IDF | BM25 |
|------|--------|------|
| TF 반영 방식 | 선형 | 포화 곡선 |
| 문서 길이 보정 | 기본 정규화만 | `b` 파라미터로 세밀 조절 |
| IDF 스무딩 | 없음 | `+0.5` 스무딩 적용 |
| 파라미터 튜닝 | 없음 | `k1`, `b` 조절 가능 |
| 실전 채택 | 레거시 | Elasticsearch 기본값 |

---

## 파라미터 튜닝 가이드

| 상황 | 권장 설정 |
|------|-----------|
| 짧은 문서 위주 (트윗, 제목) | `b=0.3` 낮게, 길이 보정 줄임 |
| 긴 문서 위주 (논문, 기사) | `b=0.9` 높게, 길이 보정 강화 |
| 키워드 반복이 중요한 경우 | `k1=2.0` 높게, 포화 느리게 |
| 키워드 존재 여부만 중요한 경우 | `k1=1.0` 낮게, 빠르게 포화 |