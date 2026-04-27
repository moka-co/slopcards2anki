# 🗃️ Slopcards to Anki
![Python](https://img.shields.io/badge/python-blue)
![License](https://img.shields.io/badge/license-AGPL%20v3.0-blue)
![Anki](https://img.shields.io/badge/Anki-Compatible-blue)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)

`slopcards-to-anki` gives Claude/Gemini the ability to transform your **local markdown notes** into high-retention flashcards. It automatically uploads and syncs them to your local Anki profile. Perfect for **Obsidian** users.

## 🚀Features
- **Automatic Upload & Sync**: automatically breaks down complex notes into single-fact "atmoic" cards for maximum retention
- **LaTeX Support & STEM Ready**: Full support for inline `$math$` and block `$$math$$` notation, preserved perfectly for Anki's rendering engine
- **Smart Cloze Deletion**: Identifies definitions and sequences to generate cloze card dynamically

> [!IMPORTANT]
> This is a **local AI skill**. It is designed to run in environments where the AI has access to your local machine:
> - ✅ Supported: Claude Code, Gemini CLI, Aider, or **any local LLM agent with shell access**.
> - ❌ Not Supported: Standard web interfaces (claude.ai, gemini.google.com, chatgPT.com). These browser-based tools cannot communicate with your local Anki installation.


## 🛠️ Quick Start
### 1. Prerequisites
- [Anki](https://apps.ankiweb.net/) must be installed and running
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) Add on: Install code `2055492159` in anki (Tools > Add-ons > Get Add-ons)

### 2. Installation
Clone this repository into your AI tool's designed skills directory (e.g., `~/.skills/` or within your project root)

```bash
git clone https://github.com/moka-co/slopcards2anki.git
```

### 3. Usage
Once the skill is registered with your AI CLI (Claude Code, Gemini CLI, etc.), you can use **natural language** to manage your deck.

**Example Prompts**:
- "Convert my 'Calculus_Notes.md' into 30 atomic flashcards using slopcards-to-anki"
- "Find the Anki card about "Photosynthetis" and update the back with more detail from this paragraph."


## 🏗️ How it works
1. The AI (e.g. Claude Code / Gemini CLI) analyzes your text and identifies high-value concepts
2. Then the AI calls a python interface that sanitizes data and pushes the cards into your local Anki profile

## ⚠️ Scope & Roadmap
- **Text & Math Focused**: currently optimized for text and LaTeX formulas.
- **Media Support**: Image and audio uploads are not currently supported (help is appreciated).
- **Format**: It has been tested with Markdown files, but it works with any file format that AI is capable of reading. However to get better result you may first want to use tools like [markitdown](https://github.com/microsoft/markitdown)


## 🛠 Troubleshooting