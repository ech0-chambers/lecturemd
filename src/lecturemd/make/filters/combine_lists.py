#!/usr/bin/env python3

from io import StringIO
from typing import Any, List
import panflute as pf
import sys

target_format = sys.argv[1]

# import logging

# logging.basicConfig(
#     filename="combine_lists.log",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     filemode="w+",
# )

# logging.debug("-"*80)

def combine_lists(elem, doc) -> pf.Element | None:
    if isinstance(elem, pf.Div) and hasattr(elem, "classes") and "combine-lists" in elem.classes:
        # this div contains multiple slides which contain lists. Combine all lists into one.
        children = elem.content
        elem_type = children[0].__class__
        if not elem_type in [pf.BulletList, pf.OrderedList, pf.DefinitionList]:
            # logging.error(f"Element type {elem_type.__name__} is not supported.")
            return
        for child in children:
            if not isinstance(child, elem_type):
                # logging.error(f"Child element type {child.__class__.__name__} is not the same as the first child element type {elem_type.__name__}.")
                return
        new_list = []
        for child in children:
            new_list.extend(child.content)
        return children[0].__class__(*new_list)

if __name__ == "__main__":
    if target_format in ["latex", "html", "chunkedhtml"]:
        pf.run_filter(combine_lists)