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

def generic_handler(environment: str, content: pf.Element, args: str) -> pf.Element:
    title = args.lstrip("[").rstrip("]")
    title_div = pf.Div(pf.Para(pf.Str(title)), classes=["title"])
    content_div = pf.Div(content, classes=["content"])
    return pf.Div(title_div, content_div, classes=["tcolorbox", environment])

def example_handler(content: pf.Element, args: str) -> pf.Element:
    return generic_handler("example", content, args)

def definition_handler(content: pf.Element, args: str) -> pf.Element:
    return generic_handler("definition", content, args)

def aside_handler(content: pf.Element, args: str) -> pf.Element:
    return generic_handler("aside", content, args)

handlers = {
    "example": example_handler,
    "definitionbox": definition_handler,
    "aside": aside_handler,
}


def filter(elem, doc):
    if target_format not in ["html", "chunkedhtml", "revealjs"]:
        return
    if not hasattr(elem, "classes") or not "latex-env" in elem.classes:
        return
    logging.debug(f"Handling {elem} with classes {elem.classes}")
    index = elem.classes.index("latex-env")
    if index + 1 >= len(elem.classes):
        return
    env = elem.classes[index + 1]
    args = elem.attributes
    if 'args' in args:
        args = args['args']
    else:
        args = ""
    if env in handlers:
        return handlers[env](elem, args)
    

if __name__ == "__main__":
    pf.run_filter(filter)