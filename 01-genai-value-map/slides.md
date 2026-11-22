---
theme: default
title: GenAI 能為公司做什麼？
info: |
  生成式AI原理 · D1-1
  從執行長的一個問題出發：生成式 AI 的價值在哪、怎麼評估、怎麼決定買或自己跑。
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
exportFilename: 01-genai-value-map
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D1-1</div>

# GenAI 能為公司做什麼？

<p class="subtitle">從執行長的一張需求單，做出一頁「用例畫布」</p>

<div class="chain flex flex-nowrap items-center gap-2 mt-8">
  <span class="chip">需求單</span><span class="arrow">→</span>
  <span class="chip">現場導覽</span><span class="arrow">→</span>
  <span class="chip">生成 vs 判別</span><span class="arrow">→</span>
  <span class="chip">四面向評估</span><span class="arrow">→</span>
  <span class="chip">用例畫布</span>
</div>

<!--
★ 開場（2 分）：這門課 48 小時，每一堂都從一張「需求單」開始，不從理論開始。今天是第一堂，需求單來自執行長。
說法：「你們已經會訓練 CNN 分類器了；這門課要教的是會『產生新東西』的模型，而且每一個都要能在 Colab T4 上跑。」
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 今天的需求單來自執行長室

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D1-1】部門：執行長室<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>競爭對手都在用生成式 AI，我們該把錢花在哪裡？</dd>
    <dt>現況痛點</dt><dd>各部門各自試用免費工具，沒有人算過價值、成本與風險</dd>
    <dt>成功指標（KPI）</dt><dd>一頁「用例畫布」：每張需求單都有價值、可行性、資料、風險四項評分</dd>
    <dt>可用資料</dt><dd>八個部門送來的需求單（也就是這門課的課程地圖）</dd>
    <dt>限制與法規</dt><dd>預算有限、算力只有一張 T4、個資法、著作權法</dd>
    <dt>為何現有工具不夠</dt><dd>分類器只會回答「是哪一類」，不會「產生新東西」</dd>
  </dl>
</div>

<div class="takeaway mt-3">今天的產出：一頁用例畫布，讓執行長知道先做哪一張需求單。</div>

<!--
★ 需求單卡片（3 分）：逐列唸過。強調「曜嶼電子」是虛構公司，名稱只是代稱。
每一堂都有一張這樣的卡片，格式固定：問題、痛點、KPI、資料、限制、為何現有工具不夠、今天的工具。
-->

---

<div class="eyebrow">00 · 這門課怎麼上</div>

# 每一堂都走同一個六步迴圈

<div class="loop6 mt-4">
  <div><b>Frame</b>定義問題<small>KPI、資料、限制是什麼？</small></div>
  <div><b>Try</b>先用現成的<small>預訓練模型能給我們什麼？</small></div>
  <div><b>Open</b>打開黑盒子<small>它怎麼運作？</small></div>
  <div><b>Adapt</b>調成我們的<small>條件、微調、門檻</small></div>
  <div><b>Measure</b>量化驗收<small>商業指標＋技術指標＋風險</small></div>
  <div><b>Ship</b>交付展示<small>Gradio 展示或一頁說明</small></div>
</div>

<table class="mt-5" style="font-size:17px">
<thead><tr><th>Vibe Coding 學過的迴圈</th><th>Specify</th><th>Generate＋Execute</th><th>—</th><th>Iterate</th><th>Audit</th><th>—</th></tr></thead>
</table>

<div class="takeaway mt-3">你已經會 Specify → Audit；這門課多了「打開黑盒子」和「交付」。</div>

<!--
★ 六步迴圈（4 分）：對照 Vibe Coding 單元 01 的 Specify → Generate → Execute → Audit → Iterate。
Open 是這門課的「原理」：每一個模型都會畫圖、類比、最多一條公式，再寫一段程式。Ship 是每天都要交出一個能點的東西（第一天在 D1-4）。
-->

---

<div class="eyebrow">00 · 課程地圖</div>

# 曜嶼電子的部門，就是六天的課程地圖

