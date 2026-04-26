import os
import requests
from dotenv import load_dotenv


#load data for airtable from a .env file  
load_dotenv(r"C:\Users\CyrilDELOINCE\.env")


#set token credentials for aitable
AIRTABLE_API_KEY = os.environ["AIRTABLE_API_KEY"]
AIRTABLE_BASE_ID = os.environ["AIRTABLE_BASE_ID"]
AIRTABLE_TABLE   = os.environ["AIRTABLE_TABLE"]


#connecting to airtable thanks to those credentials 
resp = requests.get(
    f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}",
    headers={"Authorization": f"Bearer {AIRTABLE_API_KEY}"},
    params={"fields[]": "Source URL", "pageSize": 5},
    timeout=20,
)


#if it fails, it's normally because you did not put well your credentials, thhat will say to you what's the pb 
print(resp.json())  


#just testing to take some links from airtable to see if it is well connected
for record in resp.json().get("records", []):
    print(record.get("fields", {}).get("Source URL", "—"))