---
name: slopcards-to-anki
description: Manages Anki flashcards via AnkiConnect - adds flashcards from CSV files, searches existing flashcards, and updates card content. Use when working with Anki flashcards, CSV imports, spaced repetition, or when user mentions Anki, flashcards, or flashcard management.
---

#  Re Markable Slopcards - Anki Flashcard Manager
Manages Anki flashcards using the main.py script via AnkiConnect.

## CSV Format

## Add flashcards from a CSV file
Import flashcards from a CSV file:
`main.py --f file_name.csv --deck_name "Deck Name"`

**CSV format required**:
- `front`: The question or prompt
- `back`: The answer or explanation

If the user doesn't specify a deck name, ask them which deck to use. Never assume the deck name.

## Searching for flashards
Find a flashcard by keyword:
`main.py --find_note "search term"`

Returns:
- CARD ID (needed for updates)
- Front text
- Back text

If multiple flashcards match, review the returned text to identify the correct flashcard.

## Updating cards

Update an existing flashcard using its ID::
- To update front: `main.py --update_note_by_id CARD_ID --new_front_text "Updated fresh new front text"`
- To update back: `main.py --update_note_by_id CARD_ID --new_back_text "Better back text"`
- To update both: include both `--new_front_text` and `--new_back_text` flags

To update both use:
```bash
main.py --update_note_by_id CARD_ID --new_front_text "New front" --new_back_text "New back"
```

**Workflow for enhancing an existing cards:**
1. Search for the flashcard: `main.py --find_note "keyword"`
2. Review existing back text
3. Generate improved back text with additional context, you may ask the user where to look for context
4. Update `main.py --update_note_by_id CARD_ID --new_back_text "Enhanced text with extra context"`

Ensure that the script runned correctly by checking the output. Notice the user of any output you see.

## Troubleshooting
Always notify the user of any error you encounter.

**If Anki is not running**
1. Run this exact command `main.py --anki_check`
2. Attempt auto-launch with this exact command: `main.py --try_launch_anki`
3. If auto-launch fails, notice the user and ask him to start Anki.

**If flashcard not found**
- Try broader search terms
- Check if card exists in the correct deck
- Ask the user for what to do

**On Windows:**
Use `python3 main.py` instead of `python main.py` if you encounter errors.