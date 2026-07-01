from collections import Counter, defaultdict
import math 
from tokenizer.tokenizer import tokenize

def calculate_bm25(
    query_tokens : list[str], 
    documents : dict[int ,list[str]], 
    k1 : float = 0.75,
    b : float = 0.75) -> dict[int, float]:
    """
    query_tokens : 검색어 토큰 리스트
    documents : {doc_id: tokens} 형태 (이미 토큰화된 상태)
    k1 : BM25의 k1 파라미터 (문서 길이 보정)
    b : BM25의 b 파라미터 (문서 길이 보정)
    """

    # 1. IDF 계산 (TF-IDF와 동일)
    total_docs= len(documents)
    doc_freq = defaultdict(int)

    for tokens in documents.values() :
        for word in set(tokens) :
            doc_freq[word] += 1
    
    idf = {
        word: math.log((total_docs - freq + 0.5) / (freq + 0.5) + 1)
        for word, freq in doc_freq.items()
    }

     # 2. 평균 문서 길이
    avgdl= sum(len(tokens) for tokens in documents.values()) / total_docs

    # 3. 문서별 BM25 점수
    scores = {}
    for doc_id, tokens in documents.items():
        dl = len(tokens)
        score = 0.0
        tf_map=Counter(tokens)

        for word in query_tokens :
            tf = tf_map.get(word, 0)
            if tf == 0:
                continue
            numerator = tf * (k1 + 1)
            denominator = tf + k1 * (1 - b + b * (dl / avgdl))
            score += idf.get(word, 0) * (numerator / denominator)
        scores[doc_id] = score

    return scores

def search_bm25(
    query: str,
    documents: dict[int, list[str]],
    top_k: int = 5,
):
    
    query_tokens = tokenize(query)
    scores = calculate_bm25(query_tokens, documents)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_k]


query = "GEO 검색 최적화"
documents = {
    1: "GEO 분석기로 콘텐츠의 검색 노출을 최적화합니다",
    2: "파이썬으로 검색엔진을 직접 만들어보는 프로젝트입니다",
    3: "GEO와 SEO는 서로 다른 최적화 전략입니다",
    4: "LLM이 콘텐츠를 인용하는 방식을 분석합니다",
    5: "역색인과 TF-IDF는 검색엔진의 핵심 알고리즘입니다",
}
tokenized_docs = {doc_id: tokenize(content) for doc_id, content in documents.items()}

result = search_bm25(query, tokenized_docs)
print(result)