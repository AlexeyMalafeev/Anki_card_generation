import os

from ankigenlib import parsers


def test_tab_separated_qa_parser():
    sample_file_path = os.path.join('test', 'sample_input_for_tab_separated_qa.txt')
    parser = parsers.TabSeparatedQA(sample_file_path)
    parser.parse()
    result = parser.notes
    expected = (
        ('question 1', 'answer 1', 'question 2', 'answer 2', 'question 3', 'answer 3'),
        ('question 1', 'answer 1', 'question 2', 'answer 2', 'question 3', 'answer 3',
         'question 4', 'answer 4', 'question 5', 'answer 5'),
    )
    assert result == expected
