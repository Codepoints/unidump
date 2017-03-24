import sys
from typing import TextIO


class Env(object):

    linelength = 16

    encoding = 'utf-8'

    lineformat = '{byte:>7}    {repr}    {data}\n'

    output = sys.stdout

    def __init__(self, linelength: int = None, encoding: str = None,
                 lineformat: str = None, output: TextIO = None) -> None:
        if linelength is not None:
            self.linelength = linelength
        if encoding is not None:
            self.encoding = encoding
        if lineformat is not None:
            self.lineformat = lineformat
        if output is not None:
            self.output = output
