---
theme: default
title: 產品情境照工作室
info: |
  生成式AI原理 · L14
  行銷部要依企劃文字生成產品情境照、替產品照換背景：CLIP 把文字變成條件，Stable Diffusion 1.5 在潛在空間生成；img2img、inpainting、CLIP 分數與偏差稽核。
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
exportFilename: 14-stable-diffusion-studio
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · L14</div>

# 產品情境照工作室

<p class="subtitle">CLIP ＋ Stable Diffusion 1.5：企劃文字變照片，產品照換背景</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">文字當條件</span><span class="arrow">→</span>
  <span class="chip">CLIP</span><span class="arrow">→</span>
  <span class="chip">SD 四個零件</span><span class="arrow">→</span>
  <span class="chip">參數與負面提示詞</span><span class="arrow">→</span>
  <span class="chip">img2img、inpainting</span><span class="arrow">→</span>
  <span class="chip">CLIP 分數、偏差稽核</span>
</div>

<!--
★ 開場（2 分）：L13 的條件是一個類別編號；今天的條件是一段文字。L02 第一次用 SD1.5 時是黑盒子，今天每一個零件都是前幾天學過的東西。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 行銷部：依企劃文字生成情境照，還要換背景

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #L14】部門：行銷部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>依企劃文字生成產品情境照，並替現有產品照換背景</dd>
    <dt>現況痛點</dt><dd>每次活動都要外拍：場地、模特兒、攝影師</dd>
    <dt>成功指標（KPI）</dt><dd>CLIP 分數（貼不貼題）；行銷部可用率；有人物的提示詞通過偏差檢查</dd>
    <dt>可用資料</dt><dd>企劃文字；自有產品照（今天用筆記本生成的白底產品照代替）</dd>
    <dt>限制與法規</dt><dd>Colab T4（512px、fp16）；著作權與風格模仿</dd>
    <dt>為何現有工具不夠</dt><dd>L13 只能用類別當條件，不能用一段文字</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：L07 時行銷科技組問過「一張 T4 跑得動 512px 嗎？」今天兌現。「可用率」：行銷部看過、願意拿去用的比例，要人工判斷。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明** CLIP 把文字和圖放進同一個空間，並用程式算餘弦相似度
2. **畫出** Stable Diffusion 的四個零件和每一段的 shape
3. **控制**步數、指導強度、seed、負面提示詞，並說出負面提示詞為什麼要 w ＞ 1
4. **使用** img2img 與 inpainting 換風格、換背景
5. **量測** CLIP 分數隨 w 的變化，並對有人物的提示詞做偏差稽核

<!--
★ 目標（1 分）。不教：cross-attention 的公式（L17 才教注意力）、排程器數學（附錄只認名字）、ControlNet 實作（講師示範）、SDXL。
-->

---

<div class="eyebrow">00 · Frame · 回到 L07</div>

# 512px 在 T4 上跑得動，是因為不在像素上去噪

<div class="grid grid-cols-3 gap-4 mt-4" style="font-size:18px">
<div class="node"><strong>像素</strong><small>512×512×3 ＝ 786,432</small></div>
<div class="node node--primary"><strong>SD 的潛在空間</strong><small>4×64×64 ＝ 16,384（小 48 倍，L07）</small></div>
<div class="node node--warm"><strong>條件</strong><small>L13 類別編號 → 今天一段文字</small></div>
</div>

<div style="font-size:19px" class="mt-4">

- L11、L13 的去噪 U-Net，搬到 4 × 64 × 64 的潛在空間裡做
- 最後才用 L07 的 VAE 解碼器還原成 512 × 512 的照片
- 唯一的新零件：把文字變成向量的**文字編碼器**（CLIP）

</div>

<div class="takeaway mt-3">Stable Diffusion ＝ 在小 48 倍的空間裡做 L13 的條件去噪，條件換成文字。</div>

<!--
★ Frame（4 分）：數字全部來自 L07 的投影片（786,432、16,384、48 倍），不重講 VAE。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 企劃文字 → 一張情境照

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-2">
<div>

<img class="photo" src="/lab14-run-brief.png" alt="SD1.5 生成的情境照：木頭桌面上有筆電、一杯咖啡和白色耳機充電盒（咖啡盤有明顯的變形）" style="width:100%;max-height:300px;object-fit:contain">
<div class="shot-cap">Colab T4 實跑：seed 0、25 步、w＝7.5，4.8 秒，VRAM 峰值 2.81 GB（咖啡盤形狀怪：要人工審）</div>

</div>
<div style="font-size:17px">

**企劃文字**：夏季新品：白色無線耳機，放在木頭書桌上，旁邊有咖啡和筆電，早晨窗光，溫暖、乾淨

**提示詞（英文）**：<code style="font-size:16px">product photo of white wireless earbuds with charging case on a wooden desk, coffee cup and laptop in background, soft morning window light, warm, clean, high detail</code>

</div>
</div>

<div class="takeaway mt-3">先猜：企劃文字直接用中文丟進去，會怎樣？第 2 部分會量給你看。</div>

<!--
★ 示範（4 分）：提示詞是講師從企劃文字改寫的英文；SD1.5 的文字編碼器只訓練過英文（下一頁）。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· CLIP 1</div>

# CLIP：一個空間裡，同時放文字和圖

<div class="grid grid-cols-[1.15fr_1fr] gap-5 mt-1 items-center">
<div>

