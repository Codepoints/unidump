import argparse
import codecs
import sys
from unidump import version, unidump
from unidump.env import env
from unicodedata import unidata_version
import gettext
from os.path import dirname
from textwrap import TextWrapper
from shutil import get_terminal_size


gettext.install('unidump', localedir=dirname(__file__)+'/locale')
tw = TextWrapper(width=min(80, get_terminal_size().columns),
        replace_whitespace=True,
        initial_indent='  ', subsequent_indent='  ').fill


description = '\n\n'.join([
  tw(_('A Unicode code point dump.')),

  tw(_('Think of it as hexdump(1) for Unicode. The command analyses the input '
      'and then prints three columns: the raw byte index of the first code point '
      'in this row, code points in their hex notation, and finally the raw input '
      'characters with control and whitespace replaced by a dot.')),

  tw(_('Invalid byte sequences are represented with an “X” and with the hex '
     'value enclosed in question marks, e.g., “?F5?”.')),

  tw(_('You can pipe in data from stdin, select several files at once, or '
      'even mix all those input methods together.')),
])

epilog = '\n\n'.join([
    _('Examples:'),

    tw(_('* Basic usage with stdin:')),

    '''      echo -n 'ABCDEFGHIJKLMNOP' | unidump -n 4
            0    0041 0042 0043 0044    ABCD
            4    0045 0046 0047 0048    EFGH
            8    0049 004A 004B 004C    IJKL
           12    004D 004E 004F 0050    MNOP''',

    tw(_('* Dump the code points translated from another encoding:')),

    '      unidump -c latin-1 some-legacy-file',

    tw(_('* Dump many files at the same time:')),

    '      unidump foo-*.txt',

    tw(_('* Control characters and whitespace are safely rendered:')),

    '''      echo -n -e '\\x01' | unidump -n 1
           0    0001    .''',

    tw(_('* Finally learn what your favorite Emoji is composed of:')),

    '''      ( echo -n -e '\\xf0\\x9f\\xa7\\x9d\\xf0\\x9f\\x8f\\xbd\\xe2' ; \\
        echo -n -e '\\x80\\x8d\\xe2\\x99\\x82\\xef\\xb8\\x8f' ; ) | \\
      unidump -n 5
           0    1F9DD 1F3FD 200D 2642 FE0F    .🏽.♂️''',

    tw(_('See <http://emojipedia.org/man-elf-medium-skin-tone/> for images. '
         'The “elf” emoji (the first character) is replaced with a dot here, '
         'because the current version of Python’s unicodedata doesn’t know of '
         'this character yet.')),

    tw(_('* Use it like strings(1):')),

    '      unidump -e \'{data}\' some-file.bin',

    tw(_('This will replace every unknown byte from the input file with “X” '
         'and every control and whitespace character with “.”.')),

    tw(_('* Only print the code points of the input:')),

    '''      unidump -e '{repr}'$'\\n' -n 1 some-file.txt''',

    tw(_('This results in a stream of code points in hex notation, each on a '
         'new line, without byte counter or rendering of actual data. You can '
         'use this to count the total amount of characters (as opposed to raw '
         'bytes) in a file, if you pipe it through `wc -l`.')),

    tw(_('This is version {} of unidump, using Unicode {} data.')
    .format(version, unidata_version)).lstrip() + '\n'
])


def main(args=None):
    # force stdout to be UTF-8 encoded, disregarding locale
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog='unidump',
        description=description,
        epilog=epilog,
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
                        ) % env.lineformat.replace('\n', '\\n'))
    parser.add_argument('-v', '--version', action='version',
                        version=_('%(prog)s {} using Unicode {} data').format(
                            version, unidata_version))

    a = parser.parse_args(args)

    try:
        for filename in a.files:
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
            unidump(infile, env=env(linelength=a.linelength,
                    encoding=a.encoding, lineformat=a.lineformat,
                    output=sys.stdout))
    except KeyboardInterrupt:
        sys.stdout.flush()
        return 1
    else:
        return 0
