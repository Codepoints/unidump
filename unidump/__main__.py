#!/usr/bin/env python3
"""run unidump as CLI script"""

import sys
from unidump.cli import main


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
