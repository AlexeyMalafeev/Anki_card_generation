import string


class Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __call__(self):
        import sys
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch_inst = Getch()


def add_card_or_not(question, answer):
    cls()
    print('Candidate card:\n')
    print(question)
    print('-' * 50)
    print(answer)
    # todo optionally change gap
    return yn('\nOk?')


def cls():
    print(chr(27) + "[2J")


def get_edited_snippet(curr_snippet, prefix):
    raise NotImplementedError


def get_int(a: int, b: int) -> int:
    assert a < b, f'{a = } is not less than {b = }'
    while True:
        i = input(f'Input an integer ({a}-{b}): ')
        try:
            i = int(i)
        except ValueError:
            continue
        else:
            if a <= i <= b:
                return i


def get_key():
    """
If key is pressed, return its string; if no key is pressed, return 0
    """
    return chr(ord(getch_inst()))


def get_prefix() -> str:
    prefix = input('\nChoose a prefix: ')
    if not prefix or prefix.endswith(': '):
        return prefix
    if prefix.endswith(':'):
        prefix += ' '
    else:
        prefix += ': '
    assert prefix.endswith(': '), f'prefix "{prefix}" is weird'
    return prefix


def join_snippets(
        curr_snippet: str,
        prev_snippet: str,
        next_snippet: str,
) -> tuple:
    other_snippet = menu(
        options=(
            (f'with previous: {prev_snippet}', 'previous'),
            (f'with next: {next_snippet}', 'next'),
            ('go back', 'back'),
        ),
        title='Join'
    )
    if other_snippet == 'previous':
        curr_snippet = f'{prev_snippet} {curr_snippet}'
        prev_snippet = ''
    elif other_snippet == 'next':
        curr_snippet = f'{curr_snippet} {next_snippet}'
        next_snippet = ''
    return prev_snippet, curr_snippet, next_snippet


def menu(
        options: tuple,  # of str or tuples: (str, any_other_obj)
        title: str = '',
        keys: str = '1234567890' + string.ascii_lowercase,
        new_line: bool = True
) -> str or object:
    """
Ask the user to choose one of the options from the option list.
The option list is either a tuple of strings
(then return the selected option string on user choice),
or a tuple of tuples (string, object),
(then return the object matching the choice).
    """
    if isinstance(options[0], tuple) and len(options[0]) == 2:
        displayables = []
        returnables = []
        for a, b in options:
            displayables.append(a)
            returnables.append(b)
    else:
        displayables = returnables = options
    keys = keys[:len(options)]
    if title:
        print(title)
    if new_line:
        st = '\n'
    else:
        st = '; '
    print(st.join([f' {key} - {option}' for key, option in zip(keys, displayables)]))
    while True:
        choice = get_key()
        if choice in keys:
            return returnables[keys.index(choice)]  # todo small inefficiency


def show_snippet(snippet: str, prefix: str) -> None:
    cls()
    if prefix:
        prefix += ' '
    print(f'Candidate snippet:\n{prefix}{snippet}')


def show_text_preview(text: str, first_k_chars: int = 500) -> None:
    print('TEXT PREVIEW:\n\n')
    print(text[:first_k_chars])


def split_snippets(
        snippet: str,
        prefix: str
) -> tuple:
    show_snippet(snippet, prefix)
    substr = input('Input a word or phrase that starts a new snippet: ')
    if (idx := snippet.find(substr)) != -1:
        first, second = snippet[:idx].rstrip(), snippet[idx:].lstrip()
        print(f'Snippet 1: {prefix}{first}\n----------\nSnippet 2: {prefix}{second}')
        if yn('Is this ok?'):
            return first, second
    else:
        return snippet, ''


def yn(message: str) -> str or object:
    return menu((('yes', True), ('no', False)), message, 'yn')