<svg viewBox="0 0 470 330" style="width:100%;max-height:300px" role="img" aria-label="三維座標軸的示意圖。從原點射出三對同色箭頭：藍色一對指向右上，終點是耳機照片和 headphones 這個詞；橘色一對指向左上，終點是背包照片和 backpack；綠色一對指向右下，終點是馬克杯照片和 mug。同一對的兩支箭頭方向幾乎一樣，不同對的方向差很多。">
  <defs>
    <marker id="c3-b" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--primary)"/></marker>
    <marker id="c3-o" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--warm-accent)"/></marker>
    <marker id="c3-g" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--secondary)"/></marker>
    <marker id="c3-ax" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#9aa5b4"/></marker>
  </defs>
  <!-- 座標軸 -->
  <line x1="200" y1="200" x2="455" y2="200" stroke="#9aa5b4" stroke-width="1.5" marker-end="url(#c3-ax)"/>
  <line x1="200" y1="200" x2="200" y2="14" stroke="#9aa5b4" stroke-width="1.5" marker-end="url(#c3-ax)"/>
  <line x1="200" y1="200" x2="90" y2="300" stroke="#9aa5b4" stroke-width="1.5" marker-end="url(#c3-ax)"/>
  <text x="418" y="220" style="font-size:14px;font-family:'Noto Sans TC'" fill="var(--muted-text)">維度 1</text>
  <text x="208" y="24" style="font-size:14px;font-family:'Noto Sans TC'" fill="var(--muted-text)">維度 2</text>
  <text x="40" y="318" style="font-size:14px;font-family:'Noto Sans TC'" fill="var(--muted-text)">維度 3</text>
  <!-- 耳機：右上 -->
  <line x1="200" y1="200" x2="345" y2="78" stroke="var(--primary)" stroke-width="2.5" marker-end="url(#c3-b)"/>
  <line x1="200" y1="200" x2="368" y2="108" stroke="var(--primary)" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#c3-b)"/>
  <image href="/clip-headphones.jpg" x="320" y="10" width="62" height="62"/>
  <rect x="320" y="10" width="62" height="62" fill="none" stroke="var(--primary)" stroke-width="2"/>
  <text x="374" y="122" style="font-size:16px;font-family:monospace" fill="var(--primary)">"headphones"</text>
  <!-- 背包：左上 -->
  <line x1="200" y1="200" x2="92" y2="84" stroke="var(--warm-accent)" stroke-width="2.5" marker-end="url(#c3-o)"/>
  <line x1="200" y1="200" x2="128" y2="70" stroke="var(--warm-accent)" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#c3-o)"/>
  <image href="/clip-backpack.jpg" x="30" y="30" width="62" height="62"/>
  <rect x="30" y="30" width="62" height="62" fill="none" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="96" y="58" style="font-size:16px;font-family:monospace" fill="var(--warm-accent)">"backpack"</text>
  <!-- 馬克杯：右下 -->
  <line x1="200" y1="200" x2="322" y2="268" stroke="var(--secondary)" stroke-width="2.5" marker-end="url(#c3-g)"/>
  <line x1="200" y1="200" x2="286" y2="290" stroke="var(--secondary)" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#c3-g)"/>
  <image href="/clip-mug.jpg" x="326" y="240" width="62" height="62"/>
  <rect x="326" y="240" width="62" height="62" fill="none" stroke="var(--secondary)" stroke-width="2"/>
  <text x="218" y="318" style="font-size:16px;font-family:monospace" fill="var(--secondary)">"mug"</text>
  <circle cx="200" cy="200" r="4" fill="var(--text)"/>
</svg>

</div>
<div style="font-size:18px">

- 兩個編碼器：圖 → 512 個數字、文字 → 512 個數字，放進**同一個空間**
- 實線箭頭＝圖，虛線箭頭＝文字；**同色＝同一對**
- 訓練：網路上的「圖＋說明文字」配對，同一對拉到同一個方向，不同對推開
- 這叫**對比式學習**（contrastive learning）

</div>
</div>

<div class="takeaway mt-2">訓練完，「耳機的照片」和 "headphones" 這個詞，會指向差不多的方向。</div>

<div class="src">示意：真正是 512 維，這裡只畫 3 維，位置不是實測。照片：L22 用 SD1.5 生成的虛構商品照。Radford et al., CLIP, 2021（S2，待確認）；SD1.5 用的是 CLIP 的文字編碼器</div>

<!--
★ CLIP 1（5 分）：先指同一個顏色：藍色的照片和藍色的 "headphones" 幾乎同方向；再指不同顏色：耳機和馬克杯差很遠。訓練時，一批 N 對圖文做成 N × N 的表，對角線（同一對）拉近、其他格推遠；圖上每一種顏色就是對角線上的一格。文字用英文，是因為 CLIP 用英文網路資料訓練。
contrastive（對比式）。CLIP 不會生成圖，它只會「比對」。SD 借用它的文字編碼器，把提示詞變成向量。CLIP 用英文網路資料訓練：中文提示詞的向量不可靠（「練習：同一張耳機圖，哪一句最配？」會量）。
-->

---

<div class="eyebrow">02 · Open · CLIP 2</div>

# 餘弦相似度（cosine similarity）：先變單位向量，再內積

<div class="grid grid-cols-2 gap-6 mt-1">
<div>

<svg viewBox="0 0 330 215" style="width:100%;max-height:205px" role="img" aria-label="二維座標上的單位圓。圖的向量 (3, 4) 除以長度 5 變成 (0.6, 0.8)，文字的向量 (4, 3) 變成 (0.8, 0.6)，兩支箭頭都落在半徑 1 的圓上，中間夾角 θ 很小，cos θ 等於 0.96。">
  <defs>
    <marker id="cs-b" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--primary)"/></marker>
    <marker id="cs-ax" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#9aa5b4"/></marker>
  </defs>
  <line x1="30" y1="195" x2="215" y2="195" stroke="#9aa5b4" stroke-width="1.5" marker-end="url(#cs-ax)"/>
  <line x1="30" y1="195" x2="30" y2="12" stroke="#9aa5b4" stroke-width="1.5" marker-end="url(#cs-ax)"/>
  <path d="M30,45 A150,150 0 0 1 180,195" fill="none" stroke="#9aa5b4" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="150" y="58" style="font-size:13px;font-family:'Noto Sans TC'" fill="var(--muted-text)">長度＝1 的圓</text>
  <line x1="30" y1="195" x2="120" y2="75" stroke="var(--primary)" stroke-width="2.5" marker-end="url(#cs-b)"/>
  <line x1="30" y1="195" x2="150" y2="105" stroke="var(--primary)" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#cs-b)"/>
  <path d="M62,153 A52,52 0 0 1 72,164" fill="none" stroke="var(--text)" stroke-width="1.5"/>
  <text x="74" y="152" style="font-size:15px" fill="var(--text)">θ</text>
  <text x="40" y="28" style="font-size:14px;font-family:'Noto Sans TC'" fill="var(--primary)">圖 (3,4)÷5＝(0.6, 0.8)</text>
  <text x="166" y="108" style="font-size:14px;font-family:'Noto Sans TC'" fill="var(--primary)">文字 (4,3)÷5</text>
  <text x="166" y="126" style="font-size:14px;font-family:'Noto Sans TC'" fill="var(--primary)">＝(0.8, 0.6)</text>
  <text x="186" y="170" style="font-size:15px;font-family:'Noto Sans TC'" fill="var(--text)">cos θ ＝ 0.6×0.8</text>
  <text x="192" y="190" style="font-size:15px;font-family:'Noto Sans TC'" fill="var(--text)">＋0.8×0.6 ＝ <tspan font-weight="bold">0.96</tspan></text>
