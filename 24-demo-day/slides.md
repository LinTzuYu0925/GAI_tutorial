---
theme: default
title: 期末展示日
info: |
  生成式AI原理 · D6-4
  執行長室的展示日：每人 3 分鐘（需求單 → 模型 → 現場示範 → 一個數字 → 一個風險或成本），繳交學習評量，最終 iPAS 小考，用六步驟循環與生成三難回顧整門課，交接給 Agent 模組。
colorSchema: light
fonts:
  provider: none
  sans: '"Noto Sans TC", "Microsoft JhengHei", "PingFang TC", Inter, Arial'
  mono: '"JetBrains Mono", Consolas'
lineNumbers: false
drawings:
  persist: false
transition: fade
mdc: true
exportFilename: 24-demo-day
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D6-4</div>

# 期末展示日

<p class="subtitle">每人 3 分鐘：你解決了哪一張需求單、用了什麼、證據是什麼、風險在哪裡</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">需求單</span><span class="arrow">→</span>
  <span class="chip">選模型</span><span class="arrow">→</span>
  <span class="chip">現場示範</span><span class="arrow">→</span>
  <span class="chip">一個數字</span><span class="arrow">→</span>
  <span class="chip">一個風險或成本</span>
</div>

<!--
★ 開場（2 分）：今天是曜嶼電子的執行長室展示日（虛構公司）。每個人都是自己專題的負責人。先講規則，再開始。
-->

---

<div class="eyebrow">00 · 規則</div>

# 3 分鐘的五個段落

<div class="steps mt-3" style="font-size:19px">
  <div><span class="num">1</span><strong>需求單</strong>（20 秒）：哪個部門、什麼問題、KPI 是什麼</div>
  <div><span class="num">2</span><strong>選模型</strong>（30 秒）：用了什麼、為什麼不用別的（例：為什麼擴散不用 GAN、為什麼自架不用 API）</div>
  <div><span class="num">3</span><strong>現場示範</strong>（70 秒）：打開分享連結，跑一個範例</div>
  <div><span class="num">4</span><strong>一個數字</strong>（30 秒）：你量到的指標（正確率、CLIP 分數、秒數、每千次成本……）</div>
  <div><span class="num">5</span><strong>一個風險或成本</strong>（30 秒）：授權、個資、幻覺、提示注入……你怎麼處理</div>
</div>

<div class="takeaway mt-3">講不出「一個數字」的專題，等於還沒驗收：這是整門課的 Measure。</div>

<!--
★ 規則（3 分）：講師計時，2 分 30 秒舉牌提醒。示範失敗時，直接播放備用的錄影或截圖，不要現場除錯（D6-3 的「先求能點開」）。
評分依課程地圖 §12 的期末專題評分建議：商業框架 20%、技術 25%、量測 20%、風險與授權 15%、展示與溝通 20%（比重由講師調整）。
-->

---

<div class="eyebrow">00 · 規則 · 順序</div>

# 展示順序

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--primary"><strong>現場展示</strong><small>依座號輪流；每人 3 分鐘＋30 秒換場。講師宣布今天的順序與時間</small></div>
<div class="node node--secondary"><strong>人數多的時候</strong><small>每人先交一段 3 分鐘的錄影，課堂上現場展示其中幾位（由講師挑選），其餘錄影講師課後看完並評分</small></div>
</div>

<div class="takeaway mt-4">不論現場或錄影，五個段落都一樣：評分標準相同。</div>

<!--
★ 順序（2 分）：班級人數是待決事項（課程地圖 §14）；這一頁由講師依當天人數說明。聽眾的任務：每場寫下一個「我也想試的做法」（不收回）。
-->

---

<div class="eyebrow">01 · 學習評量</div>

# 繳交學習評量

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--primary"><strong>（a）說明 Diffusion vs GAN</strong><small>給技術長的 1～2 頁備忘錄（D4-4 開始寫）：建議、三難比較、你自己 lab 的證據（D3-1、D3-3、D4-1、D4-4）、風險與授權</small></div>
<div class="node node--warm"><strong>（b）實作條件生成</strong><small>D4-1 的 <code>lab13-cfg.ipynb</code>（兩個 TODO 自己填、輸出保留）＋口頭說明 CFG 那一行（還沒口試的今天補）</small></div>
</div>

