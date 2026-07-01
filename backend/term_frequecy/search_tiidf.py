from term_frequecy.tfidf_scores import compute_tfidf_score
from tokenizer.tokenizer import tokenize

def search_tfidf(query :str, documents : dict[int ,list[str]],  top_k: int = 5) :
    query_tokens = tokenize(query) 
    scores = compute_tfidf_score(query_tokens, documents)
    ranked = sorted(scores.items(), key=lambda x : x[1] , reverse=True)
    return ranked[:top_k]

"""
documents = {
    1: "GEO 분석기로 콘텐츠의 검색 노출을 최적화합니다",
    2: "파이썬으로 검색엔진을 직접 만들어보는 프로젝트입니다",
    3: "GEO와 SEO는 서로 다른 최적화 전략입니다",
    4: "LLM이 콘텐츠를 인용하는 방식을 분석합니다",
    5: "역색인과 TF-IDF는 검색엔진의 핵심 알고리즘입니다",
}

query = "GEO 검색 최적화"

tokenized_docs = {doc_id: tokenize(content) for doc_id, content in documents.items()}

result = search_tfidf(query,tokenized_docs )
print(result)

3번 문서 0.489 — "GEO와 SEO는 서로 다른 최적화 전략입니다"
1번 문서 0.326 — "GEO 분석기로 콘텐츠의 검색 노출을 최적화합니다"
5번 문서 0.081 — "역색인과 TF-IDF는 검색엔진의 핵심 알고리즘입니다"
2번 문서 0.060 — "파이썬으로 검색엔진을 직접 만들어보는 프로젝트입니다"
4번 문서 0.000 — "LLM이 콘텐츠를 인용하는 방식을 분석합니다


TF-IDF의 한계도 여기서 보입니다. 3번보다 1번이 직관적으로 더 관련도가 높아 보이는데 역전된 건 문서 길이 보정이 부족해서예요. 
이게 BM25가 해결하는 문제입니다. 

"""
