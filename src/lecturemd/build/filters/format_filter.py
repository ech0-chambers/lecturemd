#!/usr/bin/env python3

import panflute as pf
import sys

target_format = sys.argv[1]

def filter_latex(elem, doc):
    if not hasattr(elem, "classes"):
        return
    if "html-only" in elem.classes:
        return []
    return

def filter_html(elem, doc):
    if not hasattr(elem, "classes"):
        return
    if "latex-only" in elem.classes:
        return []
    return

if __name__ == "__main__":
    if target_format in ["latex", "beamer"]:
        pf.run_filter(filter_latex)
    elif target_format in ["html", "chunkedhtml", "revealjs"]:
        pf.run_filter(filter_html)
    else:
        raise ValueError(f"Invalid target format {target_format}")