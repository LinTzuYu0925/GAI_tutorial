# Build log · Day 4 decks 13–16 (branch build-d4)

One line per step: deck · step · result · next. Re-read after any compaction.

Step definitions (confirmed by the instructor 2026-11-25, since session 1's text was not available):
- **A** = `npm run new-deck` + `outline.md` + `research/sources.md`.
- **B** = lab `.py` → `py2nb` + CPU smoke test (`research/lab-runs.md`) + `slides.md`. Decks 14–15: CPU check = notebook builds + syntax check only.
- **C** = `npm run build`, `export:png` + inspect every PNG, `check-order.cjs`, `scan-zh.py`; then a Colab T4 run via Claude in Chrome while holding the lock `C:\Users\lspss\Documents\t4.lock` (contents: owner `d4` + timestamp; wait if another owner holds it; delete when done). Colab URL uses `blob/build-d4/<path>`.
- **D** = `slide-reviewer` agent → fix → re-export → row in `planning/reviews-d4.md` → commit + push build-d4.

- 2026-11-25 · setup · D4 plans marked auto-approved in planning/slide-plan/D4-image-studio.md; step definitions recorded · next: 13 A (new-deck, outline)
- 2026-11-25 · 13 A · deck scaffolded; outline.md + research/sources.md written · next: 13 B (lab13 smoke test, slides)
- 2026-11-25 · 13 B/C · lab13 smoke-tested (CPU, T=100 and T=30), slides written, build+PNG inspected, check-order ok, scan-zh clean; T4 run started in Colab (lock held) · next: 13 C read T4 outputs; 14 A in parallel
- 2026-11-25 · 14 A · deck scaffolded; outline.md + sources.md; lab14 source written, notebooks build + syntax check pass · next: 14 B slides (while 13 T4 run trains)
- 2026-11-25 · 14 B/C (local) · slides written, PNG inspected + fixes, check-order ok, scan-zh clean; T4 run pending (lock busy with 13) · 15 A · scaffold, outline, sources, lab15 built + syntax ok · next: 13 T4 outputs, 15 slides
- 2026-11-25 · 16 A/B · scaffold, outline, sources, lab16 (CPU smoke: CycleGAN ckpt-load bug fixed, flow toy shows curved paths), slides, docs · 13 C · first T4 run aborted (metrics 6.5 min/w), lab13 fixed + rerun in progress · next: inspect 16 PNGs, read 13 T4 results
- 2026-11-25 12:25 · 13 C · T4 run OK (train 369 s, VRAM 0.95 GB, w=3 fid 97.0%/KID 0.030; all 4 acceptance criteria met); figures captured; lock released · 14–16 D · slide-reviewer 14: 28 FAIL (1b/12M), 15: 18 FAIL (1b/6M), 16: 23 FAIL (0b/10M); fixes applied, re-exported, check-order + scan-zh clean · next: 13 D review; T4 runs 14→16 when lock free
- 16:59 · 14 C · T4 run 1 partial (parts 1–4, 6a captured; mask failed on grey 'white' background → border-colour mask; Colab idled out while session stalled ~4.5 h); session 1 took stale lock 16:57 · next: fill 14, wait for lock, T4 run 2 of lab14, then 15, 16
- 16:59 · 14 C · T4 run 1 partial (parts 1–4, 6a captured; mask failed on grey 'white' background → border-colour mask; Colab idled out while this session stalled ~4.5 h); session 1 took the stale lock at 16:57 · next: wait for lock, T4 run 2 of lab14, then 15, 16
