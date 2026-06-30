import re 
from kiwipiepy import Kiwi

kiwi = Kiwi()

def tokenize(text : str) -> list[str] :
    text = text.lower()
    korean_parts  = re.findall(r'[가-힣]',text)
    english_parts  = re.findall(r'[a-z]',text)

    tokens = []

    for part in korean_parts  :
        result = kiwi.tokenize(part)
        tokens.extend([t.form for t in result if t.tag.startswith(('NN', 'VV', 'VA'))])

    tokens.extend(english_parts)

    return tokens
