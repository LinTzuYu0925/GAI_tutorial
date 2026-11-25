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

<p class="subtitle">從執行長的一張需求單，做出一頁「需求評估表」</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">需求單</span><span class="arrow">→</span>
  <span class="chip">現場導覽</span><span class="arrow">→</span>
  <span class="chip">生成 vs 判別</span><span class="arrow">→</span>
  <span class="chip">四面向評估</span><span class="arrow">→</span>
  <span class="chip">需求評估表</span>
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
    <dt>成功指標（KPI）</dt><dd>一頁「需求評估表」：每張需求單都有價值、可行性、資料、風險四項評分</dd>
    <dt>可用資料</dt><dd>各部門送來的需求單（也就是這門課的課程地圖）</dd>
    <dt>限制與法規</dt><dd>預算有限、算力只有一張 T4、個資法、著作權法</dd>
    <dt>為何現有工具不夠</dt><dd>分類器只會回答「是哪一類」，不會「產生新東西」</dd>
  </dl>
</div>

<div class="takeaway mt-3">今天的產出：一頁需求評估表，讓執行長知道先做哪一張需求單。</div>

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

<div class="muted mt-4" style="font-size:16px">對照 Vibe Coding 學過的迴圈（每一格對上面那一步）：</div>
<div class="loop6 mt-1" style="font-size:15px">
  <div>Specify</div><div>Generate＋Execute</div><div>—（新）</div><div>Iterate</div><div>Audit</div><div>—（新）</div>
</div>

<div class="takeaway mt-3">你已經會 Specify → Audit；這門課多了「打開黑盒子」和「交付」。</div>

<!--
★ 六步迴圈（4 分）：對照 Vibe Coding 單元 01 的 Specify → Generate → Execute → Audit → Iterate。
Open 是這門課的「原理」：每一個模型都會畫圖、類比、最多一條公式，再寫一段程式。Ship 是每天都要交出一個能點的東西（第一天在 D1-4）。
-->

---

<div class="eyebrow">00 · 課程地圖</div>

# 曜嶼電子的部門，就是六天的課程地圖

<table style="font-size:17px">
<thead><tr><th style="width:7%">天</th><th style="width:30%">商業問題</th><th style="width:37%">部門</th><th>會交付</th></tr></thead>
<tbody>
<tr><td>D1</td><td>GenAI 能做什麼？跑得動嗎？</td><td>執行長、行銷、資訊</td><td>分類器網頁展示</td></tr>
<tr><td>D2</td><td>找出從沒看過的瑕疵</td><td>品保（A 線）、行銷科技、客服</td><td>瑕疵檢測站</td></tr>
<tr><td>D3</td><td>GAN 還是擴散模型？</td><td>電商、品保（B 線）、行銷</td><td>放大器或 B 線轉換器</td></tr>
<tr><td>D4</td><td>行銷影像工作室</td><td>數據組、行銷、品牌、技術長</td><td>產品影像工作室</td></tr>
<tr><td>D5</td><td>客服中心</td><td>客服、資訊／法務</td><td>客服單分類助手</td></tr>
<tr><td>D6</td><td>上市與交付</td><td>行銷、電商、法遵、執行長室</td><td>個人期末專題</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">每天回答一組部門的問題；今天先決定「哪些問題值得做」。</div>

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
<div class="mt-2" style="height:200px;overflow:hidden;border:1px solid var(--border);border-radius:8px;background:var(--surface);padding:8px 12px;font-size:16px;line-height:1.45">
  <b>【曜嶼 Breeze 藍牙耳機】</b><br>
  專為通勤族打造，讓每一次音符都充滿安心與樂趣！<br>
  <b>通勤降噪</b>：輕柔耳塞設計，隔絕城市噪音……<br>
  <b>續航 30 小時</b>：高效電池技術，讓您每次使用都能享受到長達 2 小時的續航時間。
</div>
<div class="shot-cap">第 1 版節錄；三版都超過 80 字</div>

</div>
<div>

<div class="node node--secondary"><strong>產品情境圖</strong><small>SD1.5 ＋ LCM-LoRA</small></div>
<div class="mt-2 flex justify-center" style="height:200px"><img src="/tour-product-seed42.png" alt="SD1.5 產生的白色無線耳機放在木桌上" style="height:200px;border:1px solid var(--border);border-radius:8px"></div>
<div class="shot-cap">512×512 · seed 42 · 4 步，T4 約 3 秒</div>

</div>
<div>

<div class="node node--warm"><strong>10 秒片頭音樂</strong><small>MusicGen-small</small></div>
<div class="mt-2 flex flex-col items-center justify-center gap-3" style="height:200px;border:1px solid var(--border);border-radius:8px;background:var(--surface)">
  <span style="font-size:44px;line-height:1;color:var(--warm-accent)">♪</span>
  <audio controls preload="metadata" src="/tour-jingle.wav" style="width:90%"></audio>
</div>
<div class="shot-cap">9.9 秒 · 32 kHz 單聲道</div>

</div>
</div>

<div class="takeaway mt-3">同一個產品，三種模型產生三種「新東西」：文字、影像、聲音。</div>

<div class="src">示範用模型與授權見 research/sources.md S3–S6；MusicGen 權重為非商用授權，只由講師示範。</div>

<!--
★ 現場示範（8 分）：打開 D1-2 的 lab02 解答筆記本，最後貼上 `materials/tour-musicgen.py` 這一格（MusicGen）。
文案提示詞：lab02 Part A 的產品規格 SPEC ＋「請寫一段 80 字以內的上架文案。」。圖片提示詞用英文（lab02 Part B）。音樂：「upbeat electronic jingle, 10 seconds」（長度由 max_new_tokens 決定，不是提示詞裡的「10 seconds」）。
頁面上是講師在 Colab T4 實跑的結果（research/lab-runs.md）。只看結果，不解釋原理；告訴學員 D1-2 自己跑文字與影像，音樂在 D6-1。
可以順口點出：三版都超過 80 字，第 1 版寫「續航 30 小時」又說「長達 2 小時」（模型把規格裡「10 分鐘快充可聽 2 小時」的 2 小時錯接到續航），第 2、3 版混進簡體字。小模型的文案要人檢查，D1-2 會回來談。
備案：Colab 沒額度 → 直接用這頁的圖與音檔。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）</div>