</svg>
<div class="shot-cap" style="margin-top:0">① 照著算：先除以長度（變成長度 1），再內積</div>

</div>
<div>

<svg viewBox="0 0 330 215" style="width:100%;max-height:205px" role="img" aria-label="二維空間示意。耳機照片的向量從原點指向右上方；headphones 這個詞的向量方向幾乎一樣，夾角小，cos 大；mug 這個詞的向量指向右下方，夾角大，cos 小。">
  <defs>
    <marker id="cs-b2" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--primary)"/></marker>
    <marker id="cs-g2" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--secondary)"/></marker>
  </defs>
  <circle cx="60" cy="120" r="4" fill="var(--text)"/>
  <line x1="60" y1="120" x2="190" y2="50" stroke="var(--primary)" stroke-width="2.5" marker-end="url(#cs-b2)"/>
  <image href="/clip-headphones.jpg" x="194" y="10" width="54" height="54"/>
  <rect x="194" y="10" width="54" height="54" fill="none" stroke="var(--primary)" stroke-width="2"/>
  <line x1="60" y1="120" x2="200" y2="80" stroke="var(--primary)" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#cs-b2)"/>
  <text x="206" y="88" style="font-size:15px;font-family:monospace" fill="var(--primary)">"headphones"</text>
  <line x1="60" y1="120" x2="185" y2="190" stroke="var(--secondary)" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#cs-g2)"/>
  <text x="192" y="200" style="font-size:15px;font-family:monospace" fill="var(--secondary)">"mug"</text>
  <path d="M110,93 A57,57 0 0 1 114,105" fill="none" stroke="var(--primary)" stroke-width="2"/>
  <text x="210" y="116" style="font-size:14px;font-family:'Noto Sans TC'" fill="var(--primary)">夾角小 → cos 大</text>
  <path d="M110,93 A57,57 0 0 1 110,148" fill="none" stroke="var(--secondary)" stroke-width="2"/>
  <text x="210" y="160" style="font-size:14px;font-family:'Noto Sans TC'" fill="var(--secondary)">夾角大 → cos 小</text>
</svg>
<div class="shot-cap" style="margin-top:0">② 同一張耳機照：方向一樣分數高，方向不同分數低（示意）</div>

</div>
</div>

<div class="mt-1">
<div>

```python
im = out.image_embeds / out.image_embeds.norm(dim=-1, keepdim=True)
tx = out.text_embeds / out.text_embeds.norm(dim=-1, keepdim=True)
S = im @ tx.T          # [圖數, 文字數]
```

</div>
</div>

<div class="takeaway mt-1">CLIP 的分數不是「好不好看」，而是「圖和這句話的方向有多接近」。</div>

<div class="src">圖 ② 是示意，不是實測分數；S3：<code>clip-vit-base-patch32</code> 的向量是 512 維（以筆記本輸出為準）</div>

<!--
★ CLIP 2（5 分）：先看圖 ①：(3, 4) 和 (4, 3) 長度都是 5，除以 5 之後落在長度＝1 的圓上，內積 0.96，就是夾角 θ 的 cos。方向一樣 → 1，垂直 → 0，相反 → −1。再看圖 ②：同一張耳機照，"headphones" 的箭頭幾乎同方向（分數高），"mug" 的箭頭方向差很多（分數低）。程式讀作：「每個向量除以自己的長度（變成長度 1），再兩兩做內積」。ML 課學過內積和距離；這裡只看方向、不看長度。實際的分數範圍看第 2 部分的輸出；比相對大小，不看絕對值。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：同一張耳機圖，哪一句最配？

<div class="muted" style="font-size:16px"><b>照著做</b>：在第 2 部分印出的 3 × 3 表找「圖2」那一列，最大的那一格就是它最配的句子。<br>現在換成同一張耳機圖配四句：先寫預測排名（1＝最高），再執行「tricky」那一格填實際分數。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:46%">文字</th><th style="width:16%">預測排名</th><th>實際分數</th></tr></thead>
<tbody>
<tr><td><code>white wireless earbuds on a desk</code></td><td class="blank"><FillIn id="clip.r1" /></td><td class="blank"><FillIn id="clip.s1" hint="例：0.＿＿＿……" /></td></tr>
<tr><td><code>black wireless earbuds on a desk</code></td><td class="blank"><FillIn id="clip.r2" /></td><td class="blank"><FillIn id="clip.s2" /></td></tr>
<tr><td><code>white wired headphones on a desk</code></td><td class="blank"><FillIn id="clip.r3" /></td><td class="blank"><FillIn id="clip.s3" /></td></tr>
<tr><td>白色無線耳機放在書桌上</td><td class="blank"><FillIn id="clip.r4" /></td><td class="blank"><FillIn id="clip.s4" /></td></tr>
</tbody>
</table>

<FillClear group="clip" />

<div class="muted mt-1" style="font-size:16px">想一想：差一個字（white／black）分數差多少？中文那一句排第幾？</div>

<!--
★ 練習（6 分）：個人作業、不收回。重點是發現：只差一個顏色詞，分數差多少；中文句子排第幾（預期偏低，因為 CLIP 用英文資料訓練；以實跑為準）。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：差一個字，分數差多少

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:52%">文字</th><th>T4 實跑分數（seed 0）</th></tr></thead>
<tbody>
<tr><td><code>white wireless earbuds on a desk</code></td><td>0.293（1）</td></tr>
<tr><td><code>black wireless earbuds on a desk</code></td><td>0.270（2）</td></tr>
<tr><td><code>white wired headphones on a desk</code></td><td>0.263（3）</td></tr>
<tr><td>白色無線耳機放在書桌上</td><td>0.170（4）</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：看排名，不看絕對值。只差一個字，分數只差約 0.02；中文句子排最後（0.170），就是提示詞要寫英文的證據。</div>

<!--
★ 解答（2 分）：數字來自講師 T4 實跑（lab-runs.md，seed 0）。同一次實跑的 3 × 3 表：對角線 0.293／0.299／0.344，每一列都是對角線最大。學員的 seed 不同，分數會略有差異。
-->

---

<div class="eyebrow">02 · Open · 今天的主角圖</div>

# Stable Diffusion 的四個零件

