import requests
import json 
import re
import logging

ENDPOINT="http://127.0.0.1:8765" # AnkiConnect works only locally

logger = logging.getLogger(__name__)

# Get cards id by specifying a deck name
def get_cards_id_by_deckname(deck_name : str):
    payload= {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'deck:"{deck_name}"'
        }
    }

    try: 
        response = requests.post(endpoint, json=payload)
    except Exception as e:
        logger.error(f"Failed to get cards id by deckaname: {e}")
   
    body = response.json()
    return body['result']

# Get cards id by specifying a query 
# e.e. if the query is "*" then it will return every note 
# e.g. if the query is 'deck: "Test Deck"' it will return every note id from that deck
#TODO: add a query sanitizer 
def get_cards_id_by_query(query : str):
    payload= {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": f'"{query}"'
        }
    }

    try: 
        response = requests.post(endpoint, json=payload)
    except Exception as e:
        logger.error(f"Failed to get cards id by query: {e}")

    body = response.json()
    return body['result']

# Get notes info i.e. content, tags etc... by specifying a list of note ids
def get_notes_info_by_id(note_ids : list):
    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    }

    try:
        response = requests.post(endpoint, json=payload)
    except Exception as e:
        logger.error(f"Failed to get notes info by id: {e}")

    body= response.json()
    return body['result']


# Add a note to an Anki Deck 
# You need to specify: a deck name (that must exists), a model name (that must be allowed), a front content and back content
def add_note(deck_name, model_name, front_content, back_content):
    #print(f"Deck Name: {deck_name}\n Model Name: {model_name}\n Front Content: {front_content}\n Back Content: {back_content}")

    front_content = fix_formatting(front_content)
    back_content = fix_formatting(back_content)

    payload_builder = NoteBuilder().deck(deck_name)
    if model_name == "Cloze":
        payload_builder= payload_builder.cloze(front_content,back_content)
    else:
        payload_builder = payload_builder.basic(front_content,back_content)

    payload = payload_builder.build()

    try:
        response = requests.post(ENDPOINT, json=payload) # Make request
    except Exception as e:
        logger.error(f"Failed to add note (model: {model_name}) to deck {deck_name}\n Front Content: {front_content}\n Back Content: {back_content}\nError: {e}")
    
    body=response.json()
    

# Read a CSV file and add each note to the specified deck
def add_notes_from_csv_file(file_name, deck_name):
    model_name="Cloze" # By default gemini generates flashcards with cloze
    with open(file_name, newline="") as f:
        reader = csv.reader(f)
        
        # Iterate over each row in the file
        for row in reader:
            front_content = row[0]
            back_content = row[1]

            # Dynamically adapt the model_name
            pattern = r"c1::*"
            if not re.search(pattern, front_content):
                model_name = "Basic"
            else: 
                model_name = "Cloze"

            # Add note 
            add_note(
                deck_name,
                model_name,
                front_content,
                back_content
            )


# Update note by specifying an id
# Optional arguments: 
# - front and back content (that also works for cloze and other notes)
# - list of tags
def update_note(note_id: int, front: str = None, back: str = None, tags: list = None):
    # Construct the fields dynamically based on what is provided
    fields = {}
    if front:
        fields["Text"] = front
    if back:
        fields["Back Extra"] = back

    payload = {
        "action": "updateNote",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": fields
            }
        }
    }
    
    if tags:
        payload["params"]["note"]["tags"] = tags

    try:
        response = requests.post(endpoint, json=payload)
    except Exception as e:
        logger.error(f"Failed to update note with id {note_id}\n Error: {e}")
    
    return response.json()