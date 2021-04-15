import re

PHRASE_GAP = '_____(?)'
WORD_GAP = '_____'


def before_gap(prev_word):
    if prev_word in {'a', 'an'}:
        prev_word = 'a(n)'
    elif prev_word in {'A', 'An'}:
        prev_word = 'A(n)'
    return prev_word


def choose_gap(target):
    # todo more sophisticated gap choosing logic
    return PHRASE_GAP if ' ' in target else WORD_GAP


def get_gap(target):
    gap = choose_gap(target)
    gap = enhance_gap(gap, target)
    return gap


def enhance_gap(gap, target):
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


# todo make_gap needs refactoring
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
    try:
        gap_escaped = re.escape(gap)
        text = re.sub(f'(^| )a ' + gap_escaped, fr'\1a(n) ' + gap, text)
        text = re.sub(f'(^| )an ' + gap_escaped, fr'\1a(n) ' + gap, text)
        text = re.sub(f'(^| )A ' + gap_escaped, fr'\1A(n) ' + gap, text)
        text = re.sub(f'(^| )An ' + gap_escaped, fr'\1A(n) ' + gap, text)
    except re.error:
        print(f'{text = }, {target = }, {gap = }')
        raise
    return text, orig_target
