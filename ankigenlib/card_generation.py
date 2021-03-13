from ankigenlib.gap_making import PHRASE_GAP, WORD_GAP, make_gap
from ankigenlib import term_extraction

####################################################################################################
# Constants
####################################################################################################

CODE_DELIMETER = '<span style="font-size:medium"><code align="left" style="color: green"><pre>'
CODE_TAIL = '</pre></code></span>'
MIN_SENT_LENGTH = 50

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
        if not target:
            continue
        question = snippet.replace(target, PHRASE_GAP)
        temp_cards.append((f'{prefix}{question}', target))
    return tuple(temp_cards)