# 判別 vs 生成：認出一隻貓，和畫出一隻貓

<div class="grid grid-cols-2 gap-8 mt-2">
<div>

<div class="node"><strong>判別模型</strong>（discriminative）<small>你在 DL 課訓練過的 CNN</small></div>
<div class="flex items-center gap-2 mt-3">
  <div class="pic"><img src="/contrast-real-cat.jpg" alt="一隻藍眼睛的虎斑貓的真實照片"><span>真實照片</span></div>
  <span class="arrow">→</span><span class="chip">CNN</span><span class="arrow">→</span><span class="chip chip--primary">cat（貓）</span>
</div>
<p class="muted mt-2" style="font-size:18px">輸出：<b>一個標籤</b>　例：電路板良品／瑕疵</p>

</div>
<div>

<div class="node node--primary"><strong>生成模型</strong>（generative）<small>這門課的主角</small></div>
<div class="flex items-center gap-2 mt-3">
  <div class="pic pic--z"><code>0.3<br>−1.2<br>0.7<br>…</code><span>隨機數字</span></div>
  <span class="arrow">→</span><span class="chip">生成模型</span><span class="arrow">→</span>
  <div class="pic"><img src="/contrast-gan-cat.jpg" alt="GAN 產生的橘色虎斑貓，這隻貓不存在"><span>這隻貓不存在</span></div>
</div>
<p class="muted mt-2" style="font-size:18px">輸出：<b>一張新的圖</b>　例：新的產品情境圖</p>

</div>
</div>

<div class="takeaway mt-3">判別模型回答「這是什麼」；生成模型畫出「一個新的」。</div>

<div class="src">左：AdinaVoicu，CC0（Wikimedia Commons），裁切為正方形；「cat」標籤為示意。右：thiscatdoesnotexist.com 的 GAN 生成圖（公有領域）。<br>回顧：ML pp.42–43（邏輯斯迴歸＝判別模型）；DL pp.38–55（CNN 分類）；LabDay3-2 的 CIFAR-10 有 cat 這一類</div>

<!--
★ 判別 vs 生成（5 分）：從學員熟悉的 CNN 出發。LabDay3-2 的 CIFAR-10 CNN 看到貓，輸出的就是「cat」這個標籤。
先問：「兩隻貓，哪一隻是真的？」（左邊是 Pixabay 上的真實照片；右邊是 GAN 產生的，這隻貓不存在，網站 thiscatdoesnotexist.com 每次重新整理都會畫一隻新的。）答案揭曉後，再講差別：
判別模型學「給定圖片，標籤是什麼」；輸入是圖，輸出是標籤。生成模型學「這類資料長什麼樣」；輸入是一串隨機數字，輸出是一整張圖，所以能畫出新的。
右邊那隻貓用的是 GAN（第三天會自己訓練一個）；今天只要記得「模型的輸出是整筆資料」。
常見誤解：「生成模型就是比較大的分類器」。不對：輸出的型態完全不同，一個是標籤，一個是整筆資料。
圖片授權與來源見 research/sources.md S14–S15。「cat」標籤是示意，不是我們實際跑出來的結果。
-->

---

<div class="eyebrow">02 · Open · 資料分布</div>

# 一張照片，可以變成平面上的一個點

<div class="grid grid-cols-[1.35fr_1fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 520 360" style="width:100%">
  <defs><marker id="axp" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--muted-text)"/></marker></defs>
  <line x1="30" y1="345" x2="505" y2="345" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axp)"/>
  <line x1="30" y1="345" x2="30" y2="8" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axp)"/>
  <text x="418" y="338" style="font-size:17px" fill="var(--muted-text)">亮度 →</text>
  <text x="38" y="22" style="font-size:17px" fill="var(--muted-text)">鮮豔度 ↑</text>
  <ellipse cx="265" cy="180" rx="95" ry="62" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2" stroke-dasharray="6 4"/>
  <g fill="var(--text)">
    <circle cx="210" cy="160" r="4"/><circle cx="320" cy="150" r="4"/><circle cx="215" cy="205" r="4"/><circle cx="318" cy="208" r="4"/>
    <circle cx="240" cy="138" r="4"/><circle cx="295" cy="225" r="4"/><circle cx="335" cy="180" r="4"/><circle cx="195" cy="185" r="4"/>
  </g>
  <image href="/dist-cat-normal.jpg" x="230" y="145" width="70" height="70"/>
  <image href="/dist-cat-dark.jpg" x="48" y="145" width="70" height="70"/>
  <image href="/dist-cat-bright.jpg" x="420" y="145" width="70" height="70"/>
  <image href="/dist-cat-vivid.jpg" x="230" y="22" width="70" height="70"/>
  <image href="/dist-cat-gray.jpg" x="230" y="262" width="70" height="70"/>
  <g style="font-size:16px" fill="var(--warm-accent)">
    <text x="50" y="235">✗ 暗到看不清</text>
    <text x="410" y="235">✗ 亮到一片白</text>
    <text x="306" y="62">✗ 豔得像調壞的濾鏡</text>
    <text x="306" y="304">✗ 灰得像黑白照</text>
  </g>
  <text x="120" y="112" style="font-size:16px" fill="var(--primary)">✓ 真實照片擠在這</text>
</svg>

</div>
<div style="font-size:19px">

- 每張照片量兩個數字：**亮度**、**鮮豔度** → 平面上一個點
- 真實照片很少太暗、太亮，也很少灰成黑白或豔過頭
- 所以一大堆真實照片的點（●）都擠在中間一塊

</div>
</div>

<div class="takeaway mt-2">真實資料不是平均散開，而是集中在一塊區域；這塊區域就叫<strong>資料分布</strong>。</div>

