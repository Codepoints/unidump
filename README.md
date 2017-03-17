# `unidump`

## `hexdump` for your Unicode data

## Installation

[Download](https://raw.githubusercontent.com/Codepoints/unidump/master/unidump)
and put it in your path. You need Python 3 installed.

## Usage

Without further ado, here is the usage message of `unidump`:

```
$ unidump --help
usage: unidump [-h] [-n LENGTH] [-c ENC] [-e FORMAT] [-v] [FILE [FILE ...]]

  A Unicode codepoint dump.

  Think of it as  hexdump(1)  for Unicode.  The command analyses  the input and
  prints then three columns:  the raw byte count of the first codepoint in this
  row,  codepoints in their hex notation,  and finally the raw input characters
  with control and whitespace replaced by a dot.

  Invalid byte sequences are represented with an “X” and with the hex value en-
  closed in question marks, e.g., “?F5?”.

  You can pipe in  data from stdin,  select several files at once,  or even mix
  all those input methods together.

positional arguments:
  FILE                  input files. Use `-' or keep empty for stdin.

optional arguments:
  -h, --help            show this help message and exit
  -n LENGTH, --length LENGTH
                        format output using this much input characters.
                        Default is 16 characters.
  -c ENC, --encoding ENC
                        interpret input in this encoding. Default is utf-8.
                        You can choose any encoding that Python supports, e.g.
                        “latin-1”.
  -e FORMAT, --format FORMAT
                        specify a custom format in Python’s {} notation.
                        Default is “{byte:>7} {repr} {data} ”.
  -v, --version         show program's version number and exit

Examples:

* Basic usage with stdin:

      echo -n 'ABCDEFGHIJKLMNOP' | unidump -n 4
            0    0041 0042 0043 0044    ABCD
            4    0045 0046 0047 0048    EFGH
            8    0049 004A 004B 004C    IJKL
           12    004D 004E 004F 0050    MNOP

* Dump the code points translated from another encoding:

      unidump -c latin-1 some-legacy-file

* Dump many files at the same time:

      unidump foo-*.txt

* Control characters and whitespace are safely rendered:

      echo -n -e '\x01' | unidump -n 1
           0    0001    .

* Finally learn what your favorite Emoji is composed of:

      ( echo -n -e '\xf0\x9f\xa7\x9d\xf0\x9f\x8f\xbd\xe2' ; \
        echo -n -e '\x80\x8d\xe2\x99\x82\xef\xb8\x8f' ; ) | \
      unidump -n 5
           0    1F9DD 1F3FD 200D 2642 FE0F    .🏽.♂️

  See  <http://emojipedia.org/man-elf-medium-skin-tone/> for images.  The “elf”
  emoji (the first character) is replaced with a dot here,  because the current
  version of Python’s unicodedata doesn’t know of this character yet.

* Use it like strings(1):

      unidump -e '{data}' some-file.bin

  This will replace  every unknown byte from the input file  with “X” and every
  control and whitespace character with “.”.

* Only print the code points of the input:

      unidump -e '{repr}'$'\n' -n 1 some-file.txt

  This results in  a stream of codepoints in hex notation,  each on a new line,
  without byte counter  or rendering of actual data.  You can use this to count
  the total amount of characters  (as opposed to raw bytes)  in a file,  if you
  pipe it through `wc -l`.
```

## License

MIT-licensed. See [license file](LICENSE.md).
