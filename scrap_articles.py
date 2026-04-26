"""
Scrape les URLs des news sur thequantuminsider.com
"""

import requests
from bs4 import BeautifulSoup

# ─── MODE TEST ─────────────────────────────────────────────────────────────
# True  = affiche les URLs sans toucher a Airtable
# False = envoie vers Airtable
DRY_RUN = True
# ───────────────────────────────────────────────────────────────────────────

SECTIONS = {
    "Capital Markets":  "https://thequantuminsider.com/category/daily/capital-markets/",
    "National":         "https://thequantuminsider.com/category/daily/national/",
    "Quantum Business": "https://thequantuminsider.com/category/daily/business/",
    "Research":         "https://thequantuminsider.com/category/daily/researchandtech/",
}

# Update if you do not use Chrome
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}


def scrape_section(name, url) -> list[dict]:
    """Recupere les 10 premiers articles d'une section."""
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []
    seen_urls = set()

    for tag in soup.select("h6.elementor-post__title a"):
        href = tag.get("href", "")
        title = tag.get_text(strip=True)

        if href and href not in seen_urls:
            seen_urls.add(href)
            articles.append({"url": href, "title": title, "section": name})

        if len(articles) >= 10:
            break

    print(f"[scraper] {name} -> {len(articles)} article(s)")
    return articles


def scrape_news() -> list[dict]:
    """Scrape les 4 sections et retourne jusqu'a 40 articles."""
    all_articles = []

    for name, url in SECTIONS.items():
        all_articles += scrape_section(name, url)

    print(f"[scraper] Total : {len(all_articles)} article(s) trouves")
    return all_articles


# ─── MAIN ──────────────────────────────────────────────────────────────────

def main():
    articles = scrape_news()
    for i, article in enumerate(articles):
        print(i)
        print(article)
        print()


if __name__ == "__main__":
    main()