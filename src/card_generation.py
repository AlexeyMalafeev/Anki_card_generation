import re

from setup import nlp
import term_extraction
import ui

####################################################################################################
# Constants
####################################################################################################

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
            (sub_keywords, '_____'),
            (sub_terms, '_____(?)')
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


def make_gap(text: str, text_lower: str, target: str, gap: str = '_____') -> str:
    matches = re.finditer(target, text_lower)
    for match_obj in reversed(list(matches)):
        start, end = match_obj.span()
        text = text[:start] + gap + text[end:]
    return text