<div class="src">中間：真實照片（AdinaVoicu，CC0）；四周：同一張照片由講師調整亮度與鮮豔度（飽和度，Pillow ImageEnhance）。黑點為示意</div>

<!--
★ 照片變成點（5 分）：先只指中間那張正常的貓，再依序指四周：「這張暗到看不清；這張亮到一片白；這張像黑白照；這張像調壞的濾鏡。你在網路上隨便找一萬張照片，大多長得像哪一張？」學員會指中間。
說法：把每張照片量兩個數字放到平面上，真實照片的點會擠在中間；四個角落幾乎沒有點。「點擠在哪裡」就是資料分布。
四周四張是同一張照片調亮度、飽和度做出來的，不是另外拍的；黑點是示意，不是實際量出來的。
-->

---

<div class="eyebrow">02 · Open · 資料分布</div>

# 生成模型學的是「真實照片落在哪一塊」

<div class="grid grid-cols-[1fr_1.05fr] gap-6 mt-1 items-center">
<div>

<svg viewBox="0 0 400 392" style="width:100%;max-height:340px">
  <defs><marker id="axm" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--muted-text)"/></marker></defs>
  <image href="/dist-cat-map.jpg" x="40" y="6" width="340" height="340"/>
  <line x1="40" y1="356" x2="392" y2="356" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axm)"/>
  <line x1="30" y1="346" x2="30" y2="4" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axm)"/>
  <text x="300" y="380" style="font-size:17px" fill="var(--muted-text)">亮度 →</text>
  <text x="22" y="200" style="font-size:17px" fill="var(--muted-text)" transform="rotate(-90 22 200)" text-anchor="middle">鮮豔度 →</text>
  <ellipse cx="206" cy="182" rx="98" ry="96" fill="none" stroke="var(--text)" stroke-width="3" stroke-dasharray="8 5"/>
  <ellipse cx="216" cy="172" rx="92" ry="98" fill="none" stroke="var(--primary)" stroke-width="4"/>
</svg>

</div>
<div style="font-size:19px">

<div class="flex items-center gap-2"><span style="display:inline-block;width:26px;border-top:3px dashed var(--text)"></span><b>p<sub>data</sub></b>：真實照片的分布（看不到全貌）</div>
<div class="flex items-center gap-2 mt-1"><span style="display:inline-block;width:26px;border-top:4px solid var(--primary)"></span><b>p<sub>θ</sub></b>：模型學到的分布，θ 是模型參數</div>

- 平面上每一點都對應一張圖
- **訓練**：調 θ，讓藍框蓋住黑框
- **生成**：在藍框裡**抽樣**一個點，畫出那張圖

<p class="muted" style="font-size:16px">真的模型有上百個軸（形狀、姿勢、毛色……），這裡只畫兩個</p>

</div>
</div>

<div class="takeaway mt-2">訓練＝讓藍框蓋住真實資料那一塊；生成＝在藍框裡抽一個新點。</div>

<div class="src">教學示意：25 格都是同一張 CC0 照片調整亮度（左→右）與鮮豔度（下→上）。回顧：DL pp.80–81 生成式 AI 概論</div>

<!--
★ p_data 與 p_θ（6 分）：延續上一頁的兩個軸，現在把平面每一格都畫出來：每一格是一張圖。
先指黑色虛線：「真實照片落在這一塊，這叫 p_data，我們只看得到手上的照片，看不到全貌。」再指藍色實線：「模型心中『照片通常長這樣』的範圍，叫 p_θ。」
p 讀作「機率分布」；θ 讀作「theta，模型的參數」。訓練就是調 θ，讓藍框和黑框重疊；生成就是在藍框裡抽一個點，再把點畫成圖。
常見誤解一：生成模型「背下」訓練資料再拼貼。理想上它學的是範圍（分布），抽到的是新點；但 D2-3 會講到模型也可能背下資料，這是隱私風險。
常見誤解二：以為生成就是調亮度。這張圖只是為了畫得出來才用兩個軸；真正的模型（例如 D2-3 的 VAE）自己學出上百個軸，每個點畫出來是一隻不同的貓。
-->

---

<div class="eyebrow">02 · Open · 判別 vs 生成</div>

# 同一批資料：判別畫「界線」，生成畫「範圍」

<div class="grid grid-cols-2 gap-8 mt-1">
<div>

<div style="font-size:20px"><strong>判別模型</strong><span class="muted" style="font-size:17px">　例：SVM（支援向量機）、CNN</span></div>

<svg viewBox="0 0 360 250" style="width:100%;max-height:250px" class="mt-1">
  <defs><marker id="axd" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--muted-text)"/></marker></defs>
  <line x1="20" y1="235" x2="350" y2="235" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axd)"/>
  <line x1="20" y1="235" x2="20" y2="8" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axd)"/>
  <g fill="var(--primary)"><circle cx="80" cy="70" r="6"/><circle cx="110" cy="95" r="6"/><circle cx="70" cy="110" r="6"/><circle cx="125" cy="60" r="6"/><circle cx="95" cy="130" r="6"/><circle cx="140" cy="100" r="6"/></g>
  <g fill="var(--warm-accent)"><rect x="225" y="150" width="11" height="11"/><rect x="260" y="175" width="11" height="11"/><rect x="240" y="195" width="11" height="11"/><rect x="290" y="150" width="11" height="11"/><rect x="210" y="185" width="11" height="11"/><rect x="275" y="205" width="11" height="11"/></g>
  <line x1="90" y1="225" x2="300" y2="25" stroke="var(--text)" stroke-width="3"/>
  <text x="38" y="30" style="font-size:17px" fill="var(--primary)">● 貓</text>
  <text x="290" y="128" style="font-size:17px" fill="var(--warm-accent)">■ 狗</text>
  <text x="150" y="40" style="font-size:17px" fill="var(--text)">界線 →</text>
</svg>

<p class="mt-1" style="font-size:18px">回答：「這張是<b>貓還是狗</b>？」</p>

</div>
<div>

