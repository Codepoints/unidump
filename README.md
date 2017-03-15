# `unidump`

## `hexdump` for your Unicode data

## Usage

Without further ado, the usage message of `unidump`:

```
$ unidump --help
usage: unidump [-h] [-n LENGTH] [-c ENCODING] [-v] [FILE [FILE ...]]

A Unicode codepoint dump. Think of it as hexdump(1) for Unicode.

positional arguments:
  FILE                  input files. Use `-' or keep empty for stdin.

optional arguments:
  -h, --help            show this help message and exit
  -n LENGTH, --length LENGTH
                        format output using this much input characters.
                        Default is 16.
  -c ENCODING, --encoding ENCODING
                        interpret input in this encoding. Default is utf-8.
  -v, --version         show program's version number and exit
```

## Installation

Download and put in your path. You need Python 3 installed.

## Examples

```
$ echo -n 'ABCDEFGHIJKLMNOP' | unidump
     0    0041 0042 0043 0044 0045 0046 0047 0048 0049 004A 004B 004C 004D 004E 004F 0050    ABCDEFGHIJKLMNOP

# dump the code points translated from another encoding
$ unidump -c latin-1 some-legacy-file

# dump many files at the same time
$ unidump foo-*.txt

# control characters and whitespace are safely rendered:
$ echo -n -e '\x01' | unidump -n 1
     0    0001    .

# http://emojipedia.org/man-elf-medium-skin-tone/
# The "elf" emoji is replaced with a dot, because the current version of
# unicodedata doesn't know of this character yet.
$ echo -n -e '\xf0\x9f\xa7\x9d\xf0\x9f\x8f\xbd\xe2\x80\x8d\xe2\x99\x82\xef\xb8\x8f' | unidump -n 5
     0    1F9DD 1F3FD 200D 2642 FE0F    .🏽.♂️
```

## License

MIT-licensed. See [license file](LICENSE.md).
