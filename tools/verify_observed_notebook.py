#!/usr/bin/env python3
"""Execute the shipped notebook's standard-library cells without installing Jupyter."""
import contextlib
import io
import json
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]


def main():
    notebook = json.loads((ROOT/'notebooks/observed-potomac.ipynb').read_text())
    if notebook['nbformat'] != 4:
        raise ValueError('unexpected notebook format')
    os.chdir(ROOT)
    namespace = {}
    count = 0
    for cell in notebook['cells']:
        if cell['cell_type'] != 'code':
            continue
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            exec(compile(''.join(cell['source']), 'observed-potomac.ipynb', 'exec'), namespace)
        retained = ''.join(''.join(output['text']) for output in cell['outputs'] if output['output_type'] == 'stream' and output['name'] == 'stdout')
        if stream.getvalue() != retained:
            raise ValueError('notebook retained output differs from current execution')
        count += 1
    print(f'PASS: {count} executed observed-data notebook cells match their retained outputs')


if __name__ == '__main__':
    main()
