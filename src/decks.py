import requests 
import logging 

logger = logging.getLogger(__name__)

# Connect to AnkiConnect API and return all Deck Names
def get_deck_names_and_ids() -> str:
    payload = {
        "action": "deckNamesAndIds",
        "version": 6,
    }

    response = requests.post(endpoint, json=payload)
    if response.status_code: #OK
        body = response.json()
        result = body["result"]
        return result
    else:
        print(f"Request returned status code {response.status_code}")