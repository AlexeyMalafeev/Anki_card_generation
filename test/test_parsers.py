from pathlib import Path

from ankigenlib import parsers


def test_tab_separated_parser():
    sample_file_path = Path('test', 'sample_inputs', 'tab_sep.txt')
    parser = parsers.TabSepParser(sample_file_path)
    result = parser.parse()
    expected = (
        (
            'question 1', 'answer 1',
            'question 2', 'answer 2',
            'question 3', 'answer 3',
        ),
        (
            'question 1', 'answer 1',
            'question 2', 'answer 2',
            'question 3', 'answer 3',
            'question 4', 'answer 4',
            'question 5', 'answer 5',
        ),
    )
    assert result == expected


def test_angle_parser():
    sample_file_path = Path('test', 'sample_inputs', 'angle.txt')
    parser = parsers.AngleBracketsParser(sample_file_path)
    result = parser.parse()
    expected = (
        (
            'One two _____ four five six', 'three',
            'Seven _____ _____ ten eleven', 'eight nine',
            'Seven eight nine ten _____', 'eleven',
        ),
        (
            'Twelve thirteen fourteen fifteen sixteen _____', 'seventeen',
            'Twelve _____ fourteen _____ sixteen seventeen', 'thirteen<br>fifteen',
        ),
    )
    assert result == expected


# noinspection LongLine
def test_code_parser():
    sample_file_path = Path('test', 'sample_inputs', 'code.txt')
    parser = parsers.CodeParser(sample_file_path)
    result = parser.parse()
    print(result)
    expected = (
        (
            'Cool Python code:<br><span style="font-size:medium"><code align="left" style="color: green"><pre>while _____(?):<br>  print(\'love you\')</pre></code></span>', 'True',
            'Cool Python code:<br><span style="font-size:medium"><code align="left" style="color: green"><pre>while True:<br>  print(_____(?))</pre></code></span>', "'love you'"),
        (
            'More cool code:<br><span style="font-size:medium"><code align="left" style="color: green"><pre>if _____(?) < _____(?):<br>  print(\'a is less than b\')</pre></code></span>', 'a<br>b',
        )
    )
    assert result == expected
