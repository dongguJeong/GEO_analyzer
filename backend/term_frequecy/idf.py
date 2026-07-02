from collections import defaultdict
import math 

def compute_idf(documents : dict[int ,list[str]]) -> dict[str, float]:
    """
    documents: {doc_id: tokens} 형태 (이미 토큰화된 상태)
    반환값: {word: IDF값}
    
    1 : ['geo', '분석' , '검색', '최적],
    2 : ['파이썬', '검색', '엔진']
    3 : ['geo', 'seo', '최적']

    >>>
    {'geo': 0.405, '분석': 1.099, '검색': 0.405, '최적': 0.405, '파이썬': 1.099, '엔진': 1.099, 'seo': 1.099}

    전체 문서에서 특정 단어가 얼만큼 등장했나
    드물게 등장할수록 변별력이 높다고 보고 가중치를 더 줍니다.
    """

    total_docs = len(documents)
    doc_freq = defaultdict(int)

    for tokens in documents.values() :
        unique_words = set(tokens)
        for word in unique_words :
            doc_freq[word] += 1

    idf = {}
    for word, freq in doc_freq.items() :
        idf[word] = math.log(total_docs / freq)
    
    return idf