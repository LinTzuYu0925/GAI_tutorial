---
theme: default
title: 活動影片的配樂與旁白
info: |
  生成式AI原理 · D6-1
  行銷部要免版稅配樂和國語旁白：聲音也能切成 token（EnCodec），交給 Transformer 接龍（MusicGen）；文字轉語音（TTS）；而真正的限制是授權與聲音同意。
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
exportFilename: 21-music-and-voice
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D6-1</div>

# 活動影片的配樂與旁白

<p class="subtitle">聲音也是 token：MusicGen 生成配樂、TTS 念旁白；但能不能用，要先看授權</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">授權是真正的限制</span><span class="arrow">→</span>
  <span class="chip">波形與頻譜</span><span class="arrow">→</span>
  <span class="chip">EnCodec token</span><span class="arrow">→</span>
  <span class="chip">MusicGen 接龍</span><span class="arrow">→</span>
  <span class="chip">TTS</span><span class="arrow">→</span>
  <span class="chip">聲音同意</span>
</div>

<!--
★ 開場（2 分）：第六天是「上市與交付」。第一堂處理聲音：D2-4 把聲音壓成 token，D5-2 學會接龍；今天兩個加起來就能作曲。但今天的主角其實是授權。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 行銷部：活動影片需要免版稅配樂和國語旁白

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D6-1】部門：行銷部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>活動影片需要免版稅配樂與國語旁白</dd>
    <dt>現況痛點</dt><dd>買版權音樂貴，授權條款複雜</dd>
    <dt>成功指標（KPI）</dt><dd>聽感測試（自己打分）；生成時間與片長的關係；一份授權說明</dd>
    <dt>可用資料</dt><dd>文字提示；一句旁白稿</dd>
    <dt>限制與法規</dt><dd>MusicGen 權重為非商用授權；聲音複製需當事人同意</dd>
    <dt>為何現有工具不夠</dt><dd>影像與文字模型不會產生聲音</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：先預告結論：技術上做得到，但今天生成的配樂不能放進公司的正式廣告。為什麼？第 4 頁。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**取樣率、波形、頻譜圖（spectrogram）
2. **算出**一段音樂是幾個 token（EnCodec：每秒 50 個時間點 × 4 本編碼簿）
3. **說明** MusicGen ＝ 文字條件 ＋ Transformer 接聲音 token（和 D5-2 同一套）
4. **說明** TTS（文字轉語音）的三個步驟
5. **判斷**一段生成的聲音能不能商用：權重授權、聲音同意

<div class="takeaway mt-4">做得出來 ≠ 能用：今天每一段聲音都要附一行授權說明。</div>

<!--
★ 目標（1 分）。不教：旋律條件（○）、編碼簿交錯的 delay pattern（△ 附錄）、聲音複製的實作（只談同意）、音樂理論。
-->

---

<div class="eyebrow">00 · Frame · 真正的限制</div>

# 授權才是真正的限制

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:30%">今天用到的東西</th><th style="width:24%">授權</th><th>代表什麼</th></tr></thead>
<tbody>
<tr><td>MusicGen 程式碼</td><td>MIT</td><td>程式可以自由用</td></tr>
<tr><td><b>MusicGen 權重</b>（模型本身）</td><td><b>CC-BY-NC 4.0</b></td><td><b>非商用</b>：非營利研究、個人學習可以；公司廣告不行</td></tr>
<tr><td>Kokoro-82M-v1.1-zh（TTS）</td><td>Apache-2.0</td><td>可商用</td></tr>
<tr><td>BreezyVoice（台灣口音 TTS）</td><td>Apache-2.0</td><td>可商用，但聲音複製要當事人同意</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">同一個模型，「程式」和「權重」的授權可以不同：要看的是權重那一行。</div>

<div class="src">HF 模型卡 license 欄位（2026-11-26 以 Hugging Face API 讀取，S1–S3）；MusicGen 程式 MIT（audiocraft 說明，S1）。AI 生成標示是另一件事，見 D6-3</div>

<!--
★ Frame（5 分）：D1-4、D5-3 都談過授權，今天是最直接的例子。NC＝Non-Commercial。學員常以為「開源＝能商用」：MusicGen 的程式是 MIT，但權重是 NC，產品要用的是權重。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 一句英文提示 → 5 秒配樂

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-3 items-center" style="font-size:18px">
<div>

