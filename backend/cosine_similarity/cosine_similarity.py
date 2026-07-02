from sentence_transformers import SentenceTransformer
import numpy as np

# 다국어 지원 모델 (한국어 포함, 가벼운 편)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

query = "GEO 검색 최적화"
documents = {
    1: "GEO 분석기로 콘텐츠의 검색 노출을 최적화합니다",
    2: "파이썬으로 검색엔진을 직접 만들어보는 프로젝트입니다",
    3: "GEO와 SEO는 서로 다른 최적화 전략입니다",
    4: "LLM이 콘텐츠를 인용하는 방식을 분석합니다",
    5: "역색인과 TF-IDF는 검색엔진의 핵심 알고리즘입니다",
}

query_vec = model.encode(query)
doc_vecs = {doc_id : model.encode(text) for doc_id, text in documents.items()}

def cosine_similarity(vec1, vec2):
    """
    코사인 유사도 계산
    """
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


results = {doc_id: cosine_similarity(query_vec, vec) for doc_id, vec in doc_vecs.items()}
sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
print(sorted_results)