<table style="font-size:17px">
<thead><tr><th style="width:9%">天</th><th style="width:38%">商業問題</th><th>部門</th><th style="width:26%">會交付</th></tr></thead>
<tbody>
<tr><td>D1</td><td>GenAI 能做什麼？跑得動嗎？</td><td>執行長、行銷、資訊</td><td>分類器網頁展示</td></tr>
<tr><td>D2</td><td>找出從沒看過的瑕疵</td><td>品保（A 線）、行銷科技、客服</td><td>瑕疵檢測站</td></tr>
<tr><td>D3</td><td>GAN 還是擴散模型？</td><td>電商、品保（B 線）、行銷</td><td>放大器或 B 線轉換器</td></tr>
<tr><td>D4</td><td>行銷影像工作室</td><td>數據組、行銷、品牌、技術長</td><td>產品影像工作室</td></tr>
<tr><td>D5</td><td>客服中心</td><td>客服、資訊／法務</td><td>客服單分類助手</td></tr>
<tr><td>D6</td><td>上市與交付</td><td>行銷、電商、法遵、執行長室</td><td>個人期末專題</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">每天回答一個部門的問題；今天先決定「哪些問題值得做」。</div>

<!--
★ 課程地圖（3 分）：不用細講每一天，只讓學員知道「部門 → 需求單 → 工具」的對應。
LLM 在第五天才深入，緊接著就是 Agent 模組；今天的導覽先讓大家看一眼。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **區分**判別模型與生成模型，用公司的例子說明
2. **說明**生成模型學的是資料的分布，提示詞是「條件」
3. **定位** 2026 年主要的生成模型家族，以及開放權重與封閉 API 的差別
4. **評估**一張需求單：價值 × 可行性 × 資料 × 風險，並決定買 API 或自己跑

<!--
★ 目標（1 分）。不教：任何模型的程式碼（D1-2 開始）；Agent、RAG、工具呼叫（屬於後續 Agent 模組）。
-->

---

<div class="eyebrow">01 · Try（先用現成的）</div>

# 講師現場導覽：同一個產品，三種生成

<div class="grid grid-cols-3 gap-4 mt-2">
<div>

<div class="node node--primary"><strong>文案</strong><small>小型開放 LLM</small></div>
<div class="placeholder mt-2" style="height:170px">三版產品文案<small>講師實跑後替換</small></div>

</div>
<div>

<div class="node node--secondary"><strong>產品情境圖</strong><small>SD1.5 ＋ LCM-LoRA</small></div>
<div class="placeholder mt-2" style="height:170px">512×512 產品圖<small>講師實跑後替換（附 seed、步數）</small></div>

</div>
<div>

<div class="node node--warm"><strong>10 秒片頭音樂</strong><small>MusicGen-small</small></div>
<div class="placeholder mt-2" style="height:170px">音檔播放器<small>講師實跑後替換</small></div>

</div>
</div>

<div class="takeaway mt-3">一句提示詞，三種模型產生三種「新東西」：文字、影像、聲音。</div>

<div class="src">示範用模型與授權見 research/sources.md S3–S6；MusicGen 權重為非商用授權，只由講師示範。</div>

<!--
★ 現場示範（8 分）：打開 materials/demo-tour（講師版即 D1-2 的 lab02 解答筆記本＋MusicGen 一格）。
提示詞：「曜嶼電子新款藍牙耳機，主打通勤降噪，寫一段 60 字的上架文案」。圖片提示詞用英文。音樂：「upbeat electronic jingle, 10 seconds」。
只看結果，不解釋原理；告訴學員 D1-2 自己跑文字與影像，音樂在 D6-1。
備案：Colab 沒額度 → 播放講師事先存好的輸出（outputs/ 資料夾）。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）</div>

# 判別 vs 生成：同一片電路板，兩種問題

<div class="grid grid-cols-2 gap-8 mt-4">
<div>

