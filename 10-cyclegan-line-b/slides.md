---
theme: default
title: 沒有成對影像的 B 線
info: |
  生成式AI原理 · D3-2
  B 線換了相機，A 線的瑕疵模型一直誤報；沒有成對影像，用 CycleGAN 把 B 線影像轉成 A 線風格，再量過殺與瑕疵是否被抹掉。
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
exportFilename: 10-cyclegan-line-b
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D3-2</div>

# 沒有成對影像的 B 線

<p class="subtitle">CycleGAN：兩個偽造者互相檢查，把 B 線的照片「翻譯」成 A 線的樣子</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">換相機就誤報</span><span class="arrow">→</span>
  <span class="chip">沒有成對影像</span><span class="arrow">→</span>
  <span class="chip">兩個 G、兩個 D</span><span class="arrow">→</span>
  <span class="chip">循環一致</span><span class="arrow">→</span>
  <span class="chip">過殺降了嗎？</span><span class="arrow">→</span>
  <span class="chip">瑕疵還在嗎？</span>
</div>

<!--
★ 開場（2 分）：昨天（D3-1）的 GAN 是「從隨機數字畫一張圖」。今天的 GAN 是「把一張圖翻成另一種風格」，而且沒有成對的例子可以學。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 品保部 B 線：換了相機，A 線模型一直誤報

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D3-2】部門：製造品保部（B 線）<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>B 線換了相機，D2-1 在 A 線訓練的瑕疵模型，在 B 線一直誤報</dd>
    <dt>現況痛點</dt><dd>B 線過殺率高，好板子被打下來重檢；沒有「同一片板子在兩條線各拍一張」的成對影像</dd>
    <dt>成功指標（KPI）</dt><dd>轉換後，A 線模型在 B 線的過殺下降；真實瑕疵沒有被抹掉（漏檢不變差）</dd>
    <dt>可用資料</dt><dd>VisA PCB1（A 線）；用程式做出的 B 線相機差異（偏暖、偏亮、對比強、雜訊多）</dd>
    <dt>限制與法規</dt><dd>Colab T4；64 × 64 小圖、短時間訓練</dd>
    <dt>為何現有工具不夠</dt><dd>pix2pix 需要成對影像；B 線重新收集、重新訓練太慢</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：過殺（over-kill）：好的被判成壞的；漏檢：壞的沒被抓到（D2-1 學過）。今天兩個都要看：只降過殺、卻讓瑕疵消失，是更糟的結果。
B 線是我們用程式做出來的（合成），課堂上才知道「正確答案」；真實產線要先拍照比對。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **分辨**成對（paired）和不成對（unpaired）的影像轉換，說出各需要什麼資料
2. **畫出** CycleGAN：兩個生成器、兩個鑑別器
3. **讀懂**循環一致損失和 identity 損失各防止什麼錯誤
4. **說明** PatchGAN 的鑑別器為什麼輸出「一張分數圖」
5. **驗收**轉換：過殺有沒有下降、瑕疵有沒有被抹掉，並和更簡單的方法比較

<!--
★ 目標（1 分）。不教：CycleGAN 的完整原始架構（我們用縮小版）、pix2pix 實作、domain adaptation 的理論（△ 點名）。
-->

---

<div class="eyebrow">00 · Frame</div>

# 同一種板子，換一台相機，像素就不一樣了

<div class="grid grid-cols-[1.35fr_1fr] gap-6 mt-2">
<div>

<img class="photo" src="/line-a-vs-b.png" alt="上排：六張 A 線的 PCB1 板子；下排：同樣六張經過 B 線相機效果，偏暖、偏亮、雜訊多" style="width:100%">
<div class="shot-cap">上：A 線（VisA PCB1）；下：同樣的板子，B 線相機（程式產生）</div>

</div>
<div style="font-size:18px">

- 人眼：一樣是好板子
- D2-1 的 AE：只看過 A 線 → 顏色、亮度、對比、雜訊都「不正常」→ **誤報**
- 這叫**分布偏移**（domain shift）：訓練和使用時的資料長得不一樣

</div>
</div>

<div class="takeaway mt-3">模型沒有壞，是資料換了：A 線學到的「正常」，在 B 線不再成立。</div>

<div class="src">影像：VisA PCB1（Zou et al., 2022，CC BY 4.0，S1），64 × 64；B 線效果是 lab10 的 <code>to_line_b</code>（固定公式，不是模型輸出）</div>

