#!/usr/bin/env python3

from io import StringIO
from typing import Any, List
import panflute as pf
import sys

target_format = sys.argv[1]

# import logging

# logging.basicConfig(
#     filename="definitions.log",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     filemode="w+",
# )

# logging.debug("-"*80)

# def log_props(obj: Any) -> None:
#     logging.debug(f"Properties of {obj}:\n\t" + "\n\t".join(i for i in dir(obj) if not i.startswith("_")))


desc_env = "descriptions"

def process_definitions(elem: pf.DefinitionList, doc: pf.Doc) -> pf.Element:
    # logging.debug(f"Found definition list: {elem}")
    definitions = elem.content
    out = []
    out.append(pf.RawInline(rf"\begin{{{desc_env}}}" + "\n", format="latex"))
    for i, entry in enumerate(definitions):
        term = entry.term
        # logging.debug(f"Term: {term}")
        definition = entry.definitions
        # logging.debug(f"Definition: {definition}")
        row = []
        row.extend(term)
        row.append(pf.RawInline(r" | ", format="latex"))
        if len(definition) == 1:
            definition = definition[0].content
            # logging.debug(f"Definition content: {definition}")
            if len(definition) == 1:
                row.extend(definition[0].content)
            else:
                raise NotImplementedError(f"Definition content has more than one Block element: {definition}")
        else:
            raise NotImplementedError(f"Definition content has more than one Block element: {definition}")
        if i < len(definitions) - 1:
            row.append(pf.RawInline(r" \\" + "\n", format="latex"))
        # logging.debug(f"Row: {row}")
        out.extend(row)
    out.append(pf.RawInline("\n" + rf"\end{{{desc_env}}}", format="latex"))
    return pf.Plain(*out)


def definitions(elem, doc) -> pf.Element | None:
    if isinstance(elem, pf.DefinitionList):
        try:
            return process_definitions(elem, doc)
        except Exception as e:
            # logging.error(e)
            # logging.error(elem)
            raise e


if __name__ == "__main__":
    if target_format in ["latex", "beamer", "json"]:
        pf.run_filter(definitions)