---
theme: default
title: 我們的產品、我們的風格
info: |
  生成式AI原理 · D4-3
  品牌部要生成的圖必須是「我們的」產品：先用 IP-Adapter 當不訓練的基準，再用 DreamBooth ＋ LoRA 在 T4 上訓練，並檢查有沒有背下訓練照。
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
exportFilename: 15-lora-brand
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D4-3</div>

# 我們的產品、我們的風格

<p class="subtitle">IP-Adapter 不訓練、DreamBooth ＋ LoRA 只訓練一小塊：讓 SD 畫出「這一個」產品</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">提示詞描述不出來</span><span class="arrow">→</span>
  <span class="chip">IP-Adapter</span><span class="arrow">→</span>
  <span class="chip">W ＋ B·A</span><span class="arrow">→</span>
  <span class="chip">sks backpack</span><span class="arrow">→</span>
  <span class="chip">T4 設定</span><span class="arrow">→</span>
  <span class="chip">有沒有背下來？</span>
</div>

<!--
★ 開場（2 分）：D4-2 的 SD 會畫「一個背包」，但不會畫「我們的那個背包」。今天讓它認識我們的產品。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 品牌部：生成的圖必須是「我們的」產品

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D4-3】部門：品牌部<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>生成的圖必須是「我們的」產品、品牌一致的風格</dd>
    <dt>現況痛點</dt><dd>提示詞描述不出產品外觀，每次生成都不一樣</dd>
    <dt>成功指標（KPI）</dt><dd>前後對照網格；產品認得出來；沒有過度擬合（姿勢、背景都一樣）</dd>
    <dt>可用資料</dt><dd>6～10 張自有產品照（今天用 6 張背包照代替，Unsplash 授權）</dd>
    <dt>限制與法規</dt><dd>Colab T4（512px、fp16、梯度檢查點）；訓練照的授權與同意</dd>
    <dt>為何現有工具不夠</dt><dd>只靠提示詞，無法描述「這一個」產品</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：曜嶼電子是電子與生活用品公司，背包是生活用品線的產品。學員帶了自己的產品照的，lab 第 0 部分可以換掉。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **使用** IP-Adapter 當「不訓練」的基準
2. **畫出** W ＋ B·A，並算出 LoRA 的參數量
3. **說明** DreamBooth 的識別字 <code>sks</code> 和類別詞各做什麼
4. **訓練**一個符合 T4 限制的 LoRA
5. **偵測**過度擬合：前後對照、和最像的訓練照比相似度

<!--
★ 目標（1 分）。不教：textual inversion 的訓練（只認名字）、rank／alpha 的數學（附錄）、prior preservation 的實作（只講概念）。
-->

---

<div class="eyebrow">00 · Frame · 提示詞的極限</div>

# 盡力描述，畫出來的還是「別人的背包」

<div class="grid grid-cols-[1.4fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:118px;padding:10px 20px">6 張訓練照（我們的背包）<small>講師 T4 實跑後替換（lab15 <code>train_photos.png</code>）</small></div>
<div class="placeholder mt-2" style="height:118px;padding:10px 20px">只用提示詞生成的 4 張（seed 0–3）<small>講師 T4 實跑後替換（lab15 <code>prompt_only.png</code>）</small></div>

</div>
<div style="font-size:17px">

提示詞：<code style="font-size:15px">a photo of a pinkish-red backpack with small round patches on the front pocket, on a wooden bench in a park</code>

- 對照看：顏色、前口袋、小徽章、背帶一樣嗎？
- 換一個 seed，還是同一個背包嗎？

</div>
</div>

<div class="takeaway mt-3">提示詞描述的是一個類別；品牌要的是一個特定的東西。</div>

<!--
★ Frame（5 分）：請學員找三個「不一樣的地方」。預期（以 T4 輸出為準）：每個 seed 畫出不同的背包，這就是需求單的痛點。
-->

---

<div class="eyebrow">01 · Try（先看結果）· 不訓練</div>

# IP-Adapter：給一張參考照，不用訓練

