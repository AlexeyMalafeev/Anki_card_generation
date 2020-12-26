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


def make_cards(text: str, prefix: str) -> tuple:
    """Make cards from text. Split into sentences first. Add prefix.
    Return tuple of (question, answer) cards."""
    if not prefix.endswith(':'):
        prefix += ':'
    cards = []
    doc = nlp(text)
    for sent in doc.sents:
        if not (sent_stripped := sent.text.strip()):
            continue
        sub_keywords = term_extraction.get_keywords(sent_stripped, min_freq=1)
        sub_terms = term_extraction.get_terms(sent_stripped)
        temp_cards = []
        sent_stripped_lower = sent_stripped.lower()
        for keywords_or_terms, gap in (
                (sub_keywords, '_____'),
                (sub_terms, '_____(?)')
        ):
            for keyword_or_term in keywords_or_terms:
                question = make_gap(
                    text=sent_stripped,
                    text_lower=sent_stripped_lower,
                    target=keyword_or_term,
                    gap=gap
                )
                temp_cards.append((f'{prefix} {question}', keyword_or_term))
        for question, answer in temp_cards:
            print(question)
            print('-' * 50)
            print(answer)
            if ui.yn('\nOk?2'):
                cards.append((question, answer))
            ui.cls()
    return tuple(cards)


def make_gap(text: str, text_lower: str, target: str, gap: str = '_____') -> str:
    matches = re.finditer(target, text_lower)
    for match_obj in reversed(list(matches)):
        start, end = match_obj.span()
        text = text[:start] + gap + text[end:]
    return text
