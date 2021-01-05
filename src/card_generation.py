import re

from setup import nlp
import term_extraction
import ui

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

    for keywords_or_terms, gap in (
            (sub_keywords, WORD_GAP),
            (sub_terms, PHRASE_GAP)
    ):
        for keyword_or_term in keywords_or_terms:
            question = make_gap(
                text=snippet,
                text_lower=snippet_lower,
                target=keyword_or_term,
                gap=gap
            )
            temp_cards.append((f'{prefix} {question}', keyword_or_term))
    return tuple(temp_cards)


def make_gap(text: str, text_lower: str, target: str, gap: str = WORD_GAP) -> str:
    matches = re.finditer(target, text_lower)
    if target.endswith('s'):
        gap += 's'
    for match_obj in reversed(list(matches)):
        start, end = match_obj.span()
        text = text[:start] + gap + text[end:]
    text = re.sub(f'(^| )a {gap}', fr'\1a(n) {gap}', text)
    text = re.sub(f'(^| )an {gap}', fr'\1a(n) {gap}', text)
    text = re.sub(f'(^| )A {gap}', fr'\1A(n) {gap}', text)
    text = re.sub(f'(^| )An {gap}', fr'\1A(n) {gap}', text)
    return text
