from pathlib import Path

from ankigenlib.anki_connect import sync
from ankigenlib.txt2anki import ankify, PARSE_MODES
from ankigenlib.ui import menu, yn

# todo document this in README.md
# todo add machine learning for question prediction (as entity)

parse_mode = menu(
    options=tuple(sorted(PARSE_MODES.keys())),
    title='Choose a parsing mode:',
)
input_path = Path('txt', f'{parse_mode}_input.txt')

target_deck = menu(
    options=('IT', 'Life'),
    title='Choose the target deck:',
)

try:
    ankify(
        input_path=input_path,
        parse_mode=parse_mode,
        target_deck=target_deck,
        ask_before_adding=True,
    )
except Exception as e:  # noqa
    print(e)
    print('Failed to generate notes/cards')

if yn(f'Purge the source file "{input_path}"?'):
    input_path.write_text('')

if yn('Sync Anki?'):
    sync()