<!--
★ Frame（4 分）：domain（領域、資料來源）。請學員先猜：B 線的過殺會是多少？Lab 2／7 會量出來。
B 線的四個差異：紅 ×1.12、藍 ×0.80（偏暖）；gamma 0.8（偏亮）；對比 ×1.2；雜訊（標準差 0.04）。為什麼不用模糊：模糊會讓 AE 重建「更容易」，反而不會誤報（講師本機試跑發現）。
-->

---

<div class="eyebrow">00 · Frame · 為什麼不能直接學</div>

# 成對 vs 不成對：我們只有後者

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:18px">
<div class="node"><strong>成對（pix2pix）</strong><small>每一張 B 都有「同一個東西」的 A 當標準答案 → 可以直接算「G(B) 和標準答案 A 差多少」。但同一片板子要在兩條線各拍一次：產線上幾乎做不到</small></div>
<div class="node node--primary"><strong>不成對（CycleGAN）</strong><small>只有「一堆 A」和「一堆 B」，彼此不對應。沒有標準答案，只能要求：轉出來「像 A」，而且「轉得回去」</small></div>
</div>

<div class="grid grid-cols-2 gap-6 mt-3">
<div><img class="photo" src="/horse.jpg" alt="一匹灰色的馬在草地上低頭吃草" style="height:170px;width:100%;object-fit:cover"><div class="shot-cap">一堆「馬」的照片……</div></div>
<div><img class="photo" src="/zebras.jpg" alt="幾隻斑馬在稀樹草原上吃草" style="height:170px;width:100%;object-fit:cover"><div class="shot-cap">……和一堆「斑馬」的照片：沒有同一隻動物的兩種版本</div></div>
</div>

<div class="takeaway mt-2">CycleGAN 論文最有名的例子就是「馬 ↔ 斑馬」：沒有成對照片，也學得會換風格。</div>

<div class="src">Isola et al., pix2pix, 2017（S2）；Zhu et al., CycleGAN, 2017（S3）；照片：Chad Madden（CC0）、Agness Abubakar Saidi（CC0），Wikimedia Commons（S7、S8）</div>

<!--
★ 成對 vs 不成對（5 分）：問學員：「如果有成對影像，今天最簡單的做法是什麼？」→ 直接訓練一個 B → A 的 U-Net（D2-2），用 L1 比答案。沒有成對，才需要 CycleGAN。
-->

---

<div class="eyebrow">01 · Try（先看結果）</div>

# 講師跑好的 CycleGAN：B 線照片轉成 A 線風格

<div class="placeholder" style="height:300px;padding:16px 24px">B 線輸入 → epoch 1、5、10、20 的 G(B) → A 線同一片板子的照片（G 從沒看過）<small>講師 T4 實跑後替換（lab10 <code>cyclegan_epochs.png</code>）</small></div>

<div class="takeaway mt-3">先猜：轉完的顏色會像 A 線嗎？板子上的元件、文字會不會被改掉？</div>

<!--
★ 示範（5 分）：用 lab10 解答筆記本跑好的圖。最下面一排是「同一片板子的 A 線照片」：G 訓練時從來沒看過這種配對，我們拿它當答案對照。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· 今天的主角圖</div>

# CycleGAN：兩個偽造者、兩個鑑定師

<div class="grid items-center mt-3" style="font-size:17px;grid-template-columns:16% 5% 26% 5% 16% 5% 26%;row-gap:6px">
  <div class="node">B 線照片<small>b</small></div><span class="arrow text-center">→</span>
  <div class="node node--warm"><strong>G：B → A</strong><small>轉成 A 線風格</small></div><span class="arrow text-center">→</span>
  <div class="node">G(b)</div><span class="arrow text-center">→</span>
  <div class="node node--primary"><strong>D_A</strong><small>是真的 A 線照片嗎？</small></div>
  <div class="node">A 線照片<small>a</small></div><span class="arrow text-center">→</span>
  <div class="node node--warm"><strong>F：A → B</strong><small>轉成 B 線風格</small></div><span class="arrow text-center">→</span>
  <div class="node">F(a)</div><span class="arrow text-center">→</span>
  <div class="node node--primary"><strong>D_B</strong><small>是真的 B 線照片嗎？</small></div>
</div>
<div class="muted mt-1" style="font-size:16px;text-align:right">D_A 也看真的 A 線照片 a、D_B 也看真的 B 線照片 b，才學得會分真假（和 D3-1 一樣）</div>

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>和昨天一樣</strong><small>每一對 G 和 D 就是 D3-1 的 GAN：G 想騙過 D，D 想分出真假</small></div>
<div class="node node--warm"><strong>今天新的</strong><small>G 的輸入不是隨機數字，而是一張照片；而且有兩對，互相當對方的「檢查員」（下一頁）</small></div>
</div>

