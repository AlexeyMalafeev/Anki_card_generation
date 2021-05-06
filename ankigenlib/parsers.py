from collections import defaultdict
from pathlib import Path
import re
from typing import Optional


from ankigenlib import gap_making


ANSWER_ADDITION_MARKER = 'ans:'
CODE_ENDS_MARKER = '&CODE_ENDS&'
CODE_STARTS_MARKER = '&CODE_STARTS&'
CODE_ENDS_TAG = '</pre></code></span>'
CODE_STARTS_TAG = '<span style="font-size:medium"><code align="left" style="color: green"><pre>'
GT_MARKER = '&GT&'
LT_MARKER = '&LT&'
NEW_LINE_MARKER = '&NL&'
NOTE_SEPARATOR = '---'
PTRN_ANGLE_BRACKETS = r'\d?<.+?>'


def finalize_question(question: str, answer: str) -> (str, str):
    question = question.replace(CODE_STARTS_MARKER, CODE_STARTS_TAG)
    question = question.replace(CODE_ENDS_MARKER, CODE_ENDS_TAG)
    question = question.replace(LT_MARKER, '<')
    question = question.replace(GT_MARKER, '>')
    question = question.replace('\n', '<br>')
    question = question.replace(NEW_LINE_MARKER, '<br>')
    question = question.replace('\t', '  ')
    ans_add_ind = question.find(ANSWER_ADDITION_MARKER)
    if ans_add_ind != -1:
        ans_add = question[ans_add_ind:]
        ans_add = ans_add[len(ANSWER_ADDITION_MARKER):].strip()
        answer += f'<br><br>{ans_add}'
        question = question[:ans_add_ind]
    return question, answer


def format_line_for_question(line: str) -> str:
    line = line.replace('<br>', '\n')
    line = line.replace('’', '\'')
    if line.endswith('.'):
        line = line[:-1]
    return line


class BaseParser:
    """
    Base class for generating cards from a specially formatted text file.
    Abstract, not instantiated.
    All children are single use only.
    """
    def __init__(self, path_to_input: Path):
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

    def _get_line_iter(self, stripper=str.strip):
        for line in self.current_snippet.split('\n'):
            line = stripper(line)  # noqa
            if line:
                yield line

    def _get_snippet_iter(self):
        with open(self.path_to_input, 'r', encoding='utf-8') as f_in:
            yield from [content for content in f_in.read().split(NOTE_SEPARATOR)
                        if not content.isspace()]

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


class TabSepParser(BaseParser):
    """
    One line = one card.
    Tab-separated question and answer.
    Standard note separator.

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


class AngleBracketsParser(BaseParser):
    """
        One line = many cards.
        All answers are in angle brackets.
        Standard note separator.
        Multiple answers per card are supported with `1<...> ... 1<...>`, `2<...> ... 2<...>`, etc.

        Example:
            One two <three> four five six
            Seven <eight nine> ten <eleven>
            ---
            Twelve 1<thirteen> fourteen 1<fifteen> sixteen <seventeen>
            ...
    """
    forced_gap = None

    def __init__(self, path_to_input):
        super().__init__(path_to_input)
        self.spans: Optional[defaultdict] = None
        self.current_line = ''
        self.clean_line = ''

    def _make_cards(self):
        for line in self._get_line_iter():
            self.current_line = format_line_for_question(line)
            self._find_spans()
            self._make_gaps()

    def _find_spans(self):
        self.spans = defaultdict(list)
        line = self.current_line  # for brevity
        self.clean_line = ''
        matches = re.finditer(PTRN_ANGLE_BRACKETS, line)
        offset = 0
        prev_end = 0
        single_gap_id = 0
        for m in matches:
            start, end = m.span()
            self.clean_line += line[prev_end:start]
            m_text = line[start:end]
            if m_text.startswith('<'):
                diff = 2
                single_gap_id += 1
                card_id = f'auto{single_gap_id}'  # avoids overlapping with manually numbered spans
            else:
                diff = 3
                card_id = m_text[0]
            self.spans[card_id].append((start - offset, end - offset - diff))
            self.clean_line += m_text[diff - 1:-1]
            offset += diff
            prev_end = end
        self.clean_line += line[prev_end:]

    def _make_gaps(self):
        for _, spans in self.spans.items():
            question, answer = gap_making.make_gaps_by_spans(
                self.clean_line,
                *spans,
                forced_gap=self.forced_gap,
            )
            question, answer = finalize_question(question, answer)
            self._add_card(question, answer)


class CodeParser(AngleBracketsParser):
    """
        One snippet (not line) = many cards.
        All answers are in angle brackets, but literal angle brackets can be escaped with \
        Multiple answers per card are supported with `1<...> ... 1<...>`, `2<...> ... 2<...>`, etc.
        Standard note separator.
        All code lines must start with a tab.

        Example:
            Cool Python code:
                while <True>:
                    print(<'love you'>)
            ---
            More cool code:
                code <code> code
                <code code> code
    """
    forced_gap = gap_making.PHRASE_GAP

    def _make_cards(self):
        lines = []
        is_code = False
        for line in self._get_line_iter(stripper=str.rstrip):
            if line.startswith('\t'):
                line = line.replace('\t', '', 1)
                if not is_code:
                    is_code = True
                    line = CODE_STARTS_MARKER + line
            else:
                if is_code:
                    line = CODE_ENDS_MARKER + line
                    is_code = False
            line = line.replace(r'\<', LT_MARKER)
            line = line.replace(r'\>', GT_MARKER)
            lines.append(line)
        else:
            if is_code:
                lines[-1] += CODE_ENDS_MARKER
        self.current_line = '\n'.join(lines)
        self._find_spans()
        self._make_gaps()
