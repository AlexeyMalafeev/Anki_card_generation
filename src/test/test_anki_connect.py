from anki_connect import anki_invoke, make_notes


def test_anki_invoke():
    deck_names = anki_invoke('deckNames')
    print(f'{deck_names = }')
    # also deckNamesAndIds

    model_names = anki_invoke('modelNames')
    print(f'{model_names = }')

    # getEaseFactors, setEaseFactors
    # cardsInfo

    # response = anki_invoke(
    #     'addNotes',
    #     notes=[
    #         {
    #             'deckName': 'experimental',
    #             'modelName': 'theory, 4q 4a',
    #             'fields': {
    #                 '1q': 'this is first question',
    #                 '1a': 'this is first answer',
    #                 '2q': 'second question',
    #                 '2a': 'second answer',
    #                 '3q': 'third q',
    #                 '3a': 'third a',
    #                 '4q': '4q',
    #                 '4a': '4a',
    #             },
    #         },
    #     ],
    # )
    # print(response)

    # anki_invoke('sync')


def test_make_notes():
    fields = (
        ('question 1', 'answer 1', 'question 2', 'answer 2'),
        ('question 1', 'answer 1', 'question 2', 'answer 2', 'question 3', 'answer 3'),
        ('question 1', 'answer 1'),
    )
    # make_notes(fields, deck_name='experimental', print_notes=True, add_to_anki=True)
    result = make_notes(fields, deck_name='TEST', print_notes=True, add_to_anki=False)
    expected = [
        {
            'deckName': 'TEST',
            'modelName': 'theory, 2q 2a',
            'fields': {'1q': 'question 1', '1a': 'answer 1', '2q': 'question 2', '2a': 'answer 2'},
        },
        {
            'deckName': 'TEST',
            'modelName': 'theory, 3q 3a',
            'fields': {
                '1q': 'question 1',
                '1a': 'answer 1',
                '2q': 'question 2',
                '2a': 'answer 2',
                '3q': 'question 3',
                '3a': 'answer 3',
            },
        },
        {
            'deckName': 'TEST',
            'modelName': 'theory, 1q 1a',
            'fields': {'1q': 'question 1', '1a': 'answer 1'},
        },
    ]
    assert result == expected


# test_make_notes()
