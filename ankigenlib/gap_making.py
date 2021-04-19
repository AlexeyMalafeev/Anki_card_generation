import re

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


def choose_gap(target):
    # todo consider not using (?) but always unwrap instead: _____ _____ _____
    return PHRASE_GAP if ' ' in target else WORD_GAP


def get_gap(target):
    gap = choose_gap(target)
    if '-' in target and ' ' not in target:
        gap = WORD_GAP + ('-' + WORD_GAP) * target.count('-')
    gap = enhance_gap(gap, target)
    return gap


def enhance_gap(gap, target):
    # todo handle (?) gaps differently, don't replace or unwrap into _____ _____ing etc.
    if target.endswith('s'):
        gap += 's'
    elif target.endswith('ed'):
        gap += 'ed'
    elif target.endswith('ly'):
        gap += 'ly'
    elif target.endswith('tion'):
        gap += 'tion'
    elif target.endswith('able'):
        gap += 'able'
    elif target.endswith('ing'):
        gap += 'ing'
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
    for span in spans:
        start, end = span
        answer = text[start:end]
        if answer != prev_answer:
            answers.append(answer)
            prev_answer = answer
        gap = get_gap(answer)
        question = question[:start] + gap + question[end:]
    question = auto_a_before_gap(question)
    return question, answer
