import os
from pathlib import Path
import sys

import card_generation
import text_processing
import ui


class MainFlow:

    def __init__(self):
        input_text = Path('..', 'input.txt').read_text(encoding='utf-8')

        ui.show_text_preview(input_text, 500)

        self.prefix = ui.get_prefix()
        self.sentences = text_processing.get_sentences(input_text)
        self.sentences = ('',) + self.sentences + ('',)
        self.cards = []  # of tuples: (question_str, answer_str)
        self.snippets_for_editing = []

        self.curr_snippet = ''
        self.prev_snippet = ''
        self.next_snippet = ''

        self.run()

    def run(self):
        for i, curr_snippet in enumerate(self.sentences[1:-1]):
            self.curr_snippet = curr_snippet
            self.prev_snippet = self.sentences[i - 1]
            self.next_snippet = self.sentences[i + 1]

            snippet_control()

    def save(self, i):
        cards_path = Path('..', 'new_cards.txt')
        cards_lines = [f'{q}\t{a}' for q, a in self.cards]
        cards_text = '\n'.join(cards_lines)
        cards_path.write_text(cards_text, encoding='utf-8')

        editing_path = Path('..', 'snippets_for_editing.txt')
        editing_path.write_text('\n'.join(self.snippets_for_editing), encoding='utf-8')

        remaining_path = Path('..', 'input.txt')
        remaining_path.write_text('\n'.join(self.sentences[i:]), encoding='utf-8')

        print('Saved')

    def snippet_control(self):
        while True:
            ui.show_snippet(self.curr_snippet, self.prefix)

            done_with_snippet_menu = False
            go_to_next_snippet = True

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
                self.snippets_for_editing.append(self.curr_snippet)
                done_with_snippet_menu = True

            elif choice == 'Join':
                self.curr_snippet = ui.join_snippets(
                    curr_snippet=self.curr_snippet,
                    prev_snippet=self.prev_snippet,
                    next_snippet=self.next_snippet,
                )

            elif choice == 'Split':  # todo
                pass

            elif choice == 'Prefix':
                prefix = ui.get_prefix()

            elif choice == 'Save':
                self.save(i)

            elif choice == 'Save and exit':
                self.save(i)
                sys.exit()

            elif choice == 'Quit':
                sys.exit()

            if done_with_snippet_menu:
                break


    # sub_keywords = term_extraction.get_keywords(sent_stripped, min_freq=1)
    # sub_terms = term_extraction.get_terms(sent_stripped)
    # temp_cards = []
    # sent_stripped_lower = sent_stripped.lower()
    #
    # for keywords_or_terms, gap in (
    #         (sub_keywords, '_____'),
    #         (sub_terms, '_____(?)')
    # ):
    #     for keyword_or_term in keywords_or_terms:
    #         question = make_gap(
    #             text=sent_stripped,
    #             text_lower=sent_stripped_lower,
    #             target=keyword_or_term,
    #             gap=gap
    #         )
    #         temp_cards.append((f'{prefix} {question}', keyword_or_term))
    # for question, answer in temp_cards:
    #     print(question)
    #     print('-' * 50)
    #     print(answer)
    #
    #     if ui.yn('\nOk?2'):
    #         cards.append((question, answer))
    #     ui.cls()
    # return tuple(cards)





# card-level options:
# add card
# drop card
# manually edit later
# save and exit

# format output
# save results to file