<div class="grid items-center mt-3" style="font-size:16px;grid-template-columns:19% 4% 23% 4% 23% 4% 19%;row-gap:6px">
  <div class="node">提示詞<small>一段英文</small></div><span class="arrow text-center">→</span>
  <div class="node node--warm"><strong>文字編碼器</strong><small>CLIP 的文字部分 → &#91;1, 77, 768&#93;</small></div>
  <div></div><div></div><div></div><div></div>
  <div></div><div></div>
  <div class="arrow text-center" style="font-size:15px">↓ 交叉注意力</div>
  <div></div><div></div><div></div><div></div>
  <div class="node">純雜訊<small>&#91;1, 4, 64, 64&#93;</small></div><span class="arrow text-center">→</span>
  <div class="node node--primary"><strong>U-Net × N 步</strong><small>L11 的去噪 ＋ L13 的 CFG</small></div><span class="arrow text-center">⇄</span>
  <div class="node node--secondary"><strong>排程器</strong><small>決定每步減多少雜訊、走幾步</small></div><span class="arrow text-center">→</span>
  <div class="node"><strong>VAE 解碼器</strong><small>L07 → &#91;1, 3, 512, 512&#93;</small></div>
</div>

<div class="muted mt-2" style="font-size:15px">77＝提示詞最多 77 個 token（太長會截斷）。SD 用每個 token 的向量（77 × 768）；第 2 部分量分數用的是小一號 CLIP 的整句向量（512）。shape 在 lab14 第 1 部分印出。</div>

<div class="takeaway mt-3">每一塊都學過：VAE（L07）、U-Net（L06、L11）、CFG（L13）；只有文字編碼器是新的。</div>

<div class="src">Rombach et al., Latent Diffusion, 2022（S4，待確認）；shape 與參數量以 lab14 第 1 部分的輸出為準</div>

<!--
★ 主角圖（6 分）：請學員對每一個方塊說出「哪一天學過」。77 是 CLIP 文字編碼器的最大 token 數（太長的提示詞會被截斷）；768 是 SD1.5 文字編碼器的寬度（待 T4 輸出確認）。
常見誤解：SD 在像素上去噪。U-Net 只看 4 × 64 × 64。
-->

---

<div class="eyebrow">02 · Open · 交叉注意力</div>

# 文字怎麼進 U-Net：圖的每一塊去「查」每一個字

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-3 items-center">
<div>

<svg viewBox="0 0 320 200" style="width:100%" aria-label="左邊一張 4 乘 4 的潛在小格子，其中一格標亮；右邊一排詞：white、wireless、earbuds、desk；亮的那一格連到 earbuds 的線最粗">
  <g stroke="var(--primary)" stroke-width="1" fill="var(--soft-blue)">
    <rect x="10" y="30" width="35" height="35"/><rect x="45" y="30" width="35" height="35"/><rect x="80" y="30" width="35" height="35"/><rect x="115" y="30" width="35" height="35"/>
    <rect x="10" y="65" width="35" height="35"/><rect x="45" y="65" width="35" height="35" fill="var(--warm-accent)"/><rect x="80" y="65" width="35" height="35"/><rect x="115" y="65" width="35" height="35"/>
    <rect x="10" y="100" width="35" height="35"/><rect x="45" y="100" width="35" height="35"/><rect x="80" y="100" width="35" height="35"/><rect x="115" y="100" width="35" height="35"/>
  </g>
  <text x="10" y="160" style="font-size:15px" fill="var(--muted-text)">潛在圖的一小塊（示意圖）</text>
  <g style="font-size:16px">
    <text x="230" y="40" fill="var(--muted-text)">white</text><text x="230" y="80" fill="var(--muted-text)">wireless</text><text x="230" y="120" fill="var(--warm-accent)" font-weight="bold">earbuds</text><text x="230" y="160" fill="var(--muted-text)">desk</text>
  </g>
  <line x1="80" y1="82" x2="225" y2="36" stroke="#b8b8b8" stroke-width="1"/>
  <line x1="80" y1="82" x2="225" y2="76" stroke="#b8b8b8" stroke-width="2"/>
  <line x1="80" y1="82" x2="225" y2="116" stroke="var(--warm-accent)" stroke-width="5"/>
  <line x1="80" y1="82" x2="225" y2="156" stroke="#b8b8b8" stroke-width="1"/>
</svg>

</div>
<div style="font-size:18px">

- U-Net 裡每一塊潛在像素，對 77 個文字向量各打一個「相關分數」
- 依分數把文字向量加權平均，加回這一塊
- 線越粗＝這一塊越「聽」那個字

</div>
</div>

<div class="takeaway mt-3">文字不是只在開頭加一次：U-Net 的很多層、每一步，都讓每一塊圖去查一次文字。</div>

<div class="src">注意力（attention）的計算方式在 L17 教；今天只要這張圖</div>

<!--
★ 交叉注意力（4 分）：cross-attention（交叉注意力）。這張圖是示意，線的粗細不是實際數值。和 L13 對照：類別向量是「整張圖加同一個向量」；文字是「每一塊各自決定要聽哪個字」。
-->

---

<div class="eyebrow">03 · Adapt（調整）· 參數</div>

# 參數：步數、指導強度 w、seed、負面提示詞

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<img class="photo" src="/lab14-run-param-grid.png" alt="三列四行的網格：列是 10、25、50 步，行是 w 等於 1、4、7.5、12；w 等於 1 的那一行畫面糊成一團，w 越大產品越清楚" style="width:100%;max-height:290px;object-fit:contain">
<div class="shot-cap">Colab T4 實跑，seed 0：列＝10／25／50 步，行＝w 1／4／7.5／12；每格標秒數</div>

</div>
<div style="font-size:17px">

- **步數**：25 步約 4 秒、50 步約 7.6 秒（實跑）；畫面在 25 步後變化不大
- **w**（<code>guidance_scale</code>）：L13 的那一行；w＝1 一整行都糊（沒有 CFG），也最快（不用算兩次）
- **seed**：同 seed ＋ 同設定 → 同一張圖（L02）
- **負面提示詞**：下一頁

</div>
</div>

<div class="takeaway mt-3">一次只改一個參數，才知道是哪個參數造成的改變。</div>

<div class="src">lab14 第 3 部分</div>

<!--
★ 參數（3 分）：一次只改一個參數。網格以 T4 輸出為準。
-->

---

<div class="eyebrow">03 · Adapt · 負面提示詞</div>

# 負面提示詞：換掉 CFG 那一行的 ε_uncond

<div class="node node--primary" style="font-size:21px;padding:10px;text-align:center">ε ＝ <s style="color:var(--muted-text)">ε_uncond</s> <b style="color:var(--warm-accent)">ε_neg</b> ＋ w ·（ε_cond − <b style="color:var(--warm-accent)">ε_neg</b>）</div>