<div class="node"><strong>提示詞</strong><small>upbeat electronic jingle for a tech product launch, bright synth, 120 bpm</small></div>

<audio controls src="/jingle.wav" style="width:100%;margin-top:14px"></audio>
<div class="shot-cap">MusicGen-small，seed 0，guidance 3.0；講師本機 CPU 實跑：4.9 秒的配樂，生成 26.7 秒（T4 待講師實跑）</div>

</div>
<div>

- 先聽：像不像科技新品的廣告？
- 再猜：這 4.9 秒的聲音，是幾個數字？幾個 token？
- 答案在後面兩頁

</div>
</div>

<div class="takeaway mt-3">和 D1-2 生成文案、D4-2 生成圖片一樣：一句文字當條件，模型生成另一種媒體。</div>

<!--
★ Try（5 分）：現場播放。提示詞用英文，因為 MusicGen 的文字編碼器是英文的 T5。授權提醒：這一段只能在課堂播放。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 聲音是什麼</div>

# 波形與頻譜圖：同一段聲音的兩種畫法

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-1 items-center">
<div>

<img class="photo" src="/waveform_spectrogram.png" alt="上圖是波形，振幅隨時間上下跳動；下圖是頻譜圖，橫軸時間、縱軸頻率，亮的地方是大聲的頻率" style="width:100%">
<div class="shot-cap">上一頁那段配樂；lab 第 1 部分，講師本機實跑</div>

</div>
<div style="font-size:18px">

- **取樣率 32 kHz**：每秒記 32,000 個數字（振幅）
- 4.9 秒 → **158,080 個數字**
- **波形**：每個時間點的振幅（聲音的「形狀」）
- **頻譜圖**：每個時間點有哪些高低音，越亮越大聲（像樂譜）

</div>
</div>

<div class="takeaway mt-2">聲音就是一長串數字：太長了，直接接龍不實際，要先壓縮。</div>

<!--
★ 聲音基礎（5 分）：頻譜圖的橫線＝持續的音高（和弦、合成器），直條＝瞬間的打擊樂。比喻：波形像錄音機的指針，頻譜圖像鋼琴捲軸。
-->

---

<div class="eyebrow">02 · Open · 聲音變 token</div>

# EnCodec：每 20 毫秒壓成 4 個整數（D2-4 學過）

<svg viewBox="0 0 900 200" style="width:100%" aria-label="波形經過 EnCodec 編碼器變成 4 列整數的格子，每秒 50 欄；格子可以再由解碼器還原成波形">
  <defs><marker id="ec-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <path d="M10,95 Q25,40 40,95 T70,95 T100,95 T130,95 T160,95" fill="none" stroke="var(--primary)" stroke-width="2"/>
  <text x="10" y="160" style="font-size:16px" fill="var(--text)">波形 32,000／秒</text>
  <rect x="200" y="70" width="150" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="215" y="101" style="font-size:17px" fill="var(--text)">EnCodec 編碼</text>
  <g style="font-size:17px" fill="var(--text)">
  <rect x="400" y="30" width="330" height="130" fill="var(--soft-amber)" stroke="var(--warm-accent)"/>
  <text x="410" y="55">編碼簿 1： 461　 37　 912　 …</text>
  <text x="410" y="85">編碼簿 2：  95　803　 15　 …</text>
  <text x="410" y="115">編碼簿 3： 604　 12　777　 …</text>
  <text x="410" y="145">編碼簿 4：1104　540　 88　 …</text>
  </g>
  <text x="400" y="185" style="font-size:16px" fill="var(--warm-accent)">每秒 50 欄 × 4 列；每格是 0～2047 的整數</text>
  <rect x="770" y="70" width="120" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="788" y="101" style="font-size:17px" fill="var(--text)">解碼還原</text>
  <g stroke="var(--primary)" stroke-width="2.5"><line x1="165" y1="95" x2="196" y2="95" marker-end="url(#ec-a)"/><line x1="350" y1="95" x2="396" y2="95" marker-end="url(#ec-a)"/><line x1="730" y1="95" x2="766" y2="95" marker-end="url(#ec-a)"/></g>
</svg>

