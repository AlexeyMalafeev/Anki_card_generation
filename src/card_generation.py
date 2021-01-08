import re

import term_extraction

####################################################################################################
# Constants
####################################################################################################

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
    if prefix:
        prefix += ' '
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
