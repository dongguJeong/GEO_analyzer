from bs4 import BeautifulSoup
from urllib.parse import urlparse


def extract_metrics(html: str, url: str):

    soup = BeautifulSoup(html, "lxml")

    metrics = {}

    # -------------------------
    # Title
    # -------------------------

    title = soup.title

    metrics["has_title"] = title is not None

    metrics["title_length"] = (
        len(title.get_text(strip=True))
        if title
        else 0
    )

    # -------------------------
    # Meta Description
    # -------------------------

    meta = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    metrics["has_meta_description"] = meta is not None

    metrics["meta_length"] = (
        len(meta.get("content", ""))
        if meta
        else 0
    )

    # -------------------------
    # Headings
    # -------------------------

    h1_tags = soup.find_all("h1")

    metrics["has_h1"] = len(h1_tags) > 0

    metrics["h1_count"] = len(h1_tags)

    headings = soup.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6"]
    )

    metrics["heading_count"] = len(headings)

    # -------------------------
    # Paragraph
    # -------------------------

    paragraphs = soup.find_all("p")

    metrics["paragraph_count"] = len(paragraphs)

    paragraph_lengths = [
        len(
            p.get_text(" ", strip=True).split()
        )
        for p in paragraphs
    ]

    metrics["avg_paragraph_length"] = (
        sum(paragraph_lengths) / len(paragraph_lengths)
        if paragraph_lengths
        else 0
    )

    metrics["heading_ratio"] = (
        metrics["heading_count"]
        / max(metrics["paragraph_count"], 1)
    )

    # -------------------------
    # Images
    # -------------------------

    images = soup.find_all("img")

    metrics["image_count"] = len(images)

    alt_count = sum(
        1
        for img in images
        if img.get("alt")
    )

    metrics["image_alt_ratio"] = (
        alt_count / len(images)
        if images
        else 1
    )

    # -------------------------
    # Links
    # -------------------------

    page_domain = urlparse(url).netloc

    internal_links = 0
    external_links = 0

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if href.startswith("/"):
            internal_links += 1

        elif href.startswith("http"):

            link_domain = urlparse(href).netloc

            if link_domain == page_domain:
                internal_links += 1
            else:
                external_links += 1

    metrics["internal_links"] = internal_links

    metrics["external_links"] = external_links

    # -------------------------
    # Word Count
    # -------------------------

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)

    metrics["word_count"] = len(text.split())

    return metrics