<div class="takeaway mt-3">真正上線只用 G（B → A）；F、D_A、D_B 都是訓練時的幫手。</div>

<div class="src">Zhu et al., CycleGAN, ICCV 2017（S3）</div>

<!--
★ 主角圖（6 分）：請學員指出：哪兩個方塊是 D3-1 的 G？哪兩個是 D？只有箭頭的方向和輸入換了。
-->

---

<div class="eyebrow">02 · Open · 循環一致</div>

# 只騙過 D 不夠：轉過去，還要轉得回來

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:18px">
<div class="node node--warm"><strong>只有對抗損失會怎樣？</strong><small>G 只要畫出「任何一張像 A 線的板子」就能騙過 D_A，不一定是輸入的那一片——元件位置、文字都可能換掉</small></div>
<div class="node node--primary"><strong>循環一致（cycle consistency）</strong><small>b → G → F 要回到 b；a → F → G 要回到 a。轉的時候丟掉的資訊，轉回來就補不回去 → 被罰</small></div>
</div>

<div class="flex items-center justify-center gap-2 mt-4" style="font-size:17px">
  <div class="node" style="width:15%">b</div><span class="arrow">→</span>
  <div class="node node--warm" style="width:12%"><strong>G</strong></div><span class="arrow">→</span>
  <div class="node" style="width:15%">G(b)<small>A 風格</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:12%"><strong>F</strong></div><span class="arrow">→</span>
  <div class="node" style="width:18%">F(G(b))<small>要 ≈ b</small></div>
</div>

```python
loss_cyc = l1(Fb(G(b)), b) + l1(G(Fb(a)), a)     # 轉過去再轉回來，要和原圖一樣（L1）
```

<div class="muted mt-1" style="font-size:16px">L1：每個像素差的絕對值，再平均（MSE 是差的平方再平均；L1 對少數大誤差比較不敏感）。程式裡 F 寫成 <code>Fb</code>，避免和 torch 的 F 撞名。</div>

<div class="takeaway mt-2">循環一致逼 G 盡量保留內容，但不保證內容不變：第 13 頁要直接量瑕疵還在不在。</div>

<!--
★ 循環一致（6 分）：L1 讀作「每個像素差的絕對值，再平均」。程式裡 F 叫 Fb（避免和 torch.nn.functional 的 F 撞名）。
權重 λ_cyc ＝ 10：循環一致比對抗損失重要得多（論文與官方實作的預設，S3／S4，待逐字核對）。
-->

---

<div class="eyebrow">02 · Open · identity</div>

# identity（恆等）損失：已經是 A 線的照片，就別動它

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-3">
<div style="font-size:18px">

- 把 **A 線照片**交給 G（B → A）：應該原封不動；B 線照片交給 F，也應該不變
- 沒有這一項：G 可能順手把顏色也「轉」掉（例如整張偏綠），循環一致照樣成立，因為 F 會轉回來
- 權重比循環一致小：lab 用 λ_id ＝ 5

</div>
<div>

```python
loss_id = l1(G(a), a) + l1(Fb(b), b)
```

<div class="node mt-3" style="font-size:17px"><strong>生成器的總損失</strong><small>對抗 ＋ 10 × 循環一致 ＋ 5 × identity</small></div>

</div>
</div>

<div class="takeaway mt-3">對抗管「像不像 A」、循環管「內容有沒有保留」、identity 管「不該改的別改」。</div>

<div class="src">Zhu et al., 2017（identity 損失用於保留顏色，S3，待逐字核對）；λ 沿用官方實作預設（S4，待確認）</div>

<!--
★ identity（4 分）：identity（恆等）讀作「輸入什麼就輸出什麼」。這是三項損失的總整理頁，下一頁練習會用到。
-->

---

<div class="eyebrow">02 · Open · PatchGAN</div>

# PatchGAN（分塊鑑別器）：鑑定師一塊一塊看