<div class="node"><strong>判別模型</strong>（discriminative）<small>你在 DL 課訓練過的 CNN</small></div>
<div class="flex items-center gap-2 mt-3" style="font-size:19px">
  <span class="chip">電路板照片</span><span class="arrow">→</span><span class="chip">CNN</span><span class="arrow">→</span><span class="chip chip--primary">「瑕疵」或「良品」</span>
</div>
<p class="muted mt-3" style="font-size:18px">輸出：一個標籤（或機率）</p>

</div>
<div>

<div class="node node--primary"><strong>生成模型</strong>（generative）<small>這門課的主角</small></div>
<div class="flex items-center gap-2 mt-3" style="font-size:19px">
  <span class="chip">隨機數字／提示詞</span><span class="arrow">→</span><span class="chip">生成模型</span><span class="arrow">→</span><span class="chip chip--primary">一張新的電路板</span>
</div>
<p class="muted mt-3" style="font-size:18px">輸出：一筆新的資料（影像、文字、聲音）</p>

</div>
</div>

<div class="takeaway mt-6">判別模型回答「這是什麼」；生成模型畫出「一個新的」。</div>

<div class="src">回顧：ML pp.42–43（邏輯斯迴歸＝判別模型）；DL pp.38–55（CNN 分類）</div>

<!--
★ 判別 vs 生成（5 分）：從學員熟悉的 CNN 出發。判別模型學「給定圖片，標籤是什麼」；生成模型學「這類資料長什麼樣」，所以能畫出新的。
常見誤解：「生成模型就是比較大的分類器」。不對：輸出的型態完全不同，一個是標籤，一個是整筆資料。
-->

---

<div class="eyebrow">02 · Open · 資料分布</div>

# 生成模型學的是「我們的產品通常長什麼樣」

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 440 300" style="width:100%">
  <defs><marker id="ax1" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#4b5563"/></marker></defs>
  <line x1="40" y1="270" x2="420" y2="270" stroke="#4b5563" stroke-width="1.5" marker-end="url(#ax1)"/>
  <line x1="40" y1="270" x2="40" y2="20" stroke="#4b5563" stroke-width="1.5" marker-end="url(#ax1)"/>
  <text x="300" y="292" style="font-size:16px" fill="#4b5563">特徵一（例：亮度）</text>
  <text x="48" y="30" style="font-size:16px" fill="#4b5563">特徵二（例：線路密度）</text>
  <ellipse cx="220" cy="150" rx="80" ry="44" fill="#eaf1ff" stroke="#2457c5" stroke-width="2"/>
  <g fill="#172033">
    <circle cx="200" cy="140" r="5"/><circle cx="240" cy="160" r="5"/><circle cx="180" cy="160" r="5"/><circle cx="260" cy="135" r="5"/>
    <circle cx="225" cy="120" r="5"/><circle cx="150" cy="150" r="5"/><circle cx="290" cy="170" r="5"/><circle cx="210" cy="185" r="5"/>
    <circle cx="300" cy="130" r="5"/><circle cx="170" cy="120" r="5"/>
  </g>
  <g fill="#b85c20"><rect x="230" y="140" width="11" height="11"/><rect x="190" y="168" width="11" height="11"/></g>
  <text x="150" y="232" style="font-size:17px" fill="#2457c5">藍色區域＝p_θ（模型學到的）</text>
</svg>

</div>
<div style="font-size:19px">

<div class="flex items-center gap-2"><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#172033"></span>真實產品（訓練資料）</div>
<div class="flex items-center gap-2 mt-2"><span style="display:inline-block;width:12px;height:12px;background:#b85c20"></span>模型生成的新產品</div>

- **p_data**：真實資料的分布（看不到全貌）
- **p_θ**：模型的分布，θ 是模型參數
- 訓練：讓 p_θ 接近 p_data
- 生成：從 p_θ **抽樣**一個新點

</div>
</div>

<div class="takeaway mt-2">訓練＝讓藍色區域蓋住黑點；生成＝在藍色區域裡抽一個新點。</div>

<div class="src">教學示意圖（非實際資料）。回顧：DL pp.80–81 生成式 AI 概論</div>