<table class="fill tight vlines mt-3" style="font-size:16px">
<thead><tr><th>繳交前自己檢查</th><th style="width:14%">完成</th></tr></thead>
<tbody>
<tr><td>備忘錄：一句建議＋三個證據＋一個風險，1～2 頁</td><td class="blank"><FillIn id="assess.memo" check /></td></tr>
<tr><td>筆記本：從頭跑完、輸出都在、最後一格寫你建議的 w</td><td class="blank"><FillIn id="assess.nb" check /></td></tr>
<tr><td>口試：說得出 ε_uncond、ε_cond、w 各是什麼，w＝0、1、＞1 會怎樣</td><td class="blank"><FillIn id="assess.oral" check /></td></tr>
</tbody>
</table>

<FillClear group="assess" corner />

<!--
★ 學習評量（4 分）：繳交方式（Colab 連結或檔案）與期限由講師宣布。備忘錄評分建議（課程地圖 §12）：比較正確 40%、自己的證據 30%、商業建議 20%、風險與授權 10%。
-->

---

<div class="eyebrow">02 · 最終小考</div>

# 最終選擇題（1–5）

<div class="mcq" style="font-size:18px">

1. 生成模型和分類模型最大的不同是？（　）<br><span class="opts"><span class="nw">A. 分類模型學 p(y｜x)，生成模型不需要資料</span>　<span class="nw">B. 分類模型只能輸出機率</span>　<span class="nw">C. 生成模型學資料的分布，可以抽出新樣本</span>　<span class="nw">D. 生成模型一定比分類模型大</span></span>
2. VAE 的損失除了重建誤差，還多了哪一項？（　）<br><span class="opts"><span class="nw">A. KL 散度，讓潛在空間接近常態分布</span>　<span class="nw">B. 對抗損失，讓圖更清楚</span>　<span class="nw">C. CLIP 分數</span>　<span class="nw">D. L1 正則化，讓權重變小</span></span>
3. GAN 的「模式崩塌」指的是？（　）<br><span class="opts"><span class="nw">A. 生成器的 loss 一直上升</span>　<span class="nw">B. 鑑別器太弱，什麼都分不出來</span>　<span class="nw">C. 訓練到一半 loss 變成 NaN</span>　<span class="nw">D. 生成器只產生少數幾種樣子，多樣性很低</span></span>
4. DDPM 訓練時，U-Net 學著預測的是？（　）<br><span class="opts"><span class="nw">A. 加進去的雜訊 ε</span>　<span class="nw">B. 去噪後的原圖 x₀</span>　<span class="nw">C. 下一個時間步 t＋1</span>　<span class="nw">D. 類別標籤</span></span>
5. classifier-free guidance 的 w 從 1 調到 7，最可能的結果是？（　）<br><span class="opts"><span class="nw">A. 更多樣，但不符合條件</span>　<span class="nw">B. 更符合條件，但多樣性下降</span>　<span class="nw">C. FID 一定變好</span>　<span class="nw">D. 只影響速度，不影響畫面</span></span>

</div>

<!--
★ 最終小考前半（4 分）。答案：1 C（D1-1）、2 A（D2-3）、3 D（D3-1）、4 A（D3-3；B 是常見誤解：網路猜的是雜訊，不是原圖）、5 B（D4-1；C 錯：太單調時 FID 反而可能變差）。
-->

---

<div class="eyebrow">02 · 最終小考</div>

# 最終選擇題（6–10）

<div class="mcq" style="font-size:18px">

