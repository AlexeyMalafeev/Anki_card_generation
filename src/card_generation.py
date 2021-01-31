import re

import term_extraction

####################################################################################################
# Constants
####################################################################################################

CODE_DELIMETER = '<span style="font-size:medium"><code align="left" style="color: green"><div>'
CODE_TAIL = '</div></code></span>'
MIN_SENT_LENGTH = 50
PHRASE_GAP = '_____(?)'
WORD_GAP = '_____'

####################################################################################################
# Functions
####################################################################################################


def make_candidate_cards(snippet: str, prefix: str) -> tuple:
    sub_keywords = term_extraction.get_keywords(snippet, min_freq=1)
    sub_terms = term_extraction.get_terms(snippet)
    temp_cards = []
    snippet_lower = snippet.lower()
    for keywords_or_terms, gap in (
            (sub_keywords, WORD_GAP),
            (sub_terms, PHRASE_GAP)
    ):
        for keyword_or_term in keywords_or_terms:
            question, orig_target = make_gap(
                text=snippet,
                text_lower=snippet_lower,
                target=keyword_or_term,
                gap=gap
            )
            temp_cards.append((f'{prefix}{question}', orig_target))
    return tuple(temp_cards)


def make_candidate_cards_code(snippet: str, prefix: str) -> tuple:
    temp_cards = []
    replaced = set()
    try:
        target_chunk = snippet.split(CODE_DELIMETER)[1].strip()
    except IndexError:
        # todo custom exception for card formatting
        raise Exception('Input text for cards with code should contain code delimeter '
                        f'{CODE_DELIMETER} but it doesn\'t')
    target_lines = target_chunk.split('\n')
    if (last_line := target_lines[-1]).endswith(CODE_TAIL):
        target_lines[-1] = last_line.replace(CODE_TAIL, '')
    else:
        raise Exception('Input text for cards with code should contain code tag "tail" '
                        f'{CODE_TAIL} but it doesn\'t')
    for line in target_lines:
        target = line.lstrip()
        question = snippet.replace(target, PHRASE_GAP)
        temp_cards.append((f'{prefix}{question}', target))
    return tuple(temp_cards)


def make_gap(text: str, text_lower: str, target: str, gap: str = WORD_GAP) -> tuple:
    orig_target = target
    try:
        matches = re.finditer(re.escape(target), text_lower)
    except re.error:
        print(f'{text = }, {target = }, {gap = }')
        raise
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
