from pathlib import Path
from pprint import pp


from ankigenlib import anki_connect
from ankigenlib import parsers
from ankigenlib import ui


PARSE_MODES = {
    'tabs': parsers.TabSeparatedQA,
    'angle': parsers.AngleBracketsQA,
    'indent': parsers.IndentedQA,
}


def ankify(
        input_path: Path,
        parse_mode: str,  # 'tabs' | 'angle' | 'indent'
        target_deck: str = '',
        ask_before_adding: bool = False,
) -> list:
    parser_class = PARSE_MODES[parse_mode]
    parser = parser_class(input_path)
    notes = parser.parse()

    if ask_before_adding:
        pp(notes)  # todo better preview of notes
        n_notes = len(notes)
        n_cards = sum(len(n) for n in notes) // 2
        hint = f'\nAdd these {n_cards} cards as {n_notes} notes to {target_deck}?'
    else:
        hint = ''

    if not ask_before_adding or ui.yn(hint):
        return anki_connect.make_notes(
            fields_nested=notes,
            deck_name=target_deck,
            print_notes=True,
            add_to_anki=True
        )
