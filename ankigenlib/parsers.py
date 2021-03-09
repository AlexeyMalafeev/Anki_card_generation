import re


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
        self.questions_to_add = []  # whatever is between angle brackets:
                                    # [(start, end, "word_or_phrase"), ...]

    def add_card(self):

        self.current_line = re.sub(r'<|>\d{0,2}', '', self.current_line)

    def add_card_condition(self):
        return self.current_line != ''

    def add_note(self):


    def add_note_condition(self):
        return self.current_line == ''

    def format_card(self):
        for start, end, target in self.questions_to_add:

        self.question, self.answer = self.current_line.split('\t')

    def preprocess_line(self):
        super().preprocess_line()
        if '<' in self.current_line:
            matches = re.finditer(r'<.+>\d{0,2}', self.current_line)
            self.questions_to_add = []
            for match in matches:
                start, end = match.span()
                target = self.current_line[start:end]
                q_clean =
                self.questions_to_add.append((start, end, target))
            self.questions_to_add.reverse()  # for adding cards in correct order

class IndentedQA(BaseParser):
    def add_card_condition(self):
        pass

    def add_note_condition(self):
        pass

    def format_card(self):
        pass