<div class="placeholder" style="height:200px;padding:16px 24px">參考照 → IP-Adapter scale 0.3、0.6、0.9 生成的「公園長椅上的背包」<small>講師 T4 實跑後替換（lab15 <code>ip_adapter.png</code>，seed 0）</small></div>

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:17px">
<div class="node"><strong>怎麼做到的</strong><small>參考照經 CLIP 的<b>影像</b>編碼器變成向量，用另一組交叉注意力接進 U-Net（D4-2 文字那一組不動）</small></div>
<div class="node node--warm"><strong>scale 的取捨</strong><small>小：場景聽文字、產品不太像；大：產品像了，但姿勢、背景也被照抄</small></div>
</div>

<div class="takeaway mt-2">不訓練的基準：幾秒鐘就有大概的樣子；細節穩不穩，要和 LoRA 比。</div>

<div class="src">Ye et al., IP-Adapter, 2023（S4，待確認）；權重 <code>h94/IP-Adapter</code> 的 <code>ip-adapter_sd15.bin</code></div>

<!--
★ 示範（5 分）：先做不訓練的方法當基準，和 D3-2「先試顏色正規化」同一個習慣：貴的方法要贏過便宜的才值得。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 微調的兩種做法</div>

# 全部微調 vs LoRA

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node"><strong>全部微調（DL 課學過）</strong><small>U-Net 約 860M 個參數全部更新：<br>· 每個參數都要存梯度和 Adam 的兩個狀態 → T4 放不下<br>· 6 張照片，860M 個參數 → 很容易背下來<br>· 存一份新模型 ≈ 幾 GB</small></div>
<div class="node node--primary"><strong>LoRA（低秩適應）</strong><small>原本的權重 W 凍結，每個注意力層旁邊加一小塊 B·A：<br>· 只訓練不到 1% 的參數<br>· T4 跑得動<br>· 存下來只有幾 MB，可以隨時開關</small></div>
</div>

<div class="takeaway mt-4">和 DL 課的遷移學習同一個想法：大部分凍結，只調一小部分；LoRA 連「調哪一層」都只加一小塊。</div>

<div class="src">DL 課 pp.56–66（遷移學習、凍結）；Hu et al., LoRA, 2022（S2，待確認）；參數量與檔案大小以 lab15 輸出為準</div>

<!--
★ 全部 vs LoRA（5 分）：LoRA（Low-Rank Adaptation，低秩適應）。「秩」下一頁用圖解釋，不講線性代數。
-->

---

<div class="eyebrow">02 · Open · 今天的主角圖</div>

# LoRA：W 不動，旁邊加兩個很細的矩陣

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 330 200" style="width:100%" aria-label="左邊一個大方塊 W 標示凍結；右邊一個細長的 B 乘上一個扁平的 A；兩者的輸出相加">
  <rect x="10" y="30" width="120" height="120" fill="#eee" stroke="#888" stroke-width="2"/>
  <text x="48" y="95" style="font-size:22px" fill="#555">W</text>
  <text x="14" y="172" style="font-size:15px" fill="#666">d × d，凍結</text>
  <text x="145" y="98" style="font-size:24px" fill="#444">＋</text>
  <rect x="180" y="30" width="20" height="120" fill="var(--warm-accent)" fill-opacity="0.3" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="184" y="95" style="font-size:18px" fill="var(--warm-accent)">B</text>
  <text x="208" y="98" style="font-size:20px" fill="#444">·</text>
  <rect x="220" y="80" width="105" height="20" fill="var(--warm-accent)" fill-opacity="0.3" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="264" y="96" style="font-size:16px" fill="var(--warm-accent)">A</text>
  <text x="172" y="172" style="font-size:15px" fill="var(--warm-accent)">d × r 和 r × d，要訓練</text>
</svg>

</div>
<div style="font-size:18px">

- 輸出 ＝ W·x ＋ B·(A·x)
- r（秩）很小：4、8、16
- B 一開始是 0 → 訓練前和原模型一模一樣
- **照著算**：320 × 320 的層，r＝4<br>全部：320 × 320 ＝ 102,400<br>LoRA：2 × 320 × 4 ＝ **2,560**（2.5%）