6. Stable Diffusion 在哪裡去噪？（　）<br><span class="opts"><span class="nw">A. 原始像素 512 × 512 × 3</span>　<span class="nw">B. CLIP 的文字向量空間</span>　<span class="nw">C. VAE 的潛在空間（例 4 × 64 × 64）</span>　<span class="nw">D. 頻譜圖</span></span>
7. LoRA 微調只訓練什麼？（　）<br><span class="opts"><span class="nw">A. 整個模型，但學習率很小</span>　<span class="nw">B. 只有最後一層分類頭</span>　<span class="nw">C. 被凍結權重的量化版本</span>　<span class="nw">D. 加在原權重旁的兩個小矩陣 B、A</span></span>
8. 注意力中，用來和每個 key 比對相似度的是？（　）<br><span class="opts"><span class="nw">A. query</span>　<span class="nw">B. value</span>　<span class="nw">C. 位置編碼</span>　<span class="nw">D. 上一層的 loss</span></span>
9. 7B 參數模型用 4-bit 載入，權重大約需要？（　）<br><span class="opts"><span class="nw">A. 14 GB</span>　<span class="nw">B. 3.5 GB</span>　<span class="nw">C. 28 GB</span>　<span class="nw">D. 7 GB</span></span>
10. MusicGen 程式碼是 MIT、權重是 CC-BY-NC 4.0。哪一句正確？（　）<br><span class="opts"><span class="nw">A. 程式是 MIT，所以整個模型都能商用</span>　<span class="nw">B. 只要片長在 5 秒以內就能商用</span>　<span class="nw">C. 標示「AI 生成」後就能放進付費廣告</span>　<span class="nw">D. 權重是非商用授權，不能放進賣錢的產品</span></span>

</div>

<!--
★ 最終小考後半（4 分）。答案：6 C（D2-3、D4-2）、7 D（D4-3、D5-4；C 是 QLoRA 的「Q」，不是被訓練的部分）、8 A（D5-1）、9 B（D5-3；A 是 fp16）、10 D（D6-1）。答案分布：A 3、B 2、C 2、D 3。
-->

---

<div class="eyebrow">03 · 回顧 · 六步驟</div>

# 整門課：每一張需求單都走同一個循環

<svg viewBox="0 0 900 230" style="width:100%" aria-label="六個步驟排成一圈：Frame 定義問題、Try 先看結果、Open 打開黑盒子、Adapt 改成我們的、Measure 量測驗收、Ship 交付，箭頭回到 Frame">
  <defs><marker id="loop6-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <g style="font-size:18px">
  <rect x="20" y="40" width="120" height="60" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/><text x="40" y="66" fill="var(--text)" font-weight="bold">Frame</text><text x="40" y="90" style="font-size:17px" fill="var(--muted-text)">需求單、KPI</text>
  <rect x="170" y="40" width="120" height="60" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/><text x="190" y="66" fill="var(--text)" font-weight="bold">Try</text><text x="190" y="90" style="font-size:17px" fill="var(--muted-text)">先看結果</text>
  <rect x="320" y="40" width="120" height="60" rx="10" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/><text x="340" y="66" fill="var(--text)" font-weight="bold">Open</text><text x="340" y="90" style="font-size:17px" fill="var(--muted-text)">打開黑盒子</text>
  <rect x="470" y="40" width="120" height="60" rx="10" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/><text x="490" y="66" fill="var(--text)" font-weight="bold">Adapt</text><text x="490" y="90" style="font-size:17px" fill="var(--muted-text)">改成我們的</text>
  <rect x="620" y="40" width="120" height="60" rx="10" fill="var(--soft-teal)" stroke="var(--secondary)" stroke-width="2"/><text x="640" y="66" fill="var(--text)" font-weight="bold">Measure</text><text x="640" y="90" style="font-size:17px" fill="var(--muted-text)">量測驗收</text>
  <rect x="770" y="40" width="110" height="60" rx="10" fill="var(--soft-teal)" stroke="var(--secondary)" stroke-width="2"/><text x="790" y="66" fill="var(--text)" font-weight="bold">Ship</text><text x="790" y="90" style="font-size:17px" fill="var(--muted-text)">交付</text>
  </g>
  <g stroke="var(--primary)" stroke-width="2.5" fill="none"><line x1="140" y1="70" x2="166" y2="70" marker-end="url(#loop6-a)"/><line x1="290" y1="70" x2="316" y2="70" marker-end="url(#loop6-a)"/><line x1="440" y1="70" x2="466" y2="70" marker-end="url(#loop6-a)"/><line x1="590" y1="70" x2="616" y2="70" marker-end="url(#loop6-a)"/><line x1="740" y1="70" x2="766" y2="70" marker-end="url(#loop6-a)"/>
  <path d="M825,102 L825,150 L80,150 L80,104" marker-end="url(#loop6-a)"/></g>
  <text x="300" y="180" style="font-size:17px" fill="var(--primary)">交付後的新問題，就是下一張需求單</text>