<div class="grid grid-cols-[1fr_1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 300 230" style="width:100%;max-height:250px" aria-label="左邊 64 乘 64 的輸入影像上畫出一個約 46 乘 46 的虛線框；右邊 7 乘 7 的分數圖，其中一格被標出，箭頭表示這一格只看那個框">
  <rect x="10" y="20" width="160" height="160" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2"/>
  <text x="10" y="200" style="font-size:14px" fill="var(--muted-text)">輸入 64 × 64</text>
  <rect x="22" y="30" width="115" height="115" fill="var(--warm-accent)" fill-opacity="0.15" stroke="var(--warm-accent)" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="26" y="160" style="font-size:13px" fill="var(--warm-accent)">這一格看約 46 × 46</text>
  <g transform="translate(205,55)">
    <rect x="0" y="0" width="84" height="84" fill="#fff" stroke="var(--primary)" stroke-width="1.5"/>
    <g stroke="var(--primary)" stroke-width="0.6" opacity="0.7">
      <line x1="12" y1="0" x2="12" y2="84"/><line x1="24" y1="0" x2="24" y2="84"/><line x1="36" y1="0" x2="36" y2="84"/><line x1="48" y1="0" x2="48" y2="84"/><line x1="60" y1="0" x2="60" y2="84"/><line x1="72" y1="0" x2="72" y2="84"/>
      <line x1="0" y1="12" x2="84" y2="12"/><line x1="0" y1="24" x2="84" y2="24"/><line x1="0" y1="36" x2="84" y2="36"/><line x1="0" y1="48" x2="84" y2="48"/><line x1="0" y1="60" x2="84" y2="60"/><line x1="0" y1="72" x2="84" y2="72"/>
    </g>
    <rect x="12" y="12" width="12" height="12" fill="var(--warm-accent)"/>
    <text x="-2" y="102" style="font-size:14px" fill="var(--muted-text)">分數圖 7 × 7</text>
  </g>
  <path d="M137,60 L215,72" stroke="var(--warm-accent)" stroke-width="2" fill="none"/>
</svg>

</div>
<div style="font-size:18px">

- D3-1 的 D：整張圖 → **1 個**分數
- PatchGAN：整張圖 → **7 × 7 個**分數，每一格只看輸入的一塊（約 46 × 46，彼此重疊）
- 高寬：64 → 32 → 16 → 8（三次 stride 2）→ 7（最後一層 kernel 4、stride 1）
- 好處：專心看**紋理和顏色**（風格），參數少，不同大小的圖都能用

```python
D_A(x).shape   # [B, 1, 7, 7]
```

</div>
</div>

<div class="takeaway mt-3">換風格只需要「每一小塊都像 A 線」，不需要判斷整張圖的構圖。</div>

<div class="src">Isola et al., pix2pix, 2017 §3.2（PatchGAN，S2）</div>

<!--
★ PatchGAN（5 分）：patch（小塊）。每一格看到的範圍（感受野）從最後一層往回算：4 → 10 → 22 → 46。原論文多一層，每格看 70 × 70。損失就是把 7 × 7 格都和 1（或 0）比 MSE。
-->

---

<div class="eyebrow">02 · Open · 練習</div>

# 練習：哪一項損失擋住哪一種錯？

<div class="muted" style="font-size:17px">不用 AI。每一列填「對抗」、「循環一致」或「identity」，再寫一句理由。第一列已填好。</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:44%">訓練出來的 G 出了這個問題</th><th style="width:18%">哪一項損失</th><th>理由</th></tr></thead>
<tbody>
<tr><td>G(b) 一看就是 B 線的顏色，沒轉過去</td><td>對抗</td><td>D_A 一眼看出不是 A 線</td></tr>
<tr><td>G(b) 很像 A 線，但元件位置和輸入不一樣</td><td class="blank"><FillIn id="loss.a" /></td><td class="blank"><FillIn id="loss.a-why" hint="例：轉回來的時候……" /></td></tr>
<tr><td>A 線照片交給 G，整張被調成偏藍</td><td class="blank"><FillIn id="loss.b" /></td><td class="blank"><FillIn id="loss.b-why" /></td></tr>
<tr><td>同一個 PatchGAN，輸入改成 128 × 128，輸出 shape 是？</td><td class="blank" colspan="2"><FillIn id="loss.shape" /></td></tr>
</tbody>
</table>

<FillClear group="loss" />

<!--
★ 無 AI 檢核點（5 分）：個人作業，不收回。最後一列：照第 10 頁 64 → 32 → 16 → 8 → 7 的算法做一次；可以在筆記本把 t 改成 128 × 128 驗證。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 練習解答</div>

# 練習解答：三項損失各管一件事

<table class="vlines" style="font-size:18px">
<thead><tr><th style="width:44%">問題</th><th style="width:18%">損失</th><th>理由</th></tr></thead>
<tbody>
<tr><td>元件位置和輸入不一樣</td><td>循環一致</td><td>F 轉回來就不會是原本的 b，L1 很大</td></tr>
<tr><td>A 線照片被調成偏藍</td><td>identity</td><td>G(a) 應該等於 a</td></tr>
<tr><td>128 × 128 輸入</td><td colspan="2">&#91;B, 1, 15, 15&#93;：128 → 64 → 32 → 16（三次減半），最後一層 16 → 15；共 225 格</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">三項損失缺一不可：少了哪一項，就會出現那一列的錯。</div>

