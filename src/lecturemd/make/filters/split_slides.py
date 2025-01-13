#!/usr/bin/env python3

import panflute as pf
import sys

target_format = sys.argv[1]


"""
A filter that splits divs into multiple instances with the same classes, delimited by a horizontal rule. For example,
```markdown
:::{.split-on-slides .latex-env .center}

Some content

---

Some other content

:::
```

will be transformed into

```markdown
:::{.latex-env .center}

Some content

:::

---

:::{.latex-env .center}

Some other content

:::
```
"""

# import logging


def split_on_slides(elem, doc):
    if isinstance(elem, pf.Div) and (
        "split-on-slides" in elem.classes
        or ("split-on-reveal" in elem.classes and target_format == "revealjs")
        or ("split-on-beamer" in elem.classes and target_format == "beamer")
    ):
        new_elems = []
        current_elems = []
        for child in elem.content:
            if isinstance(child, pf.HorizontalRule):
                new_elems.append(
                    pf.Div(
                        *current_elems, classes=elem.classes, attributes=elem.attributes
                    )
                )
                new_elems.append(pf.HorizontalRule())
                current_elems = []
            else:
                current_elems.append(child)
        new_elems.append(
            pf.Div(*current_elems, classes=elem.classes, attributes=elem.attributes)
        )
        # logging.debug(elem)
        # logging.debug(new_elems)
        return new_elems

if __name__ == "__main__":
    # log to `splitslides.log` file
    # logging.basicConfig(
    #     filename="splitslides.log",
    #     level=logging.DEBUG,
    #     filemode="w+",
    #     format="%(asctime)s - %(levelname)s - %(message)s",
    # )
    # logging.debug("Running split_slides filter")
    if target_format in ["beamer", "revealjs"]:
        pf.run_filter(split_on_slides)
