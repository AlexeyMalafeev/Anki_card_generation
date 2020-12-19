# from collections import Counter
from pprint import pprint


from pyate import combo_basic
# noinspection PyPackageRequirements
import RAKE
import spacy
from stop_words import get_stop_words

####################################################################################################
# Setup
####################################################################################################

# read texts
input_text = open('input.txt', 'r', encoding='utf-8').read()
non_empty_lines = [parag for line in input_text.split('\n') if (parag := line.strip())]

# RAKE stands for Rapid Automatic Keyword Extraction. The algorithm itself is described in the
# Text Mining Applications and Theory book by Michael W. Berry.
stop_words = get_stop_words('en')
rake_obj = RAKE.Rake(stop_words=stop_words)

nlp = spacy.load('en_core_web_sm')

####################################################################################################
# Functions
####################################################################################################


def get_sentences(text: str) -> tuple:
    """Split text into sentences with spaCy"""
    doc = nlp(text)
    return tuple(sent_stripped for sent in doc.sents if (sent_stripped := sent.text.strip()))


def get_terms(text: str) -> tuple:
    """pyate is Python implementation of term extraction algorithms such as C-Value, Basic, Combo
    Basic, Weirdness and Term Extractor using spaCy POS tagging.
    Combo Basic seems like the best method."""
    return tuple(combo_basic(text).sort_values(ascending=False).index)


def get_terms_rake(text: str) -> tuple:
    """RAKE seems inferior to pyate (function get_terms)"""
    return tuple(word for word, score in rake_obj.run(text, maxWords=1, minFrequency=2))


# pprint(get_terms_rake(input_text)[:20])
# pprint(get_terms(input_text)[:20])
print(get_sentences(input_text))
