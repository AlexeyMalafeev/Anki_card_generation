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
        self.last_added = []  # of tuples: (question_str, answer_str)
        self.snippets_for_editing = []

        self.curr_snippet = ''
        self.prev_snippet = ''
        self.next_snippet = ''
        self.i = 0

        self.main_loop()

    def add_manually(self):
        ui.show_snippet(self.curr_snippet, self.prefix)
        snippet_lower = self.curr_snippet.lower()
        while True:
            target = input('Input target word or phrase: ').lower()
            if target in snippet_lower:
                break
        gap = card_generation.PHRASE_GAP if ' ' in target else card_generation.WORD_GAP
        question = card_generation.make_gap(
            text=self.curr_snippet,
            text_lower=snippet_lower,
            target=target,
            gap=gap
        )
        answer = target
        if ui.add_card_or_not(question, answer):
            self.last_added.append((f'{self.prefix} {question}', answer))

    def cards_control(self):
        # really big todo: distribute cards by multiple files 3q3a, 8q8a etc., use tabs
        # todo add snippet to manually edit late
        # todo save and exit
        temp_cards = card_generation.make_candidate_cards(self.curr_snippet, self.prefix)
        self.last_added = []
        for question, answer in temp_cards:
            if ui.add_card_or_not(question, answer):
                self.last_added.append((question, answer))
        while True:
            ui.cls()
            cards_preview = '\n'.join(
                (f'{i}. {q} -> {a}' for i, (q, a) in enumerate(self.last_added))
            )
            print(cards_preview)
            choice = ui.menu(
                options=(
                    'Add manually',
                    'Delete',
                    'Next snippet',
                ),
                keys='adn',
            )
            if choice == 'Add manually':
                self.add_manually()
            elif choice == 'Delete':
                self.delete_card_by_idx()
            elif choice == 'Next snippet':
                break
        for card in self.last_added:
            self.cards.append(card)

    def clean_snippet(self):
        self.curr_snippet = self.curr_snippet.replace('\t', ' ')
        self.curr_snippet = self.curr_snippet.replace('\n', '<br>')

    def delete_card_by_idx(self):
        idx = ui.get_int(0, len(self.last_added) - 1)
        print(f'Delete this?\n{self.last_added[idx]}')
        if ui.yn('Please confirm:'):
            self.last_added = self.last_added[:idx] + self.last_added[idx + 1:]

    def join_snippets(self):
        self.prev_snippet, self.curr_snippet, self.next_snippet = ui.join_snippets(
            curr_snippet=self.curr_snippet,
            prev_snippet=self.prev_snippet,
            next_snippet=self.next_snippet,
        )
        if not self.prev_snippet:
            self.sentences = (self.sentences[:max(self.i - 1, 1)] +
                              [self.curr_snippet] +
                              self.sentences[self.i + 1:])
        if not self.next_snippet:
            self.sentences = (self.sentences[:self.i] +
                              [self.curr_snippet] +
                              self.sentences[min(self.i + 2, len(self.sentences) - 1):])

    def main_loop(self):
        self.i = 1
        while True:
            self.curr_snippet = self.sentences[self.i]
            self.prev_snippet = self.sentences[self.i - 1]
            self.next_snippet = self.sentences[self.i + 1]

            use_snippet = self.snippet_control()

            if use_snippet:
                self.clean_snippet()
                self.cards_control()
                self.i += 1
                if self.i == len(self.sentences):
                    break
        self.save()
        print('All done')

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

            if choice == 'Cards':
                return True

            elif choice == 'Next':
                return False

            elif choice == 'Edit':
                self.snippets_for_editing.append(self.curr_snippet)
                return False

            elif choice == 'Join':
                self.join_snippets()

            elif choice == 'Split':  # todo
                self.split_snippets()

            elif choice == 'Prefix':
                self.prefix = ui.get_prefix()

            elif choice == 'Save':
                self.save()

            elif choice == 'Save and exit':
                self.save()
                sys.exit()

            elif choice == 'Quit':
                sys.exit()

    def split_snippets(self):
        first, second = ui.split_snippets(self.curr_snippet, self.prefix)
        if second:
            self.curr_snippet = first
            self.next_snippet = second
            self.sentences = (self.sentences[:self.i] +
                              [self.curr_snippet, self.next_snippet] +
                              self.sentences[self.i + 1:])


MainFlow()