</div>
</div>

<div class="takeaway mt-2">讀作：「原本的答案不動，再加一個『只有 r 個方向』的小修正」。</div>

<div class="src">Hu et al., 2022 §4.1（S2，待確認）；320 是 SD1.5 U-Net 第一層的通道數</div>

<!--
★ LoRA（6 分）：r 讀作「秩」：這個小修正最多只能往 r 個方向改。B 初始化為 0 很重要：一開始 B·A＝0，模型和原本完全一樣，訓練只會慢慢加上修正。
常見誤解：LoRA 是另一個模型。它是一小塊「差值」，要加在原本的 SD1.5 上才能用。
-->

---

<div class="eyebrow">02 · Open · 練習（不用 AI）</div>

# 練習：一個 768 × 768 的層，LoRA 要學幾個數字？

<div class="muted" style="font-size:17px">照上一頁「照著算」的方法。比例＝LoRA ÷ 全部（768 × 768 ＝ 589,824）。</div>

<table class="fill tight vlines mt-2">
<thead><tr><th style="width:14%">r</th><th>LoRA 參數（2 × 768 × r）</th><th>佔全部的比例</th></tr></thead>
<tbody>
<tr><td>4</td><td class="blank"><FillIn id="lora.p4" hint="例：2,560……" /></td><td class="blank"><FillIn id="lora.f4" /></td></tr>
<tr><td>8</td><td class="blank"><FillIn id="lora.p8" /></td><td class="blank"><FillIn id="lora.f8" /></td></tr>
<tr><td>16</td><td class="blank"><FillIn id="lora.p16" /></td><td class="blank"><FillIn id="lora.f16" /></td></tr>
</tbody>
</table>

<FillClear group="lora" />

<div class="muted mt-2" style="font-size:16px">做完後執行 lab 第 3 部分的第一格對答案。再想：r 加倍，LoRA 檔案大約變幾倍？</div>

<!--
★ 無 AI 檢核點（7 分）：個人作業、不收回。768 是 SD1.5 文字編碼器的寬度，也是 U-Net 部分注意力層的寬度。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：r 加倍，參數就加倍

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:14%">r</th><th>LoRA 參數</th><th>比例</th></tr></thead>
<tbody>
<tr><td>4</td><td>2 × 768 × 4 ＝ 6,144</td><td>1.04%</td></tr>
<tr><td>8</td><td>12,288</td><td>2.08%</td></tr>
<tr><td>16</td><td>24,576</td><td>4.17%</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：參數和 r 成正比；即使 r＝16，也不到全部的 5%。檔案大小同樣約和 r 成正比。</div>

<!--
★ 解答（2 分）：lab 第 3 部分的第一格會印出同樣三個數字（固定公式，不是模型輸出）。
-->

---

<div class="eyebrow">02 · Open · DreamBooth</div>

# DreamBooth：給產品取一個罕見的名字

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-3" style="font-size:18px">
<div>

<div class="node node--primary" style="font-size:22px;text-align:center;padding:14px">a photo of <span style="color:var(--warm-accent)"><b>sks</b></span> <b>backpack</b></div>

- **sks**：識別字，一個模型幾乎沒看過的字 → 學成「這一個背包」
- **backpack**：類別詞，讓模型從「已經會畫的背包」出發，不用從零學

</div>
<div>

- 訓練：6 張照片，提示詞都是同一句
- 使用：<code>a photo of sks backpack on a snowy mountain</code> → 我們的背包，新的場景
- 迴圈就是 D3-3 的預測雜訊；只更新 LoRA

</div>
</div>

<div class="takeaway mt-3">提示詞描述不出來的東西，就給它一個名字，用照片教它那個名字是什麼。</div>

<div class="src">Ruiz et al., DreamBooth, 2023（S3，待確認）</div>