<div class="grid grid-cols-[1fr_1.1fr] gap-6 mt-3">
<div><img class="photo" src="/lab14-run-negative.png" alt="兩張圖：左邊沒有負面提示，水瓶上有文字；右邊加了負面提示，文字不見了，畫面也比較清楚" style="width:100%"><div class="shot-cap">Colab T4 實跑，seed 1、w＝7.5：左邊瓶身有字，右邊沒有</div></div>
<div style="font-size:18px">

- ε_neg：給「負面提示詞」時模型預測的雜訊
- 讀作：「從負面提示詞出發，朝正面提示走 w 倍」＝ 離開不要的東西
- w＝1：ε＝ε_cond，ε_neg 完全不參與 → 沒有作用（L02 的觀察）

</div>
</div>

<div class="takeaway mt-3">負面提示詞不是「禁止清單」，而是 CFG 的起點；所以只有 w ＞ 1 才有用。</div>

<div class="src">S6：diffusers 在 w ≤ 1 時不做 CFG（待確認）</div>

<!--
★ 負面提示詞（3 分）：L02 留下的問題在這裡解答。把 L13 的 CFG 那一行寫在白板上，劃掉 ε_uncond、換成 ε_neg。
-->

---

<div class="eyebrow">03 · Adapt · img2img</div>

# img2img（以圖生圖）：strength＝要加多少雜訊

<img class="photo" src="/lab14-run-img2img.png" alt="五張圖：原圖、strength 0.3、0.5 幾乎一樣，0.7 出現閃亮的光點，0.9 變成另一張構圖" style="width:100%">
<div class="shot-cap">Colab T4 實跑，seed 0、25 步（實際跑 7／12／17／22 步）。提示詞要「冬天」，但 0.3–0.5 幾乎沒變、0.7 只多了光點、0.9 整張換掉</div>

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:17px">
<div class="node"><strong>strength 小（0.3、0.5）</strong><small>雜訊太少：幾乎改不動</small></div>
<div class="node node--primary"><strong>0.7</strong><small>開始改，但這次只多了光點，沒有雪</small></div>
<div class="node node--warm"><strong>strength 大（0.9）</strong><small>幾乎變回純雜訊：構圖也換了</small></div>
</div>

<div class="takeaway mt-3">和 L12 一樣：部分加噪再去噪。實際走的步數 ≈ strength × 步數；「改夠多」和「保留原圖」之間沒有免費的設定。</div>

<!--
★ img2img（4 分）：常見誤解：strength 是「風格強度」。它是「從第幾步開始去噪」：strength 0.3、25 步 → 只走最後約 7 步。L12 用同樣的想法把瑕疵「修掉」，今天用來換風格。
-->

---

<div class="eyebrow">03 · Adapt · inpainting</div>

# inpainting（局部重繪）：遮罩當條件，接在輸入通道上

<div class="grid items-center mt-3" style="font-size:16px;grid-template-columns:22% 4% 22% 4% 22% 4% 22%">
  <div class="node node--primary"><strong>4</strong><small>加了雜訊的潛在 x_t</small></div><span class="arrow text-center">＋</span>
  <div class="node node--warm"><strong>1</strong><small>遮罩（縮成 64 × 64）白＝重畫</small></div><span class="arrow text-center">＋</span>
  <div class="node"><strong>4</strong><small>挖掉遮罩區的原圖，經 VAE 編碼</small></div><span class="arrow text-center">→</span>
  <div class="node node--secondary"><strong>9 通道</strong><small>inpainting 專用 U-Net 的輸入</small></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div>

- 「接起來」（concatenate）：L06 的 U-Net 跳接學過
- U-Net 隨時看得到：哪裡要畫、旁邊原本長什麼樣
- 所以畫出來的背景會和產品的邊緣接得上

</div>
<div class="node node--warm"><strong>今天的用法：換背景</strong><small>白底產品照 → 背景（接近白色的像素）當遮罩 → 只重畫背景，產品保留</small></div>
</div>

<div class="takeaway mt-3">條件不一定要走嵌入那條路：直接接成輸入通道，也是一種條件。</div>

<div class="src">S5：<code>stable-diffusion-inpainting</code> 的 U-Net <code>in_channels</code> ＝ 9（lab14 第 5 部分會印出）</div>

<!--
★ inpainting（5 分）：inpainting（局部重繪）。三種條件方式對照：L13 類別 → 加到嵌入；文字 → 交叉注意力；遮罩與原圖 → 接在輸入通道。
-->

---

<div class="eyebrow">04 · Measure（量測驗收）· CLIP 分數</div>

# CLIP 分數：w 越大，越貼題嗎？

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2">
<div>

<table class="vlines" style="font-size:17px;text-align:center">
<thead><tr><th>w</th><th>1</th><th>3</th><th>5</th><th>7.5</th><th>10</th><th>14</th></tr></thead>
<tbody><tr><td>CLIP 分數</td><td>29.0</td><td>30.1</td><td>30.8</td><td><b>32.3</b></td><td>30.6</td><td>31.0</td></tr>
<tr><td>± 標準差</td><td>2.2</td><td>0.9</td><td>1.0</td><td>1.2</td><td>1.0</td><td>2.1</td></tr></tbody>
</table>
<div class="shot-cap">Colab T4 實跑：每個 w 4 個 seed（0–3）、25 步，共 81 秒</div>

</div>
<div style="font-size:18px">

- CLIP 分數 ＝ 100 × 餘弦相似度（圖，提示詞）
- 實跑：w 從 1 升到 7.5 最高（32.3），之後下降、而且變得不穩（標準差變大）
- 只有 4 個 seed：看趨勢，不看小數點

</div>
</div>

<div class="takeaway mt-3">CLIP 分數量的是「貼不貼題」，不是「好不好看」：最後仍要行銷部人工看。</div>

<div class="src">S7：CLIPScore（Hessel et al., 2021，待確認）；本 lab 用 100 × cos</div>

<!--
★ CLIP 分數（3 分）：和 L13 的忠實度是同一件事：「有沒有聽話」。差距只有 1–3 分、seed 只有 4 個：只說趨勢。
-->

---

<div class="eyebrow">04 · Measure · 偏差稽核</div>

# 偏差稽核：提示詞沒說的，模型會自己補

<div style="font-size:17px">提示詞：<code>photo of a customer service representative at an electronics store, smiling, store background</code>（沒有指定性別、年齡）。看 lab 第 6b 部分的 12 張，自己數。</div>

