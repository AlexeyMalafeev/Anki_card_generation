from pathlib import Path
import sys

import anki_connect
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
        self.notes = []
        self.current_note = []
        self.last_added = []  # of tuples: (question_str, answer_str)

        self.curr_snippet = ''
        self.prev_snippet = ''
        self.next_snippet = ''
        self.i = 0

        self.cards_path = Path('..', 'new_cards.txt')
        backup_text = self.cards_path.read_text(encoding='utf-8')
        self.backup_path = Path('..', 'new_cards_backup.txt')
        self.backup_path.write_text(backup_text, encoding='utf-8')
        self.cards_path.write_text('', encoding='utf-8')
        self.remaining_path = Path('..', 'input.txt')

        self.main_loop()

    def add_manually(self):
        ui.show_snippet(self.curr_snippet, self.prefix)
        snippet_lower = self.curr_snippet.lower()
        while True:
            target = input('Input target word or phrase: ').lower()
            if target in snippet_lower:
                break
        gap = card_generation.PHRASE_GAP if ' ' in target else card_generation.WORD_GAP
        question, orig_answer = card_generation.make_gap(
            text=self.curr_snippet,
            text_lower=snippet_lower,
            target=target,
            gap=gap
        )
        if ui.add_card_or_not(question, orig_answer):
            self.last_added.append((f'{self.prefix}{question}', orig_answer))

    def auto_save(self):
        self._save(send_to_anki=False, show_message=False)

    def cards_control(self):
        # low-priority todo save and exit
        temp_cards = card_generation.make_candidate_cards(self.curr_snippet, self.prefix)
        self.last_added = []
        for question, answer in temp_cards:
            if ui.add_card_or_not(question, answer):
                self.last_added.append((question, answer))
        while True:
            ui.cls()
            self.last_added.sort()
            cards_preview = '\n'.join(
                (f'{i}. {q} -> {a}' for i, (q, a) in enumerate(self.last_added))
            )
            print(cards_preview, '\n')
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
        for question, answer in self.last_added:
            question_cleaned = text_processing.clean_text_for_anki_import(question)
            self.cards.append((question_cleaned, answer))
            self.current_note.extend([question, answer])

    def delete_card_by_idx(self):
        idx = ui.get_int(0, len(self.last_added) - 1)
        print(f'Delete this?\n{self.last_added[idx]}')
        if ui.yn('Please confirm:'):
            self.last_added = self.last_added[:idx] + self.last_added[idx + 1:]

    def edit_snippet(self):
        new_snippet = ui.get_edited_snippet(self.curr_snippet, self.prefix)
        self.sentences = (self.sentences[:self.i] + (new_snippet, ) + self.sentences[self.i + 1:])
        self.set_snippets()

    def join_snippets(self):
        self.prev_snippet, self.curr_snippet, self.next_snippet = ui.join_snippets(
            curr_snippet=self.curr_snippet,
            prev_snippet=self.prev_snippet,
            next_snippet=self.next_snippet,
        )
        if not self.prev_snippet:
            self.sentences = (self.sentences[:max(self.i - 1, 1)] +
                              (self.curr_snippet, ) +
                              self.sentences[self.i + 1:])
            self.set_snippets()
        if not self.next_snippet:
            self.sentences = (self.sentences[:self.i] +
                              (self.curr_snippet, ) +
                              self.sentences[min(self.i + 2, len(self.sentences) - 1):])
            self.set_snippets()

    def main_loop(self):
        format_func = text_processing.format_snippet_for_anki
        self.i = 1
        while True:
            self.curr_snippet = format_func(self.sentences[self.i])
            self.prev_snippet = format_func(self.sentences[self.i - 1])
            try:
                self.next_snippet = format_func(self.sentences[self.i + 1])
            except IndexError:
                break

            use_snippet = self.snippet_control()

            if use_snippet:
                self.cards_control()
            if self.i == len(self.sentences):
                break
            self.auto_save()
        self.save()
        print('All done')

    def _save(
            self,
            send_to_anki: bool,
            show_message: bool,
    ):
        if send_to_anki:
            if self.current_note:
                self.notes.append(tuple(self.current_note))
                self.current_note = []
            if self.notes:
                anki_connect.make_notes(
                    tuple(self.notes),
                    deck_name='experimental',
                    print_notes=True,
                    add_to_anki=True,
                )
                self.notes = []

        cards_lines = [f'{q}\t{a}' for q, a in self.cards]
        cards_text = '\n'.join(cards_lines) + '\n'
        with open(self.cards_path, 'a', encoding='utf-8') as cards_out:
            cards_out.write(cards_text)
        self.cards = []

        remaining_text = '\n'.join(self.sentences[self.i:]) + '\n'
        with open(self.remaining_path, 'w', encoding='utf-8') as remaining_out:
            remaining_out.write(remaining_text)

        if show_message:
            print('Saved')

    def save(self):
        self._save(send_to_anki=True, show_message=True)

    def set_snippets(self):
        """setting next_snippet may cause IndexError, needs to be handled outside"""
        format_func = text_processing.format_snippet_for_anki
        self.curr_snippet = format_func(self.sentences[self.i])
        self.prev_snippet = format_func(self.sentences[self.i - 1])
        self.next_snippet = format_func(self.sentences[self.i + 1])

    def snippet_control(self):
        while True:
            ui.show_snippet(self.curr_snippet, self.prefix)
            new_note_text = f'New note (current: {len(self.current_note) // 2} cards)'
            choice = ui.menu(
                options=(
                    'Cards',
                    new_note_text,
                    'Next',
                    'Edit',
                    'Join',
                    'Split',
                    'Prefix',
                    'Save',
                    'Save and exit',
                    'Quit',
                ),
                keys='cNnejspSEQ',
            )

            if choice == 'Cards':
                self.i += 1
                return True

            elif choice == new_note_text:
                self.notes.append(tuple(self.current_note))
                self.current_note = []

            elif choice == 'Next':
                self.i += 1
                return False

            elif choice == 'Edit':
                self.edit_snippet()

            elif choice == 'Join':
                self.join_snippets()

            elif choice == 'Split':
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
            self.sentences = (self.sentences[:self.i] +
                              (self.curr_snippet, self.next_snippet) +
                              self.sentences[self.i + 1:])
            self.set_snippets()


MainFlow()
