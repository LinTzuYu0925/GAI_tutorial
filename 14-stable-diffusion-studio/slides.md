---
theme: default
title: 產品情境照工作室
info: |
  生成式AI原理 · D4-2
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

<div class="eyebrow">生成式AI原理 · D4-2</div>

# 產品情境照工作室

<p class="subtitle">CLIP ＋ Stable Diffusion 1.5：企劃文字變照片，產品照換背景</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">文字當條件</span><span class="arrow">→</span>
  <span class="chip">CLIP</span><span class="arrow">→</span>
  <span class="chip">SD 四個零件</span><span class="arrow">→</span>
  <span class="chip">參數與負面提示</span><span class="arrow">→</span>
  <span class="chip">img2img、inpainting</span><span class="arrow">→</span>
  <span class="chip">CLIP 分數、偏差稽核</span>
</div>

<!--
★ 開場（2 分）：D4-1 的條件是一個類別編號；今天的條件是一段文字。D1-2 第一次用 SD1.5 時是黑盒子，今天每一個零件都是前幾天學過的東西。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 行銷部：依企劃文字生成情境照，還要換背景

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D4-2】部門：行銷部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>依企劃文字生成產品情境照，並替現有產品照換背景</dd>
    <dt>現況痛點</dt><dd>每次活動都要外拍：場地、模特兒、攝影師</dd>
    <dt>成功指標（KPI）</dt><dd>CLIP 分數（貼不貼題）；行銷部可用率；有人物的提示詞通過偏差檢查</dd>
    <dt>可用資料</dt><dd>企劃文字；自有產品照（今天用筆記本生成的白底產品照代替）</dd>
    <dt>限制與法規</dt><dd>Colab T4（512px、fp16）；著作權與風格模仿</dd>
    <dt>為何現有工具不夠</dt><dd>D4-1 只能用類別當條件，不能用一段文字</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：D2-3 時行銷科技組問過「一張 T4 跑得動 512px 嗎？」今天兌現。「可用率」：行銷部看過、願意拿去用的比例，要人工判斷。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明** CLIP 把文字和圖放進同一個空間，並用程式算餘弦相似度
2. **畫出** Stable Diffusion 的四個零件和每一段的 shape
3. **控制**步數、指導強度、seed、負面提示，並說出負面提示為什麼要 w ＞ 1
4. **使用** img2img 與 inpainting 換風格、換背景
5. **量測** CLIP 分數隨 w 的變化，並對有人物的提示詞做偏差稽核

<!--
★ 目標（1 分）。不教：cross-attention 的公式（D5-1 才教注意力）、排程器數學（附錄只認名字）、ControlNet 實作（講師示範）、SDXL。
-->

---

<div class="eyebrow">00 · Frame · 回到 D2-3</div>

# 512px 在 T4 上跑得動，是因為不在像素上去噪

<div class="grid grid-cols-3 gap-4 mt-4" style="font-size:18px">
<div class="node"><strong>像素</strong><small>512 × 512 × 3 ＝ 786,432 個數字</small></div>
<div class="node node--primary"><strong>SD 的潛在空間</strong><small>4 × 64 × 64 ＝ 16,384 個數字：小 48 倍（D2-3 量過）</small></div>
<div class="node node--warm"><strong>D4-1 的條件</strong><small>一個類別編號 → 今天換成一段文字</small></div>
</div>

<div style="font-size:19px" class="mt-4">

- D3-3、D4-1 的去噪 U-Net，搬到 4 × 64 × 64 的潛在空間裡做
- 最後才用 D2-3 的 VAE 解碼器還原成 512 × 512 的照片
- 唯一的新零件：把文字變成向量的**文字編碼器**（CLIP）

</div>

<div class="takeaway mt-3">Stable Diffusion ＝ 在小 48 倍的空間裡做 D4-1 的條件去噪，條件換成文字。</div>