<table class="fill tight vlines mt-2">
<thead><tr><th style="width:34%">看起來像（粗略判斷）</th><th>張數（共 12）</th><th style="width:40%">你覺得行銷部該怎麼改提示詞？</th></tr></thead>
<tbody>
<tr><td>女性／男性／看不出來</td><td class="blank"><FillIn id="bias.gender" hint="例：5／6／1……" /></td><td class="blank" rowspan="3"><FillIn id="bias.fix" /></td></tr>
<tr><td>年輕（約 20–35）／其他</td><td class="blank"><FillIn id="bias.age" /></td></tr>
<tr><td>穿制服／穿便服</td><td class="blank"><FillIn id="bias.cloth" /></td></tr>
</tbody>
</table>

<FillClear group="bias" />

<div class="takeaway mt-2">12 張全是同一種樣子，就是模型的預設；上線前，用多個 seed 數一數。</div>

<div class="src">文字生成圖的職業偏差：Luccioni et al., Stable Bias, 2023（S10，待確認）</div>

<!--
★ 偏差稽核（6 分）：個人作業。強調「看起來像」只是粗略判斷，用來發現模型的預設傾向，不是判斷任何真人的身分；有爭議的就填「看不出來」。12 張是很小的樣本，只能發現明顯的傾向。改法：在提示詞明確寫出多樣的人物，或刻意輪流。
-->

---

<div class="eyebrow">05 · 延伸 · 講師示範</div>

# ControlNet：用線稿、姿勢控制構圖（只示範）

<img class="photo mt-2" src="/lab14-controlnet-demo.png" alt="左：第 5 部分的產品照（手機與無線耳機）；中：Canny 邊緣線稿；右：依線稿生成的圖，耳機和手機的位置、角度不變，背景換成木紋桌面" style="height:230px;margin:0 auto;object-fit:contain">
<div class="shot-cap" style="text-align:center">產品照 → Canny 線稿（控制條件）→ 依線稿生成（seed 0、25 步；6.6 秒，VRAM 峰值 4.18 GB；講師 T4 實跑）</div>

<div class="grid grid-cols-3 gap-3 mt-2" style="font-size:17px">
<div class="node"><strong>多一個條件</strong><small>邊緣圖、人體姿勢、深度圖</small></div>
<div class="node"><strong>SD 本身不動</strong><small>旁邊加一個「控制」網路</small></div>
<div class="node"><strong>適合</strong><small>產品位置、角度要固定的版面</small></div>
</div>

<div class="takeaway mt-3">提示詞管「畫什麼」，ControlNet 管「畫在哪裡、什麼角度」。</div>

<div class="src">Zhang et al., ControlNet, 2023（S9，待確認）；權重 <code>lllyasviel/sd-controlnet-canny</code></div>

<!--
○ 示範（2 分）：時間不夠就跳過。示範用的是解答筆記本最後的附錄格，不發給學員。T4 實跑：6.6 秒、VRAM 峰值 4.18 GB。請學員看：耳機和手機的位置、角度和原圖一樣，只有材質和背景（木紋桌）是新生成的；這就是「提示詞管畫什麼、ControlNet 管畫在哪裡」。
-->

---

<div class="eyebrow">05 · 延伸 · 回到工廠</div>

# 用 inpainting 合成瑕疵，補 YOLOv8 的訓練資料

<div style="font-size:19px" class="mt-4">

- 用 DL 課的 YOLOv8（物件偵測）做瑕疵偵測時，最缺的是「不良品照片」
- 在良品照上畫一個遮罩、提示詞寫「scratch」→ 合成一張帶刮痕的板子
- 遮罩是標註框的上限：仍要人工確認瑕疵真的畫出來、畫在哪裡

</div>

<div class="takeaway mt-4">和 L13 的風險一樣：合成瑕疵只進訓練集，驗收一定用真實不良品。</div>

<div class="src">YOLOv8：DL 課 pp.56–62；L06 也用過程式合成的瑕疵</div>

<!--
○ 選修（2 分）：SD1.5 沒看過 PCB 瑕疵，生成的刮痕可能不像真的；要先讓品保看過。和 L06 程式合成瑕疵的做法比較。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 排程器：同一個 U-Net，不同的「下山路線」（只認名字）

<div style="font-size:19px" class="mt-4">

- DDPM：L11 的做法，每步加一點新雜訊，要很多步
- DDIM：L12 用過，不加新雜訊，可以跳步
- DPM-Solver（今天的 lab）：把去噪看成解微分方程，25 步就夠清楚

</div>

<div class="takeaway mt-4">換排程器不用重新訓練：U-Net 一樣，只換「每一步怎麼走」。</div>

<!--
△ 備用（1 分）：學員問「為什麼 L11 要 1000 步、今天 25 步就好」時再講。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab14-sd-studio.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**（SD1.5 與 inpainting 兩個模型，各約 3.9 GB）

1. 企劃文字能變成可用的情境照嗎？
2. 產品照能只換背景、不改產品嗎？
3. 哪一個 w 最貼題？有人物時有沒有偏差？

</div>
<div>

<img class="photo" src="/lab14-lab-target.png" alt="目標：左上依企劃文字生成的情境照（seed 0、25 步、w 7.5）；右上 CLIP 分數對指導強度的曲線，w 7.5 最高；下排產品照、遮罩、換背景後" style="height:270px;width:100%;object-fit:contain"><div class="shot-cap">目標：情境照、CLIP 分數 vs w、換背景前後（lab14 T4 實跑）。Gradio 工作室見 Ship 頁</div>

</div>
</div>

<div class="takeaway mt-3">交付給行銷部：一個可以自己點的工作室，加上「w 用多少、什麼要人工審」的說明。</div>

<!--
★ Lab 開始（2 分）：所有圖都在筆記本裡生成（包括「現有產品照」），不需要上傳檔案。學員有自己的白底產品照，可以在第 5 部分換掉 product。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span><strong>文字生成</strong>：<code>StableDiffusionPipeline</code>，排程器換成 DPM-Solver；印出四個零件</div>
  <div><span class="num">2</span><strong>CLIP</strong>：<code>clip_sim(images, texts)</code> → &#91;圖數, 文字數&#93;</div>
  <div><span class="num">3</span><strong>參數</strong>：步數 × w 網格；負面提示詞對照</div>
  <div><span class="num">4</span><strong>img2img</strong>：<code>StableDiffusionImg2ImgPipeline(**pipe.components)</code>，共用權重</div>
  <div><span class="num">5</span><strong>inpainting</strong>：做背景遮罩（TODO）→ inpainting 模型換背景 → 量產品區改變多少</div>
  <div><span class="num">6</span><strong>量測</strong>：CLIP 分數 vs w、偏差稽核 12 張</div>
  <div><span class="num">7</span><strong>Ship</strong>：Gradio 兩個分頁</div>
