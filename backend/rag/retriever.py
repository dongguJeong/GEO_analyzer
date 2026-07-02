class RAGRetriever:
    def __init__(self, embedder, vector_store, llm):
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm

    def query(self, question: str, k: int = 3) -> dict:
        query_vec = self.embedder.encode([question])
        retrieved_docs = self.vector_store.search(query_vec, k)

        context = "\n".join([f"- {doc}" for doc in retrieved_docs])
        prompt = f"""다음 문서들을 참고해서 질문에 답해줘. 문서에 없는 내용은 답하지 마.

[참고 문서]
{context}

[질문]
{question}
"""
        answer = self.llm.analyze(prompt)  # 기존 ClaudeLLM 재사용

        return {
            "question": question,
            "retrieved_docs": retrieved_docs,
            "answer": answer
        }