<div class="muted" style="font-size:16px">D2-4 的 EnCodec 是 24 kHz、每秒 75 步；MusicGen 用 32 kHz、每秒 50 步、每本 2048 個碼的版本。第一欄的 4 個數字（461、95、604、1104）是 lab 實際印出的；其他欄是示意。lab 印出 <code>audio_codes 形狀：(1, 1, 4, 247)</code>，讀作［1 段, 批次 1, 4 本編碼簿, 247 個時間點（4.9 秒）］。</div>

<div class="takeaway mt-2">編碼簿 1 抓大致的聲音，後面幾本一層一層補細節（D2-4 的殘差向量量化）。</div>

<!--
★ EnCodec（8 分）：D2-4 用 EnCodec 24 kHz 壓客服錄音；MusicGen 用的是 32 kHz、4 本編碼簿的版本。重點數字：50 個時間點／秒。下一頁讓 Transformer 來接這些整數。
-->

---

<div class="eyebrow">02 · Open · MusicGen</div>

# MusicGen ＝ 文字條件 ＋ Transformer 接聲音 token

<svg viewBox="0 0 900 200" style="width:100%" aria-label="英文提示經過文字編碼器 T5 變成向量，透過交叉注意力交給 Transformer 解碼器；解碼器一個時間點一個時間點地接出 4 個聲音 token，最後由 EnCodec 解碼成波形">
  <defs><marker id="mg-a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--primary)"/></marker></defs>
  <g style="font-size:16px">
  <rect x="10" y="20" width="190" height="50" rx="8" fill="var(--surface)" stroke="#b8b8b8"/><text x="20" y="50" fill="var(--text)">"upbeat jingle…"</text>
  <rect x="240" y="20" width="160" height="50" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="252" y="50" fill="var(--text)">文字編碼器（T5）</text>
  <rect x="300" y="110" width="250" height="70" rx="8" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/><text x="315" y="140" fill="var(--text)">Transformer 解碼器</text><text x="315" y="165" style="font-size:15px" fill="var(--muted-text)">D5-2 的接龍，接的是聲音 token</text>
  <rect x="600" y="110" width="140" height="70" rx="8" fill="var(--surface)" stroke="var(--warm-accent)"/><text x="612" y="142" fill="var(--text)">4 個 token</text><text x="612" y="165" style="font-size:17px" fill="var(--muted-text)">／20 毫秒</text>
  <rect x="780" y="110" width="115" height="70" rx="8" fill="var(--soft-blue)" stroke="var(--primary)"/><text x="792" y="140" fill="var(--text)">EnCodec</text><text x="792" y="164" fill="var(--text)">解碼</text>
  <text x="435" y="92" style="font-size:17px" fill="var(--primary)">交叉注意力（D4-2）</text>
  </g>
  <g stroke="var(--primary)" stroke-width="2.5" fill="none"><line x1="200" y1="45" x2="236" y2="45" marker-end="url(#mg-a)"/><path d="M400,45 L425,45 L425,106" marker-end="url(#mg-a)"/><line x1="550" y1="145" x2="596" y2="145" marker-end="url(#mg-a)"/><line x1="740" y1="145" x2="776" y2="145" marker-end="url(#mg-a)"/><path d="M670,182 L670,195 L420,195 L420,184" marker-end="url(#mg-a)"/></g>
</svg>

<div class="grid grid-cols-2 gap-5 mt-1" style="font-size:17px">
<div class="node"><strong>和 D5-2 一樣</strong><small>預測下一步、抽樣、接上去；因果遮罩；溫度也能調</small></div>
<div class="node node--primary"><strong>和 D4-2 一樣</strong><small>文字透過交叉注意力當條件；<code>guidance_scale=3</code> 就是 CFG（D4-1）</small></div>
</div>

<div class="takeaway mt-2">換一個詞彙表（2048 種聲音 token），同一套 Transformer 就從寫字變成作曲。</div>

<!--
★ MusicGen（8 分）：把三天串起來：D2-4 的 token、D4-1/D4-2 的條件與 CFG、D5-2 的接龍。每一步同時產生 4 本編碼簿的 token，細節（delay pattern）在附錄。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：一段配樂是幾個 token？

<div class="grid grid-cols-[1fr_1.4fr] gap-5 mt-1" style="font-size:17px">
<div class="node"><strong>照著做：10 秒</strong><small>每秒 50 個時間點 × 4 本編碼簿 ＝ 200 token／秒<br>10 秒 × 200 ＝ <b>2,000 個 token</b><br>原始波形：10 × 32,000 ＝ 320,000 個數字</small></div>
<div>

