import os
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


def cls():
    print(chr(27) + "[2J")


def get_key():
    """
If key is pressed, return its string; if no key is pressed, return 0
    """
    return chr(ord(getch_inst()))


def menu(
        opt_list: tuple,  # of str or tuples: (str, obj)
        title: str = '',
        keys: str = '1234567890' + string.ascii_lowercase,
        new_line: bool = True
) -> str:
    """
Ask the user to choose one of the options from the option list.
The option list is either a tuple of strings
(then return the selected option string on user choice),
or a tuple of tuples (string, object),
(then return the object matching the choice).
    """
    if isinstance(opt_list[0], tuple) and len(opt_list[0]) == 2:
        options = []
        returnables = []
        for a, b in opt_list:
            options.append(a)
            returnables.append(b)
    else:
        options = returnables = opt_list
    keys = keys[:len(options)]
    if title:
        print(title)
    if new_line:
        st = '\n'
    else:
        st = '; '
    print(st.join([f' {key} - {option}' for key, option in zip(keys, options)]))
    while True:
        choice = get_key()
        if choice in keys:
            return returnables[keys.index(choice)]  # todo small inefficiency


def yn(message):
    return menu((('yes', True), ('no', False)), message)