<!--
★ Frame（4 分）：數字全部來自 D2-3 的投影片（786,432、16,384、48 倍），不重講 VAE。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 企劃文字 → 一張情境照

<div class="grid grid-cols-[1fr_1.2fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:300px;padding:16px 24px">SD1.5 生成的情境照（seed 0、25 步、w＝7.5）<small>講師 T4 實跑後替換（lab14 <code>brief_photo.png</code>，附時間與 VRAM）</small></div>

</div>
<div style="font-size:17px">

**企劃文字**：夏季新品：白色無線耳機，放在木頭書桌上，旁邊有咖啡和筆電，早晨窗光，溫暖、乾淨

**提示詞（英文）**：<code style="font-size:15px">product photo of white wireless earbuds with charging case on a wooden desk, coffee cup and laptop in background, soft morning window light, warm, clean, high detail</code>

</div>
</div>

<div class="takeaway mt-3">先猜：企劃文字直接用中文丟進去，會怎樣？第 2 部分會量給你看。</div>

<!--
★ 示範（4 分）：提示詞是講師從企劃文字改寫的英文；SD1.5 的文字編碼器只訓練過英文（下一頁）。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· CLIP 1</div>

# CLIP：一個空間裡，同時放文字和圖

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2 items-center">
<div>

<table class="vlines" style="font-size:16px;text-align:center">
<thead><tr><th></th><th>文字 1<br><small>耳機</small></th><th>文字 2<br><small>背包</small></th><th>文字 3<br><small>檯燈</small></th></tr></thead>
<tbody>
<tr><td><b>圖 1</b> 耳機</td><td style="background:var(--soft-blue)"><b>拉近</b></td><td>推遠</td><td>推遠</td></tr>
<tr><td><b>圖 2</b> 背包</td><td>推遠</td><td style="background:var(--soft-blue)"><b>拉近</b></td><td>推遠</td></tr>
<tr><td><b>圖 3</b> 檯燈</td><td>推遠</td><td>推遠</td><td style="background:var(--soft-blue)"><b>拉近</b></td></tr>
</tbody>
</table>

</div>
<div style="font-size:18px">

- 兩個編碼器：圖 → 512 個數字、文字 → 512 個數字
- 訓練：網路上的「圖＋說明文字」配對，配對的（對角線）拉近，其他推遠
- 這叫**對比式學習**（contrastive learning）

</div>
</div>

<div class="takeaway mt-3">訓練完，「耳機的照片」和「耳機」這個詞，會落在空間裡差不多的位置。</div>

<div class="src">Radford et al., CLIP, 2021（S2，待確認）；SD1.5 用的是 CLIP 的文字編碼器</div>

<!--
★ CLIP 1（5 分）：contrastive（對比式）。CLIP 不會生成圖，它只會「比對」。SD 借用它的文字編碼器，把提示詞變成向量。CLIP 用英文網路資料訓練：中文提示詞的向量不可靠（第 8 頁會量）。
-->

---

<div class="eyebrow">02 · Open · CLIP 2</div>

# 餘弦相似度（cosine similarity）：先變單位向量，再內積

<div class="grid grid-cols-[1fr_1.5fr] gap-6 mt-2 items-center">
<div class="node" style="font-size:17px"><strong>照著算（2 維）</strong><small>圖 ＝ (3, 4)，長度 5 → (0.6, 0.8)<br>文字 ＝ (4, 3)，長度 5 → (0.8, 0.6)<br>內積 ＝ 0.6×0.8 ＋ 0.8×0.6 ＝ <b>0.96</b>：方向很接近<br>方向一樣 → 1；垂直 → 0</small></div>
<div>

```python
im = out.image_embeds / out.image_embeds.norm(dim=-1, keepdim=True)
tx = out.text_embeds / out.text_embeds.norm(dim=-1, keepdim=True)
S = im @ tx.T          # [圖數, 文字數]
```

</div>
</div>

