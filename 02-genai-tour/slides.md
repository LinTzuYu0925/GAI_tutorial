---
theme: default
title: 今晚就要文案和產品圖
info: |
  生成式AI原理 · D1-2
  （一句話說明本單元）
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
exportFilename: 02-genai-tour
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D1-2</div>

# 今晚就要文案和產品圖

<p class="subtitle">（副標：本單元要做出什麼）</p>

<div class="chain flex flex-nowrap items-center gap-2 mt-8">
  <span class="chip">概念一</span><span class="arrow">→</span>
  <span class="chip">概念二</span><span class="arrow">→</span>
  <span class="chip">Lab</span><span class="arrow">→</span>
  <span class="chip">稽核</span>
</div>

<!--
★ 開場：上一單元留下的問題 → 今天要解決什麼。標 ★ 必教、○ 可選、△ 備用。時間見 teaching-plan.md。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **說明**……
2. **推導／計算**……
3. **實作**……（Colab T4）
4. **稽核**生成結果：shape、loss、樣本對不對？

<!--
★ 目標用可觀察的動詞。不教：（列出，並說明屬於哪個後續單元或 Agent 模組）。
-->

---

<div class="eyebrow">01 · 概念一</div>

# 一句話標題，直接說結論

<div class="grid grid-cols-2 gap-6 mt-2">
<div>

<div class="node node--warm"><strong>資料</strong><small><code>[B, 3, 32, 32]</code></small></div>

</div>
<div>

```python
z = encoder(x)        # 壓成潛在向量
x_hat = decoder(z)    # 再還原
```

</div>
</div>

<div class="takeaway mt-4">結論句：用和圖、程式碼相同的數字。</div>

<div class="src">來源：（論文或官方文件，詳見 research/sources.md S1）</div>

<!--
★ 怎麼講、常見誤解、和 DL 課程哪一頁接上（例：DL pp. 72–79 已介紹 AE 概念，這裡直接看程式碼）。
-->

---

<div class="eyebrow">02 · Lab</div>

# Lab 1／N：我們要生成什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:19px">
<div>

**打開筆記本**：`materials/lab01-topic.ipynb` → Open in Colab<br>
執行階段：**T4 GPU**

</div>
<div>

<div class="placeholder">目標樣本示意圖<small>講師實跑後換成真實輸出</small></div>

</div>
</div>

<div class="takeaway mt-4">這就是四個檢查點的 ① 目標</div>

<!--
★ Lab 流程見 demo-and-practice §3c。備案：沒有 GPU 額度 → 打開 lab01-topic-solution.ipynb 的已存輸出。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-nowrap items-center gap-2 mt-4">
  <span class="chip">概念一</span><span class="arrow">→</span>
  <span class="chip">概念二</span><span class="arrow">→</span>
  <span class="chip">Lab</span><span class="arrow">→</span>
  <span class="chip">稽核</span>
</div>

<div class="takeaway mt-6">一句話總結。</div>

<!--
★ 回扣開場的問題。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 是非題

1. ……（　　）
2. ……（　　）
3. ……（　　）

<!--
○ 答案與理由。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下個單元：……

<div class="node node--primary mt-2">今天做到……；下個單元要解決……</div>

<!--
★ 只給講師的託管版看，學員網站不顯示。
-->
