"""Streaming consistency checks for human-readable evidence tables."""
import csv
from itertools import zip_longest
from .bundle import BundleError


def verify_csv(path,rows):
    missing=object()
    with path.open(newline='',encoding='utf-8') as file:
        for actual,expected in zip_longest(csv.reader(file),rows,fillvalue=missing):
            if actual is missing or expected is missing or actual!=['' if v is None else str(v) for v in expected]:raise BundleError(path.name+': CSV differs from reconstructed evidence')

def verify_html(path,expected):
    if path.read_text(encoding='utf-8')!=expected:raise BundleError(path.name+': report differs from reconstructed evidence')