<div style="font-size:20px;color:var(--primary)"><strong>生成模型</strong><span class="muted" style="font-size:17px">　這門課的主角</span></div>

<svg viewBox="0 0 360 250" style="width:100%;max-height:250px" class="mt-1">
  <defs><marker id="axg" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--muted-text)"/></marker></defs>
  <line x1="20" y1="235" x2="350" y2="235" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axg)"/>
  <line x1="20" y1="235" x2="20" y2="8" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axg)"/>
  <ellipse cx="105" cy="95" rx="62" ry="52" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/>
  <ellipse cx="105" cy="95" rx="32" ry="26" fill="none" stroke="var(--primary)" stroke-width="1.5" stroke-dasharray="4 3"/>
  <ellipse cx="255" cy="180" rx="62" ry="46" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <ellipse cx="255" cy="180" rx="32" ry="23" fill="none" stroke="var(--warm-accent)" stroke-width="1.5" stroke-dasharray="4 3"/>
  <g fill="var(--primary)"><circle cx="80" cy="70" r="6"/><circle cx="110" cy="95" r="6"/><circle cx="70" cy="110" r="6"/><circle cx="125" cy="60" r="6"/><circle cx="95" cy="130" r="6"/><circle cx="140" cy="100" r="6"/></g>
  <g fill="var(--warm-accent)"><rect x="225" y="150" width="11" height="11"/><rect x="260" y="175" width="11" height="11"/><rect x="240" y="195" width="11" height="11"/><rect x="290" y="150" width="11" height="11"/><rect x="210" y="185" width="11" height="11"/><rect x="275" y="205" width="11" height="11"/></g>
  <text x="38" y="30" style="font-size:17px" fill="var(--primary)">貓通常在這</text>
  <text x="238" y="125" style="font-size:17px" fill="var(--warm-accent)">狗通常在這</text>
  <text x="190" y="40" style="font-size:16px" fill="var(--muted-text)">虛線＝最密的地方</text>
</svg>

<p class="mt-1" style="font-size:18px">回答：「貓<b>通常長什麼樣</b>？」→ 在範圍裡抽一個新點</p>

</div>
</div>

<div class="takeaway mt-2">判別模型只要一條線把資料分開；生成模型要知道每一類資料聚在哪，才畫得出新的。</div>

<div class="src">教學示意圖（非實際資料）。回顧：ML pp.42–43（邏輯斯迴歸＝判別模型，學一條界線）</div>

<!--
★ 判別 vs 生成（4 分）：兩張圖的點完全一樣，只差模型學的東西。
左邊：判別模型（SVM、邏輯斯迴歸〔ML pp.42–43〕、CNN）只在乎「界線在哪」；界線以外的地方長什麼樣，它不知道也不在乎。所以它能分類，但畫不出貓。
右邊：生成模型學的是每一類「點聚在哪、多密」（虛線是最密的地方）。知道範圍，就能在範圍裡抽新點，也就是畫一隻新的貓。
常見誤解：「生成模型就是比較大的分類器」。不對：分類器學界線，生成模型學範圍；問的問題不同。
-->

---

<div class="eyebrow">02 · Open · 條件</div>

# 提示詞就是「條件」：在大範圍裡挑一小塊

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 380 290" style="width:100%">
  <defs><marker id="axc" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--muted-text)"/></marker></defs>
  <line x1="20" y1="270" x2="370" y2="270" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axc)"/>
  <line x1="20" y1="270" x2="20" y2="8" stroke="var(--muted-text)" stroke-width="1.5" marker-end="url(#axc)"/>
  <text x="300" y="262" style="font-size:16px" fill="var(--muted-text)">亮度 →</text>
  <text x="28" y="24" style="font-size:16px" fill="var(--muted-text)">鮮豔度 ↑</text>
  <ellipse cx="195" cy="140" rx="150" ry="100" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2.5"/>
  <text x="62" y="170" style="font-size:17px" fill="var(--primary)">p<tspan baseline-shift="sub" style="font-size:13px">θ</tspan>（所有貓）</text>
  <ellipse cx="165" cy="105" rx="62" ry="36" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="122" y="111" style="font-size:17px" fill="var(--warm-accent)">y＝橘色的貓</text>
  <ellipse cx="250" cy="180" rx="62" ry="36" fill="var(--soft-teal)" stroke="var(--secondary)" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="207" y="186" style="font-size:17px" fill="var(--secondary)">y＝白色的貓</text>
</svg>

</div>
<div style="font-size:19px">

$$p_\theta(x \mid y)$$

- **x**：要生成的東西（一張圖、一段文字）
- **y**：條件（提示詞、類別、參考圖）
- **讀作**：「在條件 y 之下，x 出現的機率」

<p class="muted" style="font-size:16px">白貓：比較亮、不豔；橘貓：比較豔。兩塊都還在「所有貓」的範圍裡</p>

</div>
</div>

<div class="takeaway mt-3">寫提示詞，就是在 p<sub>θ</sub> 的大範圍裡，指定「要從哪一小塊抽樣」。</div>

<div class="src">教學示意圖。之後會再出現：D4-1 條件擴散模型、D5-2 GPT 依前文生成下一個字</div>

<!--
★ 條件（5 分）：延續前兩頁的同一個平面。藍色大範圍是「所有貓」，也就是前面的 p_θ。
直線 | 讀作「在……之下」。提示詞「橘色的貓」和「白色的貓」是兩個不同的 y，抽樣範圍從整個藍色縮小到裡面的一小塊；兩小塊都在藍色裡面，因為它們都還是貓。
連結 Vibe Coding：你們寫給 Claude 的提示詞，也是 y；它從「在這個提示詞之下」的文字分布裡抽樣。
-->

---

<div class="eyebrow">03 · 2026 生成式 AI 地圖</div>

# 2026 生成式 AI 地圖：五類