<div class="muted mt-2" style="font-size:16px">讀作：「每個向量除以自己的長度（變成長度 1），再兩兩做內積」。ML 課學過內積和距離；這裡只看方向、不看長度。</div>

<div class="takeaway mt-2">CLIP 的分數不是「好不好看」，而是「圖和這句話的方向有多接近」。</div>

<div class="src">S3：<code>clip-vit-base-patch32</code> 的向量是 512 維（以筆記本輸出為準）</div>

<!--
★ CLIP 2（5 分）：在白板上畫兩個箭頭。實際的 CLIP 分數通常只有 0.2～0.35 之間（不是 0～1 都會用到），所以要比相對大小，不看絕對值。這句話的數字範圍以第 2 部分的輸出為準。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：同一張耳機圖，哪一句最配？

<div class="muted" style="font-size:17px">先寫預測（1＝最高），再執行 lab 第 2 部分的「tricky」那一格，填實際分數。第一列已填好。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:46%">文字</th><th style="width:16%">預測排名</th><th>實際分數</th></tr></thead>
<tbody>
<tr><td><code>white wireless earbuds on a desk</code></td><td>1</td><td class="blank"><FillIn id="clip.s1" hint="例：0.2……" /></td></tr>
<tr><td><code>black wireless earbuds on a desk</code></td><td class="blank"><FillIn id="clip.r2" /></td><td class="blank"><FillIn id="clip.s2" /></td></tr>
<tr><td><code>white wired headphones on a desk</code></td><td class="blank"><FillIn id="clip.r3" /></td><td class="blank"><FillIn id="clip.s3" /></td></tr>
<tr><td>白色無線耳機放在書桌上</td><td class="blank"><FillIn id="clip.r4" /></td><td class="blank"><FillIn id="clip.s4" /></td></tr>
</tbody>
</table>

<FillClear group="clip" />

<div class="muted mt-1" style="font-size:16px">想一想：差一個字（white／black）分數差多少？中文那一句排第幾？</div>

<!--
★ 練習（6 分）：個人作業、不收回。重點是發現：只差一個顏色詞，分數差很小；中文句子的分數明顯偏低（CLIP 的英文訓練資料）。這解釋了為什麼提示詞要寫英文。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：差一個字，分數差多少

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:52%">文字</th><th>T4 實跑分數（seed 0）</th></tr></thead>
<tbody>
<tr><td><code>white wireless earbuds on a desk</code></td><td>實跑後填入</td></tr>
<tr><td><code>black wireless earbuds on a desk</code></td><td>實跑後填入</td></tr>
<tr><td><code>white wired headphones on a desk</code></td><td>實跑後填入</td></tr>
<tr><td>白色無線耳機放在書桌上</td><td>實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：看排名，不看絕對值；中文句子排最後，就是提示詞要寫英文的證據。</div>

<!--
★ 解答（2 分）：數字來自講師 T4 實跑（lab-runs.md）。學員的 seed 不同，分數會略有差異，排名應該相近。
-->

---

<div class="eyebrow">02 · Open · 今天的主角圖</div>

# Stable Diffusion 的四個零件

<div class="grid items-center mt-3" style="font-size:16px;grid-template-columns:19% 4% 23% 4% 23% 4% 19%;row-gap:8px">
  <div class="node">提示詞<small>一段英文</small></div><span class="arrow text-center">→</span>
  <div class="node node--warm"><strong>文字編碼器</strong><small>CLIP 的文字部分 → &#91;1, 77, 768&#93;</small></div><span class="arrow text-center">↓</span>
  <div></div><div></div><div></div>
  <div class="node">純雜訊<small>&#91;1, 4, 64, 64&#93;</small></div><span class="arrow text-center">→</span>
  <div class="node node--primary"><strong>U-Net × N 步</strong><small>D3-3 的去噪 ＋ D4-1 的 CFG</small></div><span class="arrow text-center">⇄</span>
  <div class="node node--secondary"><strong>排程器</strong><small>決定每步減多少雜訊、走幾步</small></div><span class="arrow text-center">→</span>
  <div class="node"><strong>VAE 解碼器</strong><small>D2-3 → &#91;1, 3, 512, 512&#93;</small></div>