<!--
★ DreamBooth（7 分）：為什麼不用「our backpack」？因為「our」是常見字，已經有意思了；sks 幾乎沒有意思，比較不會干擾。常見誤解：要很多照片。論文用 3～5 張；重點是角度、背景要不同。
-->

---

<div class="eyebrow">03 · Adapt（調整）· T4 設定</div>

# 在一張 T4 上訓練：省記憶體的四個設定

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:24%">設定</th><th>做什麼</th><th style="width:34%">代價</th></tr></thead>
<tbody>
<tr><td>512px、一次一張</td><td>SD1.5 原本的大小；batch＝1</td><td>每步只看一張，loss 跳動大</td></tr>
<tr><td>fp16 混合精度</td><td>U-Net 用 fp16 算，只有 LoRA 參數用 fp32 更新（D1-2、D1-4 學過 fp16）</td><td>幾乎沒有</td></tr>
<tr><td>梯度檢查點（gradient checkpointing）</td><td>反向傳播時才重算中間結果，不全部存</td><td>慢一些</td></tr>
<tr><td>先把照片編碼成潛在</td><td>VAE 編碼器只跑一次（D2-3），訓練時不再用</td><td>不能做隨機裁切等增強（只做左右翻轉）</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">VRAM 不夠時，用時間換記憶體；這四個設定讓 LoRA 訓練擠進 T4（實際 VRAM 峰值見 lab 輸出）。</div>

<div class="src">8-bit Adam（bitsandbytes）是另一個常用選項；本 lab 只訓練 LoRA，一般 AdamW 就放得下（以 T4 實測為準）</div>

<!--
★ T4 設定（6 分）：gradient checkpointing（梯度檢查點）。8-bit Adam 把優化器的狀態壓成 8 位元，全部微調時很有用；只訓練 LoRA 時優化器狀態本來就很小，所以 lab 沒用（少一個相依套件）。
-->

---

<div class="eyebrow">04 · Measure（量測驗收）· 過度擬合</div>

# 過度擬合：每張都長得像某一張訓練照

<div class="grid grid-cols-[1.25fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:260px;padding:16px 24px">前後對照：同一個 seed，LoRA 關／開；三個場景（公園、雪山、辦公室）<small>講師 T4 實跑後替換（lab15 <code>lora_before_after.png</code>）</small></div>

</div>
<div style="font-size:17px">

- **好**：產品認得出來，場景照提示詞換掉
- **背下來**：每張都是訓練照的姿勢和背景，「雪山」也變成訓練照的地點
- 量法：生成圖和 6 張訓練照比 CLIP 影像相似度，取最大值；接近 1 ＝ 幾乎是某一張訓練照
- **prior preservation**：同時用「一般背包」的圖訓練，讓模型不要忘記背包本來的樣子（今天只講概念）

</div>
</div>

<div class="takeaway mt-2">loss 低不等於成功：要看「場景換不換得過去」。</div>

<!--
★ 過度擬合（7 分）：prior preservation（先驗保留）。延伸題 1：步數改成 1200，看相似度和場景怎麼變。常見誤解：loss 越低越好——DreamBooth 的 loss 本來就跳動很大，不太能拿來判斷。
-->

---

<div class="eyebrow">05 · 延伸</div>

# Textual inversion：只學一個新字（只認名字）

<div style="font-size:19px" class="mt-4">

- 模型完全不動，只學「sks」這個字的嵌入向量（D4-1 的嵌入）
- 檔案只有幾 KB；但能學到的細節比 LoRA 少

</div>

<div class="takeaway mt-4">三種「讓模型認識我們產品」的方法：IP-Adapter（不訓練）、textual inversion（只學一個字）、LoRA（學一小塊權重）。</div>

<div class="src">Gal et al., 2023（S5，待確認）</div>

<!--
○ 選修（2 分）：只認名字。看到 Civitai 等網站上的 embedding 檔，就是這個。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# rank 和 alpha（選讀）

<div style="font-size:19px" class="mt-4">

