from collections import defaultdict
import re


from ankigenlib import gap_making


NOTE_SEP_FOR_ANGLE_BR_QA = '---'
PTRN_ANGLE_BRACKETS = r'\w?<.+?>'


class BaseParser:
    """Single use only"""
    def __init__(self, path_to_input):
        self.path_to_input: str = ''
        self.path_to_input = path_to_input
        self.notes: list = []  # nested: [(q1, a1, q2, a2, ...), (q1, a1, q2, a2, ...), ...]
        self.cards: list = []  # flat: [question1, answer1, question2, answer2, ...]
        self.current_line: str = ''
        self.question: str = ''
        self.answer: str = ''

    def add_card(self):
        self.cards.extend([self.question, self.answer])
        self.question = self.answer = ''

    def add_card_condition(self):
        raise NotImplementedError

    def add_note(self):
        self.notes.append(tuple(self.cards))
        self.cards = []

    def add_note_condition(self):
        raise NotImplementedError

    def after_parse(self):
        if self.cards:
            self.add_note()

    def before_parse(self):
        pass

    def format_card(self):
        raise NotImplementedError

    def parse(self) -> tuple:
        self.before_parse()
        with open(self.path_to_input, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                self.current_line = line
                self.preprocess_line()
                if self.add_card_condition():
                    self.format_card()
                    self.add_card()
                elif self.add_note_condition():
                    self.add_note()
        self.after_parse()
        return tuple(self.notes)

    def preprocess_line(self):
        self.current_line = self.current_line.strip()


class TabSeparatedQA(BaseParser):
    def add_card_condition(self):
        return self.current_line != ''

    def add_note_condition(self):
        return self.current_line == ''

    def format_card(self):
        self.question, self.answer = self.current_line.split('\t')


class AngleBracketsQA(BaseParser):
    def __init__(self, path_to_input):
        super().__init__(path_to_input)
        self.cards_to_add = []  # [q1, a1, q2, a2, q3, a3, ...]
        self.normal_spans = []
        self.numbered_spans = defaultdict(list)
        self.clean_line = ''

    def add_card(self):
        self.cards.extend(self.cards_to_add)
        self.cards_to_add = []

    def add_card_condition(self):
        return '<' in self.current_line

    def add_note_condition(self):
        return self.current_line == NOTE_SEP_FOR_ANGLE_BR_QA

    def format_card(self):
        self.current_line = self.format_line_for_question(self.current_line)
        self.find_spans()
        self.make_gaps()

    def find_spans(self):
        self.numbered_spans = defaultdict(list)
        self.normal_spans = []
        line = self.current_line
        self.clean_line = ''
        matches = re.finditer(PTRN_ANGLE_BRACKETS, line)
        offset = 0
        prev_end = 0
        for m in matches:
            start, end = m.span()
            self.clean_line += line[prev_end:start]
            m_text = line[start:end]
            if m_text.startswith('<'):
                diff = 2
                target_list = self.normal_spans
            else:
                diff = 3
                m_id = m_text[0]
                target_list = self.numbered_spans[m_id]
            target_list.append((start - offset, end - offset - diff))
            self.clean_line += m_text[diff - 1:-1]
            offset += diff
            prev_end = end
        self.clean_line += line[prev_end:]

    # low-prio todo move format_line_for_question to another module, it's general
    @staticmethod
    def format_line_for_question(line: str) -> str:
        line_words = line.split()
        first_word = line_words[0]
        last_word = line_words[-1]
        # if first_word.isalpha() and first_word.istitle():
        #     first_word = first_word.lower()
        if last_word.endswith('.'):
            last_word = last_word[:-1]
        line = ' '.join([first_word] + line_words[1:-1] + [last_word])
        return line

    def make_gaps(self):
        for span in self.normal_spans:
            question, answer = gap_making.make_gaps_by_spans(self.clean_line, span)
            self.cards_to_add.extend([question, answer])
        for m_id, spans in self.numbered_spans.items():
            question, answer = gap_making.make_gaps_by_spans(self.clean_line, *spans)
            self.cards_to_add.extend([question, answer])


class IndentedQA(BaseParser):  # todo IndentedQA
    def add_card_condition(self):
        pass

    def add_note_condition(self):
        pass

    def format_card(self):
        pass
