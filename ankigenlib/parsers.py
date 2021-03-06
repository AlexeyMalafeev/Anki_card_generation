class BaseParser:
    def __init__(self, path_to_input):
        self.path_to_input: str = ''
        self.set_input(path_to_input)
        self.notes: list = []  # nested: [(q1, a1, q2, a2, ...), (q1, a1, q2, a2, ...), ...]
        self.cards: list = []  # flat: [question1, answer1, question2, answer2, ...]

    def add_card(self, question, answer):
        self.cards.extend([question, answer])

    def add_note(self):
        self.notes.append(tuple(self.cards))
        self.cards = []

    def after_parse(self):
        pass

    def before_parse(self):
        pass

    def parse(self) -> tuple:
        self.before_parse()
        with open(self.path_to_input) as f_in:
            for line in f_in:
                line = self.preprocess_line(line)
                self.process_line(line)
        self.after_parse()
        return tuple(self.notes)

    @staticmethod
    def preprocess_line(line):
        return line.strip()

    def process_line(self, line):
        raise NotImplementedError

    def set_input(self, path_to_input):
        self.path_to_input = path_to_input