<!--
★ p_data 與 p_θ（6 分）：先指黑點「這是我們真正有的產品照片」，再指藍色「模型心中『產品通常長這樣』的範圍」，最後指橘色方塊「從範圍裡抽出來的新產品」。
p 讀作「機率分布」；θ 讀作「theta，模型的參數」。不推導任何公式。
常見誤解：生成模型「背下」訓練資料再拼貼。理想上它學的是範圍（分布），抽樣得到的是新點；但 D2-3 會講到模型也可能背下資料，這是隱私風險。
-->

---

<div class="eyebrow">02 · Open · 條件</div>

# 提示詞就是「條件」

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 380 250" style="width:100%">
  <ellipse cx="120" cy="125" rx="80" ry="55" fill="#eaf1ff" stroke="#2457c5" stroke-width="2"/>
  <ellipse cx="270" cy="125" rx="80" ry="55" fill="#e7f5f2" stroke="#16847a" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="70" y="130" style="font-size:18px" fill="#2457c5">y＝藍色耳機</text>
  <text x="222" y="130" style="font-size:18px" fill="#16847a">y＝白色耳機</text>
  <text x="70" y="225" style="font-size:16px" fill="#4b5563">同一個模型，換一個條件，抽樣的範圍就換了</text>
</svg>

</div>
<div style="font-size:19px">

$$p_\theta(x \mid y)$$

- **x**：要生成的東西（一張圖、一段文字）
- **y**：條件（提示詞、類別、參考圖）
- **讀作**：「在條件 y 之下，x 出現的機率」

</div>
</div>

<div class="takeaway mt-3">寫提示詞，就是在指定「要從哪一塊分布裡抽樣」。</div>

<div class="src">之後會再出現：D4-1 條件擴散模型、D5-2 GPT 依前文生成下一個字</div>

<!--
★ 條件（5 分）：直線 | 讀作「在……之下」。舉例：同一個影像模型，提示詞「藍色耳機」和「白色耳機」就是兩個不同的 y，抽出來的圖落在不同區域。
連結 Vibe Coding：你們寫給 Claude 的提示詞，也是 y；它從「在這個提示詞之下」的文字分布裡抽樣。
-->

---

<div class="eyebrow">03 · 2026 生成式 AI 地圖</div>

# 五大家族，以及「開放權重 vs 封閉 API」

<table style="font-size:17px">
<thead><tr><th style="width:20%">家族</th><th>產生什麼</th><th style="width:24%">代表例子</th><th style="width:14%">本課</th></tr></thead>
<tbody>
<tr><td><strong>LLM</strong>（大型語言模型）</td><td>文字、程式碼、JSON</td><td>Qwen、Llama、Claude</td><td>D1-2、D5</td></tr>
<tr><td><strong>擴散／Flow 模型</strong></td><td>影像、影片</td><td>Stable Diffusion</td><td>D3、D4</td></tr>
<tr><td><strong>多模態</strong>（multimodal）</td><td>看圖說話、以文搜圖</td><td>CLIP、VLM</td><td>D4-2、D6-2</td></tr>
<tr><td><strong>音訊</strong></td><td>音樂、語音</td><td>MusicGen、TTS</td><td>D2-4、D6-1</td></tr>
<tr><td><strong>Agent</strong></td><td>多步驟自動完成任務</td><td>Claude Code</td><td>下一個模組</td></tr>
</tbody>
</table>

<div class="grid grid-cols-2 gap-4 mt-3" style="font-size:18px">
<div class="node"><strong>開放權重</strong>（open weights）<small>下載模型檔，自己的 GPU 跑；資料不出門</small></div>
<div class="node node--warm"><strong>封閉 API</strong><small>呼叫廠商的服務；不用 GPU，但資料要送出去</small></div>
</div>

<div class="takeaway mt-3">選家族看「要產生什麼」；選開放或封閉看「資料能不能出門、預算多少」。</div>

<!--
★ 地圖（6 分）：每一列指出本課在哪一天處理。Agent 只點名：工具呼叫、MCP、RAG 都在下一個 Agent 模組，這門課不教。
開放權重 vs 封閉 API 是商業決定，不只是技術決定，第 13 頁再展開。
-->

