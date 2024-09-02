"""
handle the CLI logic for a unidump call
"""


import argparse
import codecs
import gettext
from os.path import dirname
from shutil import get_terminal_size
import sys
from textwrap import TextWrapper
# pylint: disable=unused-import
from typing import List, IO, Any
# pylint: enable=unused-import
from unicodedata import unidata_version

from unidump import VERSION, unidump
from unidump.env import Env


TL = gettext.translation('unidump', localedir=dirname(__file__)+'/locale',
                         fallback=True)
_ = TL.gettext
TW = TextWrapper(width=min(80, getattr(get_terminal_size(), 'columns')),
                 replace_whitespace=True,
                 initial_indent='  ', subsequent_indent='  ').fill


DESCRIPTION = '\n\n'.join([
    TW(_('A Unicode code point dump.')),

    TW(_('Think of it as hexdump(1) for Unicode. The command analyses the '
         'input and then prints three columns: the raw byte index of the '
         'first code point in this row, code points in their hex notation, '
         'and finally the raw input characters with control and whitespace '
         'replaced by a dot.')),

    TW(_('Invalid byte sequences are represented with an “X” and with the hex '
         'value enclosed in question marks, e.g., “?F5?”.')),

    TW(_('You can pipe in data from stdin, select several files at once, or '
         'even mix all those input methods together.')),
])

EPILOG = '\n\n'.join([
    _('Examples:'),

    TW(_('* Basic usage with stdin:')),

    '''      echo -n 'ABCDEFGHIJKLMNOP' | unidump -n 4
            0    0041 0042 0043 0044    ABCD
            4    0045 0046 0047 0048    EFGH
            8    0049 004A 004B 004C    IJKL
           12    004D 004E 004F 0050    MNOP''',

    TW(_('* Dump the code points translated from another encoding:')),

    '      unidump -c latin-1 some-legacy-file',

    TW(_('* Dump many files at the same time:')),

    '      unidump foo-*.txt',

    TW(_('* Control characters and whitespace are safely rendered:')),

    '''      echo -n -e '\\x01' | unidump -n 1
           0    0001    .''',

    TW(_('* Finally learn what your favorite Emoji is composed of:')),

    '''      ( echo -n -e '\\xf0\\x9f\\xa7\\x9d\\xf0\\x9f\\x8f\\xbd\\xe2' ; \\
        echo -n -e '\\x80\\x8d\\xe2\\x99\\x82\\xef\\xb8\\x8f' ; ) | \\
      unidump -n 5
           0    1F9DD 1F3FD 200D 2642 FE0F    .🏽.♂️''',

    TW(_('See <http://emojipedia.org/man-elf-medium-skin-tone/> for images. '
         'The “elf” emoji (the first character) is replaced with a dot here, '
         'because the current version of Python’s unicodedata doesn’t know of '
         'this character yet.')),

    TW(_('* Use it like strings(1):')),

    '      unidump -e \'{data}\' some-file.bin',

    TW(_('This will replace every unknown byte from the input file with “X” '
         'and every control and whitespace character with “.”.')),

    TW(_('* Only print the code points of the input:')),

    '''      unidump -e '{repr}'$'\\n' -n 1 some-file.txt''',

    TW(_('This results in a stream of code points in hex notation, each on a '
         'new line, without byte counter or rendering of actual data. You can '
         'use this to count the total amount of characters (as opposed to raw '
         'bytes) in a file, if you pipe it through `wc -l`.')),

    TW(_('This is version {} of unidump, using Unicode {} data.')
       .format(VERSION, unidata_version)).lstrip() + '\n'
])


def force_stdout_to_utf8():
    """force stdout to be UTF-8 encoded, disregarding locale

    Do not type-check this:
    error: Incompatible types in assignment (expression has type
           "StreamWriter", variable has type "TextIO")
    error: "TextIO" has no attribute "detach"
    \\o/
    """
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def main(args: List[str] = None) -> int:
    """entry-point for an unidump CLI call"""

    force_stdout_to_utf8()

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog='unidump',
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('files', nargs='*', metavar='FILE', default=('-',),
                        help=_(
                            'input files. Use “-” or keep empty for stdin.'))
    parser.add_argument('-n', '--length', type=int, default=16,
                        dest='linelength', metavar='LENGTH',
                        help=_(
                            'format output using this much input characters. '
                            'Default is %(default)s characters.'))
    parser.add_argument('-c', '--encoding', type=str, default='utf-8',
                        metavar='ENC',
                        help=_(
                            'interpret input in this encoding. Default is '
                            '%(default)s. You can choose any encoding that '
                            'Python supports, e.g. “latin-1”.'))
    parser.add_argument('-e', '--format', type=str, default=None,
                        dest='lineformat', metavar='FORMAT',
                        help=_(
                            'specify a custom format in Python’s {} notation. '
                            'Default is “%s”. '
                            'See examples below on how to use this option.'
                        ) % Env.lineformat.replace('\n', '\\n'))
    parser.add_argument('-v', '--version', action='version',
                        version=_('%(prog)s {} using Unicode {} data').format(
                            VERSION, unidata_version))

    options = parser.parse_args(args)

    try:
        for filename in options.files:
            infile = None  # type: IO[bytes]
            if filename == '-':
                infile = sys.stdin.buffer
            else:
                try:
                    infile = open(filename, 'rb')
                except FileNotFoundError:
                    sys.stdout.flush()
                    sys.stderr.write(_('File {} not found.\n')
                                     .format(filename))
                    continue
                except IsADirectoryError:
                    sys.stdout.flush()
                    sys.stderr.write(_('{} is a directory.\n')
                                     .format(filename))
                    continue
            unidump(
                infile,
                env=Env(
                    linelength=options.linelength,
                    encoding=options.encoding,
                    lineformat=options.lineformat,
                    output=sys.stdout))
    except (KeyboardInterrupt, BrokenPipeError):
        sys.stdout.flush()
        return 1
    else:
        return 0
