#!/usr/bin/env python3

from io import StringIO
from typing import List
import panflute as pf
import sys

target_format = sys.argv[1]

# import logging

# logging.basicConfig(
#     filename="tables.log",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(message)s",
#     filemode="w+",
# )

# logging.debug("-"*80)

# of_interest = [
#     "caption",
#     "colspec",
#     ("parent", type),
#     ("content", lambda x: x[0]),
# ]


import json

def pretty_list(lst) -> str:
    return json.dumps(lst, indent=4)

def colspec_to_alignment(colspec: str) -> str:
    colspec = colspec.replace("Align", "").lower()

    match colspec:
        case "left":
            return "l"
        case "right":
            return "r"
        case "center":
            return "c"
        case "default":
            return "l"
        case _:
            return "l"
        

cell_sep = pf.RawBlock(r" & ", format="latex")
row_sep = pf.RawBlock(r" \\ ", format="latex")

def construct_row(row: List[pf.Element]) -> List[pf.Element]:
    new_row = []
    for cell in row:
        if len(cell.content) == 1:
            new_row.extend(cell.content[0].content)
        else:
            raise ValueError(f"Cell content has more than one Block element: {cell}")
        new_row.append(pf.RawInline(r" & ", format="latex"))
    new_row.pop()
    new_row.append(pf.RawInline(r" \\", format="latex"))
    return pf.Plain(*new_row)


def extract_label(elem: pf.Element) -> tuple[pf.Element, str | None]:

    caption = elem.content[0].content

    if len(caption) == 0:
        return elem, None
    
    last = caption[-1]
    if isinstance(last, pf.Str):
        if last.text.startswith("{#tbl:"):
            label = last.text[2:-1].strip()
            caption.pop()
            # remove the last space
            if isinstance(caption[-1], pf.Space):
                caption.pop()
        else:
            label = None
    else:
        label = None

    # logging.debug(f"Extracted label: {label}\n\tfor caption: {elem}")

    return elem, label


def process_table(elem, doc) -> pf.Element | None:
    table_env = "tblr"
    position = "ht!"
    parent = elem.parent
    floating = False
    if parent.tag == "Div" and len(parent.content) == 1:
        if hasattr(parent, "attributes"):
            attrs = parent.attributes
            table_env = attrs.get("table-env", "tblr")
            position = attrs.get("position", "ht!")
            if "position" in attrs:
                floating = True
        if hasattr(parent, "classes") and "float" in parent.classes:
            floating = True
        # logging.debug(parent)
        
    # logging.debug(f"Table environment: {table_env}")

    headers = elem.head
    footers = elem.foot
    rows = elem.content
    assert len(rows) == 1, "Only one TableBody is expected"
    rows = rows[0]

    caption = elem.caption
    if caption is not None and len(caption.content) > 0:
        floating = True
    colspec = elem.colspec

    table = []

    # tbl_colspec = " ".join(f"X[1, {colspec_to_alignment(col[0])}, t]" for col in colspec)
    tbl_colspec = ",\n    ".join(f"cell{{1-Z}}{{{i + 1}}} = {colspec_to_alignment(col[0])}" for i, col in enumerate(colspec))

    table.append(pf.RawBlock(f"""\\begin{{{table_env}}}{{
    {tbl_colspec}
}}""", format="latex"))
    
    for header in headers.content:
        # logging.debug(construct_row(header.content))
        table.append(construct_row(header.content))    
    
    for row in rows.content:
        table.append(construct_row(row.content))

    for footer in footers.content:
        table.append(construct_row(footer.content))
    
    table.append(pf.RawBlock(f"\\end{{{table_env}}}", format="latex"))

    if floating:
        table.insert(0, pf.RawBlock(f"\\begin{{table}}[{position}]\n    \\centering", format="latex"))

        if caption is not None and len(caption.content) > 0:

            caption, label = extract_label(caption)

            # need to modify the caption content itself rather just adding to the table list
            caption.content[0].content.insert(0, pf.RawInline(r"\caption{", format="latex"))
            caption.content[-1].content.append(pf.RawInline(r"}", format="latex"))
            table.extend(caption.content)

            if label is not None:
                table.append(pf.RawBlock(rf"\label{{{label}}}", format="latex"))

        table.append(pf.RawBlock(r"\end{table}", format="latex"))

    return table

def tables(elem, doc) -> pf.Element | None:
    if isinstance(elem, pf.Table):
        try:
            return process_table(elem, doc)
        except Exception as e:
            # logging.error(e)
            # logging.error(elem)
            raise e




if __name__ == "__main__":
    if target_format in ["latex", "beamer", "json"]:
        pf.run_filter(tables)