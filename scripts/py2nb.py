"""Build a lab's student and solution notebooks from one percent-format source.

Usage:  python -X utf8 scripts/py2nb.py <deck>/materials/src/labNN-topic.py
Writes: <deck>/materials/labNN-topic.ipynb           (student: TODO blocks emptied)
        <deck>/materials/labNN-topic-solution.ipynb  (solution: full code)

Source format (Jupytext "percent" style, kept in git so diffs are readable):
  # %% [markdown]      markdown cell; following lines start with "# " (stripped)
  # %%                 code cell
  # >>> TODO: 說明      start of a block the student fills in (solution keeps the code)
  # <<< TODO           end of that block
In the student notebook a TODO block becomes "# TODO：說明" followed by "..." so the cell still parses.
"""
import json
import sys
from pathlib import Path


def parse(src: str):
    cells, kind, buf = [], None, []
    for line in src.splitlines():
        if line.startswith("# %%"):
            if kind:
                cells.append((kind, buf))
            kind, buf = ("markdown" if "[markdown]" in line else "code"), []
            continue
        if kind is None:
            continue  # header comments before the first cell
        if kind == "markdown":
            buf.append(line[2:] if line.startswith("# ") else line.lstrip("#"))
        else:
            buf.append(line)
    if kind:
        cells.append((kind, buf))
    return cells


def code_for(lines, student: bool):
    out, in_todo = [], False
    for line in lines:
        s = line.strip()
        if s.startswith("# >>> TODO"):
            in_todo = True
            if student:
                indent = line[: len(line) - len(line.lstrip())]
                hint = s.split(":", 1)[1].strip() if ":" in s else ""
                out.append(f"{indent}# TODO：{hint}")
                out.append(f"{indent}...")
            continue
        if s.startswith("# <<< TODO"):
            in_todo = False
            continue
        if in_todo and student:
            continue
        out.append(line)
    while out and not out[-1].strip():
        out.pop()
    while out and not out[0].strip():
        out.pop(0)
    return out


def notebook(cells, student: bool):
    nb_cells = []
    for kind, lines in cells:
        body = lines if kind == "markdown" else code_for(lines, student)
        while body and not body[-1].strip():
            body = body[:-1]
        text = [l + "\n" for l in body]
        if text:
            text[-1] = text[-1].rstrip("\n")
        cell = {"cell_type": kind, "metadata": {}, "source": text}
        if kind == "code":
            cell.update(execution_count=None, outputs=[])
        nb_cells.append(cell)
    return {
        "cells": nb_cells,
        "metadata": {
            "accelerator": "GPU",
            "colab": {"provenance": [], "gpuType": "T4"},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main(path: str):
    src = Path(path)
    cells = parse(src.read_text(encoding="utf-8"))
    out_dir = src.parent.parent
    stem = src.stem
    for student, name in ((True, f"{stem}.ipynb"), (False, f"{stem}-solution.ipynb")):
        (out_dir / name).write_text(
            json.dumps(notebook(cells, student), ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
    # Syntax check of the solution code (shell and magic lines removed).
    code = "\n".join(
        l for k, ls in cells if k == "code" for l in code_for(ls, False) if not l.lstrip().startswith(("!", "%"))
    )
    compile(code, str(src), "exec")
    print(f"{out_dir / stem}.ipynb and -solution.ipynb written ({len(cells)} cells); solution code compiles")


if __name__ == "__main__":
    main(sys.argv[1])
