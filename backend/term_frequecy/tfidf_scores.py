from term_frequecy.idf import compute_idf
from term_frequecy.tf import compute_tf


def compute_tfidf_score(
    query_tokens : list[str], 
    documents : dict[int, list[str]],
) -> dict[int, float] :
    """
    compute_tfidf_scores(['geo', '최적'], tokenized_docs)
    
    >>> {1: 0.2025, 2: 0.0, 3: 0.27}
    """
    idf = compute_idf(documents)
    scores = {}

    for doc_id , tokens in documents.items() :
        tf = compute_tf(tokens)
        score = 0.0
        for word in query_tokens:
            score += tf.get(word, 0) * idf.get(word,0)
        scores[doc_id] = score
    
    return scores