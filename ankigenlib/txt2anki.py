from ankigenlib import anki_connect
from ankigenlib import setup


def ankify(
        input_txt_file_name: str,
        target_deck: str = '',
) -> list:
    notes = []
    cards = []

    def _add_note():
        notes.append(tuple(cards))

    with open(input_txt_file_name, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            line = line.strip()
            if not line and cards:
                _add_note()
                cards = []
                continue
            new_card = line.split('\t')
            cards.extend(new_card)  # flat: [q_1, a_1, q_2, a_2, ...]
        else:
            if cards:
                _add_note()

    notes = tuple(notes)
    if not target_deck:
        target_deck = setup.config['target deck']
        if target_deck is None:
            target_deck = input('target deck? ')

    return anki_connect.make_notes(
        fields_nested=notes,
        deck_name=target_deck,
        print_notes=True,
        add_to_anki=True
    )
