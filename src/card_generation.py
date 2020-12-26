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
    pass





def make_gap(text: str, text_lower: str, target: str, gap: str = '_____') -> str:
    matches = re.finditer(target, text_lower)
    for match_obj in reversed(list(matches)):
        start, end = match_obj.span()
        text = text[:start] + gap + text[end:]
    return text
