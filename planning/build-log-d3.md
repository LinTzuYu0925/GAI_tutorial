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
- 2026-11-25 11:31 · 11+12 · B2 · t4.lock held by d4 (lab13, since 11:22); background watcher re-checks every 10 min · next: one lock hold for lab11 run 2 + lab12 run 1
- 2026-11-25 16:57 · 11+12 · B2 · d4 lock (lab14, since 12:19) was 4h38m old = stale per 2 h rule; took t4.lock · next: subagent runs lab11 (run 2) then lab12 on T4
- 2026-11-25 18:57 · 11+12 · B3-B4 · T4 OK: lab11 run 2 (train 470 s, pairwise 17.42, 10/10 classes, DDIM fixed); lab12 run 1 (best t=100, DDIM 5; test AE AUROC 0.944/over-kill 16.6% vs diffusion 0.930/36.4%: diffusion did NOT beat AE); runtimes deleted, lock removed · next: 11 C (put outputs on slides, QA)
- 2026-11-26 · 11 · C (local) · T4 run 2 images and numbers on every placeholder slide; honest result on Lab 7, trilemma and Ship (pairwise 17.42 < DCGAN 22.08, but 10/10 classes); sampling and DDIM slides re-laid out with cropped recorded figures; lab11 nearest-plot label overlap fixed (cosmetic, no rerun); build, PNG inspection, check-order, scan-zh clean · next: 11 D (slide-reviewer)
- 2026-11-26 · 12 · C (local) · T4 run 1 images and numbers on all slides; narrative rewritten to the measured result (test AUROC AE 0.944 vs diffusion 0.930, over-kill 16.6% vs 36.4%: KPI not met, AE wins); t=100 / DDIM 5 from the val sweep; operator view uses a real test board; Day 3 summary row updated; outline lab rows filled; build, PNG inspection, check-order, scan-zh clean · next: 12 D (slide-reviewer)
- 2026-11-26 · 11+12 · D · slide-reviewer: 11 → 17 FAIL (0b/5M/12m), 12 → 19 FAIL (1b/8M/10m); all fixed, PNGs re-exported and inspected, check-order + scan-zh clean; planning/reviews-d3.md · next: push main; instructor checks legal article numbers
