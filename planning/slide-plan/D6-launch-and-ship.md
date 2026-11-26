# Day 6 slide plan · 「上市與交付」

> **Status:** auto-approved 2026-11-26 by the instructor (build of decks 17–24); written 2026-11-23, phase 3 of the earlier /goal.
> **Source:** [course_roadmap.md](../course_roadmap.md) §7 Day 6, §9 L6-1…L6-3, §12 (assessment). Compact slide tables as in [D2-factory-qa.md](D2-factory-qa.md).
> **Decks:** D6-1 `21-music-and-voice` · D6-2 `22-catalog-search` · D6-3 `23-ship-clinic` · D6-4 `24-demo-day`.

**Day goal.** A student can generate royalty-aware music and voice-over and explain audio tokens, build a 繁中 text→image catalog search with zero-shot tags and VLM alt-text, pass a launch compliance checklist, package the capstone (Gradio app, model card, GitHub push) and present it in 3 minutes. The 學習評量 memo and notebook are submitted.

---

## D6-1 · Marketing: 「活動影片需要免版稅配樂和旁白」 (#14 → MusicGen) → `21-music-and-voice`

```
【需求單 #D6-1】部門：行銷部（虛構公司：曜嶼電子）
問題：           活動影片需要免版稅配樂與國語旁白
現況痛點：       買版權音樂貴，授權條款複雜
成功指標（KPI）： 聽感測試；生成時間與片長的關係；授權說明
可用資料：       文字提示；旁白稿
限制與法規：     MusicGen 權重為非商用授權；聲音複製需當事人同意
為何現有工具不夠： 影像與文字模型不會產生聲音
今天要用的工具：  MusicGen-small、台灣口音 TTS（授權待確認）
```

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: licensing is the real constraint | ★ | — | Licence table | §9.2 |
| 5 | Try: MusicGen-small | ★ | Prompt → jingle | Audio placeholder | L6-1 |
| 6 | Audio basics: sample rate, waveform, spectrogram | ★ | — | Picture | — |
| 7 | Codec tokens (EnCodec) | ★ | Recall D2-4 | Diagram | D2-4 |
| 8 | MusicGen = Transformer over audio tokens + text conditioning | ★ | Same as GPT, new vocabulary | Diagram | D5-2 |
| 9 | Practice: tokens per second of audio | ★ | Arithmetic | FillIn | — |
| 10 | Answer (hostOnly) | ★ | — | — | — |
| 11 | Why 「MusicNet」 became MusicGen | ★ | MusicNet is a dataset | Note | curriculum-analysis |
| 12 | TTS overview: text → acoustic tokens → waveform | ★ | — | Pipeline | — |
| 13 | The licence lesson: NC weights | ★ | Demo vs product | — | §14 |
| 14 | Consent for voice cloning | ★ | — | — | — |
| 15 | Melody conditioning; commercial alternatives | ○ | Terms to verify | — | — |
| 16 | Codebook interleaving (delay pattern) | △ | — | — | — |
| 17–21 | Lab L6-1 (Try lab, 4-page) | ★ | Prompt and duration sweeps; TTS demo | `lab21-music-voice.ipynb` | L6-1 |
| 22 | Risk: music copyright, voice consent, deepfake audio | ★ | — | — | — |
| 23–25 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

## D6-2 · E-commerce: 「一萬張沒有標籤的商品照，顧客用中文搜尋」 (K8) → `22-catalog-search`

