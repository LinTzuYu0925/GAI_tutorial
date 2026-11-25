# Visual survey for Day 5–6 (decks 17–24)

> Written 2026-11-26 before building decks 17–24, per the instructor's note: *"For each new model flow or family, introduce the mechanism at a high level in a popular-science tone. Skip the hard math. Survey how other courses introduce the concept, especially the graph."*
> Sources were found with web search on 2026-11-26. "Seen" means the search result described the figure. Pages not opened in full are marked (not opened).

## How other courses draw each concept, and what we adopt

| Concept (deck) | How others draw it | What we adopt |
|---|---|---|
| **Tokens and BPE** (17) | HF LLM Course ch.6 §5 grows a merge table from a 5-word toy corpus ("hug, pug, pun, bun, hugs"). It is text and printed counts, with no diagram. Karpathy's *Let's build the GPT Tokenizer* (minbpe) shows coloured token boundaries in tiktokenizer.vercel.app. 李宏毅 (GenAI 2024 *0503 transformer*) opens the Transformer with "Tokenization" as step 1 of 文字接龍. | A **coloured-token strip** of one 繁中 ticket under 3 tokenizers (real output from the lab), plus a **3-row merge ladder** from our own corpus (字 → 字字 → 詞). There is no merge formula. |
| **Embedding = lookup table** (17) | Alammar's *Illustrated Word2vec* and the *Hands-On LLMs* book (ch.2, ~300 figures) draw the embedding as a tall table with one row per token, and an ID that "pulls out" a row. Similar words are drawn as nearby points. | A **table with one highlighted row**: ID → row → vector. A real cosine table is measured on Qwen2.5's embedding matrix and labelled as measured. |
| **RNN / seq2seq bottleneck** (17) | Classic CS224N/Alammar *Visualizing seq2seq*: unrolled boxes passing one hidden vector to the right, with the encoder's last state as a single "context" arrow into the decoder. | **One row of boxes passing one small vector**, then a **funnel into one vector**. It is the same picture twice, with the bottleneck circled. |
| **Self-attention Q/K/V** (17) | 李宏毅 ML2021 *self_v7*: each word makes q, k, v; q·k gives scores α; softmax gives α′; a weighted sum of v. Each step is drawn as arrows from one query to every key. leerob.com and similar explainers say "soft database lookup: click a word to make it the query". 3Blue1Brown ch.6: the grid of query–key dot products, with "it" drawn towards "cat". | The **soft-lookup metaphor** (library search: query = what I'm looking for, key = each book's label, value = the content) and **one query fanning out to every key** with widths = weights. Then the **3×3 hand-computed grid** with the same numbers as the practice and the code. |
| **Transformer block / GPT** (18) | 李宏毅 GenAI 2024: 文字接龍 pipeline Tokenization → Input layer → Attention → Feed-forward → Output layer, with a deliberately simplified block. Alammar's *Illustrated GPT-2*: a stack of decoder blocks; masked self-attention drawn as a triangle with greyed future cells. Transformer Explainer (Polo Club, GPT-2 in the browser): data flow plus a **temperature slider re-shaping the next-token bars**. | **文字接龍 loop** (predict → append → repeat) as the frame. **The block as 4 stacked boxes** with residual bypass arrows. The **causal mask as a lower triangle**. **Sampling as one bar chart under three knobs** (temperature reshapes, top-k cuts by count, top-p cuts by cumulative share). We point students to Transformer Explainer as optional play. |
| **Quantisation** (19) | Grootendorst's *A Visual Guide to Quantization* (50+ visuals): a number line of fp32 values snapped to a few int levels; bits-per-weight boxes. | A **ruler with 16 tick marks** (4 bits = 16 levels): weights snap to the nearest mark, the same "snap to nearest" idea as VQ in D2-4. Then a **bytes-per-parameter bar chart**: fp32 4 B, fp16 2 B, 4-bit ≈ 0.5 B. |
| **Training pipeline / RLHF** (20) | HF blog *Illustrating RLHF*: 3 panels (pretrain LM → reward model from human rankings → RL fine-tune). InstructGPT Fig.2 / NeMo-Aligner Fig.1 show the same 3 steps. | A **4-stop train line**: 預訓練（讀遍網路） → SFT（看範例學格式） → 偏好調整 RLHF/DPO（學人比較喜歡哪個） → 推理 RL. Each stop has one sentence on "what data it eats", which is the hook for 繁中 drift. |
| **QLoRA** (20) | The QLoRA visual guides: a frozen big block drawn in 4-bit colour, with a small trainable side path. | Reuse the D4-3 LoRA picture (W + B·A) with **W shaded as "4-bit, frozen"**. |
| **Audio tokens / MusicGen** (21) | AudioCraft docs: a 32 kHz EnCodec tokenizer with **4 codebooks at 50 Hz**. The paper's figure shows the **codebook interleaving patterns** (flatten vs delay). Tutorials draw waveform → codec → token grid → LM. | **Waveform → token grid (4 rows × 50 columns per second) → the same GPT as D5-2 → back to waveform.** The delay pattern is the △ appendix, drawn as a staircase grid. |
| **CLIP / contrastive search** (22) | CLIP paper Fig.1: an **N×N image–text similarity matrix with a bright diagonal**, the most copied figure in courses. | Reuse the D4-2 CLIP recap, then the **N×N matrix with diagonal**, and finally **search = one row of that matrix sorted**. |
| **VLM captioning** (22) | Usually drawn as image patches → vision encoder → "visual tokens" placed before text tokens in an LLM. | **Image patches become tokens** that sit before the question in the same 文字接龍 loop as D5-2. |

## Tone rule carried into slides

- Popular-science metaphor first (圖書館查書、接龍、尺上的刻度、火車路線), then the mechanism picture, then at most one line of code or formula with its 中文讀法.
- There are no derivations on ★ slides. △ appendix slides hold the complexity math, DPO and the delay pattern.

## Sources (search results, 2026-11-26)

- HF LLM Course, ch.6 §5 *Byte-Pair Encoding tokenization*: https://huggingface.co/learn/llm-course/chapter6/5
- Karpathy, *minbpe*: https://github.com/karpathy/minbpe ; fast.ai write-up: https://www.fast.ai/posts/2025-10-16-karpathy-tokenizers
- 李宏毅, GenAI 2024 *0503 transformer* (not opened): https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring-course-data/0503/0503_transformer.pdf ; ML2021 *self_v7* (not opened): https://speech.ee.ntu.edu.tw/~hylee/ml/ml2021-course-data/self_v7.pdf ; GenAI-ML 2025 *LLM* (not opened): https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall-course-data/LLM.pdf
- Soft-lookup attention explainer: https://leerob.com/glossary/attention
- Alammar, *The Illustrated GPT-2* (mirror): https://gwern.net/docs/www/jalammar.github.io/9c8f9cd3340b81bff85edf494914cb32c3cfa752.html ; *Hands-On LLMs* ch.2: https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/ch02.html
- Transformer Explainer (Cho et al., 2024): https://arxiv.org/abs/2408.04619 ; https://github.com/poloclub/transformer-explainer
- Grootendorst, *A Visual Guide to Quantization*: https://maartengrootendorst.com/blog/quantization/
- HF blog, *Illustrating RLHF*: https://huggingface.co/blog/rlhf
- AudioCraft MusicGen docs: https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md ; Copet et al. 2023: https://arxiv.org/abs/2306.05284
