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
        self.i = 0

        self.main_loop()

    def card_control(self):
        # todo manually edit later
        # todo save and exit
        temp_cards = card_generation.make_candidate_cards(self.curr_snippet, self.prefix)
        for question, answer in temp_cards:
            if ui.add_card_or_not(question, answer):
                self.cards.append((question, answer))

    def main_loop(self):
        for self.i, self.curr_snippet in enumerate(self.sentences[1:-1]):
            self.prev_snippet = self.sentences[self.i - 1]
            self.next_snippet = self.sentences[self.i + 1]

            use_snippet = self.snippet_control()

            if use_snippet:
                self.card_control()

    def save(self):
        cards_path = Path('..', 'new_cards.txt')
        cards_lines = [f'{q}\t{a}' for q, a in self.cards]
        cards_text = '\n'.join(cards_lines)
        cards_path.write_text(cards_text, encoding='utf-8')

        editing_path = Path('..', 'snippets_for_editing.txt')
        editing_path.write_text('\n'.join(self.snippets_for_editing), encoding='utf-8')

        remaining_path = Path('..', 'input.txt')
        remaining_path.write_text('\n'.join(self.sentences[self.i:]), encoding='utf-8')

        print('Saved')

    def snippet_control(self):
        while True:
            ui.show_snippet(self.curr_snippet, self.prefix)
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
                return True

            elif choice == 'Next':
                return False

            elif choice == 'Edit':
                self.snippets_for_editing.append(self.curr_snippet)
                return False

            elif choice == 'Join':
                self.curr_snippet = ui.join_snippets(
                    curr_snippet=self.curr_snippet,
                    prev_snippet=self.prev_snippet,
                    next_snippet=self.next_snippet,
                )

            elif choice == 'Split':  # todo
                pass

            elif choice == 'Prefix':
                self.prefix = ui.get_prefix()

            elif choice == 'Save':
                self.save()

            elif choice == 'Save and exit':
                self.save()
                sys.exit()

            elif choice == 'Quit':
                sys.exit()
