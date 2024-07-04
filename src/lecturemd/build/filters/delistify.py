#!/usr/bin/env python3

import panflute as pf
import logging
import json
# import itertools

# # log to "./filter.log"
# logging.basicConfig(
#     filename="filter.log",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     filemode="w+",
# )

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


def compress_list(elem: pf.BulletList) -> pf.Para:
    """Compress a bullet list into a paragraph."""
    # This is a mess. It definitely feels like there's a better way, but it's not clear from the documentation what that could be.
    if isinstance(elem.parent, pf.ListItem):
        # we don't want to change nested lists
        return elem 
    if hasattr(elem.parent, "classes") and "list" in elem.parent.classes:
        # this should be a list in all document types
        return elem
    # logging.debug(json.dumps(elem.to_json(), indent = 4))
    components = []
    for i, item in enumerate(elem.content):
        content = item.content
        components.extend(content.list)
    components = [c.content.list if isinstance(c, pf.Plain) else c for c in components]
    components = [c for cs in components for c in (cs if isinstance(cs, list) else [cs])]
    components = intersperse(components, pf.Space())
    # remove double spaces
    components = [c for i, c in enumerate(components) if i == 0 or not (isinstance(c, pf.Space) and isinstance(components[i - 1], pf.Space))]
    # logging.debug(components)
    sections = [[]]
    for component in components:
        if isinstance(component, pf.Inline):
            sections[-1].append(component)
        else:
            sections.append(component)
            sections.append([])
    # logging.debug(sections)
    sections[0::2] = [pf.Para(*s) for s in sections[0::2]]
    return sections

def filter(elem, doc):
    if isinstance(elem, pf.BulletList):
        return compress_list(elem)

if __name__ == "__main__":
    pf.run_filter(filter)