# Day 5 slide plan · 「客服中心」

> **Status:** auto-approved 2026-11-26 by the instructor (build of decks 17–24); written 2026-11-23, phase 3 of the earlier /goal.
> **Source:** [course_roadmap.md](../course_roadmap.md) §7 Day 5, §9 L5-1…L5-4, §11, §13 (hand-off to the Agent module). Compact slide tables as in [D2-factory-qa.md](D2-factory-qa.md).
> **Decks:** D5-1 `17-tokens-attention-bridge` · D5-2 `18-mini-gpt` · D5-3 `19-api-vs-self-host` · D5-4 `20-qlora-sft`.
> **Scope boundary:** tool calling, MCP, RAG, streaming, schema-enforced output and CoT/ToT are named only and deferred to the Agent module (CLAUDE.md).

**Day goal.** A student can estimate token cost for 繁中 tickets, compute attention by hand (the sequence→attention bridge the DL course did not teach), train a mini character-level GPT and explain sampling, choose between a cloud API and a self-hosted 4-bit model with a JSON-output triage assistant, and run a QLoRA SFT with a before/after eval.

---

## D5-1 · Support: 「每天 2,000 張繁中客服單：用 LLM 要花多少？為什麼字序很重要？」 (#12, #2) → `17-tokens-attention-bridge`

```
【需求單 #D5-1】部門：客服中心（虛構公司：曜嶼電子）
問題：           每天 2,000 張繁中客服單，交給 LLM 處理每月要花多少？
現況痛點：       沒人算過 token；繁中比英文貴多少也不知道
成功指標（KPI）： 每月成本估算；注意力熱力圖指向關鍵字
可用資料：       合成繁中客服單（講師製作）
限制與法規：     不能把真實客服單送到免費 API（個資法）
為何現有工具不夠： 詞袋模型分不出「不是不好」和「不好」
今天要用的工具：  tokenizer、從零寫的注意力
```

Objectives: count tokens with 2–3 tokenizers and estimate cost; explain embeddings as a lookup table; explain why order matters, the RNN and seq2seq bottlenecks; compute single-head attention (Q, K, V, softmax, √d) by hand and in code.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: cost = tokens × price | ★ | — | Formula + monthly arithmetic | Vibe 01 |
| 5 | Try: the same ticket, three tokenizers | ★ | 繁中 often costs more tokens | Token table (from lab) | L5-1 |
| 6 | BPE in one picture | ★ | Frequent pieces merge | Merge steps | — |
| 7 | Practice: estimate the monthly bill | ★ | FillIn with own counts | FillIn | L5-1 |
| 8 | Answer (hostOnly) | ★ | — | — | — |
| 9 | Embeddings: a lookup table | ★ | Token ID → row → vector; similar words close | Table picture | D2-4 tokens |
| 10 | Bridge 1: bag-of-words fails on 「不是不好」 | ★ | Order carries meaning | Two sentences, same bag | — |
| 11 | Bridge 2: RNN reads word by word | ★ | One memory vector → bottleneck | One diagram | DL pp.7, 29 |
| 12 | Bridge 3: seq2seq squeezes a sentence into one vector | ★ | Long sentences lose detail | Diagram | — |
| 13 | Bridge 4: attention looks back at every word | ★ | Soft lookup with weights | Picture | — |
| 14 | Q, K, V: query vs keys → softmax → weighted values | ★ | Dot product, softmax, weighted sum | Tiny 3-word matrix worked by hand | DL p.16 |
| 15 | Why divide by √d | ★ | Keeps softmax from saturating | One line | — |
| 16 | Practice: attention by hand | ★ | 3×3 toy, compute weights | FillIn | L5-1 |
| 17 | Answer (hostOnly) | ★ | — | — | — |
| 18 | LSTM/GRU gates | ○ | Named only (official roadmap item) | — | — |
| 19 | Bahdanau history | △ | — | — | — |
| 20–22 | Lab L5-1 (bridge 3-page pattern) | ★ | Token-cost calculator + attention heatmap | `lab17-tokens-attention.ipynb` | L5-1 |
| 23 | Risk: 個資法 | ★ | Synthetic tickets only | — | — |
| 24–26 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L5-1 (`lab17-tokens-attention.ipynb`, ~40 min, CPU fine): token counts and monthly cost; attention from scratch on toy sentences with a heatmap.

---

## D5-2 · Support: 「模型到底怎麼『寫』出一封回覆？」 (#12, #13, #2) → `18-mini-gpt`