<!--
★ 解答（2 分）：補充：循環一致不能保證「完全不改內容」——G 可以把資訊藏在人眼看不到的細微雜訊裡，F 再讀出來（Chu et al. 2017 的觀察，S9）。所以下一頁還要直接檢查瑕疵。
-->

---

<div class="eyebrow">03 · Measure（量測驗收）· 最重要的失敗</div>

# 轉換會不會把瑕疵「抹掉」？

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2">
<div>

<div class="placeholder" style="height:270px;padding:16px 24px">A 線不良品 → B 線版本 → G(B) → 瑕疵遮罩（被轉換傷害最大的 4 張）<small>講師 T4 實跑後替換（lab10 <code>defect_survival.png</code>）</small></div>

</div>
<div style="font-size:18px">

- G 學的是「把 B 變得像 A 線的**良品**」：它只看過良品
- 刮痕、缺件在 G 眼中是「不像 A」的地方 → 可能被「修好」
- 量法：用 A 線 AE 的重建誤差圖，算「瑕疵區的誤差 ÷ 其他區的誤差」。比值接近 1 → 瑕疵被抹掉了
- lab 用 &lt; 1.5 當「瑕疵看不太出來」：本機試跑時，A 線原圖只有 4／100 張低於 1.5

</div>
</div>

<div class="takeaway mt-3">對檢測來說，抹掉瑕疵比誤報更糟：過殺降了，真瑕疵卻可能看不出來。</div>

<!--
★ 瑕疵存活（5 分）：這頁是今天最重要的「Measure」。和 D3-1 的假細節是同一件事的兩面：D3-1 是畫出不存在的東西，今天是擦掉存在的東西。
-->

---

<div class="eyebrow">04 · Adapt（調整）· 先試簡單的</div>

# 更簡單的方法，常常就夠了

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:24%">方法</th><th>做什麼</th><th style="width:30%">什麼時候夠用</th></tr></thead>
<tbody>
<tr><td>顏色正規化</td><td>把 B 線每個顏色通道的平均、標準差調成 A 線的（lab 第 4 部分）</td><td>差異主要是顏色、亮度</td></tr>
<tr><td>用 B 線良品重新訓練 AE</td><td>收集幾百張 B 線良品（不用標註），重跑 D2-1</td><td>B 線已經開工一段時間</td></tr>
<tr><td>CycleGAN</td><td>學出「B → A」的轉換</td><td>差異複雜（紋理、雜訊），又收不到 B 線良品</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">先試最便宜的方法當基準：CycleGAN 要贏過它，才值得多花訓練和驗收的成本。</div>

<!--
○ 選修（3 分）：lab 的對照表會把顏色正規化和 CycleGAN 放在一起比。我們的 B 線有雜訊和對比變化，顏色正規化只能調平均和標準差——但結果如何，以實跑為準。
-->

---

<div class="eyebrow">附錄 · 備用</div>

# Domain adaptation：讓模型本身適應新資料（只認名字）

<div style="font-size:19px" class="mt-4">

- 今天的做法：**改資料**（把 B 轉成 A），模型不動
- 另一派：**改模型**，讓特徵在 A、B 兩邊長得一樣
- CyCADA：兩件事一起做（像素轉換 ＋ 特徵對齊）

</div>

<div class="takeaway mt-4">看到 domain adaptation、CyCADA，知道是在解決同一個「換相機」問題。</div>

<div class="src">Hoffman et al., CyCADA, ICML 2018（S10，待確認）</div>

<!--
△ 備用（2 分）：學員問「可不可以不要轉影像」時再講。
-->

---

<div class="eyebrow">05 · Lab L3-2</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：<code>lab10-cyclegan.ipynb</code>（在 <code>materials/</code>）→ Open in Colab<br>
執行階段：**T4 GPU**

1. A 線模型在 B 線的過殺是多少？
2. CycleGAN 轉換後，過殺降了多少？
3. 有沒有瑕疵被抹掉？比顏色正規化好嗎？

</div>
<div>

<div class="placeholder" style="height:250px;padding:16px 24px">目標：轉換網格、四列對照表（過殺、漏檢、AUROC）、瑕疵存活圖<small>講師 T4 實跑後換成真實輸出（含 VRAM 峰值與總時間）</small></div>

</div>
</div>

<div class="takeaway mt-3">交付給 B 線品保：一張「過殺、漏檢、瑕疵存活」對照表，不是一句「轉得很像」。</div>

