#!/usr/bin/env python3
"""Earth Rehearsal standard-library entry point. AGPL-3.0-only."""
import pathlib
import sys

if sys.version_info < (3, 12):
    raise SystemExit('Earth Rehearsal requires Python 3.12 or newer; see the release-specific environment evidence.')
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / 'src'))
from earth_rehearsal.cli import main

if __name__ == '__main__':
    raise SystemExit(main())