- 實際加上的修正 ＝ (α ／ r) · B·A
- α（alpha）是縮放係數；lab 設 α＝r，所以係數是 1
- 換 r 時若固定 α，修正的大小就會跟著變：調 r 時記得一起看 α

</div>

<div class="takeaway mt-4">r 決定「能改多少方向」，α／r 決定「改多大力」。</div>

<!--
△ 附錄（1 分）：學員問 lora_alpha 是什麼時再講。
-->

---

<div class="eyebrow">06 · Lab L4-3</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab15-lora.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**；照片從 GitHub 下載（6 張背包）

1. IP-Adapter 不訓練，像到什麼程度？
2. LoRA 訓練完，「雪山上的我們的背包」畫得出來嗎？
3. 有沒有背下訓練照？

</div>
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">目標：IP-Adapter 三個 scale、LoRA 前後對照、相似度表<small>講師 T4 實跑後換成真實輸出（含訓練時間與 VRAM 峰值）</small></div>

</div>
</div>

<div class="takeaway mt-3">交付給品牌部：一個幾 MB 的 LoRA 檔，加上「能換哪些場景、哪裡會背下來」的說明。</div>

<!--
★ Lab 開始（2 分）：有自己的產品照的學員：放進 my_photos/，把 PHOTO_DIR 改掉。只用自己有權使用的照片。
-->

---

<div class="eyebrow">06 · Lab L4-3</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">0</span><strong>產品照</strong>：下載 6 張，裁成正方形 512 × 512</div>
  <div><span class="num">1</span><strong>基準</strong>：只用提示詞的 4 張</div>
  <div><span class="num">2</span><strong>IP-Adapter</strong>：<code>load_ip_adapter</code>、<code>set_ip_adapter_scale</code></div>
  <div><span class="num">3</span><strong>LoRA</strong>：<code>LoraConfig</code>（TODO）→ <code>unet.add_adapter</code>；印出要訓練的參數量</div>
  <div><span class="num">4</span><strong>訓練</strong>：照片 → 潛在（一次）→ 每步：加雜訊、U-Net 預測雜訊、MSE；存 <code>lora_sks_backpack</code></div>
  <div><span class="num">5</span><strong>驗收</strong>：<code>disable_adapters</code>／<code>enable_adapters</code> 前後對照；和最像的訓練照的相似度</div>
</div>

<div class="takeaway mt-3">一個 TODO：LoRA 設定（r、alpha、加在哪幾層）。訓練迴圈和 D3-3 一樣。</div>

<!--
★ 拆塊（3 分）：第 4 部分的迴圈請學員和 D3-3 對照：只多了「潛在」和「文字向量」兩個輸入。
-->

---

<div class="eyebrow">06 · Lab L4-3</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>訓練一個 LoRA，讓「sks backpack」畫出我們的背包，而且能放進新場景<br>
<strong>【輸入與輸出】</strong>照片 &#91;6, 3, 512, 512&#93; → 潛在（含翻轉）&#91;12, 4, 64, 64&#93;；文字向量 &#91;1, 77, 768&#93;；U-Net 預測雜訊 &#91;1, 4, 64, 64&#93;<br>
<strong>【限制】</strong>只訓練 LoRA（r＝4，注意力的 to_q、to_k、to_v、to_out.0）；400 步；Colab T4<br>
<span class="muted" style="font-size:16px">為什麼：步數太多會背下 6 張照片；r 太大檔案變大、也更容易背</span><br>
<strong>【驗收】</strong>① LoRA 參數 &lt; U-Net 的 1%　② LoRA 開的三張，產品比關的時候更像訓練照　③ 三個場景的背景都不同　④ 和最像的訓練照的相似度，低於訓練照彼此之間的平均

</div>

<!--
★ Specify（3 分）：第 ④ 點是「沒有背下來」的數字版本：生成圖不該比「訓練照彼此」還像某一張訓練照。門檻是課前定的，T4 實跑後再調。
-->

---