<!--
★ Lab 開始（3 分）：VisA 約 1.9 GB，D2-1 已下載過的話把 DATA_DIR 改成雲端硬碟的資料夾。下載、訓練時間與 VRAM 待 T4 實測（teaching-plan 課前清單）。沒有 GPU → EPOCHS_AE＝2、EPOCHS_GAN＝1。
-->

---

<div class="eyebrow">05 · Lab L3-2</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:18px">
  <div><span class="num">1</span><strong>資料</strong>：A 線 400、B 線 400（不同的板子）、A 線驗證 100、測試良品 104、不良品 100（附遮罩）；<code>to_line_b</code> 做出 B 線</div>
  <div><span class="num">2</span><strong>A 線檢測器</strong>：D2-1 的 AE；門檻＝A 線驗證良品的第 95 百分位；<code>report</code> 算過殺、漏檢、AUROC</div>
  <div><span class="num">3</span><strong>CycleGAN</strong>：<code>generator()</code>（殘差區塊）、<code>patch_d()</code>；每個 epoch 存 G(B) 快照</div>
  <div><span class="num">4</span><strong>驗收</strong>：顏色正規化 vs CycleGAN 的對照表；<code>defect_ratio</code> 瑕疵存活</div>
</div>

<div class="takeaway mt-4">兩個 TODO：<code>report</code> 裡的漏檢與 AUROC、生成器的循環一致與 identity 兩行。</div>

<!--
★ 拆塊（3 分）：第 2 部分是 D2-1 的濃縮版，不用重講；把時間留給第 3、4 部分。
-->

---

<div class="eyebrow">05 · Lab L3-2</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>把 B 線影像轉成 A 線風格，讓 A 線模型在 B 線的過殺下降，且瑕疵不被抹掉<br>
<strong>【輸入與輸出】</strong>B 線照片 <code>&#91;B,3,64,64&#93;</code>（0～1）→ G → A 線風格 <code>&#91;B,3,64,64&#93;</code>；D 輸出 <code>&#91;B,1,7,7&#93;</code><br>
<strong>【限制】</strong>A 線和 B 線用不同的板子（不成對）；不良品不能拿來訓練；Colab T4<br>
<span class="muted" style="font-size:16px">為什麼：真實情況就是沒有成對影像；拿不良品訓練，等於偷看考題</span><br>
<strong>【驗收】</strong>① B 線直接檢測的過殺 ≥ A 線的 3 倍（確認問題存在）　② 轉換後過殺 ≤ 10%　③ 轉換後 AUROC ≥ A 線 − 0.03　④ 瑕疵比值 &lt; 1.5 的不良品，不多於「B 線直接」的張數

</div>

<!--
★ Specify（3 分）：驗收第 ③④ 點是今天的重點：只看第 ② 點，會選到一個「把所有東西都修成良品」的 G。數字是課前定的門檻，不是預測結果；T4 實跑後可能要調。
-->

---

<div class="eyebrow">05 · Lab L3-2</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是 PyTorch 筆記本，請只填兩個 # TODO：<br>
① report：miss ＝ 不良品分數 ≤ THR 的比例；auroc ＝ roc_auc_score（良品標 0、不良品標 1）<br>
② CycleGAN 迴圈：loss_cyc ＝ l1(Fb(G(b)), b) ＋ l1(G(Fb(a)), a)；loss_id ＝ l1(G(a), a) ＋ l1(Fb(b), b)<br>
不要改模型大小、λ 和 epochs。每一格說明每一行在做什麼。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>AE 和 CycleGAN 的訓練時間待 T4 實測；等待時看每個 epoch 印出的四個損失</div>
  <div><span class="num">2</span>沒有 Agent 額度：照「循環一致」和「identity」兩頁的程式填；卡住開 <code>-solution.ipynb</code></div>
  <div><span class="num">3</span>預期輸出：<code>G 輸出 (4, 3, 64, 64) | D 輸出 (4, 1, 7, 7)</code>，之後每個 epoch 一行四個損失</div>
</div>

<div class="node node--warm mt-2" style="font-size:16px"><strong>常見錯誤</strong><small>循環一致寫成 <code>l1(G(b), b)</code>：那只轉了一次，而且 G(b) 本來就不該等於 b。要轉兩次：<code>l1(Fb(G(b)), b)</code></small></div>

<!--
★ 執行（約 25 分，CycleGAN 訓練時先看第 2 部分的過殺）：最常見錯誤：循環一致寫成 l1(G(b), b)——那是 identity 的寫法，而且方向錯（b 是 B 線，G(b) 應該是 A 線風格，本來就不該等於 b）。
-->

---

