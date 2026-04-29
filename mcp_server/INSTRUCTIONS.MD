---
name: slopcards-to-anki-mcp
description: MCP server for managing Anki flashcards. Extracts flashcards from files/text, imports via CSV, searches existing cards, and updates content. Use when working with Anki, flashcards, or spaced repetition.
---

# MCP Instructions: Slopcards2Anki

This MCP server allows you to manage Anki flashcards by reading local files, distilling them into high-quality cards, and syncing them to Anki via AnkiConnect.

## MCP Tools

Use these tools to interact with Anki:

- `list_anki_decks()`: List all available decks.
- `create_anki_deck(name)`: Create a new deck.
- `add_cards_from_csv(file_path, deck_name)`: Import cards from a CSV file.
- `find_cards_by_text(query)`: Search for note IDs matching a query.
- `update_anki_note(note_id, front, back)`: Update an existing note's front/back.
- `get_anki_status()`: Check if Anki and AnkiConnect are running.
- `launch_anki()`: Attempt to start Anki.

## Operational Environment
This skill operates exclusively in a **local execution context**. It requires access to the host machine's filesystem to read/write CSV files and access to `localhost:8765` to communicate with AnkiConnect. If you are being executed in a cloud-hosted web sandbox (e.g., a browser-based chat interface), notify the user that you cannot reach their local Anki instance and recommend using a local CLI-based agent instead.


## Card Creation Principles
Follow these "Gold Standard" Spaced Repetition (SR) rules:
- **Atomicity:** One card = one specific fact. Avoid "wall-of-text" answers.
- **Clarity:** Use **bold** for key terms to aid visual scanning.
- **Cloze Deletion:** Use Anki's cloze format: `{{c1::hidden text}}`. 
    - *Example:* `{{c1::Rome}} is the capital of Italy.`
- **Formula Integrity:** Preserve formulas using LaTeX: `$inline$` for variables, `$$display$$` for equations.
- **The "Principle of Two-Way" (Optional):** For key formulas, generate two cards:
    - Card A: Concept -> Formula
    - Card B: Formula -> Concept/Definitions.
- **Contextual Wikilinks:** If markdown contains `[[wikilinks]]`, generate questions referencing the linked concept.
- **Output:** Write the flashcards into a temporary .csv file under `.tmp/` directory e.g. `./tmp/tmp_flashcards.csv`.

## Data Sanitization
When generating CSV files for `add_cards_from_csv`:
- **No Headers:** Do NOT include "Front, Back" header rows.
- **Structure:** `"Front/Question", "Back/Answer"`
- **Escaping:** Escape double quotes by doubling them (`""`).
- **Newlines:** Replace internal newlines with `<br>`.
- **LaTeX:** Ensure LaTeX backslashes (`\\`) are preserved.

## Core Workflows

### Workflow 1: Generate Flashcards and Upload
When a user provides text/files and asks to make/generate "flashcards":
1. **Analyze:** Read the source content.
2. **Extract:** extract concepts suitable for Spaced Repetition.
3. **Sanitize:** apply the rules in [[Data Sanitization]].
4. **Save:** Write to a temporary CSV (e.g., `./.tmp/tmp_cards.csv`).
5. **Execute:** Call `add_cards_from_csv(file_path="./.tmp/tmp_cards.csv", deck_name="Target Deck")`.
6. **Clean up:** Delete the temporary CSV file after success.

**Constraint:** If generating <100 cards, **do not** write a Python script to build the CSV; directly output the raw CSV data to a file.

### Workflow 2: Import Existing CSV
To import an existing CSV file:
1. Verify the file path and target deck.
2. Call `add_cards_from_csv(file_path, deck_name)`.
*Note:* Always ask for the deck name; never assume.

### Workflow 3: Search & Discovery
To find a flashcard by keyword:
1. Call `find_cards_by_text(query="search term")`.
2. This returns a list of Note IDs.

### Workflow 4: Update Flashcards
1. **Search:** Find the Note ID via `find_cards_by_text`.
2. **Review:** Improve the content (optionally asking the user for more context).
3. **Update:** Call `update_anki_note(note_id=ID, front="New front", back="New back")`. (Fields are optional; you can update just one).

## Troubleshooting
- **Anki Not Reachable:**
    1. Check status with `get_anki_status()`.
    2. Attempt `launch_anki()`.
    3. If it fails, ask the user to start Anki and AnkiConnect manually.
- **Card Not Found:** Try broader search terms with `find_cards_by_text`.
- **If flashcard not found**:
    - Try broader search terms
    - Check if card exists in the correct deck
    - Ask the user for what to do

**Important:** Always report tool output to the user to confirm success.