```
【需求單 #D5-2】部門：客服中心（虛構公司：曜嶼電子）
問題：           把回覆交給模型寫之前，要先懂它怎麼「寫」
現況痛點：       主管不信任黑盒子
成功指標（KPI）： loss 曲線下降；樣本品質與溫度、top-k、top-p 的關係
可用資料：       合成繁中客服回覆語料（課程製作）
限制與法規：     Colab T4；小模型
為何現有工具不夠： D5-1 只有一層注意力，還不會生成
今天要用的工具：  Transformer block、迷你字元 GPT、一個 0.5–1.5B 開放模型
```

Objectives: draw the Transformer block (multi-head attention, causal mask, positional encoding, residual + LayerNorm); place BERT/T5/GPT on the encoder/decoder map; read next-token cross-entropy as maximum likelihood; use temperature/top-k/top-p; explain the KV cache; DiT payoff.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: writing = next token, repeated | ★ | Recall D1-2 | Loop picture | D1-2 |
| 5 | Try: top-k next tokens of a real small model | ★ | — | Bar chart (from lab) | L5-2 B |
| 6 | Multi-head attention | ★ | Several lookups in parallel | Picture | D5-1 |
| 7 | Causal mask | ★ | No peeking at the future | Triangle matrix | — |
| 8 | Positional encoding (sinusoidal; RoPE named) | ★ | Same idea as the D3-3 time embedding | Stripe picture | D3-3 |
| 9 | Residual + LayerNorm = the block | ★ | Block diagram | Diagram | DL ResNet |
| 10 | Practice: shapes through one block | ★ | No-AI checkpoint | FillIn | L5-2 |
| 11 | Answer (hostOnly) | ★ | — | — | — |
| 12 | Encoder / encoder–decoder / decoder | ★ | BERT, T5, GPT | Map | — |
| 13 | Next-token cross-entropy = maximum likelihood | ★ | In words + loss curve | Curve (from lab) | DL pp.25–27, D1-3 ○ |
| 14 | Temperature, top-k, top-p | ★ | Three knobs on the same distribution | Bars | D1-2 |
| 15 | KV cache | ★ | Reuse past keys/values → faster | Picture | — |
| 16 | DiT payoff | ★ | 「現在換 Transformer 來畫圖」 | Diagram | D4-2 |
| 17 | GQA/MQA; context cost | ○ | Named | — | — |
| 18 | Attention complexity math | △ | — | — | — |
| 19–25 | Lab L5-2 pages 1–7 | ★ | Mini char-GPT + real model logits | `lab18-mini-gpt.ipynb` | L5-2 |
| 26 | Risk: fluent ≠ correct | ★ | Hallucination preview | — | — |
| 27–29 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L5-2 (`lab18-mini-gpt.ipynb`, ~60 min): character-level GPT on the course 繁中 reply corpus (fallback checkpoint); sampling sweeps; top-k logits of Qwen2.5-0.5B/1.5B-Instruct (licence per size to verify).

---

## D5-3 · IT/Legal: 「雲端 API 還是自架模型？成本、個資法、延遲」 (K6, goal 9) → `19-api-vs-self-host`

```
【需求單 #D5-3】部門：資訊部／法務（虛構公司：曜嶼電子）
問題：           客服單分類要用雲端 API 還是自架開放模型？
現況痛點：       法務擔心個資外流；資訊部擔心成本與延遲
成功指標（KPI）： 每 1,000 張的成本、延遲、品質評分；有效 JSON 比例
可用資料：       合成繁中客服單
限制與法規：     個資法、資料落地；免費方案提示可能被再利用；開放權重授權依大小不同
為何現有工具不夠： D1-2 只做過一次呼叫，沒有比較與結構化輸出
今天要用的工具：  Claude API（anthropic SDK）、transformers generate、4-bit（bitsandbytes）
```

Objectives: read an SDK call's anatomy and its token usage; request JSON in the prompt, parse with `json.loads`, retry on failure; generate with `transformers`; load in 4-bit and do the VRAM arithmetic; fill the open-vs-closed decision table.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: the decision table | ★ | Cost, privacy, licence, latency, quality | Empty table filled by the end | D1-1 |
| 5 | Try: SDK call anatomy | ★ | messages, system, max_tokens, usage | Code + reading | Vibe 11–12, D1-2 |
| 6 | Token usage → cost per 1,000 tickets | ★ | Arithmetic from `usage` | Worked example | D5-1 |
| 7 | JSON via prompt + json.loads + retry | ★ | Validate, don't trust | Code | — |
| 8 | Practice: will this parse? | ★ | Predict which outputs break json.loads | FillIn | L5-3 |
| 9 | Answer (hostOnly) | ★ | — | — | — |
| 10 | transformers `generate` + chat templates | ★ | Same task, self-hosted | Code | D5-4 preview |
| 11 | Quantisation = fewer bits per weight | ★ | 4-bit ≈ 0.5 byte/param | D1-4 arithmetic extended | D1-4, DL pp.67–72 |
| 12 | Practice: VRAM at fp16 vs 4-bit | ★ | 7B fits after all | FillIn | D1-4 practice |
| 13 | Answer (hostOnly) | ★ | — | — | — |
| 14 | Ollama/GGUF on a laptop; TTFT | ○ | Instructor demo | — | — |
| 15 | NF4, GPTQ, AWQ | △ | Named | — | — |
| 16 | Deferred to the Agent module | ★ | Streaming, schema-enforced output, tool calling | Hand-off box | roadmap §13 |
| 17–23 | Lab L5-3 pages 1–7 | ★ | Same triage three ways | `lab19-triage.ipynb` | L5-3 |
| 24 | Ship: triage assistant (Day 5 ship) | ★ | Gradio | Screenshot placeholder | — |
| 25 | Risk: residency, prompt reuse, licence by size | ★ | — | Table | §9.2 |
| 26–28 | Summary · 隨堂檢核 · 下一步 (hostOnly) | ★ | — | MCQ ×4 | — |