<div class="eyebrow">06 · Lab L4-3</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 diffusers ＋ peft 的筆記本，請只填第 3 部分的 # TODO：<br>
用 peft 的 LoraConfig 建立 lora_cfg：r＝RANK、lora_alpha＝RANK、init_lora_weights＝"gaussian"，<br>
target_modules 只放注意力的 to_q、to_k、to_v、to_out.0。不要改其他格，說明每個參數的意思。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>訓練時間與 VRAM 待 T4 實測；每 100 步印一次平均 loss</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「LoRA」那頁和 PromptBox 填；卡住開 <code>-solution.ipynb</code></div>
  <div><span class="num">3</span>預期輸出：「LoRA 要訓練 ＿＿ 個（＿＿%）」，之後 4 行 loss，最後 LoRA 檔案大小</div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>target_modules 寫錯名字（例如 <code>q_proj</code>，那是 LLM 的名字）：會出錯或一個參數都沒加上。先看「要訓練幾個參數」再訓練</small></div>

<!--
★ 執行（約 24 分，含訓練）：訓練時先看第 5 部分要對照的問題。斷線：重新執行第 1 部分，再用 pipe.load_lora_weights("lora_sks_backpack") 跳到第 5 部分（檔案若已存到雲端硬碟）。
-->

---

<div class="eyebrow">06 · Lab L4-3</div>

# Lab 5／7：前後對照、對照預測

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

1. IP-Adapter 0.9 和 LoRA：哪一個產品細節（前口袋、小徽章）比較穩？
2. LoRA 關的那一排：「sks backpack」畫出什麼？為什麼？
3. 雪山、辦公室：背景真的換了嗎？還是變成訓練照的地點？

</div>
<div>

<div class="node node--primary"><strong>和隔壁同學比</strong><small>同樣 400 步，不同的 seed：如果你的雪山也變成了訓練照的背景，就是過度擬合的徵兆</small></div>

</div>
</div>

<div class="takeaway mt-4">LoRA 關的時候，sks 只是一個沒意義的字：模型只畫得出「一個背包」。</div>

<!--
★ 對照（7 分）：第 2 題的答案在這頁的 takeaway：LoRA 關 → 回到原本的 SD1.5，sks 沒有意義。
-->

---

<div class="eyebrow">06 · Lab L4-3</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:15px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:34%">應該是</th></tr></thead>
<tbody>
<tr><td>Agent 的 LoRA 真的加上了嗎？</td><td>看「要訓練幾個參數」</td><td>大於 0，且 &lt; U-Net 的 1%</td></tr>
<tr><td>原本的 U-Net 有沒有被改？</td><td><code>disable_adapters()</code> 後生成</td><td>和原本的 SD1.5 一樣</td></tr>
<tr><td>訓練的是預測雜訊嗎？</td><td>看 <code>mse_loss(pred, noise)</code></td><td>和 D3-3 一樣，比的是雜訊</td></tr>
<tr><td>有沒有背下來？</td><td>看相似度表</td><td>LoRA 開的相似度，低於訓練照彼此的平均</td></tr>
<tr><td>照片能用嗎？</td><td>看授權檔</td><td>每張有出處，或是自己拍的</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如步數 400 → 1200，看相似度和雪山背景怎麼變（延伸題 1）。</div>

<!--
★ 稽核（7 分）：數字以 T4 輸出為準（lab-runs.md）。
-->

---

<div class="eyebrow">06 · Lab L4-3 · Ship</div>

# Lab 7／7：交給品牌部的比較

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:24%">方法</th><th>要訓練嗎</th><th>產品像不像</th><th>場景換得過去嗎</th><th>和最像訓練照的相似度</th></tr></thead>
<tbody>
<tr><td>只用提示詞</td><td>否</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>IP-Adapter 0.6</td><td>否</td><td>實跑後填入</td><td>實跑後填入</td><td>—</td></tr>
<tr><td>LoRA r＝4、400 步</td><td>約 ＿ 分鐘</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">建議句型：「品牌部的主力產品用 LoRA（＿ MB、訓練 ＿ 分鐘）；臨時的活動用 IP-Adapter」。</div>

