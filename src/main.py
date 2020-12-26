import os

import card_generation
import ui


# read texts
input_text = open(os.path.join('..', 'input.txt'), 'r', encoding='utf-8').read()
# non_empty_lines = [parag for line in input_text.split('\n') if (parag := line.strip())]

# print(get_sentences(input_text))
# card_generation.make_cards(input_text, prefix='UIMA')

ui.show_text_preview(input_text, 500)

# set first prefix
# split into sentences (=snippets), iterate over them

# show snippet with prefix, then
# show snippet-level options:
# skip snippet
# edit snippet
# join snippets (previous, next)
# split snippet
# change prefix

# card-level options:
# add card
# drop card
# manually edit later

# format output
# save results to file


def process_text(text: str, prefix: str) -> tuple:
    """Make cards from text. Split into sentences first. Add prefix.
    Return tuple of (question, answer) cards."""
    if not prefix.endswith(':'):
        prefix += ':'
    cards = []
    doc = nlp(text)
    for sent in doc.sents:
        if not (sent_stripped := sent.text.strip()):
            continue
        sub_keywords = term_extraction.get_keywords(sent_stripped, min_freq=1)
        sub_terms = term_extraction.get_terms(sent_stripped)
        temp_cards = []
        sent_stripped_lower = sent_stripped.lower()
        for keywords_or_terms, gap in (
                (sub_keywords, '_____'),
                (sub_terms, '_____(?)')
        ):
            for keyword_or_term in keywords_or_terms:
                question = make_gap(
                    text=sent_stripped,
                    text_lower=sent_stripped_lower,
                    target=keyword_or_term,
                    gap=gap
                )
                temp_cards.append((f'{prefix} {question}', keyword_or_term))
        for question, answer in temp_cards:
            print(question)
            print('-' * 50)
            print(answer)

            if ui.yn('\nOk?2'):
                cards.append((question, answer))
            ui.cls()
    return tuple(cards)
