from ankigenlib.setup import nlp


def clean_text_for_anki_import(text: str) -> str:
    text = text.replace('\t', ' ')
    text = text.replace('\n', '<br>')
    return text


def format_snippet_for_anki(snippet: str) -> str:
    if not snippet.strip():
        return ''
    doc = nlp(snippet)
    formatted = doc.text
    first = doc[0]
    if first.text.istitle() and not first.ent_type_:
        formatted = formatted[0].lower() + formatted[1:]
    if formatted.endswith('.'):
        formatted = formatted[:-1]
    return formatted


def get_sentences(text: str) -> tuple:
    sentences = []
    doc = nlp(text)
    for sent in doc.sents:
        if sent.text.isspace():
            continue
        sent_processed = sent.text.strip()
        sentences.append(sent_processed)
    return tuple(sentences)