```
【需求單 #D6-2】部門：電商部（虛構公司：曜嶼電子）
問題：           一萬張沒有標籤的商品照，顧客用中文搜尋
現況痛點：       只能靠檔名搜尋，找不到就不會買
成功指標（KPI）： 小型標註集上的 precision@k；繁中替代文字的品質
可用資料：       課程商品照集（自有或 CC0）
限制與法規：     Colab T4；零樣本標籤的偏差
為何現有工具不夠： 分類器只認得訓練過的類別；英文 CLIP 不懂中文
今天要用的工具：  多語 CLIP 類模型（SigLIP 2 等級）、小型 VLM
```

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: search by meaning | ★ | — | Filename vs meaning | — |
| 5 | Try: zero-shot tags | ★ | Text prompts as classes | Tag table (from lab) | L6-2 |
| 6 | Contrastive embeddings recap | ★ | One space, cosine similarity | Picture | D4-2 |
| 7 | Applied search: embed catalog, embed query, top-k | ★ | — | Code | — |
| 8 | Choosing a multilingual model | ★ | OpenAI CLIP is English-only; SigLIP 2 class | Comparison table (licences to verify) | §9.2 |
| 9 | Practice: precision@k by hand | ★ | — | FillIn | — |
| 10 | Answer (hostOnly) | ★ | — | — | — |
| 11 | VLM captioning for alt-text and SEO | ★ | Image → 繁中 text | Placeholder | L6-2 |
| 12 | Video generation overview | ○ | — | — | — |
| 13 | Vector databases | △ | Text-to-SQL module | — | §13 |
| 14–20 | Lab L6-2 pages 1–7 | ★ | Search app + zero-shot tags + alt-text | `lab22-catalog-search.ipynb` | L6-2 |
| 21 | Risk: tag bias; misleading captions | ★ | — | — | — |
| 22–24 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

## D6-3 · Compliance & Ops: ship clinic (K9, K10, goals 9/11) → `23-ship-clinic`

First 30 minutes are slides (★); the remaining 90 minutes are individual build time with instructor help.

| # | Title | Mark | Takeaway | Content / visual | Cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket (法遵部) · Objectives | ★ | Every prototype passes the checklist before demo | — | — |
| 4 | Checklist 1: licences of code, weights, data | ★ | — | Table | D1-4 |
| 5 | Checklist 2: copyright and consent | ★ | — | — | D4-3 |
| 6 | Checklist 3: deepfake / AI-content disclosure; watermarking and C2PA | ★ | — | — | D3-4 |
| 7 | Checklist 4: 個資法 and AI 基本法 (status to verify) | ★ | — | — | §4 |
| 8 | Checklist 5: prompt injection | ★ | — | — | D5-4 |
| 9 | Checklist 6: cost and latency budget; edge notes (quantisation, distillation) | ★ | — | — | D5-3 |
| 10 | Practice: run the checklist on your capstone | ★ | FillIn checklist | FillIn | — |
| 11 | Packaging: Gradio Blocks app | ★ | — | Code | D1-4 |
| 12 | Model card | ★ | — | Template | D1-4 |
| 13 | GitHub remote push (goal 11) | ★ | Local Git from Vibe 02/07a + remote | Steps | Vibe 07a |
| 14 | HF Hub push or Colab share link | ★ | — | Steps | — |
| 15 | HF Spaces free-tier limits | ○ | — | — | — |
| 16 | Monitoring in production | △ | Agent #10 | — | §13 |
| 17 | Build time: what "done" looks like | ★ | App + card + push + 3-min script | Checklist | — |

## D6-4 · CEO office: demo day (all) → `24-demo-day`

| # | Title | Mark | Takeaway | Content / visual | Cite |
|---|---|---|---|---|---|
| 1–2 | Cover · Format | ★ | 3 minutes: ticket → model choice → demo → one metric → one risk/cost | Timer card | §12 |
| 3 | Running order (or recorded-demo selection if the class is large) | ★ | — | — | §14 open item |
| 4 | Submit the 學習評量 | ★ | Memo + L4-1 notebook + oral CFG check | Checklist | §12 |
| 5 | Final iPAS-style quiz (10) | ★ | — | MCQ | goal 10 |
| 6 | Course recap: the six-step loop | ★ | — | Loop diagram | D1-1 |
| 7 | Course recap: the trilemma | ★ | — | Triangle with class evidence | D3, D4 |
| 8 | Hand-off: tool calling, MCP, RAG → next module | ★ | — | Hand-off table | §13 |
| 9 | 下一步 (hostOnly) | ★ | Agent module preview | — | — |

Assessment rubrics: roadmap §12 (memo 40/30/20/10; capstone 20/25/20/15/20).