<table class="fill tight vlines">
<thead><tr><th style="width:30%">片長</th><th>token 數</th><th>原始數字數</th></tr></thead>
<tbody>
<tr><td>30 秒（廣告）</td><td class="blank"><FillIn id="tok.30" hint="例：1,234……" /></td><td class="blank"><FillIn id="raw.30" /></td></tr>
<tr><td>2 分鐘（整首）</td><td class="blank"><FillIn id="tok.120" /></td><td class="blank"><FillIn id="raw.120" /></td></tr>
<tr><td colspan="2">壓縮了幾倍？</td><td class="blank"><FillIn id="tok.ratio" /></td></tr>
</tbody>
</table>

<FillClear group="tok" />

</div>
</div>

<div class="muted mt-2" style="font-size:16px">做完後：lab 第 2 部分的 <code>tokens_per_second()</code> 會印出 30 秒的答案。</div>

<!--
★ 練習（7 分）：個人、不收回。發現：一首 2 分鐘的歌是 24,000 個 token，比 D5 的客服回覆長一百多倍：這就是生成長音樂很慢、很吃記憶體的原因（D5-2 的 T × T）。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：壓縮 160 倍，但還是很長

<table class="vlines" style="font-size:19px">
<thead><tr><th>片長</th><th>token 數</th><th>原始數字數</th></tr></thead>
<tbody>
<tr><td>30 秒</td><td>30 × 200 ＝ 6,000</td><td>30 × 32,000 ＝ 960,000</td></tr>
<tr><td>2 分鐘</td><td>120 × 200 ＝ 24,000</td><td>120 × 32,000 ＝ 3,840,000</td></tr>
<tr><td colspan="2">壓縮倍數</td><td>32,000 ÷ 200 ＝ 160 倍</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：lab 印出「30 秒的廣告配樂 ≈ 6,000 個 token」。</div>

<!--
★ 解答（2 分）：補充：MusicGen 訓練時一次只看 30 秒，所以預設最長約 30 秒；要更長要用續寫的技巧。
-->

---

<div class="eyebrow">02 · Open · 名字的由來</div>

# 為什麼課綱的「MusicNet」變成 MusicGen

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:19px">
<div class="node"><strong>MusicNet</strong><small>一個<b>資料集</b>：古典音樂錄音，加上每個音符的標註（哪個樂器、什麼音高）。用來訓練「聽音樂、標音符」的模型</small></div>
<div class="node node--primary"><strong>MusicGen</strong><small>一個<b>生成模型</b>：文字 → 音樂。今天的主角；用 2 萬小時授權音樂訓練</small></div>
</div>

<div class="takeaway mt-4">課綱 #14 的目標是「生成音樂」：用今天的生成模型 MusicGen 來教，MusicNet 只認名字。</div>

<div class="src">Thickstun et al., MusicNet, 2017；Copet et al., MusicGen, 2023（S4、S5，待確認）</div>

<!--
★ 名字（2 分）：這是課程設計的說明，讓學員知道課綱和教材對得上。
-->

---

<div class="eyebrow">02 · Open · TTS</div>

# TTS（文字轉語音）：三個步驟

<div class="steps mt-3" style="font-size:19px">
  <div><span class="num">1</span><strong>文字 → 讀音</strong>：斷詞、標注音或拼音；「行」念 ㄒㄧㄥˊ 還是 ㄏㄤˊ？（破音字）</div>
  <div><span class="num">2</span><strong>讀音 → 聲學特徵</strong>：模型決定每個音多長、多高、什麼音色（說話人）</div>
  <div><span class="num">3</span><strong>聲學特徵 → 波形</strong>：聲碼器（vocoder）變成 24,000 個數字／秒；常用 GAN 訓練（D3-1）</div>
</div>

<div class="muted mt-3" style="font-size:17px">lab 的 Kokoro：「曜嶼電子新品上市……」先轉成一串注音式的讀音符號（講師本機印出的開頭是「要4/ㄩ3/ㄉ言4…」），再生成 24 kHz 的聲音。</div>

<div class="takeaway mt-3">台灣口音難在第 1 步：破音字和台灣讀法；BreezyVoice 的模型卡說它用注音輸入來處理。</div>

<div class="src">Kokoro 讀音：lab21 本機實跑；BreezyVoice：HF 模型卡與 arXiv 2501.17790（S3，細節待確認）</div>

