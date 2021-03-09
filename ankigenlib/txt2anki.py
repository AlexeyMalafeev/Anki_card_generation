from ankigenlib import anki_connect
from ankigenlib import parsers


PARSE_MODES = {
    'tabs': parsers.TabSeparatedQA,
    'angle': parsers.AngleBracketsQA,
    'indent': parsers.IndentedQA,
}


def ankify(
        input_path: str,
        parse_mode: str,  # 'tabs' | 'angle' | 'indent'
        target_deck: str = '',
) -> list:
    parser_class = PARSE_MODES[parse_mode]
    parser = parser_class(input_path)
    notes = parser.parse()

    return anki_connect.make_notes(
        fields_nested=notes,
        deck_name=target_deck,
        print_notes=True,
        add_to_anki=True
    )
