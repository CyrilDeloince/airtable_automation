"""
main.py
Scrape les articles et envoie dans Airtable uniquement les nouveaux liens.
"""

import os
import requests
from dotenv import load_dotenv
from scrap_articles import scrape_news

load_dotenv(r"C:\Users\CyrilDELOINCE\.env")

AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_TABLE   = os.environ["AIRTABLE_TABLE"]

HEADERS_AT = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json",
}
BASE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}"


def get_existing_urls() -> set[str]:
    """Récupère toutes les URLs déjà présentes dans Airtable (gère la pagination)."""
    existing = set()
    params = {"fields[]": "Source URL", "pageSize": 100}

    while True:
        resp = requests.get(BASE_URL, headers=HEADERS_AT, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        for record in data.get("records", []):
            url = record.get("fields", {}).get("Source URL")
            if url:
                existing.add(url)

        # Airtable pagine avec un offset
        offset = data.get("offset")
        if not offset:
            break
        params["offset"] = offset

    print(f"[airtable] {len(existing)} URL(s) déjà présentes")
    return existing


def push_articles(articles: list[dict]) -> None:
    """Envoie une liste d'articles vers Airtable (max 10 par batch)."""
    # Airtable accepte max 10 records par requête POST
    for i in range(0, len(articles), 10):
        batch = articles[i:i+10]
        payload = {
            "records": [
                {
                    "fields": {
                        "Source URL": a["url"],
                    }
                }
                for a in batch
            ]
        }
        resp = requests.post(BASE_URL, headers=HEADERS_AT, json=payload, timeout=20)
        resp.raise_for_status()
        print(f"[airtable] {len(batch)} record(s) ajouté(s)")


def main():
    # 1. Scrape
    articles = scrape_news()

    # 2. URLs déjà dans Airtable
    existing_urls = get_existing_urls()

    # 3. Filtre : garde uniquement les nouveaux
    new_articles = [a for a in articles if a["url"] not in existing_urls]

    print(f"[main] {len(new_articles)} nouveau(x) article(s) à insérer "
          f"({len(articles) - len(new_articles)} déjà présent(s))")

    if not new_articles:
        print("[main] Rien à faire.")
        return

    # 4. Push
    push_articles(new_articles)
    print("[main] Terminé.")


if __name__ == "__main__":
    main()