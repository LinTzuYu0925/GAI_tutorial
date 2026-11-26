# D5-4 · 用 QLoRA 教模型說台灣話 · 工作筆記

最後更新：2026-11-26。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md` | 大綱（講師指示自動核准） |
| `slides.md` | 投影片（29 頁，其中 2 頁 hostOnly；含第五天總整理、小考、作業） |
| `teaching-plan.md` | 時間表 |
| `materials/src/make_sft.py` → `materials/data/sft_train.jsonl` | 216 筆合成 SFT 資料（seed 2026） |
| `materials/data/eval_tickets.jsonl` | 評估集＝D5-1 的 40 張客服單（從沒拿來訓練） |
| `materials/src/lab20-qlora.py` | 筆記本原始檔 |
| `public/before_after_cpu.png` | 講師本機 CPU 小規模試跑的前後回覆（真實輸出排成圖，因為含簡體字原文） |

## 2. 進度

- [x] 大綱、投影片、筆記本、SFT 資料
- [x] 本機 CPU 煙霧測試（fp32 不量化、`MAX_STEPS=6`、`N_EVAL=8`，沒有金鑰）
- [ ] 講師 Colab T4 實跑：前測表、前後對照表、訓練秒數、VRAM（第 6、18、22 頁佔位圖），釘版本
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（10 FAIL：1 blocker、3 major；已修正）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-26 | 基礎模型 Qwen2.5-0.5B-Instruct（本機實測會寫出整段簡體字，問題真實存在；1.5B 留作選項） |
| 2026-11-26 | 評估集用 D5-1 的手寫客服單，SFT 用模板資料：說法不同，避免考題洩漏 |
| 2026-11-26 | 簡體字判斷：OpenCC `s2tw` 會變且 `t2s` 不變，排除「台里后干只系才面伙」 |
| 2026-11-26 | 微調後評估用原本的短提示詞，證明是「習慣」改了 |
| 2026-11-26 | 版本先不釘（`%pip install -q` 未指定版本）：T4 實跑後依印出的版本再釘 |
| 2026-11-26 | Try 頁的前後回覆含簡體原文：用圖片呈現（真實輸出），避免 `scan-zh` 誤報，並標示為 CPU 小規模試跑 |

| 2026-11-26 | `scan-zh` 例外：第 11、13 頁刻意引用大陸用語（視頻、質量）當「要避免的例子」；程式裡的簡體字一律由 OpenCC 在執行時產生，原始碼不放簡體字 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| pretraining | 預訓練 | 4 |
| SFT (supervised fine-tuning) | 監督式微調 | 3、4 |
| preference tuning (RLHF / DPO) | 偏好調整；RLHF＝人類回饋強化學習 | 4 |
| RL | 強化學習 | 3、4 |
| few-shot | 少量範例 | 6 |
| RAG | 檢索增強生成（Agent 模組） | 3 |
| QLoRA | 量化＋LoRA | 9 |
| adapter | 轉接器 | 9 |
| evaluation set | 評估集 | 11 |
| LLM-as-judge | LLM 評審 | 14 |
| position / length / self-preference bias | 位置／長度偏差、自我偏好 | 14 |
| hallucination | 幻覺（D5-2） | 15 |
| scaling laws / MoE | 縮放定律／混合專家 | 16 |
| prompt injection | 提示注入 | 25 |