<div class="eyebrow">05 · Lab L3-2</div>

# Lab 5／7：看轉換、對照預測

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

跑完第 3 部分後：

1. 第幾個 epoch 開始，G(B) 的顏色像 A 線？
2. 對照最下排「同一片板子的 A 線照片」：元件、文字有沒有被改？
3. 回到「練習：哪一項損失擋住哪一種錯？」：你的答案在網格裡看得到嗎？

</div>
<div>

<div class="node node--primary"><strong>和隔壁同學比</strong><small>同樣的程式、不同的隨機性，轉換結果可能不一樣：這就是 D3-1 說的 GAN 不穩定</small></div>

</div>
</div>

<div class="takeaway mt-4">轉得「像」要用眼睛看，轉得「對」要用數字量：下一頁量。</div>

<!--
★ 對照（6 分）：第 2 題是給下一頁的伏筆：肉眼看起來一樣，不代表瑕疵還在。
-->

---

<div class="eyebrow">05 · Lab L3-2</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:15px">
<thead><tr><th style="width:28%">稽核問題</th><th>具體動作</th><th style="width:32%">應該是</th></tr></thead>
<tbody>
<tr><td>A、B 線是不同的板子？</td><td>看 <code>split</code> 的切法</td><td>A_train、B_train 沒有重疊</td></tr>
<tr><td>不良品有沒有進訓練？</td><td>找 <code>X&#91;"bad"&#93;</code> 用在哪裡</td><td>只在驗收時用</td></tr>
<tr><td>門檻是在哪裡定的？</td><td>看 <code>THR</code></td><td>A 線驗證良品，不是測試集</td></tr>
<tr><td>Agent 寫的 <code>miss</code>、AUROC 對嗎？</td><td>看 <code>report</code></td><td><code>miss</code> 用 ≤（和過殺的 &gt; 互補）；良品標 0、不良品標 1</td></tr>
<tr><td>Agent 寫的 <code>loss_cyc</code> 對嗎？</td><td>看迴圈</td><td>轉兩次：<code>Fb(G(b))</code>、<code>G(Fb(a))</code></td></tr>
<tr><td>CycleGAN 比顏色正規化好嗎？</td><td>對照表第 3、4 列</td><td>講師實跑後填入</td></tr>
<tr><td>有瑕疵被抹掉嗎？</td><td>比值 &lt; 1.5 的張數</td><td>講師實跑後填入</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如把 λ_cyc 從 10 降到 1，看瑕疵存活會不會變差。</div>

<!--
★ 稽核（7 分）：λ_cyc 降低 → G 比較自由 → 通常更像 A 線，但內容（包括瑕疵）更容易被改。這是今天的取捨。
-->

---

<div class="eyebrow">05 · Lab L3-2 · Ship</div>

# Lab 7／7：交給 B 線品保的對照表

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:30%">做法</th><th>AUROC</th><th>瑕疵比值 &lt; 1.5</th><th>過殺</th><th>漏檢</th></tr></thead>
<tbody>
<tr><td>A 線（原本的相機）</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>B 線直接用 A 線模型</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>B 線 → 顏色正規化</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
<tr><td>B 線 → CycleGAN</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td><td>實跑後填入</td></tr>
</tbody>
</table>

<div class="muted mt-2" style="font-size:16px">先看 AUROC 和瑕疵比值（不受門檻影響）。過殺、漏檢都用 A 線定的門檻：B 線直接檢測時幾乎每張都超過門檻，所以漏檢會是 0%——那不是好，是全部打下來。</div>

<div class="takeaway mt-2">建議要附理由：「B 線先用 ＿＿：過殺從 ＿＿ 降到 ＿＿，漏檢 ＿＿；有 ＿＿ 張瑕疵被抹淡」。</div>

<!--
★ Ship（4 分）：門檻設計成 A 線過殺約 5%；測試只有 104 張良品，實際會在幾 % 上下（本機試跑 1.9%）。數字全部以 T4 實跑為準。
-->

---

<div class="eyebrow">06 · Measure & Risk（風險）</div>

# 風險：轉換會「畫」也會「擦」

<div class="grid grid-cols-2 gap-6 mt-3" style="font-size:18px">
<div class="node node--warm"><strong>檢測影像</strong><small>轉換可能抹掉真瑕疵、或畫出假瑕疵。品質決策用的影像，要逐張保留原圖，並定期抽查轉換前後的瑕疵</small></div>
<div class="node node--warm"><strong>換臉、換聲音</strong><small>同樣的「轉換」技術可以把一個人的臉換到另一段影片上（deepfake，深度偽造）。用在真人身上要有當事人同意，並標示經過 AI 處理</small></div>
</div>