<table style="font-size:17px">
<thead><tr><th style="width:31%">類別</th><th style="width:22%">產生什麼</th><th style="width:33%">代表例子</th><th>本課</th></tr></thead>
<tbody>
<tr><td><strong>LLM</strong>（大型語言模型）</td><td>文字、程式碼、JSON</td><td>Qwen、Llama、Claude</td><td>D1-2、D5</td></tr>
<tr><td><strong>擴散</strong>／Flow Matching（流匹配）</td><td>影像、影片</td><td>Stable Diffusion</td><td>D3、D4</td></tr>
<tr><td><strong>多模態</strong>（multimodal）</td><td>看圖說話</td><td>VLM（視覺語言模型）；CLIP 負責對齊文字與影像，本身不生成</td><td>D4-2、D6-2</td></tr>
<tr><td><strong>音訊</strong></td><td>音樂、語音</td><td>MusicGen、TTS（文字轉語音）</td><td>D2-4、D6-1</td></tr>
<tr><td><strong>Agent</strong>（LLM 組成的系統）</td><td>多步驟自動完成任務</td><td>Claude Code</td><td>下一個模組</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">選類別看「要產生什麼」；開放權重還是封閉 API，「買 API，還是自己跑」那頁再決定。</div>

<!--
★ 地圖（6 分）：每一列指出本課在哪一天處理。Agent 只點名：工具呼叫、MCP、RAG 都在下一個 Agent 模組，這門課不教。
開放權重 vs 封閉 API 是商業決定，不只是技術決定，「買 API，還是自己跑開放權重？」那頁再展開。
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

<div class="takeaway mt-8">每一個里程碑，課程裡都會有一天用到或親手做一個小版本。</div>

<div class="src">年份：arXiv 首次投稿日（VAE、GAN、Transformer、DDPM）、Stability AI 與 OpenAI 發布頁、Hugging Face 權重公開日（research/sources.md S8–S13）</div>

<!--
○ 時間軸（3 分）：只講年份與名字，下面一列是本課哪一天實作。時間不夠可略過。
-->

---

<div class="eyebrow">04 · Measure（量化驗收）</div>

# 從四個面向打分數，評估需求該怎麼做

<table style="font-size:18px">
<thead><tr><th style="width:18%">面向</th><th>要問的問題</th><th style="width:30%">1 分 → 5 分</th></tr></thead>
<tbody>
<tr><td><strong>價值</strong></td><td>做成了，每月省多少時間或多賺多少？</td><td>很少 → 很多</td></tr>
<tr><td><strong>可行性</strong></td><td>現成模型＋一張 T4 做得到嗎？</td><td>要大量研發 → 現成可用</td></tr>
<tr><td><strong>資料</strong></td><td>有足夠、合法、可用的資料嗎？</td><td>沒有 → 充足且有授權</td></tr>
<tr><td><strong>風險</strong></td><td>出錯的代價？個資、著作權？</td><td>很高 → 很低</td></tr>
</tbody>
</table>

<div class="node node--primary mt-3" style="font-size:18px">McKinsey（2023）估計（數字待確認）：生成式 AI 約 75% 的價值集中在<strong>客服、行銷與銷售、軟體工程、研發</strong>四個領域</div>

<div class="takeaway mt-3">四項都是分數越高越好（風險 5 分＝風險很低）；先做四項都高的需求。</div>

<div class="src">McKinsey Global Institute, The economic potential of generative AI (2023)，research/sources.md S1（原文與頁碼待確認：2026-11-26 兩次連線逾時）</div>

<!--
★ 四面向評估（5 分）：分數越高越好；特別強調風險 5 分代表風險很低，避免學員搞混方向。
曜嶼電子的需求單剛好落在這四個領域：客服（D5）、行銷（D1-2、D4）、研發與品保（D2、D3）。下一頁每個面向各舉一個高分、一個低分的例子。
-->

---

<div class="eyebrow">04 · Measure · 例子</div>

# 同樣用生成式 AI，分數可以差很多

<table style="font-size:17px">
<thead><tr><th style="width:12%">面向</th><th style="width:44%">高分的例子</th><th>低分的例子</th></tr></thead>
<tbody>
<tr><td><strong>價值</strong></td><td>用擴散模型產生<b>活動封面插圖</b>：省下找畫師、來回改稿的一兩週</td><td>用擴散模型產生<b>產品範例圖</b>：產品就在手邊，直接拍更快，也更準確</td></tr>
<tr><td><strong>可行性</strong></td><td>客服回覆草稿：現成 LLM 就寫得出來</td><td>一鍵生成 60 秒 4K 廣告影片：T4 跑不動，要大量研發</td></tr>
<tr><td><strong>資料</strong></td><td>行銷部有數百張自己拍、自己擁有的產品照</td><td>想模仿某位插畫家的畫風，但沒有任何授權作品</td></tr>
<tr><td><strong>風險</strong></td><td>內部會議的標語腦力激盪：寫錯也沒關係（5 分）</td><td>自動回覆客戶保固條款：答錯可能要賠（1 分）</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">同一個模型：封面插圖價值高，產品範例圖價值低。</div>

<!--
★ 例子（4 分）：先問：「用擴散模型產生圖片，價值高還是低？」讓學員發現答案是「看用在哪」。
封面插圖：原本要找畫師、等稿、改稿，生成模型省下的是一兩週和外包費，價值高。
產品範例圖：產品就在桌上，手機拍一張只要一分鐘，而且一定是真的產品；生成的圖還可能把按鍵、接孔畫錯，價值低。
風險欄再提醒一次方向：風險低＝高分。
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
★ 買或自己跑（5 分）：這一頁就是需求評估表的一個欄位。舉例：客服單有客戶個資 → 開放權重或去識別化；行銷文案沒有個資 → API 最快。
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
○ 不該用的地方（3 分）：這三點也是需求評估表「風險」欄位的檢查。
-->

---

<div class="eyebrow">05 · Ship（交付）· Lab L1-1</div>

# Lab L1-1 1／2：一張需求評估表有八格

