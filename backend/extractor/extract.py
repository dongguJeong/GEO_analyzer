from bs4 import BeautifulSoup

REMOVE_TAGS = [
    "scripts","style","nav","footer","header","aside"
]

def clean_html(soup) :
    for tag in REMOVE_TAGS :
        for element in soup.find_all(tag) :
            element.decompose()

def extract_text(html : str) -> str :
    soup = BeautifulSoup(html,"lxml")
    clean_html(soup)
    
    title = soup.title.get_text(strip=True) if soup.title else ""

    paragraph  = soup.find_all("p")
    text= "\n".join([p.get_text() for p in paragraph])

    return f"{title}\n\n{text}"