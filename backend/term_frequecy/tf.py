from collections import Counter

def compute_tf(tokens : list[str]) -> dict[str,float] :
    """
    tokens: 한 문서를 토큰화한 결과
    반환값: {word: TF값}
    """
    total = len(tokens)
    if total == 0 :
        return {}
    
    counts  = Counter(tokens)
    return {word : count/total for  word, count in counts.items()}