Lab L5-3 (`lab19-triage.ipynb`, ~60 min): cloud API (skips without a key), HF fp16, 4-bit; rubric score, latency, cost per 1,000; valid-JSON rate.

---

## D5-4 · Support: 「模型回覆混進簡體字和大陸用語，格式也不聽話」 (K5, K7, K9) → `20-qlora-sft`

```
【需求單 #D5-4】部門：客服中心（虛構公司：曜嶼電子）
問題：           模型回覆混進簡體字和大陸用語，JSON 格式也不聽話
現況痛點：       每封回覆都要人工改字
成功指標（KPI）： 簡體字比例、有效 JSON 比例、LLM 評審分數（前後對照）
可用資料：       合成 SFT 資料（繁中台灣用語＋JSON）
限制與法規：     Colab T4（fp16 計算、短序列、釘版本）
為何現有工具不夠： 提示詞修正有上限
今天要用的工具：  QLoRA（peft、trl、bitsandbytes）
```

Objectives: draw the training pipeline (pretrain → SFT → RLHF/DPO → reasoning RL); format SFT data with a chat template; decide prompting vs RAG vs fine-tuning; run QLoRA on a T4; design an eval set; use LLM-as-judge and name its biases.

| # | Title | Mark | Takeaway | Content / visual | Lab · cite |
|---|---|---|---|---|---|
| 1–3 | Cover · Ticket · Objectives | ★ | — | — | — |
| 4 | Frame: behaviour comes from training data | ★ | — | Pipeline picture | — |
| 5 | Try: prompt fixes first | ★ | System prompt + examples help, but not fully | Before/after table (from lab) | D1-2 |
| 6 | The training pipeline | ★ | Pretrain → SFT → RLHF/DPO → reasoning RL | Picture | — |
| 7 | SFT data format + chat template | ★ | One example rendered | Code | D5-3 |
| 8 | Prompting vs RAG vs fine-tuning | ★ | Decision guide (RAG → later module) | Flowchart | §13 |
| 9 | QLoRA = 4-bit base + LoRA | ★ | Recall D4-3 picture | Diagram | D4-3 |
| 10 | T4 configuration | ★ | fp16 compute, short sequences, pinned versions | Config table | D1-4 |
| 11 | Eval-set design | ★ | Held-out, covers failure types | Table | ML pp.9–10 |
| 12 | Practice: write three eval items | ★ | FillIn | FillIn | — |
| 13 | Answer (hostOnly) | ★ | — | — | — |
| 14 | LLM-as-judge and its biases | ★ | Position, length, self-preference | List | — |
| 15 | Hallucination | ★ | Measure it, don't assume | Example | — |
| 16 | Scaling laws, MoE; reasoning models | ○ | Concept; CoT/ToT prompting → Agent #2 | — | §13 |
| 17 | DPO objective | △ | Appendix | — | — |
| 18–24 | Lab L5-4 pages 1–7 | ★ | QLoRA before/after eval | `lab20-qlora.ipynb` | L5-4 |
| 25 | Risk: prompt-injection preview; judge bias | ★ | Tickets can contain instructions | — | — |
| 26 | Day 5 summary | ★ | — | Chain | — |
| 27 | Day 5 iPAS quiz (6) | ★ | — | MCQ | — |
| 28 | Day 5 homework | ★ | Improve triage by eval; build capstone | — | — |
| 29 | 下一步 (hostOnly) | ★ | D6 launch | — | — |

Lab L5-4 (`lab20-qlora.ipynb`, ~60 min): QLoRA on a 0.5–1.5B instruct model with pinned `trl`/`peft`/`bitsandbytes`; Simplified-character rate, valid-JSON rate, LLM-judge before/after.