<div class="grid grid-cols-4 gap-3 mt-3" style="font-size:18px">
  <div class="node"><strong>① 問題</strong><small>一句話</small></div>
  <div class="node"><strong>② KPI</strong><small>可量化的驗收</small></div>
  <div class="node"><strong>③ 資料</strong><small>有什麼、多少、授權</small></div>
  <div class="node"><strong>④ 模型家族</strong><small>LLM／擴散／音訊……</small></div>
  <div class="node"><strong>⑤ API 或開放權重</strong><small>理由一句</small></div>
  <div class="node node--warm"><strong>⑥ 最大風險</strong><small>個資、著作權、幻覺（流暢但錯）</small></div>
  <div class="node node--primary"><strong>⑦ 四項分數</strong><small>四項各 1–5 分</small></div>
  <div class="node node--primary"><strong>⑧ 決定</strong><small>先做／補資料／不做</small></div>
</div>

<div class="muted mt-3" style="font-size:16px">英文常見的說法是 use-case canvas（用例畫布）；這門課叫它「需求評估表」。</div>

<div class="takeaway mt-2">需求評估表＝把一張需求單翻譯成「能不能做、值不值得做」。</div>

<!--
★ 評估表欄位（3 分）：①②③來自需求單，④⑤是今天學的，⑥⑦⑧是判斷。下一頁看一個填好的例子。不需要 GPU。
名稱：英文叫 use-case canvas，「use case」在軟體工程譯成「用例」，但中文聽起來很陌生，所以課堂上一律叫「需求評估表」。學員在外面看到 AI canvas、use-case canvas 指的就是這種一頁表。
-->

---

<div class="eyebrow">05 · Ship · Lab L1-1</div>

# Lab L1-1 2／2：照著做——客服回覆草稿

<table style="font-size:17px">
<thead><tr><th style="width:22%">欄位</th><th>客服中心：「每張客服單都要寫回覆草稿」</th></tr></thead>
<tbody>
<tr><td>① 問題</td><td>客服人員每天花 3 小時打回覆，語氣不一致</td></tr>
<tr><td>② KPI</td><td>草稿採用率 ≥ 70%；平均回覆時間減半</td></tr>
<tr><td>③ 資料</td><td>過去的客服單與回覆（含客戶個資，需去識別化：把姓名、電話等個資遮掉）</td></tr>
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

# 練習 1／2：行銷部「每週要 50 張新品情境圖」

<div class="grid grid-cols-[0.75fr_1.6fr] gap-5 mt-1">
<div>

<img src="/scene-commuter.jpg" alt="戴耳機的年輕人走在斯德哥爾摩街頭的真實照片" style="width:100%;border:1px solid var(--border);border-radius:8px">
<div class="shot-cap"><b>產品情境圖</b>：產品出現在真實使用的場景</div>
<p style="font-size:17px" class="mt-2">現在：每張都要約模特兒外拍，一週拍不到 50 張</p>

</div>
<div>

<div class="muted" style="font-size:16px">1. 每格從選單挑一個　2. 四項分數各選 1–5（越高越好）　3. 總分自動加總</div>

<table class="fill tight vlines mt-1">
<tbody>
<tr><td style="width:24%">② KPI</td><td class="blank"><PickIn id="mkt.kpi" :options="['每週張數 ≥ 50 就好', '每張成本、可用率 ≥ 60%（人工挑過能用）', '圖越精緻越好']" /></td></tr>
<tr><td>③ 資料</td><td class="blank"><PickIn id="mkt.data" :options="['網路上抓的情境圖，授權不明', '自有產品照與品牌規範', '沒有任何產品照']" /></td></tr>
<tr><td>④ 模型家族</td><td class="blank"><PickIn id="mkt.family" :options="['LLM（文字）', '擴散模型（影像）', '一般分類器', '音訊模型']" /></td></tr>
<tr><td>⑤ API 或開放</td><td class="blank"><PickIn id="mkt.api" :options="['封閉 API：先快速試作', '開放權重：資料不出公司', '開放權重＋微調：品牌風格一致']" /></td></tr>
<tr><td>⑥ 最大風險</td><td class="blank"><PickIn id="mkt.risk" :options="['生成圖把產品細節畫錯', '模型授權、他牌商標、肖像權', '客戶個資外流']" /></td></tr>
</tbody>
</table>

<table class="fill tight vlines mt-2">
<thead><tr><th>⑦ 價值</th><th>可行性</th><th>資料</th><th>風險</th><th style="width:22%">總分</th></tr></thead>
<tbody><tr>
<td class="blank"><PickIn id="mkt.s1" hint="分" :options="['1','2','3','4','5']" /></td>
<td class="blank"><PickIn id="mkt.s2" hint="分" :options="['1','2','3','4','5']" /></td>
<td class="blank"><PickIn id="mkt.s3" hint="分" :options="['1','2','3','4','5']" /></td>
<td class="blank"><PickIn id="mkt.s4" hint="分" :options="['1','2','3','4','5']" /></td>
<td class="text-center"><ScoreSum :ids="['mkt.s1','mkt.s2','mkt.s3','mkt.s4']" :max="20" /></td>
</tr></tbody>
</table>

<table class="fill tight vlines mt-2">
<tbody><tr><td style="width:24%">⑧ 決定</td><td class="blank"><PickIn id="mkt.decide" :options="['先做', '先補資料或流程再做', '不做']" /></td></tr></tbody>
</table>

<FillClear group="mkt" />

</div>
</div>

<div class="src">照片：Yingchou Han（Unsplash），CC0（Wikimedia Commons，research/sources.md S16）</div>

<!--
★ 練習 1（6 分）：個人作業，不收回。選單裡有干擾選項（例如 KPI 的「每週張數 ≥ 50 就好」只算數量、「圖越精緻越好」量不出來；資料的「網路上抓的情境圖」授權不明），選錯也沒關係，重點是每一格說得出理由。
先讓學員看左邊的照片：這就是「產品情境圖」，產品出現在真實使用的場景裡。行銷部要的是每週 50 張這種圖。
目的：學員自己發現「這張可行性高，但產品細節可能被畫錯，授權、他牌商標和肖像也是風險」。連回「同樣用生成式 AI，分數可以差很多」：產品本身不能亂畫。答案在練習 2 之後的解答頁（學員網站不含）。
-->