---

<div class="eyebrow">03 · 時間軸</div>

# 今天的模型，站在 2013–2022 年的想法上

<div class="flex items-start justify-between mt-8" style="font-size:18px">
  <div class="text-center" style="width:15%"><div class="step-num">1</div><strong>2013</strong><br>VAE</div>
  <div class="text-center" style="width:15%"><div class="step-num">2</div><strong>2014</strong><br>GAN</div>
  <div class="text-center" style="width:15%"><div class="step-num">3</div><strong>2017</strong><br>Transformer</div>
  <div class="text-center" style="width:15%"><div class="step-num">4</div><strong>2020</strong><br>DDPM 擴散模型</div>
  <div class="text-center" style="width:15%"><div class="step-num">5</div><strong>2022</strong><br>Stable Diffusion</div>
  <div class="text-center" style="width:15%"><div class="step-num">6</div><strong>2022</strong><br>ChatGPT</div>
</div>

<div class="grid grid-cols-6 gap-2 mt-6 muted" style="font-size:15px">
  <div class="text-center">D2-3</div><div class="text-center">D3-1</div><div class="text-center">D5-1</div><div class="text-center">D3-3</div><div class="text-center">D4</div><div class="text-center">D5</div>
</div>

<div class="takeaway mt-8">每一個里程碑，課程裡都會有一天親手做一個小版本。</div>

<div class="src">年份依原始論文與官方發布（research/sources.md S8–S13）</div>

<!--
○ 時間軸（3 分）：只講年份與名字，下面一列是本課哪一天實作。時間不夠可略過。
-->

---

<div class="eyebrow">04 · Measure（量化驗收）</div>

# 用四個面向替每一張需求單打分數

<table style="font-size:18px">
<thead><tr><th style="width:18%">面向</th><th>要問的問題</th><th style="width:30%">1 分 → 5 分</th></tr></thead>
<tbody>
<tr><td><strong>價值</strong></td><td>做成了，每月省多少時間或多賺多少？</td><td>很少 → 很多</td></tr>
<tr><td><strong>可行性</strong></td><td>現成模型＋一張 T4 做得到嗎？</td><td>要大量研發 → 現成可用</td></tr>
<tr><td><strong>資料</strong></td><td>有足夠、合法、可用的資料嗎？</td><td>沒有 → 充足且有授權</td></tr>
<tr><td><strong>風險</strong></td><td>出錯的代價？個資、著作權？</td><td>很高 → 很低</td></tr>
</tbody>
</table>

<div class="node node--primary mt-3" style="font-size:18px">McKinsey（2023）估計：生成式 AI 約 75% 的價值集中在<strong>客服、行銷與銷售、軟體工程、研發</strong>四個領域</div>

<div class="takeaway mt-3">先做「四項都高」的需求單；價值高但資料或風險分數低的，先補資料或流程。</div>

<div class="src">McKinsey Global Institute, The economic potential of generative AI (2023)，research/sources.md S1</div>

<!--
★ 四面向評估（6 分）：分數越高越好（風險 5 分代表風險很低，避免學員搞混方向）。
曜嶼電子的需求單剛好落在這四個領域：客服（D5）、行銷（D1-2、D4）、研發與品保（D2、D3）。
-->

---

<div class="eyebrow">04 · Adapt（調成我們的）</div>

# 買 API，還是自己跑開放權重？

<table style="font-size:18px">
<thead><tr><th style="width:20%"></th><th>封閉 API</th><th>開放權重（自己跑）</th></tr></thead>
<tbody>
<tr><td><strong>成本</strong></td><td>依使用量計費，起步便宜</td><td>買或租 GPU，用量大時較划算</td></tr>
<tr><td><strong>資料</strong></td><td>要送到廠商；看服務條款</td><td>留在自己的機器</td></tr>
<tr><td><strong>控制</strong></td><td>廠商可能改版、下架</td><td>版本固定，可以微調</td></tr>
<tr><td><strong>工程量</strong></td><td>幾行程式就能用</td><td>要處理 GPU、記憶體、部署</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">有個資或機密 → 先考慮開放權重；要快速驗證 → 先用 API。</div>

