#!/usr/bin/env python3

import panflute as pf
import sys

target_format = sys.argv[1]

def filter_notes(elem, doc):
    # remove any Rule elements
    if isinstance(elem, pf.HorizontalRule):
        return []

if __name__ == "__main__":
    if target_format in ["latex", "html", "chunkedhtml"]:
        pf.run_filter(filter_notes)
    else:
        raise ValueError(f"Invalid target format {target_format}")