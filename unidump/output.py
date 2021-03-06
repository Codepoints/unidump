"""
handle output of arbitrary Unicode data
"""

import unicodedata
from typing import List

from unidump.env import Env


def sanitize_char(char: str) -> str:
    """replace char with a dot, if it's a control or whitespace char

    Close to what hexdump does, but Unicode-aware. Characters that unicodedata
    is not aware of will also be replaced with a dot.

    >>> sanitize_char('A')
    'A'
    >>> sanitize_char('\U0001F678')
    '\U0001F678'
    >>> sanitize_char(' ')
    '.'
    >>> sanitize_char('\x01')
    '.'
    >>> # un-set Unicode character, should have category "Cn"
    >>> sanitize_char('\U000D0000')
    '.'
    >>> sanitize_char('a1')
    Traceback (most recent call last):
        ...
    TypeError: category() argument must be a unicode character, not str
    """
    category = unicodedata.category(char)
    if category[0] in ('C', 'Z'):
        return '.'
    return char


def print_line(line: List, env: Env) -> None:
    """
    >>> import sys
    >>> from unidump.env import Env
    >>> _env = Env(linelength=4, output=sys.stdout)
    >>> print_line([0, ['00A0', '00B0', '00C0'], 'ABC'], _env)
          0    00A0 00B0 00C0         ABC\n
    >>> print_line([12, ['00A0', '1F678', '00C0'], 'A\U0001F678C'], _env)
         12    00A0 1F678 00C0        A\U0001F678C\n
    """
    env.output.write(env.lineformat.format(
        byte=line[0],
        repr=' '.join(line[1]).ljust(env.linelength*5-1),
        data=line[2]
    ))


def fill_and_print(current_line: List, byteoffset: int, representation: str,
                   char: str, env: Env) -> List:
    """
    >>> import sys
    >>> from unidump.env import Env
    >>> _env = Env(linelength=2, output=sys.stdout)
    >>> current_line = [0, [], '']
    >>> current_line = fill_and_print(current_line, 0, '0076', 'v', _env)
    >>> current_line == [0, ['0076'], 'v']
    True
    >>> current_line = fill_and_print(current_line, 1, '0076', 'v', _env)
    >>> current_line = fill_and_print(current_line, 2, '0077', 'w', _env)
          0    0076 0076    vv\n
    >>> current_line == [2, ['0077'], 'w']
    True
    """
    if len(current_line[1]) >= env.linelength:
        print_line(current_line, env)
        current_line = [byteoffset, [representation], char]
    else:
        current_line[1].append(representation)
        current_line[2] += char

    return current_line
