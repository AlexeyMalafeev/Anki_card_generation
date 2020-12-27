from setup import nlp


def get_sentences(text: str) -> tuple:
    sentences = []
    doc = nlp(text)
    for sent in doc.sents:
        if not (sent_stripped := sent.text.strip()):
            continue
        sentences.append(sent_stripped)
    return tuple(sentences)
