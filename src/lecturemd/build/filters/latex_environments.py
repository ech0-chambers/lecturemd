#!/usr/bin/env python3

import panflute as pf
import sys
import logging

# log to "./filter.log"
logging.basicConfig(
    filename="filter.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="w+",
)


target_format = sys.argv[1]

def handle_environment(elem):
    index = elem.classes.index("latex-env")
    if index + 1 >= len(elem.classes):
        return
    env = elem.classes[index + 1]
    args = elem.attributes
    if 'args' in args:
        args = args['args']
    else:
        args = ""
    inline = isinstance(elem, pf.Inline)
    raw_constructor = pf.RawBlock if not inline else pf.RawInline
    pre = raw_constructor(r"\begin{" + env + "}" + args, format="latex")
    post = raw_constructor(r"\end{" + env + "}", format="latex")
    return [pre, elem, post]

def handle_macro(elem):
    index = elem.classes.index("latex-macro")
    if index + 1 >= len(elem.classes):
        return
    macro = elem.classes[index + 1]
    args = elem.attributes
    # Assume that the contents of the span is the final mandatory argument
    if 'args' in args:
        args = args['args']
    else:
        args = ""
    inline = isinstance(elem, pf.Inline)
    raw_constructor = pf.RawBlock if not inline else pf.RawInline
    pre = raw_constructor("\\" + macro + args + "{", format="latex")
    post = raw_constructor("}", format="latex")
    return [pre, elem, post]

def filter(elem, doc):
    if target_format not in ["latex", "beamer"]:
        return
    if hasattr(elem, "classes") and "latex-env" in elem.classes:
        return handle_environment(elem)

    if hasattr(elem, "classes") and "latex-macro" in elem.classes:
        return handle_macro(elem)
    
    
if __name__ == "__main__":
    pf.run_filter(filter)