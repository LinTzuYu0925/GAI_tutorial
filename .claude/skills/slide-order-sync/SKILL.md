---
name: slide-order-sync
description: Re-check and fix everything that depends on slide order after slides are moved, added, or removed in a Slidev deck - eyebrow numbering labels, concept chains and grids, summary tables, outline.md, speaker-note cross-references, and the progress log. Use every time the order of slides changes.
---

# Slide Order Sync Skill

Slide order is encoded in many places besides the file order. After any move, insert, delete, or split of slides, run this skill before reporting the change as done. Do not build or export; this is a static check (the instructor rebuilds).

## When to run

Any change to the order or count of slides in a deck's `slides.md`, including moving a section, deleting a slide, or inserting one.

## Workflow

1. **List the current order.** Run `node .claude/skills/slide-order-sync/check-order.cjs <deck-dir>` (for example `01-pytorch-bridge`). It prints, per slide: number, eyebrow label, title; then the order of concept chips on the cover, nodes on the overview slide, and rows of every summary table; then `outline.md` row titles with a mismatch marker. Treat its output as the checklist, not as the fix.
2. **Decide the intended order** of concepts from the instructor's latest instruction. If the instruction is ambiguous or contradicts itself (for example a verbal "move X" and a numbered list that implies moving Y), follow the explicit numbered list and say which reading you used.
3. **Fix each place** listed below, in this order.
4. **Re-run the script** and confirm every section is consistent. Then run `python -X utf8 scripts/scan-zh.py <deck>`.
5. **Report** the new order, what changed in each place, and any interpretation you chose.

## Places that depend on order

| Place | What to fix |
|---|---|
| Eyebrow labels (`<div class="eyebrow">NN · Topic</div>`) | Number sections in teaching order, same number for every slide of one section, no gaps or duplicates. Unnumbered openers (cover, demo) and closers (summary, quiz, references) stay unnumbered. Sub-topics of a numbered section keep its number and add a suffix (for example `03 · VAE · 重參數化`). Circled sub-numbers (①②③) restart from ① inside a section and follow slide order; remove them from slides that sit outside that section. |
| Cover concept chain | Chip order equals teaching order. Do not highlight (`chip--primary`) a single concept unless the instructor asks. |
| Overview grid (concept nodes) | Same order as the chain. |
| Summary tables | Rows in the same order as the slides they summarize. A section-closing table lists only the techniques that are still inside that section; remove rows for slides moved out and add rows for slides moved in. Keep "given precise information" style rows last. |
| Speaker notes | Fix "上一頁／下一頁／前一頁／前面第 N 頁／後面" references and recap sentences that list concepts in order. Re-read the first and last line of notes on every slide whose neighbors changed. |
| Source lines | Phrases such as "依前五頁整理" must match the new count of pages. |
| `outline.md` | Slide table rows in the new order and renumbered; trimming notes ("只講第 N、M 頁") use the new numbers; any section-range note ("第 13–15 頁") updated. |
| Quiz and recap slides | Check items that depend on order or on pages moving between sections. |
| `research/sources.md` | Only if it cites slide numbers; renumber them. |
| `NOTES.md` | Append one line: what moved, the new label scheme, and files synced. |

## Rules

- Keep slide content unchanged unless a cross-reference forces a wording fix.
- Prefer a small script or `sed` on exact strings over retyping slides; verify the slide separator count (`---` lines) is unchanged after moving blocks. Frontmatter uses two `---`, and a slide that shows a Markdown example may contain more.
- When moving a slide block, cut from its leading `---` separator up to (not including) the next one, so separators never double up or disappear.
- Never change the numbering of one section without checking the sections after it.
- If the instructor's numbered list conflicts with the file (for example two sections both labelled 8), ask only if both readings are plausible and costly; otherwise follow the list and mention it.

## Checklist before finishing

- [ ] (MISMATCH in the outline section only flags different wording; compare the order, not the exact text.)
- [ ] Script output shows eyebrow numbers rising in order with no duplicates (except intended sub-topic suffixes).
- [ ] Cover chain, overview grid, and every summary table match the slide order.
- [ ] No speaker note points to the wrong neighbor page.
- [ ] `outline.md` rows and trimming notes match.
- [ ] `NOTES.md` has the new entry.
- [ ] Simplified-character scan is clean.
