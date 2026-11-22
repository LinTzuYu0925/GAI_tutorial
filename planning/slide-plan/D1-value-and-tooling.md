# Day 1 slide plan · 「GenAI 能為我們做什麼？跑得動嗎？」

> **Status:** auto-approved for production (2026-11-23, per the instructor's /goal: "write down slide-to-slide plan for 1-1 to 2-1 then assume auto approval"). Step 2 of phase 2 in [CLAUDE.md](../../CLAUDE.md).
> **Source:** [course_roadmap.md](../course_roadmap.md) §7 Day 1, §9 labs L1-1…L1-4, §11 math map, §15 template.
> **Deck split (decided here):** **one deck per 2-hour session**, so each deck stays within the 15–25-slide range and maps 1:1 to a roadmap block. Deck names:
>
> | Session | Deck | Lab |
> |---|---|---|
> | D1-1 | `01-genai-value-map` | L1-1 use-case canvas (no GPU) |
> | D1-2 | `02-genai-tour` | L1-2 `lab02-genai-tour.ipynb` |
> | D1-3 | `03-keras-to-pytorch` | L1-3 `lab03-keras-to-pytorch.ipynb` |
> | D1-4 | `04-colab-hub-gradio` | L1-4 `lab04-checkpoint-gradio.ipynb` |
>
> D2-1 is in [D2-factory-qa.md](D2-factory-qa.md) as deck `05-ae-anomaly-detection`.

**Day goal.** By the end of Day 1 a student can say where GenAI creates value for the company (and where it should not be used), run a text model and an image model on a Colab T4, explain why outputs vary run to run, port a Keras training loop to PyTorch, and wrap a model in a Gradio app that a manager can click.

**Running case.** 曜嶼電子 (Yaoyu Electronics), **虛構**, placeholder name pending instructor check (roadmap §4). Every ticket card carries the 虛構 mark.

**Conventions for every deck below.**
- Session shape: ticket card → objectives → Frame/Try/Open/Adapt/Measure/Ship blocks → lab pages → Measure & Risk → summary → 隨堂檢核 → hostOnly 下一步.
- ★ must / ○ optional / △ backup. Slide counts include hostOnly pages.
- Every number shown on a slide comes from a recorded Colab T4 run in that deck's `research/lab-runs.md`. Until the run exists, the slide shows a `.placeholder` labelled 「講師實跑後替換」 (R-C8). Arithmetic (bytes per parameter) and teaching numbers labelled 教學用數字 are not run outputs and may be shown.
- Abbreviations in the cite column: DL = 深度學習 deck, ML = 機器學習 deck, Vibe NN = Vibe Coding deck NN (citations from [curriculum-analysis.md](../curriculum-analysis.md) and roadmap §7).

---

## D1-1 · CEO: 「競爭對手都在用 GenAI，我們的價值在哪？」 (#1, #2) → deck `01-genai-value-map`

### Ticket card

```
【需求單 #D1-1】部門：執行長室（虛構公司：曜嶼電子）
問題：           競爭對手都在用生成式 AI，我們該把錢花在哪裡？
現況痛點：       各部門各自試用免費工具，沒有人算過價值、成本與風險
成功指標（KPI）： 一頁「用例畫布」：每張需求單有價值、可行性、資料、風險四項評分
可用資料：       八個部門的需求單（本課程的課程地圖）
限制與法規：     預算有限、算力只有一張 T4、個資法、著作權法
為何現有工具不夠： 分類器只會回答「是哪一類」，不會「產生新東西」
今天要用的工具：  講師現場導覽（文字、影像、音樂生成）＋用例畫布
```

### Objectives
1. **區分** discriminative and generative models with a company example.
2. **說明** in words and a picture that a generative model learns p_data and samples from p_θ; a prompt is a condition p(x|y).
3. **定位** the main 2026 model families and open vs closed weights.
4. **評估** a ticket on value × feasibility × data × risk and choose API vs open weights (use-case canvas).

### Slides (23, of which 2 hostOnly)

| # | Title | ★/○/△ | Objective | One-sentence takeaway | Content | Visual / example | Lab hook | Prior cite | Source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cover: GenAI 能為公司做什麼？ | ★ | Open | Today: from the CEO's question to a one-page canvas | Title, chain 需求單→導覽→生成 vs 判別→評估→畫布 | Concept chain | — | — | — |
| 2 | 需求單 #D1-1 | ★ | Frame | The course starts from a business ticket, not a theory | Ticket card above | Ticket card | — | — | roadmap §4 |
| 3 | 這門課怎麼上：六步迴圈 | ★ | Frame | Every session runs Frame→Try→Open→Adapt→Measure→Ship | Six steps, each with its question; maps to Vibe's Specify→…→Iterate | Loop diagram with Vibe mapping row | — | Vibe 01 (loop) | roadmap §2.3 |
| 4 | 曜嶼電子的八個部門 = 課程地圖 | ★ | Frame | Each day answers one department's ticket | 6 days × department × business question table | Day/department table | — | — | roadmap §4, §7.0 |
| 5 | 學習目標 | ★ | — | Four observable objectives | Objectives above | List | — | — | — |
| 6 | Try：講師現場導覽 | ★ | Try | One prompt → copy, image, jingle | Demo: product copy (small open LLM), product image (SD1.5 + LCM-LoRA), 10-s jingle (MusicGen-small, instructor only, NC licence) | 3 placeholders until the instructor's run | Same models as L1-2 | DL pp.80–81 | sources S3–S6 |
| 7 | 判別 vs 生成：同一片電路板，兩種問題 | ★ | Open | A classifier answers 「瑕疵或不是」; a generator draws a new board | Left: CNN → label; right: generator → new image | Side-by-side pipeline | — | ML pp.42–43; DL pp.38–55 | — |
| 8 | 生成模型學的是「產品通常長什麼樣」 | ★ | Open | Learn p_data, approximate it with p_θ, sample new points | Scatter of real products (2 features) + density contour; sampling = new dots | 2-D scatter + contour SVG (教學示意) | — | DL pp.80–81 | roadmap §11 |
| 9 | Prompt 就是條件：p(x\|y) | ★ | Open | Same model, different condition → different distribution | y = 「藍色耳機」 vs 「白色耳機」 → two clouds | Two-cluster picture; one formula with Chinese reading | Returns D4-1, D5-2 | — | roadmap §11 |
| 10 | 2026 生成式 AI 地圖 | ★ | Open | Five families; open vs closed weights is a business choice | LLM, diffusion/flow, multimodal, audio, agents (agents → Agent module) | Map grid with course day per family | — | Vibe 01 | S7 |
| 11 | 從 VAE 到今天：時間軸 | ○ | Context | Today's models stand on 2013–2022 ideas | VAE 2013, GAN 2014, Transformer 2017, DDPM 2020, LDM 2021/SD 2022, ChatGPT 2022 | Timeline | Course days on the timeline | DL pp.72–87 | S8–S13 |
| 12 | Measure：四個面向評估需求單 | ★ | Measure | Value × feasibility × data × risk, 1–5 each | Scoring table; McKinsey: four functions ≈ 75 % of GenAI value | Scoring rubric table | Used in canvas | — | S1 |
| 13 | 買 API 還是自己跑開放權重？ | ★ | Adapt | Decide by data sensitivity, cost, control | Comparison table: API vs open weights (cost, privacy, control, effort) | Two-column table | Canvas field | — | iPAS 導入評估 (待確認) |
| 14 | 哪裡不該用 GenAI | ○ | Measure | No exact answers, no review, no tolerance for error → don't | Three red flags + examples (稅額計算, 安全規格) | Red-flag list | — | — | — |
| 15 | Lab L1-1 1/2：用例畫布長什麼樣 | ★ | Ship | One canvas = one ticket in eight boxes | Canvas fields: 問題, KPI, 資料, 模型家族, API/開放權重, 風險, 四項分數, 決定 | Canvas diagram | L1-1 | — | — |
| 16 | Lab L1-1 2/2：照著做（客服回覆草稿） | ★ | Ship | Worked example on a different ticket | Filled canvas for 客服回覆草稿 (D5 ticket) | Filled canvas | L1-1 | — | — |
| 17 | 練習：替兩張需求單填畫布 | ★ | Ship | Student scores two tickets | FillIn table: 行銷新品圖 / 品保瑕疵檢測 × KPI, 資料, 模型家族, API/開放, 最大風險, 總分 | `table.fill` | L1-1 | — | — |
| 18 | 練習解答 (hostOnly) | ★ | — | Reference canvas + how to tell | Same table filled | — | — | — | — |
| 19 | Risk：幻覺與人工審核 | ★ | Measure | Generated ≠ verified; high stakes need a human | Hallucination example (invented spec), review rule | Example + rule | — | Vibe 01 | S2 |
| 20 | 其他生成模型家族（只認名字） | △ | Context | Flows and autoregressive image models exist | Normalizing flows, autoregressive image models | Two named boxes | — | — | — |
| 21 | 總整理 | ★ | — | Chain of today's ideas | Chain + one-line summary | Concept chain | — | — | — |
| 22 | 隨堂檢核 | ★ | — | iPAS-style MCQ ×4 | Q1 生成 vs 判別; Q2 p(x\|y); Q3 API vs open weights; Q4 不該用的情境 | MCQ | — | — | — |
| 23 | 下一步 (hostOnly) | ★ | — | Next: run them ourselves | D1-2 preview | — | — | — | — |

### Lab L1-1 spec (no GPU, ~25 min)
- Steps: read worked canvas (slide 16) → fill two tickets on slide 17 → compare with the answer page.
- Expected output: two canvases with total scores; 品保 scores high on value and data, 行銷 scores high on feasibility.
- No-AI checkpoint: the whole practice (no notebook).
- Fallback: none needed.

### Measure & Risk: hallucination; human review on high-stakes outputs (slide 19).
### Homework (Day 1, given at D1-4): a third canvas.
### iPAS-style questions: slide 22.

---

## D1-2 · Marketing: 「今晚就要新品文案和一張產品圖」 (#1, #2) → deck `02-genai-tour`

### Ticket card

```
【需求單 #D1-2】部門：行銷部（虛構公司：曜嶼電子）
問題：           新款藍牙耳機今晚要上架預告，需要三版文案與一張產品情境圖
現況痛點：       外包文案三天、攝影一週，趕不上檔期
成功指標（KPI）： 3 版文案（每版 ≤ 80 字）＋1 張 512×512 圖；同樣設定能重現同一張圖
可用資料：       產品規格一頁（講師提供，虛構）
限制與法規：     免費 Colab T4；不能出現他牌商標；模型授權要能商用
為何現有工具不夠： 分類器、迴歸模型都不會「寫」或「畫」
今天要用的工具：  transformers pipeline、diffusers、一次雲端 LLM API 呼叫
```

### Objectives
1. **執行** a text-generation `pipeline` and an fp16 `DiffusionPipeline` on a Colab T4.
2. **呼叫** a cloud LLM once with the key kept out of the code.
3. **說明** why output varies: sampling from next-token probabilities; temperature reshapes them.
4. **重現** an output with a fixed seed, and **讀出** a model card's licence.

### Slides (24, of which 3 hostOnly)

| # | Title | ★/○/△ | Objective | Takeaway | Content | Visual / example | Lab hook | Prior cite | Source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cover | ★ | Open | Today we make the copy and the image ourselves | Chain 開 GPU→文字→影像→機率→溫度/seed→授權 | Chain | — | — | — |
| 2 | 需求單 #D1-2 | ★ | Frame | Deliverables + constraints | Ticket card | Card | — | — | — |
| 3 | 學習目標 | ★ | — | Four objectives | — | List | — | — | — |
| 4 | Frame：驗收清單先寫好 | ★ | Frame | Write acceptance before generating | 4 checks: 字數, 無他牌商標, 可重現, 可商用授權 | Checklist | Lab audit | Vibe 01 (驗收) | — |
| 5 | 打開 T4：Colab 執行階段 | ★ | Try | Runtime → T4, then verify in code | Steps + `torch.cuda.is_available()` | Steps + code | Cell 1 | ML pp.5–6 | S1 |
| 6 | Try 1：三行程式寫文案 | ★ | Try | `pipeline("text-generation")` hides tokenizer + model + sampling | Code with Qwen2.5-0.5B-Instruct + output placeholder | Code + placeholder | Lab part A | — | S2 |
| 7 | Try 2：一張產品情境圖 | ★ | Try | SD1.5 + LCM-LoRA, fp16, 4 steps | Code + image placeholder with seed caption | Code + placeholder | Lab part B | — | S3, S4 |
| 8 | Try 3：第一次呼叫雲端 LLM | ★ | Try | Key from Colab Secrets / `.env`, never in code | `anthropic` SDK call; open-model fallback without key | Code; key-safety callout | Lab part C | Vibe 11–12 | S5 |
| 9 | Open：為什麼每次文案都不一樣？ | ★ | Open | The model outputs a probability for every next token | Bar chart of top-5 next-token probabilities for 「這款耳機」 | Bar chart placeholder (real values from lab) | Lab part D | DL pp.80–81 | — |
| 10 | 生成 = 依機率抽籤，一次一個 token | ★ | Open | Sampling picks proportionally; greedy always picks the top | Draw → append → repeat loop | Loop picture | — | Vibe 01 | — |
| 11 | 溫度：把機率分布變尖或變平 | ★ | Open | softmax(z/T): T<1 sharper, T>1 flatter | One formula with Chinese reading; worked numbers z=[2,1,0] at T=0.5/1/2 (computed, not run) | Three small bar sets | Lab part D | DL pp.69–71 (distillation T) | — |
| 12 | 練習：溫度高低，文案怎麼變？ | ★ | Open | Student discovers repetition vs chaos | FillIn: T=0.2/1.0/1.5 × 「三次一樣嗎」「通順嗎」 | `table.fill` | Lab part D | — | — |
| 13 | 練習解答 (hostOnly) | ★ | — | — | Expected pattern + how to tell | — | — | — | — |
| 14 | Seed：讓「隨機」可以重現 | ★ | Adapt | Same seed + same settings + same versions → same output | `torch.manual_seed`, `torch.Generator("cuda").manual_seed(42)`; caveat: GPU/version change can differ | Code + caveat | Lab part B/D | — | S6 |
| 15 | System 與 User 提示 | ○ | Adapt | System sets the role, user gives the task | chat template messages | Code | Lab part A | Vibe 01–02 | — |
| 16 | 負面提示（預告 D4-2） | ○ | Adapt | Tell the image model what to avoid | `negative_prompt="logo, text"` | Code | Lab part B | — | — |
| 17 | Lab 1/4：我們要生成什麼？ | ★ | Lab | Goal: 3 copies + 1 image + reproducible | Notebook link, runtime T4, target placeholders, 2 questions | Lab page 1 | L1-2 | — | — |
| 18 | Lab 2/4：pipeline 拆成哪幾塊？ | ★ | Lab | Text: tokenizer→model→sampler→decode; image: text encoder→U-Net→VAE decoder | Diagram with shapes | Two pipelines | L1-2 | — | S2, S3 |
| 19 | 練習：每一塊的輸入與輸出 | ★ | Lab | No-AI checkpoint: shapes/types through the text pipeline | FillIn table (first row filled) | `table.fill` | L1-2 | — | — |
| 20 | 練習解答 (hostOnly) | ★ | — | — | Filled + `print(...)` checks | — | — | — | — |
| 21 | Lab 3/4：Specify → Generate → Execute | ★ | Lab | Four checkpoints, then fill TODO cells | 【目標】【輸入與輸出】【限制】【驗收】 + TODO cell list + fallback | Skeleton | L1-2 | Vibe 01 | — |
| 22 | Lab 4/4：Audit → Iterate + Ship | ★ | Lab | Check against slide-4 list; save outputs + licence line | Audit table; licence lines (Apache-2.0, CreativeML OpenRAIL-M) | Audit table | L1-2 | — | S2, S3 |
| 23 | Risk：提示隱私與生成物歸屬 | ★ | Measure | Free tiers may reuse prompts; ownership of outputs is unsettled | Two risks + rules (no 個資 in prompts; check terms) | Two cards | — | — | S7 (待確認) |
| 24 | 總整理 + 隨堂檢核 + 下一步 | ★ | — | (three slides: summary, MCQ ×4, hostOnly next) | — | — | — | — | — |

(Slide 24 is three slides in the deck: 總整理, 隨堂檢核, 下一步 hostOnly → deck total 26 incl. 3 hostOnly.)

### Lab L1-2 spec (`lab02-genai-tour.ipynb`, ~40 min)
- Parts: A text pipeline (Qwen2.5-0.5B-Instruct, fp16) · B image (SD1.5 mirror + LCM-LoRA, 4 steps, seed 42) · C cloud call (`anthropic`, skipped if no key) · D next-token probabilities + temperature sweep.
- Expected outputs: 3 copies, one 512×512 image saved to `outputs/`, a top-5 probability table, temperature comparison.
- Checkpoints: GPU name printed; image identical on re-run with the same seed; copy ≤ 80 字.
- No-AI checkpoint: slide 19 shape table.
- Fallback: no GPU → part A on CPU (0.5B fits), part B uses saved image in solution notebook; no key → part C prints the fallback message and uses part A's model.

### Risk: prompt privacy on free tiers; ownership of generated output (待確認 against 著作權法 commentary).
### iPAS-style questions: temperature effect; seed purpose; licence field; pipeline parts.

---

## D1-3 · Factory IT: 「瑕疵分類器是 Keras 寫的，生成式工具卻都是 PyTorch」 (bridge) → deck `03-keras-to-pytorch`

### Ticket card

```
【需求單 #D1-3】部門：工廠資訊組（虛構公司：曜嶼電子）
問題：           現有的瑕疵分類器是 Keras 寫的，要接 Hugging Face 生態系得先搬到 PyTorch
現況痛點：       生成式工具（transformers、diffusers、peft、trl）都以 PyTorch 為主
成功指標（KPI）： PyTorch 版測試準確率與 Keras 版差距在 ±2 個百分點內；存成 state_dict
可用資料：       CIFAR-10（代替公司的瑕疵影像；DL 課 LabDay3-2 用過）
限制與法規：     Colab T4；一堂課內訓練完
為何現有工具不夠： Keras 的 fit() 把訓練迴圈藏起來，生成模型需要自己寫迴圈
今天要用的工具：  PyTorch：Tensor、nn.Module、DataLoader、autograd
```

### Objectives
1. **對照** each Keras step to its PyTorch counterpart.
2. **預測** tensor shapes through a CNN in CHW layout (no-AI checkpoint).
3. **寫出** and explain the five-line training step (forward, loss, zero_grad, backward, step).
4. **移植** the LabDay3-2 CNN, compare accuracy, and save a `state_dict`.

### Slides (24, of which 2 hostOnly). Bridge deck: simplified 3-page lab pattern (demo-and-practice §3c).

| # | Title | ★/○/△ | Objective | Takeaway | Content | Visual | Lab hook | Prior cite | Source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cover | ★ | — | Same CNN, new framework | Chain 為何→對照→Tensor→Module→迴圈→移植 | Chain | — | — | — |
| 2 | 需求單 #D1-3 | ★ | Frame | — | Card | Card | — | — | — |
| 3 | 學習目標 | ★ | — | — | — | List | — | — | — |
| 4 | 為什麼要搬到 PyTorch？ | ★ | Frame | The GenAI libraries we use are PyTorch-first | transformers/diffusers/peft/trl logos as text boxes | Ecosystem map | — | DL pp.36–37 | S1–S4 |
| 5 | Try：先回顧你跑過的 Keras 版 | ★ | Try | You already know every step; Keras hid the loop | Keras code excerpt (Sequential CNN, compile, fit) | Code | Lab cell 1 | DL pp.38–55, LabDay3-2 | — |
| 6 | Keras ↔ PyTorch 對照表 | ★ | Open | Model/compile/fit ↔ nn.Module/optimizer/loop | 7-row table | Table | Whole lab | DL pp.16–33 | — |
| 7 | Tensor：dtype 與 device | ★ | Open | Data and model must be on the same device | `torch.tensor`, `.dtype`, `.to(device)`; error message when mismatched | Code + error | Lab | Vibe 12a | S5 |
| 8 | 通道放哪裡？HWC vs CHW | ★ | Open | Keras [B,32,32,3]; PyTorch [B,3,32,32] | Picture of the same image in two layouts; `permute` | Two stacks | Lab | Vibe 12a (shape) | S5 |
| 9 | nn.Module：和繼承 keras.Model 一樣 | ★ | Open | `__init__` builds layers, `forward` connects them | `class Net(nn.Module)` excerpt | Code with Chinese reading | Lab | DL p.20; Vibe 13 | S5 |
| 10 | 練習：預測每一層的輸出 shape | ★ | Open | No-AI checkpoint | FillIn table: input [64,3,32,32] → conv1 → pool → … → logits | `table.fill` | Lab cell | — | — |
| 11 | 練習解答 (hostOnly) | ★ | — | — | Filled + `print(x.shape)` method | — | — | — | — |
| 12 | Dataset 與 DataLoader | ★ | Open | DataLoader = batches + shuffle, like `fit(batch_size=…)` | torchvision CIFAR10 + transforms + DataLoader | Code | Lab | DL pp.16–33 | S5 |
| 13 | 訓練一步：五行程式 | ★ | Open | forward → loss → zero_grad → backward → step | Code with Chinese reading per line (golden ex. 4) | Code + readings | Lab | DL pp.25–27 | S5 |
| 14 | 常見錯誤：忘了 zero_grad | ★ | Open | Gradients add up unless cleared | Before/after of `.grad` values over two steps (computed in lab) | Before/after | Lab | — | S5 |
| 15 | 評估：model.eval() 與 torch.no_grad() | ★ | Open | eval switches dropout/BN; no_grad saves memory | Code; decorator `@torch.no_grad()` explained | Code | Lab | — | S5 |
| 16 | 存檔：state_dict | ★ | Ship | Save weights, rebuild class, load | `torch.save(model.state_dict())` / `load_state_dict` | Code | Lab | — | S5 |
| 17 | Broadcasting | ○ | Open | Shapes stretch to match from the right | `[64,3,32,32] - [3,1,1]` normalisation | Picture | — | Vibe 12a | — |
| 18 | 暖身：用梯度下降找平均值 | ○ | Open | Minimising squared error by autograd finds the mean (MLE intuition) | 5-line autograd fit of μ to data | Code + curve | Lab optional cell | — | — |
| 19 | Lab 1/3：Specify | ★ | Lab | Four checkpoints for the port | 【目標】【輸入與輸出】【限制】【驗收】; data link | Skeleton | L1-3 | — | — |
| 20 | Lab 2/3：Generate → Execute | ★ | Lab | Agent writes, you audit | PromptBox; TODO cells; fallback | PromptBox | L1-3 | Vibe 01 | — |
| 21 | Lab 3/3：Audit → Iterate | ★ | Lab | "Runs" ≠ "correct" | Audit table: shapes, loss falling, accuracy vs Keras, eval/no_grad present, normalisation | Audit table | L1-3 | — | — |
| 22 | Lightning / Accelerate（只認名字） | △ | — | Wrappers exist; learn the loop first | Two named boxes | — | — | — | — |
| 23 | 總整理 / 隨堂檢核 | ★ | — | (two slides) | MCQ ×4 | — | — | — | — |
| 24 | 下一步 (hostOnly) | ★ | — | — | D1-4 preview | — | — | — | — |

(Slide 23 is two slides → deck total 25 incl. 2 hostOnly.)

### Lab L1-3 spec (`lab03-keras-to-pytorch.ipynb`, ~45 min)
- Model: the LabDay3-2 CNN architecture. **待確認:** the exact layers must be copied from the DL course notebook; until then the notebook uses the classic Keras CIFAR-10 CNN (Conv32-Conv32-Pool-Conv64-Conv64-Pool-Dense512-Dropout-Dense10) and says so.
- Expected outputs: training loss per epoch; test accuracy; Keras reference accuracy (from the student's own DL run or the instructor's run); saved `cifar_cnn.pt`.
- Checkpoints: shape table matches `print`; loss decreases; accuracy within ±2 pp of Keras reference at equal epochs.
- No-AI checkpoint: slide 10.
- Fallback: no GPU → 1 epoch on CPU with a subset; no agent → TODO cells from slide excerpts; disconnect → solution notebook.

### Risk: "the agent's port runs" ≠ "the port is correct" (audit table, slide 21).

---

## D1-4 · IT: 「Colab 斷線害我們白訓練一天；主管要能點的展示」 (K10, #2) → deck `04-colab-hub-gradio`

### Ticket card

```
【需求單 #D1-4】部門：資訊部（虛構公司：曜嶼電子）
問題：           訓練跑到一半 Colab 斷線就全部重來；主管想要自己點得到的展示
現況痛點：       上週白訓練一天；成果只有截圖
成功指標（KPI）： 斷線後能從最後一個 epoch 接著訓練；給主管一個可以上傳圖片的網址
可用資料：       D1-3 的 CIFAR-10 分類器
限制與法規：     免費 Colab（連線時間、閒置中斷、GPU 額度都有限制）；模型授權
為何現有工具不夠： 只存在記憶體裡的模型，斷線就沒了；Notebook 不是給主管用的介面
今天要用的工具：  Google Drive 檢查點、Hugging Face Hub、Gradio
```

### Objectives
1. **存與接續** training with Drive checkpoints (model + optimizer + epoch).
2. **說明** what a Hub model repo contains and why safetensors replaces pickle.
3. **估算** VRAM from parameters × bytes and **量測** one model at fp32 vs fp16.
4. **處理** an out-of-memory error with four moves.
5. **交付** a Gradio app with a share link (Day 1 ship).

### Slides (27, of which 3 hostOnly)

| # | Title | ★/○/△ | Objective | Takeaway | Content | Visual | Lab hook | Prior cite | Source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Cover | ★ | — | — | Chain 斷線→檢查點→Hub→VRAM→Gradio | Chain | — | — | — |
| 2 | 需求單 #D1-4 | ★ | Frame | — | Card | Card | — | — | — |
| 3 | 學習目標 | ★ | — | — | — | — | — | — | — |
| 4 | Frame：免費 Colab 的三個限制 | ★ | Frame | Max session, idle timeout, GPU not guaranteed | Three cards; numbers 待確認 against Colab FAQ | Cards | — | ML pp.5–6; DL pp.34–35 | S1 |
| 5 | 掛載 Drive，檢查點存在雲端硬碟 | ★ | Adapt | Save model + optimizer + epoch every epoch | `drive.mount`; `torch.save({...})` | Code | Lab part A | — | S2 |
| 6 | 斷線後接著訓練 | ★ | Adapt | Load, set start epoch, continue | Resume code; timeline picture epoch 1-2-3 ✗ → resume 3 | Timeline | Lab part A | — | S2 |
| 7 | Try：from_pretrained 一行下載模型 | ★ | Try | Hub = GitHub for models | `AutoModel.from_pretrained(...)` | Code | Lab part B | — | S3 |
| 8 | Open：模型倉庫裡有什麼？ | ★ | Open | config + weights + model card + licence | File tree of a repo | Tree | Lab part B | — | S3 |
| 9 | safetensors：為什麼不用 pickle | ★ | Open | Pickle can run code on load; safetensors stores only numbers | Comparison | Two boxes | — | Vibe 12 (pickle risk) | S4 |
| 10 | VRAM 估算：參數 × 每個參數的位元組 | ★ | Measure | fp32 = 4 B, fp16 = 2 B; weights only | Worked: 0.5B × 2 B ≈ 1 GB (arithmetic) | Calculator layout | Lab part B | — | — |
| 11 | 練習：跑得動嗎？ | ★ | Measure | Student computes three models | FillIn: params → fp32 GB, fp16 GB, fits T4? | `table.fill` | Lab part B | — | — |
| 12 | 練習解答 (hostOnly) | ★ | — | — | Filled; why real use > weights | — | — | — | — |
| 13 | T4 的三件事 | ★ | Open | fp16 yes; no native bf16; no FlashAttention-2 | Three rows + what to do instead | Table | All labs | — | S5, S6 |
| 14 | CUDA out of memory 怎麼辦 | ★ | Adapt | Batch ↓, fp16, free memory, restart | Four moves in order; error snippet | Flow | Lab | — | S2 |
| 15 | 一張圖看一批樣本：matplotlib 網格 | ★ | Ship | Grids are how we will judge every generator | `plt.subplots` grid code | Code + placeholder | Lab part C | Vibe 12a | — |
| 16 | Gradio：三行做出網頁 | ★ | Ship | `gr.Interface(fn, inputs, outputs).launch(share=True)` | Code + reading | Code | Lab part C | 數據代理人 pp.50–61 (Dash) | S7 |
| 17 | HF 快取與磁碟空間 | ○ | Open | Models cache under `~/.cache/huggingface`; Colab disk is limited | `nvidia-smi`, `df -h` | Code | — | — | S3 |
| 18 | HF Spaces（預告 D6-3） | △ | Ship | Permanent hosting option | Named only | — | — | — | — |
| 19 | Lab 1/5：我們要做出什麼？ | ★ | Lab | Resumable training + memory table + app | Link, runtime, target placeholders | Page 1 | L1-4 | — | — |
| 20 | Lab 2/5：拆成哪幾塊？ | ★ | Lab | checkpoint → resume → classifier → predict fn → Gradio | Diagram | Page 2 | L1-4 | — | — |
| 21 | 練習：每一塊的輸入與輸出 | ★ | Lab | `predict(img)` input/output types | FillIn | Page 3 | L1-4 | — | — |
| 22 | 練習解答 (hostOnly) | ★ | — | — | — | — | — | — | — |
| 23 | Lab 3/5：Specify | ★ | Lab | Four checkpoints | Skeleton | Page 4 | L1-4 | — | — |
| 24 | Lab 4/5：Generate → Execute | ★ | Lab | PromptBox + fallback | — | Page 5 | L1-4 | — | — |
| 25 | Lab 5/5：Audit → Iterate | ★ | Lab | Resume really resumes; app handles any image size | Audit table | Page 6 | L1-4 | — | — |
| 26 | Risk：授權家族 | ★ | Measure | Apache / MIT / OpenRAIL / NC: can we sell it? | Four-row table | Table | — | — | S8 |
| 27 | 第一天總整理 / 第一天 iPAS 隨堂檢核 / 作業 / 下一步 (hostOnly) | ★ | — | (four slides) | Day 1 chain; MCQ ×6; homework list | — | — | — | — |

(Slide 27 is four slides → deck total 30 incl. 3 hostOnly.)

### Lab L1-4 spec (`lab04-checkpoint-gradio.ipynb`, ~45 min)
- Part A: train the D1-3 CNN 3 epochs with checkpoint each epoch → simulate disconnect (restart runtime) → resume.
- Part B: load `Qwen/Qwen2.5-0.5B-Instruct` at fp32 and fp16; record `torch.cuda.max_memory_allocated()`; compare with the estimate.
- Part C: Gradio `Interface` over the classifier; `share=True`.
- Checkpoints: resumed run starts at the saved epoch; measured fp16 ≈ half of fp32; app returns top-3 labels.
- Fallback: no Drive → save to `/content`; no GPU → part B on CPU (memory via parameter count only); no `share` link → in-notebook UI.

### Day 1 homework: canvas for a third ticket; finish the port; iPAS quiz (slide 27).
### Day 1 iPAS-style questions (6): generative vs discriminative; p(x|y); temperature; seed; VRAM estimate; licence family.
