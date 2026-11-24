# Build log · Day 3 decks 11–12 (branch build-d3)

One line per step: deck · step · result · next. Re-read after any compaction.

- 2026-11-25 · setup · D3-3/D3-4 plans marked auto-approved in planning/slide-plan/D3-gan-vs-diffusion.md · next: 11 A (new-deck, outline)
- 2026-11-25 · 11 · A build · outline (auto-approved, 30 slides), slides.md, NOTES, teaching-plan, sources, lab11 source + py2nb; CPU smoke test passes (245 s) · next: CPU quality check (3 epochs), then 11 B commit/push + T4 run
- 2026-11-25 · 12 · A build (early, while 11 waits) · new-deck, slides (28), outline, NOTES, teaching-plan, sources, lab12 + py2nb; CPU smoke passes after utf-8 fix · next: wait for 11 CPU quality check, then 11 B
- 2026-11-25 · 11 · A quality check · 3-epoch CPU run gives recognisable multi-class samples (pairwise 21.32) → keep EPOCHS=20 for T4 · next: 11 B commit/push, lock, T4 subagent