<div class="takeaway mt-4">轉換後的影像不是「原始證據」：品質紀錄、新聞、法律用途都要保留原圖。</div>

<div class="src">deepfake 與同意：D6-1 會再談（聲音複製）</div>

<!--
★ 風險（4 分）：deepfake（深度偽造）。和 D3-1 的假細節、今天的瑕疵存活連起來：生成模型改過的影像，都要能追溯到原圖。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">換相機 → 分布偏移</span><span class="arrow">→</span>
  <span class="chip">沒有成對影像</span><span class="arrow">→</span>
  <span class="chip">G、F、D_A、D_B</span><span class="arrow">→</span>
  <span class="chip">對抗＋循環＋identity</span><span class="arrow">→</span>
  <span class="chip">PatchGAN</span><span class="arrow">→</span>
  <span class="chip">過殺、漏檢、瑕疵存活</span>
</div>

<div class="takeaway mt-6">不成對轉換解決了「沒有答案可學」，但驗收一定要看瑕疵有沒有被改掉，並和簡單方法比。</div>

<div class="muted mt-3" style="font-size:17px">和學習評量的關係：CycleGAN 是「以一張圖為條件」的生成；D4 的條件式生成和 GAN vs 擴散備忘錄，會用到今天的證據（過殺、AUROC、瑕疵存活）。</div>

<!--
★ 總整理（2 分）：請學員用一句話回答「為什麼只看過殺不夠」。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 1／2（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="2"
  :options="['CycleGAN 不需要鑑別器', 'pix2pix 只能處理黑白圖', 'CycleGAN 不需要成對影像', 'CycleGAN 訓練時不用 GPU']"
  :why="['CycleGAN 有兩個鑑別器，一個領域一個。', 'pix2pix 可以處理彩色圖。', '', '兩者都要用 GPU 訓練。']"
  explain="pix2pix 要同一片板子在兩條線拍的成對影像；CycleGAN 只要兩堆照片，靠循環一致損失對齊。">
CycleGAN 和 pix2pix 最大的差別？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="3"
  :options="['G(b) 和 b 一樣', 'D_A 把 G(b) 判成真', 'G(a) 和 a 一樣', 'F(G(b)) 和 b 一樣']"
  :why="['G(b) 要像 A 線，不該和 b 一樣；這是最常見的錯誤。', '這是對抗損失，不是循環一致。', '這是 identity（恆等）損失：已經是 A 線的圖丟進 G 應該不變。', '']"
  explain="b 轉到 A 線再轉回來，F(G(b)) 要和原本的 b 一樣，板子的內容才不會在轉換中被換掉。">
循環一致損失要求？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／2（2 分）：學員自己點；點錯會出現「再想想」和那個選項錯在哪，可以再點一次。答案：1 C、2 D。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／2（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="1"
  :options="['一個分數', '一張「每一小塊真假」的分數圖', '一張彩色圖', '類別標籤']"
  :why="['一個分數是一般 GAN 的鑑別器；PatchGAN 對每一小塊各給一分。', '', '鑑別器不產生圖。', 'PatchGAN 不分類別，只判真假。']"
  explain="每一格分數只看輸入的一小塊，逼生成器把每一處的紋理都做像。">
PatchGAN 的鑑別器輸出？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="3"
  :options="['轉換後顏色像不像 A 線', '生成器的參數量', '鑑別器的損失有沒有下降', '瑕疵有沒有被抹掉']"
  :why="['只看「像不像」正是陷阱：瑕疵被抹掉的圖也很像 A 線。', '參數量和這個風險無關。', 'D 的損失下降只代表訓練在進行，不代表瑕疵保住了。', '']"
  explain="轉換後的圖要拿去做異常偵測，瑕疵一被抹掉就是漏檢；要用有瑕疵的 B 線圖確認瑕疵還在。">
用轉換解決換相機的誤報，最需要額外檢查？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／2（1 分）。答案：3 B、4 D。
全部答案與理由：1 C、2 D（A 是常見錯誤；C 是 identity）、3 B、4 D（A 只是「像」，不代表瑕疵還在）。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D3-3：GAN 一直畫同樣的圖，換擴散模型？

<div style="font-size:19px" class="mt-4">

- 行銷部：GAN 生的商品情境圖都長得差不多（D3-1 的 mode collapse）
- 擴散模型：從雜訊一步一步去噪，多樣性好，但慢
- 我們會從零寫一個小 DDPM

</div>

<!--
★ 下一步（1 分）：預告。生成三難的第三列（擴散模型）下一堂（D3-3）填。
-->