<!--
★ TTS（5 分）：GAN 不是過時技術的又一個例子：很多聲碼器（HiFi-GAN）用對抗損失訓練（第三天說過）。
-->

---

<div class="eyebrow">03 · 授權的一課</div>

# 非商用權重：示範可以，產品不行

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--primary"><strong>可以</strong><small>非營利的研究、個人學習。付費課程的課堂示範：待艾鍗確認</small></div>
<div class="node node--warm"><strong>不行</strong><small>放進公開的廣告、賣錢的影片、App 的背景音樂（即使只有 5 秒）；公司內部用途是否算商用：交法務判斷</small></div>
</div>

<div class="mt-3" style="font-size:18px">

正式版的三條路：① 換權重是可商用授權的模型（條款逐一確認）② 向權利人買授權 ③ 請作曲家

</div>

<div class="takeaway mt-3">授權看「用途」，不看「長度」：5 秒也算商用。</div>

<!--
★ 授權（4 分）：課程地圖 §14 的待決事項：付費課程使用 NC 資產是否可以，要問艾鍗。這裡的立場：只在課堂示範，交付給行銷部的說明一定要寫清楚。
-->

---

<div class="eyebrow">03 · 聲音同意</div>

# 聲音複製：一定要當事人同意

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>技術上很容易</strong><small>一小段錄音就能讓 TTS 模仿一個人的聲音（BreezyVoice 的模型卡說明它支援聲音複製）</small></div>
<div class="node node--primary"><strong>公司的規則</strong><small>① 只用合成聲音，或 ② 有當事人書面同意（用途、期間、可撤回）；代言人、員工、客人都一樣</small></div>
</div>

<div class="takeaway mt-4">聲音是個人的特徵：沒有同意就模仿，可能侵害人格權或個資（細節交法務判斷），也可能被用來詐騙。</div>

<div class="src">BreezyVoice 模型卡（S3，細節待確認）</div>

<!--
★ 同意（4 分）：今天的 lab 只用 Kokoro 內建的合成聲音，不做聲音複製。法律細節（肖像權、個資法對聲紋的規定）由法務判斷。
-->

---

<div class="eyebrow">04 · 延伸 · 只認名字</div>

# 旋律條件、可商用的替代方案

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>旋律條件（melody conditioning）</strong><small>MusicGen-melody：除了文字，再給一段旋律，讓生成的配樂跟著哼的曲調走</small></div>
<div class="node node--secondary"><strong>其他音樂模型</strong><small>Stable Audio Open 等：授權條款各不相同（社群授權、營收門檻），上線前逐條確認</small></div>
</div>

<div class="takeaway mt-4">換模型前先讀授權：「開放」的定義每家不同。</div>

<div class="src">S6（待確認）</div>

<!--
○ 選修（2 分）：只認名字；條款待確認（S6）。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 4 本編碼簿怎麼同時接龍：delay pattern（延遲排列，選讀）

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2 items-center">
<div>

<table class="vlines" style="font-size:17px;text-align:center">
<thead><tr><th>步驟</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr></thead>
<tbody>
<tr><td>編碼簿 1</td><td>t1</td><td>t2</td><td>t3</td><td>t4</td><td>t5</td></tr>
<tr><td>編碼簿 2</td><td>·</td><td>t1</td><td>t2</td><td>t3</td><td>t4</td></tr>
<tr><td>編碼簿 3</td><td>·</td><td>·</td><td>t1</td><td>t2</td><td>t3</td></tr>
<tr><td>編碼簿 4</td><td>·</td><td>·</td><td>·</td><td>t1</td><td>t2</td></tr>
</tbody>
</table>

</div>
<div style="font-size:18px">

- 每一步同時預測 4 個 token，但每本編碼簿晚一步（樓梯狀）
- 編碼簿 2 預測時間點 t1 時，編碼簿 1 的 t1 已經有了
- 比「4 本攤平成一長串」快約 4 倍，品質相近

</div>
</div>

<div class="takeaway mt-3">樓梯狀錯開：又能平行算，又讓細節編碼簿看得到粗略編碼簿。</div>

<div class="src">Copet et al., 2023（S5，待確認）</div>

<!--
△ 附錄（1 分）：學員問「4 本編碼簿怎麼一起生成」時再講。
-->