</svg>

<div class="muted" style="font-size:18px">例：D5 客服中心：Frame token 成本 → Try 真模型 → Open 注意力 → Adapt QLoRA → Measure 簡體字比例 → Ship 分流助理</div>

<div class="takeaway mt-2">工具會換（GAN、擴散、LLM、MusicGen），循環不變：先定義問題，最後用數字交付。</div>

<!--
★ 六步驟（4 分）：D1-1 第一次出現這個循環。請學員用自己的期末專題，把六步各說一個字。
-->

---

<div class="eyebrow">03 · 回顧 · 生成三難</div>

# 生成三難：品質、多樣性、速度，用我們自己的證據

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:18%">家族</th><th style="width:20%">品質</th><th style="width:22%">多樣性</th><th style="width:20%">速度</th><th>課堂上的證據</th></tr></thead>
<tbody>
<tr><td>VAE</td><td>偏模糊</td><td>高</td><td>快</td><td>D2-3 Fashion-MNIST 重建</td></tr>
<tr><td>GAN</td><td>清楚</td><td>可能模式崩塌</td><td>快（一步）</td><td>D3-1 DCGAN、Real-ESRGAN</td></tr>
<tr><td>擴散</td><td>清楚</td><td>高</td><td>慢（多步）→ 蒸餾變快</td><td>D3-3 DDPM、D4-1 CFG、D4-4 LCM</td></tr>
<tr><td>自回歸（GPT 類）</td><td>規模越大越好（D5-3 0.5B vs 雲端大模型）</td><td>靠溫度控制</td><td>一個 token 一個 token</td><td>D5-2 迷你 GPT、D6-1 MusicGen</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">沒有一個家族三項全贏：選模型就是在三難裡，依需求單的 KPI 做取捨。</div>

<div class="src">生成三難：Xiao et al., 2022（D3 引用，待確認）；自回歸一列是本課延伸</div>

<!--
★ 三難（4 分）：D3 建立的表，加上第五、六天的自回歸列。數字請學員回自己的 lab 找（備忘錄也用這張表）。GAN 不是過時：ADD／Turbo 和聲碼器都還在用對抗損失（D4-4、D6-1）。
-->

---

<div class="eyebrow">04 · 交接</div>

# 交給 Agent 模組：我們停在哪裡、下一站接什麼

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:26%">主題</th><th style="width:38%">生成式AI原理停在</th><th>Agent 模組接手</th></tr></thead>
<tbody>
<tr><td>LLM API</td><td>一次 SDK 呼叫、token 成本、JSON＋json.loads</td><td>結構化輸出（schema）、串流</td></tr>
<tr><td>工具與外部系統</td><td>只認名字</td><td>tool calling、MCP</td></tr>
<tr><td>知識</td><td>記憶體內的 cosine 搜尋（D6-2）</td><td>RAG、向量資料庫</td></tr>
<tr><td>提示技巧</td><td>基本提示詞；推理模型是訓練出來的（D5-4）</td><td>CoT／ToT 等提示方法</td></tr>
<tr><td>上線</td><td>Gradio＋分享連結、模型卡</td><td>多代理人、部署、監控</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">你已經懂模型裡面在做什麼：下一個模組，讓它會用工具、查資料、自己完成任務。</div>

<!--
★ 交接（3 分）：課程地圖 §13。Agent 模組的講師會建立在 D5-1／D5-2 的 Transformer 內部之上，不重講。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一個模組：AI 代理人（Agent）

<div style="font-size:19px" class="mt-4">

- 讓 LLM 呼叫工具：查訂單、寄信、算帳（D5 的分流助理再往前一步）
- MCP：一套讓模型接上外部系統的標準
- RAG：先查公司文件，再回答，減少幻覺
- 期末專題可以帶進「學員結訓 AI 專題製作輔導」繼續發展

</div>

<!--
★ 下一步（1 分）：感謝學員。提醒學習評量與期末專題的繳交期限。
-->