<div class="src">對應 iPAS AI 應用規劃師「導入評估」「導入規劃」（對應關係待確認）</div>

<!--
★ 買或自己跑（5 分）：這一頁就是用例畫布的一個欄位。舉例：客服單有客戶個資 → 開放權重或去識別化；行銷文案沒有個資 → API 最快。
這門課兩種都會用：D1-2 一次 API 呼叫，其他大多是開放權重（因為要打開黑盒子）。
-->

---

<div class="eyebrow">04 · Measure</div>

# 哪裡不該用生成式 AI

<div class="grid grid-cols-3 gap-4 mt-4" style="font-size:18px">
<div class="node node--warm"><strong>需要唯一正確答案</strong><small>稅額計算、庫存數量 → 用一般程式或資料庫</small></div>
<div class="node node--warm"><strong>出錯代價極高又沒人審</strong><small>安全規格、醫療建議 → 至少要人工複核</small></div>
<div class="node node--warm"><strong>沒有可驗收的標準</strong><small>說不出「怎樣算好」→ 先定 KPI 再談</small></div>
</div>

<div class="takeaway mt-6">生成式 AI 擅長「產生候選」，不擅長「保證正確」。</div>

<!--
○ 不該用的地方（3 分）：這三點也是用例畫布「風險」欄位的檢查。
-->

---

<div class="eyebrow">05 · Ship（交付）· Lab L1-1</div>

# Lab L1-1 1／2：一張用例畫布有八格

<div class="grid grid-cols-4 gap-3 mt-4" style="font-size:18px">
  <div class="node"><strong>① 問題</strong><small>一句話</small></div>
  <div class="node"><strong>② KPI</strong><small>可量化的驗收</small></div>
  <div class="node"><strong>③ 資料</strong><small>有什麼、多少、授權</small></div>
  <div class="node"><strong>④ 模型家族</strong><small>LLM／擴散／音訊……</small></div>
  <div class="node"><strong>⑤ API 或開放權重</strong><small>理由一句</small></div>
  <div class="node node--warm"><strong>⑥ 最大風險</strong><small>個資、著作權、幻覺</small></div>
  <div class="node node--primary"><strong>⑦ 四項分數</strong><small>價值／可行／資料／風險</small></div>
  <div class="node node--primary"><strong>⑧ 決定</strong><small>先做／補資料／不做</small></div>
</div>

<div class="takeaway mt-5">畫布＝把需求單翻譯成「能不能做、值不值得做」。</div>

<!--
★ 畫布欄位（3 分）：①②③來自需求單，④⑤是今天學的，⑥⑦⑧是判斷。下一頁看一個填好的例子。不需要 GPU。
-->

---

<div class="eyebrow">05 · Ship · Lab L1-1</div>

# Lab L1-1 2／2：照著做——客服回覆草稿

<table style="font-size:17px">
<thead><tr><th style="width:22%">欄位</th><th>客服中心：「每張客服單都要寫回覆草稿」</th></tr></thead>
<tbody>
<tr><td>① 問題</td><td>客服人員每天花 3 小時打回覆，語氣不一致</td></tr>
<tr><td>② KPI</td><td>草稿採用率 ≥ 70%；平均回覆時間減半</td></tr>
<tr><td>③ 資料</td><td>過去的客服單與回覆（含客戶個資，需去識別化）</td></tr>
<tr><td>④ 模型家族</td><td>LLM</td></tr>
<tr><td>⑤ API 或開放權重</td><td>開放權重：客服單有個資，不想送出公司</td></tr>
<tr><td>⑥ 最大風險</td><td>幻覺（答應不存在的保固）→ 人工送出前審核</td></tr>
<tr><td>⑦ 四項分數</td><td>價值 5／可行 4／資料 3／風險 3 ＝ 15</td></tr>
<tr><td>⑧ 決定</td><td>先做，D5 實作；先完成去識別化</td></tr>
</tbody>
</table>