</div>

<div class="takeaway mt-3">一個 TODO：背景遮罩（第 5 部分）。其他格是「改參數、看結果」。</div>

<!--
★ 拆塊（2 分）：第 5 部分會先刪掉第一個 pipeline 再載 inpainting 模型，避免兩份權重同時佔 VRAM。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>依企劃文字生成情境照；替白底產品照換背景且產品不變；找出貼題的 w<br>
<strong>【輸入與輸出】</strong>提示詞（英文）→ 圖 512 × 512；產品照 ＋ 遮罩（白＝背景）→ 換背景的圖；CLIP：&#91;圖數, 文字數&#93; 的相似度<br>
<strong>【限制】</strong>SD1.5 fp16、512px、25 步；一次只載一個 pipeline；Colab T4<br>
<span class="muted" style="font-size:16px">為什麼：兩個 SD 模型同時在 GPU 上，VRAM 會吃緊；fp16 省一半 VRAM（速度待 T4 實測）</span><br>
<strong>【驗收】</strong>① 背景遮罩佔 40%～90% 的像素　② 產品區（遮罩外）平均改變 &lt; 背景區的 1／3　③ w＝7.5 的 CLIP 分數高於 w＝1　④ 偏差表 12 張都填了

</div>

<!--
★ Specify（2 分）：驗收門檻是課前定的，T4 實跑後若明顯不合理再調。第 ② 點用數字取代「看起來沒變」。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 diffusers 的筆記本，請只填第 5 部分的 # TODO：<br>
product 是白底產品照；arr 是它的 numpy 陣列（512, 512, 3）；bg_color 是邊框像素的中位數（背景色）。<br>
做一張遮罩 mask（PIL 灰階圖）：三個通道都和 bg_color 相差小於 30 的像素＝255（背景，要重畫），其餘＝0（產品，保留）。<br>
只用 numpy 和 PIL，不要改其他格。說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>T4 實測：SD1.5、inpainting 各下載約 3.9 GB；一張 512px、25 步約 4–5 秒；下載時先看第 2 部分</div>
  <div><span class="num">2</span>沒有 Agent 額度：遮罩只要兩行（<code>(np.abs(arr - bg_color) &lt; 30).all(axis=-1)</code>，再轉成 0／255 的圖）；卡住開 <code>-solution.ipynb</code></div>
  <div><span class="num">3</span>預期輸出：「背景佔 ＿＿% 的像素」、<code>inpainting U-Net 輸入通道： 9</code></div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>遮罩黑白顛倒：白色是產品 → inpainting 會把產品重畫掉、背景留著。先看遮罩圖再跑</small></div>

<!--
★ 執行（約 17 分）：常見錯誤是遮罩顛倒。講師第一次實跑用「很白＝背景」（> 235）：生成的「白底」其實是淺灰，只有耳機的亮面最白，背景只佔 5%、遮罩選到的是產品（下一頁的圖）——所以改用邊框顏色。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 5／7：看結果、對照預測

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

1. 參數網格：從幾步開始，圖就「夠用」了？
2. 負面提示詞：寫了 <code>people, hands, text</code> 之後，圖裡還有嗎？
3. img2img：哪一個 strength 最像「同一張照片的冬天版」？
4. 換背景：放大看耳機的形狀、白色外殼的邊緣

</div>
<div>

<div><img class="photo" src="/lab14-run-mask-fail.png" alt="講師第一次實跑的失敗：白底產品照、遮罩只選到耳機的亮面、換背景後幾乎沒變" style="width:100%"><div class="shot-cap">講師第一次 T4 實跑的失敗：「很白＝背景」只選到耳機亮面（背景佔 5%）</div></div>

</div>
</div>

<div class="takeaway mt-4">生成圖要「先看再用」：每一個參數的改變，都要用同一個 seed 對照。</div>

<!--
★ 對照（5 分）：第 4 題是伏筆：下一頁用數字量產品區改變多少。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:34%">應該是</th></tr></thead>
<tbody>
<tr><td>Agent 做的遮罩方向對嗎？</td><td>看遮罩圖</td><td>背景白、產品黑</td></tr>
<tr><td>產品有沒有被改？</td><td>看「產品區平均改變」</td><td>遠小於背景區（驗收 ②）</td></tr>
<tr><td>U-Net 真的是 9 通道？</td><td>看印出的 <code>in_channels</code></td><td>inpainting 9、一般 SD 4</td></tr>
<tr><td>偏差表的判斷可靠嗎？</td><td>「看不出來」有幾張</td><td>不確定就填看不出來</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：遮罩那一格可以單獨重跑，例如門檻 30 → 20，看背景比例怎麼變。</div>

<!--
★ 稽核（5 分）：數字以 T4 輸出為準（lab-runs.md）。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 7／7：換背景前後

<img class="photo" src="/lab14-inpaint-swap.png" alt="左：現有產品照；中：遮罩，白色是要重畫的區域；右：換背景後，右上角多了一塊木桌" style="height:260px;margin:0 auto;object-fit:contain"><div class="shot-cap" style="text-align:center">現有產品照 → 遮罩（白＝重畫）→ 換背景後（inpainting 5.0 秒，VRAM 峰值 3.41 GB；lab14，T4 實跑）</div>

<div class="node mt-3" style="font-size:17px"><strong>延伸（選做）</strong><small>把遮罩反過來（產品白、背景黑），提示詞寫「black wireless earbuds」：變成「換產品顏色、背景不動」。先預測：產品的形狀會保留嗎？</small></div>

<div class="takeaway mt-2">遮罩決定「改哪裡」，提示詞決定「改成什麼」。</div>

<!--
★ 結果（3 分）：延伸題的預期（未實跑）：形狀大致保留（背景會「框住」它），細節可能會變；所以不能拿來做真的商品圖。講師可在課前實跑確認。
-->

---

<div class="eyebrow">07 · Ship（交付）· Day 4 交付物</div>

# Ship：行銷部可以自己點的工作室

<div class="mt-4" style="font-size:20px">

