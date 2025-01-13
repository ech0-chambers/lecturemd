#!/usr/bin/env python3

import panflute as pf
import sys

target_format = sys.argv[1]

# import logging

# # log to examples.log
# logging.basicConfig(filename='examples.log', level=logging.DEBUG)

def reveal_example(elem, doc):
    if hasattr(elem, "classes") and "example" in elem.classes:
        if target_format == "revealjs":
            # just return the div's contents
            # logging.debug(f"Received {elem}")
            # logging.debug(f"Returning {[*elem.content]}")
            return [*elem.content]

def beamer_example(elem, doc):
    if hasattr(elem, "classes") and "example" in elem.classes:
        # get the example name from args
        args = elem.attributes
        if 'args' in args:
            args = args['args']
        else:
            args = ""
        if args:
            example_name = args.lstrip("[").rstrip("]")
        else:
            example_name = ""
        if target_format == "beamer":
            begin = pf.RawBlock(r"\begin{example}[" + example_name + "]", format="latex")
            end = pf.RawBlock(r"\end{example}", format="latex")
            # logging.debug(f"Received {elem}")
            # logging.debug(f"Returning {[begin, *elem.content, end]}")
            return [begin, *elem.content, end]
        
if __name__ == "__main__":
    if target_format == "beamer":
        pf.run_filter(beamer_example)
    elif target_format == "revealjs":
        pf.run_filter(reveal_example)