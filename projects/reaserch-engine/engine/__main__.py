"""``python3 -m engine`` → iterative retrieval CLI (see ``engine.cli``)."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
