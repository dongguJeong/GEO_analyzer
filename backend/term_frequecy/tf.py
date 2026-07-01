from collections import Counter

def compute_tf(tokens : list[str]) -> dict[str,float] :
    """
    tokens: 한 문서를 토큰화한 결과
    반환값: {word: TF값}

    전체 단어 중에서 몇 퍼센트나 등장했는지

    >>> compute_tf(['geo', '분석', '검색', '검색', '최적'])
    {'geo': 0.2, '분석': 0.2, '검색': 0.4, '최적': 0.2}
    """
    total = len(tokens)
    if total == 0 :
        return {}
    
    counts  = Counter(tokens)
    return {word : count/total for  word, count in counts.items()}