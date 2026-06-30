from collections import defaultdict
from backend.tokenizer.tokenizer import tokenize

def build_inverted_index(documents: dict[int, str]) -> dict[str, set[int]]:
    """
    documents: {doc_id: content} 형태
    반환값: {word: {doc_id, doc_id, ...}}
    """

    inverted_index = defaultdict(set)

    for doc_id, content in documents.items() :
        tokens = tokenize(content)

        for token in tokens :
            inverted_index[token].add(doc_id)
    
    return inverted_index

