from setup import nlp


def clean_text_for_anki_import(text: str) -> str:
    text = text.replace('\t', ' ')
    text = text.replace('\n', '<br>')
    return text


def get_sentences(text: str) -> tuple:
    sentences = []
    doc = nlp(text)
    for sent in doc.sents:
        if not (sent_stripped := sent.text.strip()):
            continue
        sentences.append(sent_stripped)
    return tuple(sentences)
