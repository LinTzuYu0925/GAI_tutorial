"""Protect shape brackets like [B, 3, 32, 32] from Slidev's MDC parser.

With `mdc: true`, a bare `[text]` in slide markdown is parsed as an MDC span and the
brackets vanish in the render ("B, C, H, W"). This rewrites such brackets to the HTML
entities &#91; &#93;, which render as [ ] both in markdown and inside raw HTML.

Skipped: frontmatter, fenced code, inline `code`, KaTeX math ($...$, $$...$$), HTML comments (speaker notes),
lines with Vue components (attribute values), and markdown links `[x](url)`.

Usage: python -X utf8 scripts/fix-brackets.py <deck> [<deck> ...]
"""
import re
import sys
from pathlib import Path

SHAPE = re.compile(r"\[([^\[\]\n`]{1,60})\](?![(\{:])")


def fix_text(seg):
    return SHAPE.sub(lambda m: f"&#91;{m.group(1)}&#93;", seg)


def fix_line(line):
    parts = re.split(r"(`[^`]*`|<[^>]*>|\$\$.*?\$\$|\$[^$\n]+\$)", line)   # keep inline code, HTML tags (class="grid-cols-[...]") and KaTeX math untouched
    return "".join(p if p.startswith(("`", "<", "$")) else fix_text(p) for p in parts)


def run(deck):
    path = Path(deck) / "slides.md"
    lines = path.read_text(encoding="utf-8").split("\n")
    out, fence, comment, front, n = [], False, False, False, 0
    for i, line in enumerate(lines):
        s = line.strip()
        if s == "---":
            # a '---' starts frontmatter when the next non-empty line looks like 'key: value'
            nxt = next((l for l in lines[i + 1:i + 3] if l.strip()), "")
            front = not front and bool(re.match(r"^[A-Za-z]+:", nxt)) if not front else False
            out.append(line); continue
        if front or s.startswith("```"):
            fence = (not fence) if s.startswith("```") else fence
            out.append(line); continue
        if fence:
            out.append(line); continue
        if "<!--" in s:
            comment = "-->" not in s
            out.append(line); continue
        if comment:
            comment = "-->" not in s
            out.append(line); continue
        if re.search(r"<[A-Z][A-Za-z]+", line):     # Vue component props
            out.append(line); continue
        new = fix_line(line)
        n += new != line
        out.append(new)
    path.write_text("\n".join(out), encoding="utf-8", newline="\n")
    print(f"{deck}: {n} lines changed")


for d in sys.argv[1:]:
    run(d)
