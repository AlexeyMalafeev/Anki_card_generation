from collections import defaultdict
import re


from ankigenlib import gap_making


NOTE_SEP_FOR_ANGLE_BR_QA = '---'
PTRN_ANGLE_BRACKETS_CAPTURE = r'<.+?>'
PTRN_ANGLE_BRACKETS_CAPTURE_NUMBERED = r'\d{1,2}<.+?>'
PTRN_ANGLE_BRACKETS_REPLACE = r'<|>'
PTRN_ANGLE_BRACKETS_NUMBERED_REPLACE = r'\d{1,2}<|>'
PTRN_ANGLE_BRACKETS_NUMBERED_LEFT1_REPLACE = r'\d<'
PTRN_ANGLE_BRACKETS_NUMBERED_LEFT2_REPLACE = r'\d\d<'
PTRN_ANGLE_BRACKETS_CATCHALL_REPLACE = r'\d{0,2}<|>'


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
        # todo refactor AngleBracketsQA.format_card
        line = self.format_line_for_question(self.current_line)
        matches_numbered = re.finditer(PTRN_ANGLE_BRACKETS_CAPTURE_NUMBERED, line)
        matchnum_dict = defaultdict(list)
        for matchnum in matches_numbered:
            start, end = matchnum.span()
            m_text = line[start:end]
            digits = re.findall(r'\d+', m_text)[0]
            matchnum_dict[digits].append(matchnum)
        # line_with_spaces = line
        for digit, matchnums in matchnum_dict.items():
            question = line
            prev_answer = ''
            answers = []
            for matchnum in reversed(matchnums):
                start, end = matchnum.span()
                answer = question[start:end]
                # answer_with_spaces = re.sub(PTRN_ANGLE_BRACKETS_NUMBERED_REPLACE, ' ', answer)
                # line_with_spaces = line[:start] + answer_with_spaces + line[end:]
                answer = re.sub(PTRN_ANGLE_BRACKETS_NUMBERED_REPLACE, '', answer)
                if answer != prev_answer:
                    answers.append(answer)
                    prev_answer = answer
                gap = gap_making.get_gap(answers[-1])
                question = question[:start] + gap + question[end:]
            answer = '<br>'.join(reversed(answers))
            question = re.sub(PTRN_ANGLE_BRACKETS_CATCHALL_REPLACE, '', question)
            question = gap_making.auto_a_before_gap(question)
            self.cards_to_add.extend([question, answer])
        line = re.sub(PTRN_ANGLE_BRACKETS_NUMBERED_LEFT2_REPLACE, '  ', line)
        line = re.sub(PTRN_ANGLE_BRACKETS_NUMBERED_LEFT1_REPLACE, ' ', line)
        matches = re.finditer(PTRN_ANGLE_BRACKETS_CAPTURE, line)
        for match in matches:
            start, end = match.span()
            answer = line[start:end]
            answer = re.sub(PTRN_ANGLE_BRACKETS_REPLACE, '', answer)
            gap = gap_making.get_gap(answer)
            question = line[:start] + gap + line[end:]
            question = re.sub(PTRN_ANGLE_BRACKETS_REPLACE, '', question)
            question = re.sub(' {2,}', ' ', question)
            # question = gap_making.auto_a_before_gap(question)
            self.cards_to_add.extend([question, answer])

    # low-prio todo move format_line_for_question to another module
    @staticmethod
    def format_line_for_question(line: str) -> str:
        line_words = line.split()
        first_word = line_words[0]
        last_word = line_words[-1]
        if first_word.isalpha() and first_word.istitle():
            first_word = first_word.lower()
        if last_word.endswith('.'):
            last_word = last_word[:-1]
        line = ' '.join([first_word] + line_words[1:-1] + [last_word])
        return line


class IndentedQA(BaseParser):  # todo IndentedQA
    def add_card_condition(self):
        pass

    def add_note_condition(self):
        pass

    def format_card(self):
        pass