<!--
★ 示範（4 分）：刻意用 D5 的需求單當示範，和練習的兩張不同（golden example 3：示範與練習不同題目）。
說明分數怎麼來：資料 3 分是因為有資料但要先處理個資；風險 3 分是因為有人工審核。
-->

---

<div class="eyebrow">05 · Ship · Lab L1-1 · 練習</div>

# 練習：替兩張需求單填畫布

<div class="muted" style="font-size:17px">1. 讀兩張需求單的一句話　2. 每格寫短答案　3. 四項分數各 1–5 分，加總</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:18%">欄位</th><th>行銷部：「每週要 50 張新品情境圖」</th><th>品保部：「AOI 新瑕疵常漏檢」</th></tr></thead>
<tbody>
<tr><td>② KPI</td><td class="blank"><FillIn id="canvas.mkt-kpi" hint="例：每張成本……" /></td><td class="blank"><FillIn id="canvas.qa-kpi" /></td></tr>
<tr><td>③ 資料</td><td class="blank"><FillIn id="canvas.mkt-data" /></td><td class="blank"><FillIn id="canvas.qa-data" hint="例：良品多、瑕疵……" /></td></tr>
<tr><td>④ 模型家族</td><td class="blank"><FillIn id="canvas.mkt-family" /></td><td class="blank"><FillIn id="canvas.qa-family" /></td></tr>
<tr><td>⑤ API 或開放</td><td class="blank"><FillIn id="canvas.mkt-api" /></td><td class="blank"><FillIn id="canvas.qa-api" /></td></tr>
<tr><td>⑥ 最大風險</td><td class="blank"><FillIn id="canvas.mkt-risk" /></td><td class="blank"><FillIn id="canvas.qa-risk" /></td></tr>
<tr><td>⑦ 總分（/20）</td><td class="blank"><FillIn id="canvas.mkt-score" hint="例：4+4+3+3……" /></td><td class="blank"><FillIn id="canvas.qa-score" /></td></tr>
</tbody>
</table>

<FillClear group="canvas" />

<!--
★ 練習（12 分）：個人作業，不收回。答案沒有唯一標準，重點是每一格有理由。下一頁是參考答案（學員網站不含）。
目的：學員自己發現「品保那張價值和資料都高，但不是用一般分類器」，以及「行銷那張可行性高，但授權和商標是風險」。
-->

---
hostOnly: true
---

<div class="eyebrow">05 · Ship · Lab L1-1 · 練習解答</div>

# 練習解答：參考畫布

<table class="tight vlines" style="font-size:16px">
<thead><tr><th style="width:18%">欄位</th><th>行銷部：每週 50 張新品情境圖</th><th>品保部：AOI 新瑕疵常漏檢</th></tr></thead>
<tbody>
<tr><td>② KPI</td><td>每張成本、可用率 ≥ 60%、無他牌商標</td><td>漏檢率 ≤ 5% 下過殺率下降</td></tr>
<tr><td>③ 資料</td><td>產品照、品牌規範（自有）</td><td>大量良品、很少瑕疵、沒有新瑕疵</td></tr>
<tr><td>④ 模型家族</td><td>擴散模型（影像）</td><td>生成模型做異常偵測（AE／擴散）</td></tr>
<tr><td>⑤ API 或開放</td><td>開放權重＋微調（品牌一致）或 API 試作</td><td>開放權重（產線影像是機密）</td></tr>
<tr><td>⑥ 最大風險</td><td>模型授權、商標、肖像</td><td>漏檢造成客訴；過殺浪費人力</td></tr>
<tr><td>⑦ 總分</td><td>例：價值 3／可行 5／資料 4／風險 3 ＝ 15</td><td>例：價值 5／可行 3／資料 4／風險 3 ＝ 15</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">怎麼判斷：每格都有理由、分數和理由一致就對；兩張都會在 D2、D4 實作。</div>

<!--
★ 解答（3 分）：強調品保那張的「模型家族」不是分類器，因為沒有新瑕疵的標註——這就是 D2-1 的主題。
-->

---

