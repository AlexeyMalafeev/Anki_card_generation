from collections import defaultdict
import re


from ankigenlib import gap_making


NOTE_SEPARATOR = '---'
PTRN_ANGLE_BRACKETS = r'\w?<.+?>'


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


class BaseParser:
    """
    Base class for generating cards from a specially formatted text file.
    Abstract, not instantiated.
    All children are single use only.
    """
    def __init__(self, path_to_input):
        self.path_to_input: str = ''
        self.path_to_input = path_to_input
        self.notes: list = []  # nested: [(q1, a1, q2, a2, ...), (q1, a1, q2, a2, ...), ...]
        self.cards: list = []  # flat: [question1, answer1, question2, answer2, ...]
        self.current_snippet: str = ''
        self.question: str = ''
        self.answer: str = ''

    def _add_card(self, question, answer):
        self.cards.extend([question, answer])

    def _add_note(self):
        self.notes.append(tuple(self.cards))
        self.cards = []

    def _do_after_iteration(self):
        if self.cards:
            self._add_note()

    def _get_line_iter(self):
        for line in self.current_snippet.split('\n'):
            line = line.strip()
            if line:
                yield line

    def _get_snippet_iter(self):
        with open(self.path_to_input, 'r', encoding='utf-8') as f_in:
            yield from f_in.read().split(NOTE_SEPARATOR)

    def _iterate_over_snippets(self):
        for snippet in self._get_snippet_iter():
            self.current_snippet = snippet
            self._make_cards()
            self._add_note()

    def _make_cards(self):
        raise NotImplementedError

    def parse(self) -> tuple:
        self._iterate_over_snippets()
        self._do_after_iteration()
        return tuple(self.notes)


class TabSeparatedQA(BaseParser):
    """
    One line = one card (tab-separated question and answer)
    Standard note separator

    Example:
        question1\tanswer1
        question2\tanswer2
        question3\tanswer3
        ---
        question1\tanswer1
        question2\tanswer2
        ...
    """
    def _make_cards(self):
        for line in self._get_line_iter():
            question, answer = line.split('\t')
            self._add_card(question, answer)


class AngleBracketsQA(BaseParser):
    """
        One line = many cards (all answers are in angle brackets)
        Standard note separator
        Multiple answers per card are supported with `1<...> ... 1<...>`, `2<...> ... 2<...>`, etc.

        Example:
            One two <three> four five six
            Seven <eight nine> ten <eleven>
            ---
            Twelve 1<thirteen> fourteen 1<fifteen> sixteen <seventeen>
            ...
        """
    def __init__(self, path_to_input):
        super().__init__(path_to_input)
        # self.cards_to_add = []  # [q1, a1, q2, a2, q3, a3, ...]
        self.normal_spans = []
        self.numbered_spans = defaultdict(list)
        self.current_line = ''
        self.clean_line = ''

    def _make_cards(self):
        for line in self._get_line_iter():
            self.current_line = format_line_for_question(line)
            self._find_spans()
            self._make_gaps()

    def _find_spans(self):
        self.numbered_spans = defaultdict(list)
        self.normal_spans = []
        line = self.current_line  # for brevity
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

    def _make_gaps(self):
        for span in self.normal_spans:
            question, answer = gap_making.make_gaps_by_spans(self.clean_line, span)
            self._add_card(question, answer)
        for m_id, spans in self.numbered_spans.items():
            question, answer = gap_making.make_gaps_by_spans(self.clean_line, *spans)
            self._add_card(question, answer)


class CodeQA(BaseParser):
    def _make_cards(self):
        pass
