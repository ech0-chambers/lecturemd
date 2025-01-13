#!/usr/bin/env python3

import panflute as pf
import sys

target_format = sys.argv[1]



def pause_before(elem, doc):
    if hasattr(elem, "classes") and "pause-before" in elem.classes:
        if target_format == "beamer":
            if "only" in elem.classes:
                return [pf.RawBlock("\\only<+->{", format="latex"), elem, pf.RawBlock("}", format="latex")]
            return [pf.RawBlock("\\uncover<+->{", format="latex"), elem, pf.RawBlock("}", format="latex")]
        if target_format == "revealjs":
            elem.classes.remove("pause-before")
            elem.classes.append("fragment")
            elem.classes.append("fade-in")
            return
        
        # add fragment to each non-header row in tables
    if isinstance(elem, pf.TableBody) and target_format == "revealjs":
        for row in elem.content:
            if isinstance(row, pf.TableRow):
                row.classes.append("fragment")
                row.classes.append("fade-in")
    

if __name__ == "__main__":
    if target_format in ["beamer", "revealjs"]:
        pf.run_filter(pause_before)
    