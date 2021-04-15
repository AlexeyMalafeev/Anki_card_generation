import os
from pathlib import Path

from ankigenlib.txt2anki import ankify, PARSE_MODES
from ankigenlib.ui import menu, yn


parse_mode = menu(
    options=tuple(sorted(PARSE_MODES.keys())),
    title='Choose a parsing mode:',
)
input_path = Path('txt', f'{parse_mode}_input.txt')

ankify(
    input_path=input_path,
    parse_mode=parse_mode,
    target_deck='IT',
    ask_before_adding=True,
)

if yn(f'Purge the source file "{input_path}"?'):
    input_path.write_text('')
