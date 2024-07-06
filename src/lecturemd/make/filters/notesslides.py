#!/usr/bin/env python3

import panflute as pf
import sys

target_format = sys.argv[1]

def filter_notes(elem, doc):
    if not hasattr(elem, "classes"):
        return
    if "slides-only" in elem.classes:
        return []
    return

def filter_slides(elem, doc):
    if not hasattr(elem, "classes"):
        return
    if "notes-only" in elem.classes:
        return []
    return

if __name__ == "__main__":
    if target_format in ["latex", "html", "chunkedhtml"]:
        pf.run_filter(filter_notes)
    elif target_format in ["beamer", "revealjs"]:
        pf.run_filter(filter_slides)
    else:
        raise ValueError(f"Invalid target format {target_format}")