import re


from ankigenlib import gap_making
from ankigenlib import text_processing


NOTE_SEP_FOR_ANGLE_BR_QA = '---'
PTRN_ANGLE_BRACKETS_CAPTURE = r'<.+?>'
PTRN_ANGLE_BRACKETS_CAPTURE_NUMBERED = r'\d{1,2}<.+?>'
PTRN_ANGLE_BRACKETS_REPLACE = r'\d{0,2}<|>'


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
        with open(self.path_to_input) as f_in:
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

    def add_card(self):
        self.cards.extend(self.cards_to_add)
        self.cards_to_add = []

    def add_card_condition(self):
        return '<' in self.current_line

    def add_note_condition(self):
        return self.current_line == NOTE_SEP_FOR_ANGLE_BR_QA

    def format_card(self):
        line = text_processing.format_line_for_question(self.current_line)
        matches = re.finditer(PTRN_ANGLE_BRACKETS_CAPTURE, line)
        matches_numbered = re.finditer(PTRN_ANGLE_BRACKETS_CAPTURE, line)
        for match in matches_numbered:
            pass  # todo handle numbered matches
        for match in matches:
            start, end = match.span()
            answer = line[start:end]
            answer = re.sub(PTRN_ANGLE_BRACKETS_REPLACE, '', answer)
            gap = gap_making.get_gap(answer)
            question = line[:start] + gap + line[end:]
            question = re.sub(PTRN_ANGLE_BRACKETS_REPLACE, '', question)
            # todo postprocess previous word before gap and a/an -> a(n)
            self.cards_to_add.extend([question, answer])


class IndentedQA(BaseParser):  # todo IndentedQA
    def add_card_condition(self):
        pass

    def add_note_condition(self):
        pass

    def format_card(self):
        pass
