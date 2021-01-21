from setup import nlp


def clean_text_for_anki_import(text: str) -> str:
    text = text.replace('\t', ' ')
    text = text.replace('\n', '<br>')
    return text


def get_sentences(text: str) -> tuple:
    sentences = []
    doc = nlp(text)
    for sent in doc.sents:
        if sent.text.isspace():
            continue
        sent_processed = sent.text.strip()
        first = sent[0]
        if first.text.istitle() and not first.ent_type_:
            sent_processed = sent_processed[0].lower() + sent_processed[1:]
        if sent_processed.endswith('.'):
            sent_processed = sent_processed[:-1]
        sentences.append(sent_processed)
    return tuple(sentences)
