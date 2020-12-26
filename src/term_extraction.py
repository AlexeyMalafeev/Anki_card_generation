from setup import combo_basic, nlp, rake_obj


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
