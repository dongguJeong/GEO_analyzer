from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

documents = {
    1: "GEO 분석기로 콘텐츠의 검색 노출을 최적화합니다",
    2: "파이썬으로 검색엔진을 직접 만들어보는 프로젝트입니다",
    3: "GEO와 SEO는 서로 다른 최적화 전략입니다",
    4: "LLM이 콘텐츠를 인용하는 방식을 분석합니다",
    5: "역색인과 TF-IDF는 검색엔진의 핵심 알고리즘입니다",
}

doc_ids = list(documents.keys())
doc_texts = list(documents.values())

# 임베딩 생성 (batch로 한 번에)
doc_embeddings = model.encode(doc_texts).astype('float32')

# FAISS 인덱스 생성 — 384차원, L2 거리 기반
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# 벡터 등록
index.add(doc_embeddings)

# 쿼리 검색
query = "GEO 검색 최적화"
query_vec = model.encode([query]).astype('float32')

k = 5  # 상위 5개
distances, indices = index.search(query_vec, k)

# 결과 출력 (원래 doc_id로 매핑)
for rank, idx in enumerate(indices[0]):
    print(f"{rank+1}위: doc_id={doc_ids[idx]}, 거리={distances[0][rank]:.4f}, 내용={doc_texts[idx]}")