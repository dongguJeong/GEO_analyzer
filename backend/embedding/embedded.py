from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def encode(self, texts: list[str]):
        embeddings = self.model.encode(texts).astype('float32')
        return embeddings