---

<div class="eyebrow">05 · Ship · Lab L1-1 · 練習</div>

# 練習 2／2：品保部「AOI 新瑕疵常漏檢」

<div class="grid grid-cols-[0.75fr_1.6fr] gap-5 mt-1">
<div>

<div class="flex items-center gap-2"><span style="font-size:26px;color:var(--secondary);font-weight:700">✓</span><img src="/pcb1-normal.jpg" alt="良品電路板，四根針腳都是直的" style="width:72%;border:2px solid var(--secondary);border-radius:6px"></div>
<div class="shot-cap" style="margin-left:30px">良品：四根針腳都直</div>
<div class="flex items-center gap-2 mt-2"><span style="font-size:26px;color:var(--warm-accent);font-weight:700">✗</span><img src="/pcb1-bent-outline.jpg" alt="瑕疵電路板，一根針腳彎掉並以綠線標出" style="width:72%;border:2px solid var(--warm-accent);border-radius:6px"></div>
<div class="shot-cap" style="margin-left:30px">瑕疵：一根針腳彎掉（綠線）</div>
<p style="font-size:16px" class="mt-1">AOI（自動光學檢測）抓不到沒看過的新瑕疵；過殺＝良品被誤判成瑕疵</p>

</div>
<div>

<div class="muted" style="font-size:16px">1. 每格從選單挑一個　2. 四項分數各選 1–5（越高越好）　3. 總分自動加總</div>

<table class="fill tight vlines mt-1">
<tbody>
<tr><td style="width:24%">② KPI</td><td class="blank"><PickIn id="qa.kpi" :options="['每張成本、可用率 ≥ 60%', '漏檢率 ≤ 5%、過殺（良品被誤判）下降', '模型參數越多越好']" /></td></tr>
<tr><td>③ 資料</td><td class="blank"><PickIn id="qa.data" :options="['自有產品照與品牌規範', '大量良品、很少瑕疵、沒有新瑕疵', '網路上抓的圖，授權不明']" /></td></tr>
<tr><td>④ 模型家族</td><td class="blank"><PickIn id="qa.family" :options="['LLM（文字）', '異常偵測：只學良品，不像就報警', '一般分類器（要有瑕疵標註）', '音訊模型']" /></td></tr>
<tr><td>⑤ API 或開放</td><td class="blank"><PickIn id="qa.api" :options="['封閉 API：先快速試作', '開放權重：產線影像不出公司', '開放權重＋微調：品牌風格一致']" /></td></tr>
<tr><td>⑥ 最大風險</td><td class="blank"><PickIn id="qa.risk" :options="['模型授權、他牌商標', '漏檢造成客訴；過殺浪費人力', '客戶個資外流']" /></td></tr>
</tbody>
</table>

<table class="fill tight vlines mt-2">
<thead><tr><th>⑦ 價值</th><th>可行性</th><th>資料</th><th>風險</th><th style="width:22%">總分</th></tr></thead>
<tbody><tr>
<td class="blank"><PickIn id="qa.s1" hint="分" :options="['1','2','3','4','5']" /></td>
<td class="blank"><PickIn id="qa.s2" hint="分" :options="['1','2','3','4','5']" /></td>
<td class="blank"><PickIn id="qa.s3" hint="分" :options="['1','2','3','4','5']" /></td>
<td class="blank"><PickIn id="qa.s4" hint="分" :options="['1','2','3','4','5']" /></td>
<td class="text-center"><ScoreSum :ids="['qa.s1','qa.s2','qa.s3','qa.s4']" :max="20" /></td>
</tr></tbody>
</table>

<table class="fill tight vlines mt-2">
<tbody><tr><td style="width:24%">⑧ 決定</td><td class="blank"><PickIn id="qa.decide" :options="['先做', '先補資料或流程再做', '不做']" /></td></tr></tbody>
</table>

<FillClear group="qa" />

</div>
</div>

<div class="src">影像：VisA PCB1 良品與不良品 001（Zou et al., 2022，CC BY 4.0），講師裁切；D2-1 會用同一個資料集</div>

<!--
★ 練習 2（6 分）：先指兩張電路板：「左上這片是良品，下面這片有一根針腳彎掉。產線上的 AOI 認得它看過的瑕疵，但沒看過的新瑕疵常漏掉。」
目的：學員自己發現「品保這張價值和資料都高，但模型家族不是一般分類器」：一般分類器要每種瑕疵都有標註，新瑕疵根本沒有樣本。
選「一般分類器」的學員不用糾正太久，解答頁會說明；這就是 D2-1 的主題。
異常偵測讀作「只學良品長什麼樣，看到不像良品的就報警」，所以不需要新瑕疵的樣本（D2-1 實作）。過殺讀作「良品被誤判成瑕疵、白白丟掉」。
-->

---
hostOnly: true
---

<div class="eyebrow">05 · Ship · Lab L1-1 · 練習解答</div>

# 練習解答：參考需求評估表

<table class="tight vlines" style="font-size:16px">
<thead><tr><th style="width:18%">欄位</th><th>行銷部：每週 50 張新品情境圖</th><th>品保部：AOI 新瑕疵常漏檢</th></tr></thead>
<tbody>
<tr><td>② KPI</td><td>每張成本、可用率 ≥ 60%（人工挑過能用）</td><td>漏檢率 ≤ 5%、過殺（良品被誤判）下降</td></tr>
<tr><td>③ 資料</td><td>自有產品照與品牌規範</td><td>大量良品、很少瑕疵、沒有新瑕疵</td></tr>
<tr><td>④ 模型家族</td><td>擴散模型：只生成場景，產品用真實產品照合成（D4）</td><td>異常偵測（不是一般分類器：新瑕疵沒有標註）</td></tr>
<tr><td>⑤ API 或開放</td><td>開放權重＋微調（品牌一致）；或先用 API 試作</td><td>開放權重：產線影像不出公司</td></tr>
<tr><td>⑥ 最大風險</td><td>產品細節被畫錯；其次是授權、他牌商標、肖像（兩個都算對）</td><td>漏檢造成客訴；過殺浪費人力</td></tr>
<tr><td>⑦ 分數</td><td>例：價值 4／可行 4／資料 4／風險 3 ＝ 15</td><td>例：價值 5／可行 3／資料 4／風險 3 ＝ 15</td></tr>
<tr><td>⑧ 決定</td><td>先做（D4 實作）</td><td>先做（D2 實作）</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">怎麼判斷：②–⑥ 和上表一致就對；分數差 1 分沒關係，只要說得出理由。</div>

