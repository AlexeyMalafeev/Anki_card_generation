import os

from ankigenlib.txt2anki import ankify, PARSE_MODES
from ankigenlib.ui import menu


parse_mode = menu(
    options=tuple(sorted(PARSE_MODES.keys())),
    title='Choose a parsing mode:',
)
input_path = os.path.join('txt', f'{parse_mode}_input.txt')

ankify(
    input_path=input_path,
    parse_mode=parse_mode,
    target_deck='IT',
    ask_before_adding=True,
)
