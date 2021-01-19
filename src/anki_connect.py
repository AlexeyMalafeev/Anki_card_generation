import json
import urllib.request


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
    test()


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