</div>

<div class="muted mt-3" style="font-size:16px">77＝提示詞最多 77 個 token（太長會被截斷）；U-Net 參數量與 in_channels 在 lab14 第 1 部分印出。</div>

<div class="takeaway mt-3">每一塊都學過：VAE（D2-3）、U-Net（D2-2、D3-3）、CFG（D4-1）；只有文字編碼器是新的。</div>

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
  <text x="10" y="160" style="font-size:15px" fill="var(--muted-text)">潛在圖的一小塊</text>
  <g style="font-size:16px">
    <text x="230" y="40" fill="#444">white</text><text x="230" y="80" fill="#444">wireless</text><text x="230" y="120" fill="var(--warm-accent)" font-weight="bold">earbuds</text><text x="230" y="160" fill="#444">desk</text>
  </g>
  <line x1="80" y1="82" x2="225" y2="36" stroke="#999" stroke-width="1"/>
  <line x1="80" y1="82" x2="225" y2="76" stroke="#999" stroke-width="2"/>
  <line x1="80" y1="82" x2="225" y2="116" stroke="var(--warm-accent)" stroke-width="5"/>
  <line x1="80" y1="82" x2="225" y2="156" stroke="#999" stroke-width="1"/>
</svg>

</div>
<div style="font-size:18px">

- U-Net 裡每一塊潛在像素，對 77 個文字向量各打一個「相關分數」
- 依分數把文字向量加權平均，加回這一塊
- 線越粗＝這一塊越「聽」那個字

</div>
</div>

<div class="takeaway mt-3">文字不是只在開頭加一次：U-Net 的很多層、每一步，都讓每一塊圖去查一次文字。</div>

<div class="src">注意力（attention）的計算方式在 D5-1 教；今天只要這張圖</div>

<!--
★ 交叉注意力（4 分）：cross-attention（交叉注意力）。這張圖是示意，線的粗細不是實際數值。和 D4-1 對照：類別向量是「整張圖加同一個向量」；文字是「每一塊各自決定要聽哪個字」。
-->

---

<div class="eyebrow">03 · Adapt（調整）· 參數</div>

# 參數：步數、指導強度 w、seed、負面提示

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:270px;padding:16px 24px">3 × 4 網格：步數 10／25／50 × w＝1／4／7.5／12，seed 0，每格附秒數<small>講師 T4 實跑後替換（lab14 <code>param_grid.png</code>）</small></div>

</div>
<div style="font-size:17px">

- **步數**：太少會糊，25 步之後差異變小，時間大約跟步數成正比
- **w**（<code>guidance_scale</code>）：D4-1 的那一行；預設 7.5
- **seed**：同 seed ＋ 同設定 → 同一張圖（D1-2）
- **負面提示**：拿來**取代 ε_uncond**：「離開負面、走向正面」。所以 w＝1 時沒有作用（D1-2 的觀察）

</div>
</div>

<div class="takeaway mt-3">一次只改一個參數，才知道是哪個參數造成的改變。</div>

<div class="src">S6：diffusers 在 w ≤ 1 時不做 CFG（待確認）；負面提示對照圖見 lab14 第 3 部分（<code>negative_prompt.png</code>）</div>

<!--
★ 參數（5 分）：D1-2 留下的問題在這裡解答：負面提示是 CFG 那一行裡的 ε_uncond 換成「負面提示的預測」。w＝1 時 ε＝ε_cond，ε_uncond 完全不參與，所以負面提示沒有作用。
-->

---

<div class="eyebrow">03 · Adapt · img2img</div>

# img2img：strength＝要加多少雜訊

