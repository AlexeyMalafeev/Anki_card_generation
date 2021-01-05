import os
import sys

import card_generation
import text_processing
import ui


# read texts
input_text = open(os.path.join('..', 'input.txt'), 'r', encoding='utf-8').read()
# non_empty_lines = [parag for line in input_text.split('\n') if (parag := line.strip())]

# print(get_sentences(input_text))
# card_generation.make_cards(input_text, prefix='UIMA')

ui.show_text_preview(input_text, 500)

prefix = ui.get_prefix()
sentences = text_processing.get_sentences(input_text)
sentences = ('', ) + sentences + ('', )
cards = []  # of tuples: (question_str, answer_str)
snippets_for_editing = []

for i, curr_snippet in enumerate(sentences[1:-1]):
    prev_snippet = sentences[i - 1]
    next_snippet = sentences[i + 1]

    ui.show_snippet(curr_snippet, prefix)

    done_with_snippet_menu = False
    go_to_next_snippet = True

    while True:
        choice = ui.menu(
            options=(
                'Cards',
                'Next',
                'Edit',
                'Join',
                'Split',
                'Prefix',
                'Save',
                'Save and exit',
                'Quit',
            ),
            keys='cnejspSEQ',
        )

        # todo I know this is ugly
        if choice == 'Cards':
            go_to_next_snippet = False
            done_with_snippet_menu = True

        elif choice == 'Next':
            done_with_snippet_menu = True

        elif choice == 'Edit':
            snippets_for_editing.append(curr_snippet)
            done_with_snippet_menu = True

        elif choice == 'Join':
            curr_snippet = ui.join_snippets(curr_snippet, prev_snippet, next_snippet)

        elif choice == 'Split':  # todo
            pass

        elif choice == 'Prefix':
            prefix = ui.get_prefix()

        elif choice == 'Save':
            save()

        elif choice == 'Save and exit':
            save()
            sys.exit()

        elif choice == 'Quit':
            sys.exit()


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





# card-level options:
# add card
# drop card
# manually edit later
# save and exit

# format output
# save results to file

