# from collections import Counter
# from pprint import pprint
import os
import re

from pyate import combo_basic
# noinspection PyPackageRequirements
import RAKE
import spacy
from stop_words import get_stop_words

import ui

####################################################################################################
# Setup
####################################################################################################

# read texts
input_text = open(os.path.join('..', 'input.txt'), 'r', encoding='utf-8').read()
non_empty_lines = [parag for line in input_text.split('\n') if (parag := line.strip())]

# RAKE stands for Rapid Automatic Keyword Extraction. The algorithm itself is described in the
# Text Mining Applications and Theory book by Michael W. Berry.
stop_words = get_stop_words('en')
rake_obj = RAKE.Rake(stop_words=stop_words)

nlp = spacy.load('en_core_web_sm')

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
        sub_keywords = get_keywords(sent_stripped, min_freq=1)
        sub_terms = get_terms(sent_stripped)
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


def get_keywords(text: str, min_freq: int = 2) -> tuple:
    """RAKE is used to get keywords (single words). min_freq is a hyperparameter."""
    return tuple(word for word, score in rake_obj.run(text, maxWords=1, minFrequency=min_freq))


def get_sentences(text: str) -> tuple:
    """Split text into sentences with spaCy"""
    doc = nlp(text)
    return tuple(sent_stripped for sent in doc.sents if (sent_stripped := sent.text.strip()))


def get_terms(text: str) -> tuple:
    """pyate is Python implementation of term extraction algorithms such as C-Value, Basic, Combo
    Basic, Weirdness and Term Extractor using spaCy POS tagging.
    Combo Basic seems like the best method."""
    return tuple(combo_basic(text).sort_values(ascending=False).index)


# print(get_sentences(input_text))
make_cards(input_text, prefix='UIMA')