<div class="placeholder" style="height:200px;padding:16px 24px">原圖 → strength 0.3、0.5、0.7、0.9（提示詞改成冬天）<small>講師 T4 實跑後替換（lab14 <code>img2img_strength.png</code>）</small></div>

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:17px">
<div class="node"><strong>strength 小（0.3）</strong><small>只加一點雜訊：構圖、細節都保留，只改一點顏色</small></div>
<div class="node node--primary"><strong>中間（0.5～0.7）</strong><small>構圖保留，風格換掉</small></div>
<div class="node node--warm"><strong>strength 大（0.9）</strong><small>幾乎變回純雜訊：只剩構圖的影子</small></div>
</div>

<div class="takeaway mt-3">和 D3-4 一樣：部分加噪再去噪。實際走的步數 ≈ strength × 步數。</div>

<!--
★ img2img（4 分）：常見誤解：strength 是「風格強度」。它是「從第幾步開始去噪」：strength 0.3、25 步 → 只走最後約 7 步。D3-4 用同樣的想法把瑕疵「修掉」，今天用來換風格。
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

- 「接起來」（concatenate）：D2-2 的 U-Net 跳接學過
- U-Net 隨時看得到：哪裡要畫、旁邊原本長什麼樣
- 所以畫出來的背景會和產品的邊緣接得上

</div>
<div class="node node--warm"><strong>今天的用法：換背景</strong><small>白底產品照 → 背景（接近白色的像素）當遮罩 → 只重畫背景，產品保留</small></div>
</div>

<div class="takeaway mt-3">條件不一定要走嵌入那條路：直接接成輸入通道，也是一種條件。</div>

<div class="src">S5：<code>stable-diffusion-inpainting</code> 的 U-Net <code>in_channels</code> ＝ 9（lab14 第 5 部分會印出）</div>

<!--
★ inpainting（5 分）：inpainting（局部重繪）。三種條件方式對照：D4-1 類別 → 加到嵌入；文字 → 交叉注意力；遮罩與原圖 → 接在輸入通道。
-->

---

<div class="eyebrow">04 · Measure（量測驗收）· CLIP 分數</div>

# CLIP 分數：w 越大，越貼題嗎？

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:260px;padding:16px 24px">CLIP 分數 vs w（1、3、5、7.5、10、14），每個 w 4 個 seed 的平均 ± 標準差<small>講師 T4 實跑後替換（lab14 <code>clip_vs_cfg.png</code>）</small></div>

</div>
<div style="font-size:18px">

- CLIP 分數 ＝ 100 × 餘弦相似度（圖，提示詞）
- 預期：w 從 1 往上，分數先升，之後持平甚至下降（過飽和、怪紋路）
- 只有 4 個 seed：看趨勢，不看小數點

</div>
</div>

<div class="takeaway mt-3">CLIP 分數量的是「貼不貼題」，不是「好不好看」：最後仍要行銷部人工看。</div>

<div class="src">S7：CLIPScore（Hessel et al., 2021，待確認）；本 lab 用 100 × cos</div>

<!--
★ CLIP 分數（3 分）：和 D4-1 的忠實度是同一件事：「有沒有聽話」。實際曲線以 T4 輸出為準。
-->

---

<div class="eyebrow">04 · Measure · 偏差稽核</div>

# 偏差稽核：提示詞沒說的，模型會自己補

<div style="font-size:17px">提示詞：<code>photo of a customer service representative at an electronics store, smiling</code>（沒有指定性別、年齡）。看 lab 第 6b 部分的 12 張，自己數。</div>

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

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-3">
<div class="placeholder" style="height:240px;padding:16px 24px">產品線稿 → 依線稿生成的情境照<small>講師示範（課前跑好、標明 seed 與步數）；未跑前不放圖</small></div>
<div style="font-size:18px">

- 多加一個條件：邊緣圖、人體姿勢、深度圖
- 原本的 SD 不動，旁邊加一個「控制」網路
- 適合：產品位置、角度要固定的版面

