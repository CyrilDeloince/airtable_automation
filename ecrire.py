import os
import requests
from dotenv import load_dotenv

load_dotenv(r"C:\Users\CyrilDELOINCE\.env")

AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_TABLE   = os.environ["AIRTABLE_TABLE"]

# Écriture d'un record de test
resp = requests.post(
    f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}",
    headers={
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "fields": {
            "Source URL": "j'ecris dans une cellule"
        }
    },
    timeout=20,
)

print(resp.status_code)
print(resp.json())