<!--
★ Ship（4 分）：表格由講師 T4 實跑後填入；學員填自己的數字。
-->

---

<div class="eyebrow">07 · 風險（Risk）</div>

# 風險：照片的同意、智慧財產、模仿別的品牌

<div class="grid grid-cols-3 gap-4 mt-3" style="font-size:17px">
<div class="node node--warm"><strong>只用自有的照片</strong><small>產品照要是公司拍的、或有授權；照片裡有人（今天的第 1 張有人背著背包），要有本人同意</small></div>
<div class="node node--warm"><strong>不訓練別人的產品</strong><small>拿競爭對手的產品、他人的作品訓練 LoRA，可能侵害商標、著作權</small></div>
<div class="node node--warm"><strong>LoRA 檔也是資產</strong><small>它記住了產品的樣子：和原始照片一樣要管控，不要隨便上傳到公開網站</small></div>
</div>

<div class="takeaway mt-4">LoRA 學得越像，越要確定「它學的東西你有權使用」。</div>

<div class="src">今天的背包照：Unsplash 授權（S1、S6，待確認）。法律問題以公司法務意見為準</div>

<!--
★ 風險（5 分）：用真人的臉訓練 LoRA（換臉）也是同一個技術，和 D3-2 的 deepfake 風險連起來。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">提示詞描述不出來</span><span class="arrow">→</span>
  <span class="chip">IP-Adapter（不訓練）</span><span class="arrow">→</span>
  <span class="chip">W ＋ B·A</span><span class="arrow">→</span>
  <span class="chip">sks ＋ 類別詞</span><span class="arrow">→</span>
  <span class="chip">fp16、梯度檢查點</span><span class="arrow">→</span>
  <span class="chip">前後對照、相似度</span>
</div>

<div class="takeaway mt-6">讓模型認識一個特定的東西：先試不訓練的，再訓練一小塊；最後確認它沒有背下來。</div>

<!--
★ 總整理（2 分）：請學員用一句話說出 LoRA 為什麼能在 T4 上訓練。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq" style="font-size:17px">

1. LoRA 訓練時，原本的權重 W？（　）<br><span class="opts"><span class="nw">A. 全部更新</span>　<span class="nw">B. 凍結不動，只訓練 B 和 A</span>　<span class="nw">C. 刪掉</span>　<span class="nw">D. 換成 8 位元</span></span>
2. 768 × 768 的層加 r＝8 的 LoRA，要訓練幾個參數？（　）<br><span class="opts"><span class="nw">A. 589,824</span>　<span class="nw">B. 6,144</span>　<span class="nw">C. 12,288</span>　<span class="nw">D. 64</span></span>
3. DreamBooth 提示詞「a photo of sks backpack」中，sks 的作用？（　）<br><span class="opts"><span class="nw">A. 描述背包的顏色</span>　<span class="nw">B. 一個罕見的字，學成「這一個產品」</span>　<span class="nw">C. 負面提示</span>　<span class="nw">D. 排程器的名字</span></span>
4. 生成的「雪山上的背包」背景和訓練照一模一樣，最可能是？（　）<br><span class="opts"><span class="nw">A. 過度擬合，背下了訓練照</span>　<span class="nw">B. r 太小</span>　<span class="nw">C. 指導強度太低</span>　<span class="nw">D. VAE 壞了</span></span>

</div>

<!--
★ 檢核（3 分）。答案：1 B、2 C（B 是 r＝4）、3 B、4 A。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D4-4：GAN 還是擴散？公司標準選哪個？

<div style="font-size:19px" class="mt-4">

- 技術長室：季節性產品照編修要定一個公司標準
- 同一張照片、三種方法：CycleGAN、InstructPix2Pix、SD ＋ LCM-LoRA（又一個 LoRA！）
- 學習評量（a）：寫一頁備忘錄，用自己的證據說明 GAN vs 擴散

</div>

<!--
★ 下一步（1 分）：預告。LCM-LoRA 是把「少步數生成」的能力做成一個 LoRA，今天學的開關方式明天會再用到。
-->