---

<div class="eyebrow">05 · Lab L6-1</div>

# Lab 1／4：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:18px">
<div>

**打開筆記本**：<code>lab21-music-voice.ipynb</code>（在 <code>materials/</code>）→ Open in Colab；執行階段：**T4 GPU**

1. 三種風格的提示詞，聽得出差別嗎？
2. 片長加倍，生成時間也加倍嗎？
3. 中文旁白自然嗎？哪個字念錯？

</div>
<div>

<div class="node node--primary"><strong>要交出的三樣東西</strong><small>① 三段 5 秒配樂（三種風格）<br>② 一張「片長 vs 生成時間」圖<br>③ 一段中文旁白</small></div>

</div>
</div>

<div class="src">Colab：colab.research.google.com/github/LinTzuYu0925/GAI_tutorial/blob/day6-done/21-music-and-voice/materials/lab21-music-voice.ipynb</div>

<div class="takeaway mt-1">交付給行銷部：一段配樂＋一段旁白＋三行授權說明。</div>

<!--
★ Lab 開始（5 分）：這是「Try」型 lab（四頁）：模型都是現成的，重點在量測與授權。CPU 也能跑，但每 5 秒配樂要等二、三十秒。
-->

---

<div class="eyebrow">05 · Lab L6-1</div>

# Lab 2／4：Specify → Execute

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>三段 5 秒配樂、一張片長 vs 時間圖、一段中文旁白<br>
<strong>【輸入與輸出】</strong>英文提示 → <code>mg.generate</code> → 波形 <code>&#91;1, 1, 樣本數&#93;</code>（32 kHz）；旁白文字 → Kokoro → 24 kHz 波形<br>
<strong>【限制】</strong>MusicGen-small；<code>guidance_scale=3.0</code>；一次只改一件事（先換提示、再換長度）<br>
<strong>【驗收】</strong>① <code>audio_codes</code> 形狀是 (1, 1, 4, 約 50 × 秒數)　② 三段配樂聽得出風格差別　③ 時間圖有三個點　④ 旁白可以播放

</div>

<div class="steps mt-3" style="font-size:17px">
  <div><span class="num">1</span>TODO 只有一個：<code>tokens_per_second()</code>（編碼簿數 × 每秒時間點）</div>
  <div><span class="num">2</span>TTS 失敗（套件或下載問題）：筆記本會自動下載講師的 <code>voiceover.wav</code> 來聽</div>
</div>

<!--
★ Specify＋執行（約 20 分）：MusicGen 下載約 2 GB。提示詞要用英文。
-->

---

<div class="eyebrow">05 · Lab L6-1</div>

# Lab 3／4：Measure：聽感測試與時間

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

1. 三段配樂，各打 1～5 分：「適合放進那種活動影片嗎？」（先寫，再聽別人的）
2. 看時間圖：片長加倍，生成時間大約變幾倍？
3. 旁白：找一個念錯或不自然的地方，記下來

</div>
<div>

<img class="photo" src="/length_vs_time.png" alt="片長 5、10、15 秒對應的生成時間折線圖，大致是一直線" style="width:100%">
<div class="shot-cap">講師本機 CPU：5 秒的配樂每次約 17～27 秒（第一次較慢：暖機）；T4 待講師實跑</div>

</div>
</div>

<div class="takeaway mt-3">聲音的品質只能用耳朵量：多人、各自、先寫再統計（D4-4 的人的評分）。</div>

<!--
★ Measure（14 分）：講師本機 CPU：片長 5／10／15 秒 → 生成 17.3／37.5／62.9 秒。時間大約和片長成正比（每一步產生一個時間點）；但注意力是 T × T，越長每一步越慢一點。
-->

---

<div class="eyebrow">05 · Lab L6-1 · Ship</div>

# Lab 4／4：交付：配樂＋旁白＋授權說明

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

<audio controls src="/voiceover.wav" style="width:100%"></audio>
<div class="shot-cap">Kokoro-82M-v1.1-zh，聲音 zf_001：「曜嶼電子新品上市，藍牙耳機限時優惠，歡迎到官網選購。」講師本機 CPU 實跑</div>

