import re


from ankigenlib.gap_special_cases import GAP_SPECIAL_CASES


DO_NOT_REPLACE = {
    'a',
    'an',
    'and',
    'at',
    'by',
    'for',
    'in',
    'of',
    'on',
    'or',
    'the',
    'to',
    'up',
}
ENDINGS_TO_KEEP = (
    'ed',
    'er',
    'ly',
    'less',
    'ty',
    'tion',
    'tions',
    'able',
    'al',
    'ing',
    'ism',
    'isms',
    's',
)


DIGIT_GAP = '__'
MAX_SEPARATE_GAPS = 2  # if _above_ this number of words to be gapped, make a phrase gap: _____(?)
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


def check_for_digit_gap(target):
    return target.isdigit() or all(not c.isalnum() for c in target)


def get_simple_gap(target):
    if ' ' in target:
        gap = PHRASE_GAP
    elif check_for_digit_gap(target):
        gap = DIGIT_GAP
    else:
        gap = WORD_GAP
    return gap


def get_smart_gap(target: str) -> str:
    if target in GAP_SPECIAL_CASES:
        return GAP_SPECIAL_CASES[target]
    gaps = []
    parts = target.split()
    if len(parts) > MAX_SEPARATE_GAPS:
        return PHRASE_GAP
    for targ in parts:
        gaps.append(_enhance_gap(targ))
    return ' '.join(gaps)


def _enhance_gap(target):
    gap = WORD_GAP
    add_comma = False
    if target.endswith(','):
        target = target[:-1]
        add_comma = True
    if '-' in target:
        gap = '-'.join([_enhance_gap(w) for w in target.split('-')])
    elif '/' in target:
        gap = '/'.join([_enhance_gap(w) for w in target.split('/')])
    else:
        for repl in ENDINGS_TO_KEEP:
            if target.endswith(repl):
                gap += repl
                break
    if check_for_digit_gap(target):
        gap = DIGIT_GAP
    if add_comma:
        gap += ','
    return gap


def make_gap(text: str, text_lower: str, target: str, gap: str = WORD_GAP) -> tuple:
    orig_target = target
    try:
        matches = re.finditer(re.escape(target), text_lower)
    except re.error:
        print(f'{text = }, {target = }, {gap = }')
        raise
    gap = get_smart_gap(target)
    for match_obj in reversed(list(matches)):
        start, end = match_obj.span()
        orig_target = text[start:end]
        text = text[:start] + gap + text[end:]
    text = auto_a_before_gap(text)
    return text, orig_target


def make_gaps_by_spans(text: str, *spans, use_simple_gaps=False) -> (str, str):
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
        if use_simple_gaps:
            gap = get_simple_gap(answer)
        else:
            gap = get_smart_gap(answer)
        gaps.append(gap)
    spans = reversed(spans)
    gaps = reversed(gaps)
    for span, gap in zip(spans, gaps):
        start, end = span
        question = question[:start] + gap + question[end:]
    question = auto_a_before_gap(question)
    answer = '<br>'.join(answers)
    return question, answer
