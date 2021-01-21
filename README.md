# Anki_card_generation

Semi-automatically generate Anki cards from arbitrary text using basic NLP techniques (spaCy) and statistical measures for keyword and term extraction.

Usage:

0. [Anki](https://apps.ankiweb.net/) desktop app must be installed and **running**, with installed add-on called [AnkiConnect](https://ankiweb.net/shared/info/2055492159)
1. Create file `input.txt` in the root directory
2. Paste into the file some text from which you want to generate cards
3. Run `main.py` and enjoy

Note: For now, generation is heavily tied to my 35 custom note types and a specific deck called "experimental", but with some tinkering, it is possible to change this behavior (PRs welcome ;) ). Maybe some time I will get around to implementing programmatic generation of the required note models.