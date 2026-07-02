import faiss
import numpy as np

# false_cpu를 코드를 클래스화
class VectorStore:
    def __init__(self, dimension : int = 384):
        self.index = faiss.IndexFlatIP(dimension)
        self.doc_texts = []

    def add(self, embeddings : np.ndarray, text : list[str]):
        faiss.normalize_L2(embeddings)  # 벡터 정규화
        self.index.add(embeddings)
        self.doc_texts.extend(text)
    
    def search(self, query_embedding : np.ndarray, top_k : int = 5):
        faiss.normalize_L2(query_embedding)  # 쿼리 벡터 정규화
        distances, indices = self.index.search(query_embedding, top_k)
        results = [(self.doc_texts[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
        return results