<!--
★ 解答（3 分）：強調品保那張的「模型家族」不是分類器，因為沒有新瑕疵的標註——這就是 D2-1 的主題。
行銷那張和「產品範例圖」的差別：情境圖要約模特兒、外拍，生成的是「場景」，省最多，所以價值 4；但產品本身不能讓模型亂畫（按鍵、接孔會畫錯），要用真實產品照合成進場景（D4 的 LoRA／局部重繪），所以可行性 4、最大風險是產品細節被畫錯。
-->

---

<div class="eyebrow">06 · Measure & Risk</div>

# 風險：生成的內容不等於查證過的內容

<div class="grid grid-cols-2 gap-6 mt-3">
<div>

<div class="node node--warm"><strong>幻覺</strong>（hallucination）<small>模型說得很流暢，但內容是錯的或編的</small></div>

<p style="font-size:18px" class="mt-3">真實例子（開場導覽時，講師在 Colab T4 跑的小模型）：文案寫「<b>續航 30 小時</b>」，下一句卻說「享受到長達 <b>2 小時</b>的續航時間」。</p>

</div>
<div>

<div class="node node--primary"><strong>規則</strong><small>出錯代價越高，越要人工審核</small></div>

- 數字、規格、法律用語 → 對照原始資料
- 對外發布 → 人工送出前審核
- 用字（另外兩版混進簡體字，不是幻覺，但一樣要改）
- 留下提示詞與輸出紀錄

</div>
</div>

<div class="takeaway mt-4">生成模型是從分布裡抽樣，不是查資料庫；抽到「看起來合理但錯」的內容很正常。</div>

<!--
★ 風險（4 分）：連回「生成模型學的是『真實照片落在哪一塊』」那頁：模型抽的是「看起來像」的點，不保證是真的。Vibe Coding 學過「Agent 的程式要稽核」，生成內容也一樣。
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

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">需求單</span><span class="arrow">→</span>
  <span class="chip">判別 vs 生成</span><span class="arrow">→</span>
  <span class="chip">p<sub>data</sub> 與 p<sub>θ</sub></span><span class="arrow">→</span>
  <span class="chip">條件 p(x|y)</span><span class="arrow">→</span>
  <span class="chip">四面向評估</span><span class="arrow">→</span>
  <span class="chip">需求評估表</span>
</div>

<div class="takeaway mt-6">生成模型學「通常長什麼樣」再抽樣；用不用它，先看價值、可行性、資料與風險。</div>

<!--
★ 總整理（2 分）：回到需求單：執行長要的一頁需求評估表，學員已經填好兩張。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 1／2（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="2"
  :options="['判斷電路板是否有瑕疵', '預測下個月營收', '產生一張新的產品情境圖', '把客服單分成五類']"
  :why="['這是判別：輸入一張圖，輸出「良品／瑕疵」一個標籤。', '預測一個數字是迴歸，輸出不是一整筆新資料。', '', '分成五類是分類（判別），輸出的是標籤。']"
  explain="生成模型的輸出是一整筆新資料（一張新的圖），不是標籤，也不是一個數字。">
下列哪一個是<b>生成</b>任務？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="1"
  :options="['θ：模型參數', '輸入給模型的條件', '損失函數', 'x：生成出來的那張圖']"
  :why="['θ 是模型參數，訓練完就固定；換提示詞不會改變 θ。', '', '損失函數只在訓練時用，生成時用不到。', '生成出來的圖是 x（直線左邊），不是 y。']"
  explain="直線右邊的 y 是條件：「在 y＝白色的貓之下」，抽樣範圍縮小到白貓那一小塊。">
對影像模型輸入提示詞「白色的貓」，模型就從 p<sub>θ</sub>(x | y) 抽一張圖。這裡的 <b>y</b> 是什麼？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／2（2 分）：學員自己點；點錯會出現「再想想」和那個選項錯在哪，可以再點一次。答案：1 C、2 B。
第 2 題回扣「提示詞就是條件」那頁：p_θ(x | y) 的直線讀作「在……之下」，左邊 x 是要生成的圖，右邊 y 是條件。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／2（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="1"
  :options="['直接用免費聊天網站', '開放權重模型在公司內部執行', '不做任何評估就上線', '只用分類器']"
  :why="['免費方案可能把輸入拿去改進服務，客戶個資就離開公司了。', '', '沒評估就上線，需求評估表的風險欄根本沒填。', '分類器只會分類，寫不出回覆草稿。']"
  explain="開放權重模型在公司自己的機器上跑，客戶資料不會送出去。">
客服單含客戶個資，公司不希望資料離開內部，最適合？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="2"
  :options="['文案初稿', '腦力激盪標語', '產品安全規格說明', '產品圖草稿']"
  :why="['初稿本來就會有人改，寫錯代價低。', '腦力激盪要的就是多樣，寫錯也沒關係。', '', '草稿圖之後還會經過設計師。']"
  explain="安全規格需要唯一正確的答案，出錯代價又極高，至少要人工複核。">
下列哪個情境<b>最不適合</b>直接交給生成式 AI 而無人審核？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／2（2 分）。答案：3 B、4 C。
理由：3 資料不出門；4 出錯代價高且需要正確答案（回扣「哪裡不該用生成式 AI」）。
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