</div>
</div>

<div class="takeaway mt-3">提示詞管「畫什麼」，ControlNet 管「畫在哪裡、什麼角度」。</div>

<div class="src">Zhang et al., ControlNet, 2023（S9，待確認）</div>

<!--
○ 示範（2 分）：時間不夠就跳過。示範用的筆記本不發給學員。
-->

---

<div class="eyebrow">05 · 延伸 · 回到工廠</div>

# 用 inpainting 合成瑕疵，補 YOLOv8 的訓練資料

<div style="font-size:19px" class="mt-4">

- DL 課的 YOLOv8 瑕疵偵測，最缺的是「不良品照片」
- 在良品照上畫一個遮罩、提示詞寫「scratch」→ 合成一張帶刮痕的板子
- 遮罩本身就是標註框：不用再人工標

</div>

<div class="takeaway mt-4">和 D4-1 的風險一樣：合成瑕疵只進訓練集，驗收一定用真實不良品。</div>

<div class="src">YOLOv8：DL 課 pp.56–62；D2-2 也用過程式合成的瑕疵</div>

<!--
○ 選修（2 分）：SD1.5 沒看過 PCB 瑕疵，生成的刮痕可能不像真的；要先讓品保看過。和 D2-2 程式合成瑕疵的做法比較。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# 排程器：同一個 U-Net，不同的「下山路線」（只認名字）

<div style="font-size:19px" class="mt-4">

- DDPM：D3-3 的做法，每步加一點新雜訊，要很多步
- DDIM：D3-4 用過，不加新雜訊，可以跳步
- DPM-Solver（今天的 lab）：把去噪看成解微分方程，25 步就夠清楚

</div>

<div class="takeaway mt-4">換排程器不用重新訓練：U-Net 一樣，只換「每一步怎麼走」。</div>

<!--
△ 備用（1 分）：學員問「為什麼 D3-3 要 1000 步、今天 25 步就好」時再講。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab14-sd-studio.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**（模型約 4 GB，第一次下載要幾分鐘）

1. 企劃文字能變成可用的情境照嗎？
2. 產品照能只換背景、不改產品嗎？
3. 哪一個 w 最貼題？有人物時有沒有偏差？

</div>
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">目標：情境照、換背景前後、CLIP 分數曲線、Gradio 工作室<small>講師 T4 實跑後換成真實輸出（含 VRAM 峰值與總時間）</small></div>

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
  <div><span class="num">3</span><strong>參數</strong>：步數 × w 網格；負面提示對照</div>
  <div><span class="num">4</span><strong>img2img</strong>：<code>StableDiffusionImg2ImgPipeline(**pipe.components)</code>，共用權重</div>
  <div><span class="num">5</span><strong>inpainting</strong>：做背景遮罩（TODO）→ inpainting 模型換背景 → 量產品區改變多少</div>
  <div><span class="num">6–7</span><strong>量測與 Ship</strong>：CLIP 分數 vs w、偏差稽核 12 張、Gradio 兩個分頁</div>
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
<span class="muted" style="font-size:16px">為什麼：兩個 SD 模型同時在 GPU 上，VRAM 會吃緊；fp16 讓一張圖幾秒內完成</span><br>
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
product 是白底產品照；arr 是它的 numpy 陣列（512, 512, 3）。<br>
做一張遮罩 mask（PIL 灰階圖）：三個通道都大於 235 的像素＝255（背景，要重畫），其餘＝0（產品，保留）。<br>
只用 numpy 和 PIL，不要改其他格。說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>下載、載入與每張圖的時間待 T4 實測；第一次下載時先看第 2 部分</div>
  <div><span class="num">2</span>沒有 Agent 額度：遮罩只要兩行（<code>(arr &gt; 235).all(axis=-1)</code>，再轉成 0／255 的圖）；卡住開 <code>-solution.ipynb</code></div>
  <div><span class="num">3</span>預期輸出：「背景佔 ＿＿% 的像素」、<code>inpainting U-Net 輸入通道： 9</code></div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>遮罩黑白顛倒：白色是產品 → inpainting 會把產品重畫掉、背景留著。先看遮罩圖再跑</small></div>