- 兩個分頁：「文字生成」、「換風格（img2img）」（lab14 第 7 部分）
- <code>gr.Blocks</code> ＋ <code>gr.Tab</code>：一個網頁、兩個工具（L04 是單一的 <code>Interface</code>）
- 兩個分頁共用同一組權重：<code>StableDiffusionImg2ImgPipeline(**pipe.components)</code>
- 標題寫明「AI 生成，使用前請人工審核」
- <code>share=True</code>：暫時的公開網址（期限看執行時的輸出，L04）

</div>

<div class="takeaway mt-4">交付的不只是圖，而是「行銷部自己能用、而且知道要審核」的工具。</div>

<!--
★ Ship（4 分）：這是 Day 4 的交付物。share=True 的網址任何人都能用，課堂結束記得關掉 Colab。
-->

---

<div class="eyebrow">08 · 風險（Risk）</div>

# 風險：著作權、模仿風格、偏差、標示

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:24%">風險</th><th>例子</th><th style="width:36%">今天的做法</th></tr></thead>
<tbody>
<tr><td>著作權</td><td>提示詞寫「某品牌的廣告風格」、上傳別人的照片做 img2img</td><td>只用自有照片；提示詞不寫他人品牌</td></tr>
<tr><td>模仿風格</td><td>寫在世藝術家的名字</td><td>不寫人名；用描述詞（溫暖、乾淨）</td></tr>
<tr><td>偏差</td><td>人物都是同一種樣子</td><td>多個 seed 數一數；提示詞明確寫多樣性</td></tr>
<tr><td>標示</td><td>顧客以為是實拍</td><td>標示 AI 生成；可考慮 C2PA 內容憑證</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">商品圖不能誇大產品：換背景可以，改產品外觀不行（L09 的假細節是同一件事）。</div>

<div class="src">SD1.5 授權 CreativeML OpenRAIL-M（S1，模型卡另寫「僅供研究」）；C2PA（S8，待確認）。法律問題以公司法務意見為準</div>

<!--
★ 風險（3 分）：C2PA（內容憑證）：在檔案裡記錄「這張圖怎麼產生、被誰改過」的標準。OpenRAIL-M 授權列了不可用的用途；SD1.5 鏡像的模型卡寫「僅供研究」：商用前一定要法務確認。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">CLIP：文字和圖同一空間</span><span class="arrow">→</span>
  <span class="chip">文字編碼器 → 交叉注意力</span><span class="arrow">→</span>
  <span class="chip">潛在空間 4 × 64 × 64</span><span class="arrow">→</span>
  <span class="chip">CFG w、負面提示詞</span><span class="arrow">→</span>
  <span class="chip">img2img、inpainting</span><span class="arrow">→</span>
  <span class="chip">CLIP 分數、偏差稽核</span>
</div>

<div class="takeaway mt-6">SD 的每一塊都學過；今天學會的是「控制」：參數、起點（img2img）、範圍（遮罩），以及量測。</div>

<!--
★ 總整理（2 分）：請學員說出三種把條件交給 U-Net 的方式：嵌入相加（L13）、交叉注意力（文字）、接成輸入通道（inpainting）。和學習評量的關係：文字、遮罩都是「條件」；L16 的備忘錄會用到今天的 CLIP 分數。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 1／2（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['3 × 512 × 512 的像素', '4 × 64 × 64 的潛在', '77 × 768 的文字向量', '1 × 28 × 28']"
  :why="['SD 不在像素上去噪，運算量會大很多。', '', '77 × 768 是文字編碼器輸出的向量，是條件，不是被去噪的東西。', '1 × 28 × 28 是 Fashion-MNIST 灰階圖的大小，不是 SD。']"
  explain="VAE 先把 512 × 512 的圖壓成 4 × 64 × 64 的潛在，U-Net 在潛在上去噪，所以快（L07 的 VAE）。">
Stable Diffusion 1.5 的 U-Net 在什麼大小上去噪？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="2"
  :options="['負面提示詞只支援英文', '步數太少', '負面提示詞取代 ε_uncond，而 w＝1 時 ε＝ε_cond', 'seed 固定了']"
  :why="['和語言無關：負面提示詞和其他提示詞一樣被文字編碼器處理。', '步數不影響這個結果，問題出在公式。', '', 'seed 只決定起始雜訊，和 guidance 的公式無關。']"
  explain="負面提示詞被放在 ε_uncond 的位置；w＝1 時 ε＝ε_cond，ε_uncond 不出現，負面提示詞就沒有作用。">
為什麼 guidance_scale＝1 時負面提示詞沒有作用？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／2（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：1 B、2 C。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／2（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="1"
  :options="['圖更像原圖', '加更多雜訊，和原圖差更多', '生成更快', '解析度變高']"
  :why="['strength 低才更像原圖。', '', 'strength 大時實際走的步數也變多，反而更慢。', '輸出大小和 strength 無關。']"
  explain="strength 決定先加多少雜訊再去噪：越大雜訊越多，和原圖差越多、改動越大。">
img2img 的 strength 從 0.3 調到 0.9，最可能？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="0"
  :options="['圖和提示詞的方向接近', '圖很好看', '圖沒有偏差', '圖沒有侵權']"
  :why="['', '常見誤解：CLIP 分數衡量圖文對不對得上，不是美感。', '分數看不出偏差（例如刻板印象）。', '分數和著作權、侵權完全無關。']"
  explain="CLIP 分數是圖和提示詞在 CLIP 空間的相似度（方向接近），只回答「圖文對不對得上」。">
CLIP 分數高代表？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／2（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：3 B、4 A。
全部答案與理由：
1 B：VAE 先把 512 × 512 的圖壓成 4 × 64 × 64 的潛在，U-Net 在潛在上去噪，所以快（L07 的 VAE）。
2 C：負面提示詞被放在 ε_uncond 的位置；w＝1 時 ε＝ε_cond，ε_uncond 不出現，負面提示詞就沒有作用。
3 B：strength 決定先加多少雜訊再去噪：越大雜訊越多，和原圖差越多、改動越大。
4 A：CLIP 分數是圖和提示詞在 CLIP 空間的相似度（方向接近），只回答「圖文對不對得上」。
-->


---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 L15：生成的圖必須是「我們的」產品

<div style="font-size:19px" class="mt-4">

- 品牌部：提示詞描述不出我們產品的樣子，每次都不一樣
- 不訓練：IP-Adapter 給一張參考照
- 訓練一點點：DreamBooth ＋ LoRA，只學一對很細的矩陣

</div>

<!--
★ 下一步（1 分）：預告。請學員準備約 10 張自己拍的產品照（自有、同意使用）；沒有的話用講師提供的資料。
-->
