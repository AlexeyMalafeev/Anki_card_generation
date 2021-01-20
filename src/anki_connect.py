import json
from pprint import pprint
import urllib.request


MAX_NUM_QUESTIONS_PER_NOTE = 35


def _make_note():
    pass


def _request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def anki_invoke(action, **params):
    print(f'to Anki: {action} with {params}')
    request_json = json.dumps(_request(action, **params)).encode('utf-8')
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request('http://localhost:8765', request_json)
        )
    )
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def main():
    make_notes_test()


def make_notes(
        fields_nested: tuple,  # of tuples
        deck_name: str = 'experimental',
        print_notes: bool = False,
        add_to_anki: bool = True,
):
    notes = []
    for fields in fields_nested:
        note = {'deckName': deck_name}
        n_fields = len(fields)
        assert n_fields > 0, f'number of fields must be > 0 in \n{fields = }'
        assert n_fields % 2 == 0, f'number of fields must be even in \n{fields = }'

        # determine model
        n_questions = n_fields // 2
        assert n_questions <= MAX_NUM_QUESTIONS_PER_NOTE, \
            f'number of questions ({n_questions}) must not exceed {MAX_NUM_QUESTIONS_PER_NOTE}'
        note['modelName'] = f'theory, {n_questions}q {n_questions}a'

        # map fields
        fields_mapping = {}
        for i in range(0, n_fields, 2):
            q = fields[i]
            a = fields[i + 1]
            n = i // 2 + 1
            fields_mapping[f'{n}q'] = q
            fields_mapping[f'{n}a'] = a
        note['fields'] = fields_mapping

        notes.append(note)

        if print_notes:
            pprint(note)

    # add all notes
    if add_to_anki:
        pass


def make_notes_test():
    fields = (
        ('question 1', 'answer 1', 'question 2', 'answer 2'),
        ('question 1', 'answer 1', 'question 2', 'answer 2', 'question 3', 'answer 3'),
        ('question 1', 'answer 1'),
    )
    make_notes(fields, deck_name='TEST', print_notes=True, add_to_anki=False)


def test():
    deck_names = anki_invoke('deckNames')
    print(f'{deck_names = }')
    # also deckNamesAndIds

    model_names = anki_invoke('modelNames')
    print(f'{model_names = }')

    # getEaseFactors, setEaseFactors
    # cardsInfo

    response = anki_invoke(
        'addNotes',
        notes=[
            {
                'deckName': 'experimental',
                'modelName': 'theory, 4q 4a',
                'fields': {
                    '1q': 'this is first question',
                    '1a': 'this is first answer',
                    '2q': 'second question',
                    '2a': 'second answer',
                    '3q': 'third q',
                    '3a': 'third a',
                    '4q': '4q',
                    '4a': '4a',
                },
            },
        ],
    )
    print(response)

    anki_invoke('sync')


if __name__ == '__main__':
    main()