<div class="eyebrow">06 · Measure & Risk</div>

# 風險：生成的內容不等於查證過的內容

<div class="grid grid-cols-2 gap-6 mt-3">
<div>

<div class="node node--warm"><strong>幻覺</strong>（hallucination）<small>模型說得很流暢，但內容是錯的或編的</small></div>

<p style="font-size:18px" class="mt-3">例：請 LLM 寫耳機文案，它自己加上「續航 60 小時」，但規格書寫 30 小時。</p>

</div>
<div>

<div class="node node--primary"><strong>規則</strong><small>出錯代價越高，越要人工審核</small></div>

- 數字、規格、法律用語 → 對照原始資料
- 對外發布 → 人工送出前審核
- 留下提示詞與輸出紀錄

</div>
</div>

<div class="takeaway mt-4">生成模型是從分布裡抽樣，不是查資料庫；抽到「看起來合理但錯」的內容很正常。</div>

<!--
★ 風險（4 分）：連回第 8 頁：模型抽的是「看起來像」的點，不保證是真的。Vibe Coding 學過「Agent 的程式要稽核」，生成內容也一樣。
-->

---

<div class="eyebrow">附錄 · 只認名字</div>

# 其他生成模型家族

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>Normalizing Flow</strong>（正規化流）<small>用一連串可逆轉換把簡單分布變成資料分布，可以算出精確機率</small></div>
<div class="node"><strong>自迴歸影像模型</strong><small>像 GPT 一樣，一次產生影像的一小塊（token）</small></div>
</div>

<div class="takeaway mt-6">本課不實作；聽到名字時知道它們也是「學分布、再抽樣」。</div>

<!--
△ 備用（2 分）：有學員問「還有哪些生成模型」時再用。自迴歸影像 token 的概念在 D2-4（VQ-VAE）會出現。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-nowrap items-center gap-2 mt-4">
  <span class="chip">需求單</span><span class="arrow">→</span>
  <span class="chip">判別 vs 生成</span><span class="arrow">→</span>
  <span class="chip">p_data 與 p_θ</span><span class="arrow">→</span>
  <span class="chip">條件 p(x|y)</span><span class="arrow">→</span>
  <span class="chip">四面向評估</span><span class="arrow">→</span>
  <span class="chip">用例畫布</span>
</div>

<div class="takeaway mt-6">生成模型學「通常長什麼樣」再抽樣；用不用它，先看價值、可行性、資料與風險。</div>

<!--
★ 總整理（2 分）：回到需求單：執行長要的一頁畫布，學員已經有兩張。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq">

1. 下列哪一個是**生成**任務？（　）<br><span class="opts">A. 判斷電路板是否有瑕疵　B. 預測下個月營收　C. 產生一張新的產品情境圖　D. 把客服單分成五類</span>
2. p(x | y) 中的 y 最接近下列何者？（　）<br><span class="opts">A. 模型參數　B. 提示詞或類別等條件　C. 損失函數　D. 生成的影像</span>
3. 客服單含客戶個資，公司不希望資料離開內部，最適合？（　）<br><span class="opts">A. 直接用免費聊天網站　B. 開放權重模型在內部執行　C. 不做任何評估就上線　D. 只用分類器</span>
4. 下列哪個情境**最不適合**直接交給生成式 AI 而無人審核？（　）<br><span class="opts">A. 文案初稿　B. 腦力激盪標語　C. 產品安全規格說明　D. 產品圖草稿</span>

</div>

<!--
★ 檢核（4 分）。答案：1 C、2 B、3 B、4 C。
理由：1 其他都是判別或迴歸；2 y 是條件；3 資料不出門；4 出錯代價高且需要正確答案。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D1-2：今晚就要文案和產品圖

<div class="node node--primary mt-2">今天看講師示範、決定要做哪些需求單；下一堂打開 Colab T4，自己跑文字模型和影像模型，並弄懂「為什麼每次輸出都不一樣」。</div>

<!--
★ 只給講師的託管版看。請學員確認 Google 帳號與 Hugging Face 帳號已建立（課前準備）。
-->