</div>
<div class="node node--primary"><strong>授權說明範本（三行）</strong><small>① 配樂：MusicGen-small 生成，權重 CC-BY-NC 4.0 → 不能用在正式廣告（內部用途是否可以：交法務），正式版要換方案<br>② 旁白：Kokoro（Apache-2.0）合成聲音，沒有模仿真人<br>③ 影片上標示「本影片配樂與旁白由 AI 生成」</small></div>
</div>

<div class="takeaway mt-3">交付的不只是檔案：一段聲音配一行「能不能用、為什麼」。</div>

<!--
★ Ship（8 分）：Kokoro 的中文聲音是大陸口音；需要台灣口音時，講師示範 BreezyVoice（Apache-2.0，安裝較複雜，聲音複製一定要有同意書）。
-->

---

<div class="eyebrow">06 · 風險（Risk）</div>

# 風險：音樂著作權、聲音同意、深偽語音

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:22%">風險</th><th>例子</th><th style="width:34%">怎麼做</th></tr></thead>
<tbody>
<tr><td>音樂著作權</td><td>提示「像某某歌手的歌」，生成的旋律太像原曲</td><td>不在提示裡指名歌手或歌曲；正式使用前比對</td></tr>
<tr><td>聲音同意</td><td>用代言人的舊影片聲音做旁白</td><td>沒有書面同意就不做</td></tr>
<tr><td>深偽語音</td><td>假冒主管的聲音打電話要求轉帳</td><td>公司內部流程：金錢指示一律二次確認</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">聲音生成越來越像真的：標示 AI 生成，並把「聽到的不一定是真的」寫進公司流程。</div>

<!--
★ 風險（3 分）：深偽語音詐騙是真實存在的手法；這裡只建立警覺，不教製作。D6-3 的合規檢查表會再出現。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">32,000 個數字／秒</span><span class="arrow">→</span>
  <span class="chip">EnCodec：200 token／秒</span><span class="arrow">→</span>
  <span class="chip">Transformer 接聲音 token</span><span class="arrow">→</span>
  <span class="chip">文字條件＋CFG</span><span class="arrow">→</span>
  <span class="chip">TTS 三步驟</span><span class="arrow">→</span>
  <span class="chip">權重授權＋聲音同意</span>
</div>

<div class="takeaway mt-6">聲音＝token 序列：D2-4 的壓縮＋D5-2 的接龍＋D4 的條件；能不能用，看權重授權和當事人同意。</div>

<!--
★ 總整理（2 分）：請學員說出 MusicGen 每秒幾個 token、權重是什麼授權。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq" style="font-size:17px">

1. 32 kHz 取樣率的意思是？（　）<br><span class="opts"><span class="nw">A. 每秒記錄 32,000 個振幅數值</span>　<span class="nw">B. 最高音是 32 kHz</span>　<span class="nw">C. 每秒 32 個 token</span>　<span class="nw">D. 檔案 32 KB</span></span>
2. MusicGen 每秒 50 個時間點、4 本編碼簿，20 秒是幾個 token？（　）<br><span class="opts"><span class="nw">A. 50</span>　<span class="nw">B. 200</span>　<span class="nw">C. 4,000</span>　<span class="nw">D. 640,000</span></span>
3. MusicGen 程式碼是 MIT、權重是 CC-BY-NC 4.0，能否放進公司付費廣告？（　）<br><span class="opts"><span class="nw">A. 可以，因為程式是 MIT</span>　<span class="nw">B. 不行，權重是非商用授權</span>　<span class="nw">C. 5 秒以內可以</span>　<span class="nw">D. 標示 AI 生成就可以</span></span>
4. 要用代言人的聲音做 AI 旁白，最重要的前提是？（　）<br><span class="opts"><span class="nw">A. 錄音品質夠好</span>　<span class="nw">B. 用台灣口音的模型</span>　<span class="nw">C. 取得當事人書面同意</span>　<span class="nw">D. 用 GPU 生成</span></span>

</div>

<!--
★ 檢核（3 分）。答案：1 A、2 C（20 × 200）、3 B（D 錯：標示不會改變授權）、4 C。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D6-2：一萬張沒有標籤的商品照，顧客用中文搜尋

<div style="font-size:19px" class="mt-4">

- 電商部：只能用檔名搜尋，找不到就不會買
- D4-2 的 CLIP：圖片和文字放進同一個空間；今天換成懂中文的多語模型
- 再用小型 VLM 替每張圖寫繁中說明（alt-text）

</div>

<!--
★ 下一步（1 分）：預告。
-->
