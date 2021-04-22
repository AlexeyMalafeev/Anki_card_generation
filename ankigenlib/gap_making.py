import re


DO_NOT_REPLACE = set('a an and at by in of on or to up'.split())


PHRASE_GAP = '_____(?)'
WORD_GAP = '_____'


def a_before_gap(prev_word):
    if prev_word in {'a', 'an'}:
        prev_word = 'a(n)'
    elif prev_word in {'A', 'An'}:
        prev_word = 'A(n)'
    return prev_word


def auto_a_before_gap(text: str) -> str:
    text = re.sub('(^| )(a|an|A|An) ___', r'\1a(n) ___', text)
    return text


def get_gap(target):
    gaps = []
    for targ in target.split():
        gaps.append(_enhance_gap(targ))
    return ' '.join(gaps)


def _enhance_gap(target):
    gap = WORD_GAP
    if '-' in target:
        gap = WORD_GAP + ('-' + WORD_GAP) * target.count('-')
    if target.endswith('ed'):
        gap += 'ed'
    elif target.endswith('ly'):
        gap += 'ly'
    elif target.endswith('less'):
        gap += 'less'
    elif target.endswith('ty'):
        gap += 'ty'
    elif target.endswith('tion'):
        gap += 'tion'
    elif target.endswith('tions'):
        gap += 'tions'
    elif target.endswith('s'):
        gap += 's'
    elif target.endswith('able'):
        gap += 'able'
    elif target.endswith('ing'):
        gap += 'ing'
    elif target in DO_NOT_REPLACE:
        gap = target
    return gap


def make_gap(text: str, text_lower: str, target: str, gap: str = WORD_GAP) -> tuple:
    orig_target = target
    try:
        matches = re.finditer(re.escape(target), text_lower)
    except re.error:
        print(f'{text = }, {target = }, {gap = }')
        raise
    gap = get_gap(target)
    for match_obj in reversed(list(matches)):
        start, end = match_obj.span()
        orig_target = text[start:end]
        text = text[:start] + gap + text[end:]
    text = auto_a_before_gap(text)
    return text, orig_target


def make_gaps_by_spans(text: str, *spans) -> (str, str):
    answers = []
    prev_answer = ''
    question = text
    gaps = []
    for span in spans:
        start, end = span
        answer = text[start:end]
        if answer != prev_answer:
            answers.append(answer)
            prev_answer = answer
        gap = get_gap(answer)
        gaps.append(gap)
    spans = reversed(spans)
    gaps = reversed(gaps)
    for span, gap in zip(spans, gaps):
        start, end = span
        question = question[:start] + gap + question[end:]
    question = auto_a_before_gap(question)
    answer = '<br>'.join(answers)
    return question, answer