<!--
★ 執行（約 18 分）：常見錯誤是遮罩顛倒；另一個是門檻太低，產品的白色外殼也被當成背景（白色耳機！）——這時要看「背景佔幾 %」並調門檻或手動補遮罩。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 5／7：看結果、對照預測

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

1. 參數網格：從幾步開始，圖就「夠用」了？
2. 負面提示：寫了 <code>people, hands, text</code> 之後，圖裡還有嗎？
3. img2img：哪一個 strength 最像「同一張照片的冬天版」？
4. 換背景：放大看耳機的形狀、白色外殼的邊緣

</div>
<div>

<div class="node node--warm"><strong>白色產品＋白色背景</strong><small>白色耳機的外殼也接近白色：遮罩可能把產品的一部分當成背景。這是今天最常見的失敗</small></div>

</div>
</div>

<div class="takeaway mt-4">生成圖要「先看再用」：每一個參數的改變，都要用同一個 seed 對照。</div>

<!--
★ 對照（5 分）：第 4 題是伏筆：下一頁用數字量產品區改變多少。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:15px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:34%">應該是</th></tr></thead>
<tbody>
<tr><td>Agent 做的遮罩方向對嗎？</td><td>看遮罩圖</td><td>背景白、產品黑</td></tr>
<tr><td>產品有沒有被改？</td><td>看「產品區平均改變」</td><td>遠小於背景區（驗收 ②）</td></tr>
<tr><td>U-Net 真的是 9 通道？</td><td>看印出的 <code>in_channels</code></td><td>inpainting 9、一般 SD 4</td></tr>
<tr><td>CLIP 分數比的是同一句提示詞嗎？</td><td>看 <code>clip_sim(ims, &#91;PROMPT&#93;)</code></td><td>每個 w 都和同一句比</td></tr>
<tr><td>偏差表的判斷可靠嗎？</td><td>「看不出來」的有幾張</td><td>不確定就填看不出來，不硬猜</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如遮罩門檻從 235 改成 245，看背景比例和產品區改變怎麼變。</div>

<!--
★ 稽核（5 分）：數字以 T4 輸出為準（lab-runs.md）。
-->

---

<div class="eyebrow">06 · Lab L4-2</div>

# Lab 7／7：換背景前後

<div class="placeholder" style="height:260px;padding:16px 24px">白底產品照 → 遮罩 → 換背景後（咖啡廳桌面）<small>講師 T4 實跑後替換（lab14 <code>inpaint_swap.png</code>，附產品區／背景區的平均改變）</small></div>

<div class="node mt-3" style="font-size:17px"><strong>延伸（選做）</strong><small>把遮罩反過來（產品白、背景黑），提示詞寫「black wireless earbuds」：變成「換產品顏色、背景不動」。先預測：產品的形狀會保留嗎？</small></div>

<div class="takeaway mt-2">遮罩決定「改哪裡」，提示詞決定「改成什麼」。</div>

<!--
★ 結果（3 分）：延伸題的答案：形狀大致保留（旁邊的背景會「框住」它），但細節（Logo、按鍵）通常會變，所以不能拿來做真的商品圖。
-->

---

<div class="eyebrow">07 · Ship（交付）· Day 4 交付物</div>

# Ship：行銷部可以自己點的工作室

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:260px;padding:16px 24px">Gradio 工作室截圖：「文字生成」、「換風格（img2img）」兩個分頁<small>講師 T4 實跑後替換（lab14 第 7 部分）</small></div>

</div>
<div style="font-size:17px">

- <code>gr.Blocks</code> ＋ <code>gr.Tab</code>：一個網頁、兩個工具（D1-4 是單一的 <code>Interface</code>）
- 兩個分頁共用同一組權重：<code>Img2Img(**pipe.components)</code>
- 標題寫明「AI 生成，使用前請人工審核」
- <code>share=True</code>：72 小時有效的公開網址（D1-4）

</div>
</div>

<div class="takeaway mt-3">交付的不只是圖，而是「行銷部自己能用、而且知道要審核」的工具。</div>

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

<div class="takeaway mt-3">商品圖不能誇大產品：換背景可以，改產品外觀不行（D3-1 的假細節是同一件事）。</div>

<div class="src">SD1.5 授權 CreativeML OpenRAIL-M（S1）；C2PA（S8）；皆待確認。法律問題以公司法務意見為準</div>

<!--
★ 風險（3 分）：C2PA（內容憑證）：在檔案裡記錄「這張圖怎麼產生、被誰改過」的標準。OpenRAIL-M 授權允許商業使用，但列了不可用的用途（模型卡）。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">CLIP：文字和圖同一空間</span><span class="arrow">→</span>
  <span class="chip">文字編碼器 → 交叉注意力</span><span class="arrow">→</span>
  <span class="chip">潛在空間 4 × 64 × 64</span><span class="arrow">→</span>
  <span class="chip">CFG w、負面提示</span><span class="arrow">→</span>
  <span class="chip">img2img、inpainting</span><span class="arrow">→</span>
  <span class="chip">CLIP 分數、偏差稽核</span>
</div>

<div class="takeaway mt-6">SD 的每一塊都學過；今天學會的是「控制」：參數、起點（img2img）、範圍（遮罩），以及量測。</div>

<!--
★ 總整理（2 分）：請學員說出三種把條件交給 U-Net 的方式：嵌入相加（D4-1）、交叉注意力（文字）、接成輸入通道（inpainting）。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq" style="font-size:17px">

1. Stable Diffusion 1.5 的 U-Net 在什麼大小上去噪？（　）<br><span class="opts"><span class="nw">A. 3 × 512 × 512 的像素</span>　<span class="nw">B. 4 × 64 × 64 的潛在</span>　<span class="nw">C. 77 × 768 的文字向量</span>　<span class="nw">D. 1 × 28 × 28</span></span>
2. 為什麼 guidance_scale＝1 時負面提示沒有作用？（　）<br><span class="opts"><span class="nw">A. 負面提示只支援英文</span>　<span class="nw">B. 步數太少</span>　<span class="nw">C. 負面提示取代 ε_uncond，而 w＝1 時 ε＝ε_cond</span>　<span class="nw">D. seed 固定了</span></span>
3. img2img 的 strength 從 0.3 調到 0.9，最可能？（　）<br><span class="opts"><span class="nw">A. 圖更像原圖</span>　<span class="nw">B. 加更多雜訊，和原圖差更多</span>　<span class="nw">C. 生成更快</span>　<span class="nw">D. 解析度變高</span></span>
4. CLIP 分數高代表？（　）<br><span class="opts"><span class="nw">A. 圖和提示詞的方向接近</span>　<span class="nw">B. 圖很好看</span>　<span class="nw">C. 圖沒有偏差</span>　<span class="nw">D. 圖沒有侵權</span></span>

</div>

<!--
★ 檢核（3 分）。答案：1 B、2 C、3 B（實際走的步數也變多，所以 C 錯）、4 A（B 是常見誤解）。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D4-3：生成的圖必須是「我們的」產品

<div style="font-size:19px" class="mt-4">

- 品牌部：提示詞描述不出我們產品的樣子，每次都不一樣
- 不訓練：IP-Adapter 給一張參考照
- 訓練一點點：DreamBooth ＋ LoRA，只學一對很細的矩陣

</div>

<!--
★ 下一步（1 分）：預告。請學員準備約 10 張自己拍的產品照（自有、同意使用）；沒有的話用講師提供的資料。
-->
