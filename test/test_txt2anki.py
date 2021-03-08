import os

from ankigenlib import txt2anki


def test_ankify():
    sample_file_path = os.path.join('test', 'sample_input_for_txt2anki.txt')
    result = txt2anki.ankify(
        input_path=sample_file_path,
        parse_mode='tabs',
        target_deck='TEST'
    )
    expected = [
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
            'fields': {
                '1q': 'question 1',
                '1a': 'answer 1',
                '2q': 'question 2',
                '2a': 'answer 2',
                '3q': 'question 3',
                '3a': 'answer 3',
                '4q': 'question 4',
                '4a': 'answer 4',
                '5q': 'question 5',
                '5a': 'answer 5',
            },
            'modelName': 'theory, 5q 5a',
        },
    ]
    assert result == expected
