# Build log · Day 3 decks 11–12 (branch build-d3)

One line per step: deck · step · result · next. Re-read after any compaction.

- 2026-11-25 · setup · D3-3/D3-4 plans marked auto-approved in planning/slide-plan/D3-gan-vs-diffusion.md · next: 11 A (new-deck, outline)
- 2026-11-25 · 11 · A build · outline (auto-approved, 30 slides), slides.md, NOTES, teaching-plan, sources, lab11 source + py2nb; CPU smoke test passes (245 s) · next: CPU quality check (3 epochs), then 11 B commit/push + T4 run
- 2026-11-25 · 12 · A build (early, while 11 waits) · new-deck, slides (28), outline, NOTES, teaching-plan, sources, lab12 + py2nb; CPU smoke passes after utf-8 fix · next: wait for 11 CPU quality check, then 11 B
- 2026-11-25 · 11 · A quality check · 3-epoch CPU run gives recognisable multi-class samples (pairwise 21.32) → keep EPOCHS=20 for T4 · next: 11 B commit/push, lock, T4 subagent
- 2026-11-25 00:56 · 11 · B1-B2 · committed+pushed 3ec0559; took t4.lock · next: T4 subagent run of lab11-ddpm-solution
- 2026-11-25 10:57 · 11 · B3 · first subagent attempt stopped: two extension browsers, Edge unidentified; user chose Browser 1; subagent resumed · next: wait for T4 results
- 2026-11-25 11:18 · 11 · B3-B4 · T4 run OK (T4, ~10 min; train 477 s, loss 0.0334, VRAM 1.07 GB); runtime deleted; lock removed. Problems: DDIM worse with more steps (250 = noise); DDPM pairwise 16.41 < DCGAN 22.08 · next: debug DDIM locally with T4 checkpoint
- 2026-11-25 11:31 · 11 · B fix · DDIM bug = DDIMScheduler clip_sample=True (fixed: False; lab12 clamp removed); pairwise low due to thin/dark samples, not class loss (added classifier class-count cell); CPU smoke OK · next: commit/push, lock, T4 run 2 of lab11
