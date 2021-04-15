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
        input_path: str,
        parse_mode: str,  # 'tabs' | 'angle' | 'indent'
        target_deck: str = '',
        ask_before_adding: bool = False,
) -> list:
    parser_class = PARSE_MODES[parse_mode]
    parser = parser_class(input_path)
    notes = parser.parse()

    if ask_before_adding:
        pp(notes)

    if not ask_before_adding or ui.yn(f'\nAdd these {len(notes)} notes to {target_deck}?'):
        return anki_connect.make_notes(
            fields_nested=notes,
            deck_name=target_deck,
            print_notes=True,
            add_to_anki=True
        )
