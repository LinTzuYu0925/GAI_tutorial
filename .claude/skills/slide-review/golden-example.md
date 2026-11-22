# Golden Example：學員最容易看懂的頁面

> 來源說明：以下範例全部來自同一位講師的前一門課 Vibe Coding with Python（`C:\Users\lspss\Documents\Vibe_coding_python`），學員是本課程的同一批人。照用的是**做法**（比喻、前後對照、中文唸程式碼、帶著做的實作），不是內容。本課程有講師認可的頁面後，加在檔案最後的「本課程範例」。

這份檔案收集講師認為「學員一看就懂」的頁面。**之後做新投影片，遇到類似概念，請先參考這裡的做法**。每個範例附上為什麼有效，以及可以直接複製修改的 Slidev 原始碼（出處：`05-variables-types-expressions/slides.md`；範例 3 的空白欄位之後要改成可直接輸入的 `FillIn` 元件，寫法見 `demo-and-practice` 第 3 節，範本是單元 04 的練習頁）。

用法：複製範例的 `<svg>`，只改文字、數字與變數名稱。顏色一律用 `style.css` 的 CSS 變數，不要寫死色碼（灰色 `#b8b8b8` 與白色除外）。

---

## 範例 1：變數是貼了標籤的盒子（單元 05 第 6 頁）

**概念**：`score = 90` 是把 90 放進 `score` 盒子，取代原本的 85。

**為什麼學員看得懂**

1. **具體實物比喻**：盒子 ＋ 貼在盒子上的標籤（名字），盒子裡的東西（值）可以換。
2. **三格連續畫面**：執行前 → 執行中 → 執行後，由左到右，視線只走一個方向。
3. **同一個盒子出現三次**：標籤（`score`）完全相同，只有內容變，學員直接看見「名字不變、值會換」。
4. **舊值被「劃掉」**：中間格的 85 變灰並畫刪除線，清楚表示被取代，而不是還留著。
5. **新值有「動作」**：橘色的 90 用箭頭落進盒子，旁邊標 `score = 90`，把程式碼與畫面直接連起來。
6. **編號說明放在每格下方**：①②③ 一句話，不用旁白也看得懂。
7. 下方緊接最小的程式碼與一句 takeaway，圖、碼、結論三者一致（都用 85 → 90）。

**注意事項（踩過的坑）**

- SVG 文字大小要寫成 `style="font-size:46px"`，不要用 `font-size="46"` 屬性（在 Slidev 會被外部樣式蓋掉，字會變得超大）。
- 標籤放在盒子左側，避免箭頭與標籤重疊。
- 說明文字放在盒子下方，不要貼著下面的程式碼區塊（留 10px 以上）。
- `<marker>` 的 `id` 在同一份簡報要唯一（這裡是 `ah`、`ah7`）。

````markdown
<div class="eyebrow">01 · 變數</div>

# 變數（variable）：貼了標籤的盒子

<svg viewBox="0 0 900 232" style="width:100%; max-height:235px" class="mt-1">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--muted-text)"/></marker>
    <marker id="ahw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--warm-accent)"/></marker>
  </defs>
  <!-- 左：score 盒子裡是 85 -->
  <rect x="30" y="85" width="190" height="110" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2.5"/>
  <rect x="45" y="55" width="100" height="32" rx="6" fill="#fff" stroke="var(--primary)" stroke-width="2"/>
  <text x="95" y="78" text-anchor="middle" style="font-size:22px" font-family="JetBrains Mono, Consolas, monospace" font-weight="700">score</text>
  <text x="125" y="155" text-anchor="middle" style="font-size:46px" font-weight="700">85</text>
  <text x="125" y="224" text-anchor="middle" style="font-size:19px" fill="var(--muted-text)">① 盒子裡現在是 85</text>
  <path d="M232 140 H292" stroke="var(--muted-text)" stroke-width="2.5" marker-end="url(#ah)"/>
  <!-- 中：90 放進去，85 被換掉 -->
  <rect x="305" y="85" width="190" height="110" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2.5"/>
  <rect x="320" y="55" width="100" height="32" rx="6" fill="#fff" stroke="var(--primary)" stroke-width="2"/>
  <text x="370" y="78" text-anchor="middle" style="font-size:22px" font-family="JetBrains Mono, Consolas, monospace" font-weight="700">score</text>
  <text x="400" y="155" text-anchor="middle" style="font-size:46px" font-weight="700" fill="#b8b8b8">85</text>
  <path d="M372 134 H428" stroke="#999" stroke-width="3"/>
  <rect x="415" y="2" width="70" height="38" rx="8" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="450" y="30" text-anchor="middle" style="font-size:26px" font-weight="700">90</text>
  <path d="M450 42 V105" stroke="var(--warm-accent)" stroke-width="3" marker-end="url(#ahw)"/>
  <text x="466" y="78" style="font-size:18px" font-family="JetBrains Mono, Consolas, monospace">score = 90</text>
  <text x="400" y="224" text-anchor="middle" style="font-size:19px" fill="var(--muted-text)">② 90 放進去，舊的 85 被換掉</text>
  <path d="M507 140 H567" stroke="var(--muted-text)" stroke-width="2.5" marker-end="url(#ah)"/>
  <!-- 右：score 盒子裡是 90 -->
  <rect x="580" y="85" width="190" height="110" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2.5"/>
  <rect x="595" y="55" width="100" height="32" rx="6" fill="#fff" stroke="var(--primary)" stroke-width="2"/>
  <text x="645" y="78" text-anchor="middle" style="font-size:22px" font-family="JetBrains Mono, Consolas, monospace" font-weight="700">score</text>
  <text x="675" y="155" text-anchor="middle" style="font-size:46px" font-weight="700">90</text>
  <text x="675" y="224" text-anchor="middle" style="font-size:19px" fill="var(--muted-text)">③ 標籤沒變，內容變了</text>
</svg>

```python
score = 85      # 名字 = 值，「=」是「放進去」，不是「等於」
score = 90      # 舊的值被換掉
```

<div class="takeaway mt-2">變數是<strong>名字加上目前的值</strong>。不是數學的未知數，隨時可以換。</div>

<!--
★ 比喻：貼了標籤的盒子，盒子裡的東西可以換。常見誤解：把 = 當成數學的等號。念的時候念「放進去」：score 放進 85。順帶說明命名：名字要看得懂，chinese 比 s1 好，這點在稽核時會用到。
-->
````

---

## 範例 2：`x = x + 1`：先算右邊，再放回左邊（單元 05 第 7 頁）

**概念**：賦值（assignment）的執行順序。學員最常卡在 `score = score + bonus`，因為把 `=` 當成數學等號。

**為什麼學員看得懂**

1. **沿用範例 1 的盒子**：學員已經熟悉「名字＝標籤、值＝盒子內容」，不用再學新圖。
2. **把一行程式拆成兩個動作**：① 先算右邊 ② 放回左邊，用編號與箭頭固定順序。
3. **中間那一格是「計算區」**：用橘色框獨立出來，寫出 `count + 1 = 3 + 1 = 4`，並註明「盒子還沒有被動過」，直接破除「count 同時在兩邊」的疑惑。
4. **先用另一個例子（`count`），練習頁才用 `score = score + bonus`**：先看範例，再自己追蹤，不會看完答案才練習。
5. **takeaway 直接點名誤解**：「不是數學的等式」。
6. 講師備註寫教學動作：念法不念「等於」，念「算出右邊，放進左邊」；請學員用手遮住左邊。

````markdown
<div class="eyebrow">01 · 變數</div>

# 最容易卡住：先算右邊，再放回左邊

<div class="muted" style="font-size:18px">範例：<code>count</code> 盒子裡原本是 3，執行這一行：</div>

```python
count = count + 1
```

<svg viewBox="0 0 900 215" style="width:100%; max-height:215px">
  <defs>
    <marker id="ah7" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--muted-text)"/></marker>
  </defs>
  <rect x="20" y="60" width="170" height="100" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2.5"/>
  <rect x="40" y="30" width="100" height="32" rx="6" fill="#fff" stroke="var(--primary)" stroke-width="2"/>
  <text x="90" y="53" text-anchor="middle" style="font-size:22px; font-weight:700" font-family="JetBrains Mono, Consolas, monospace">count</text>
  <text x="105" y="128" text-anchor="middle" style="font-size:46px; font-weight:700">3</text>
  <text x="105" y="198" text-anchor="middle" style="font-size:19px; fill:var(--muted-text)">執行前：盒子裡是 3</text>
  <path d="M205 110 H265" stroke="var(--muted-text)" stroke-width="2.5" marker-end="url(#ah7)"/>
  <rect x="280" y="40" width="340" height="120" rx="10" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="450" y="76" text-anchor="middle" style="font-size:21px; font-weight:700">① 先算右邊（盒子裡還是 3）</text>
  <text x="450" y="122" text-anchor="middle" style="font-size:28px; font-weight:700" font-family="JetBrains Mono, Consolas, monospace">count + 1 = 3 + 1 = 4</text>
  <text x="450" y="198" text-anchor="middle" style="font-size:19px; fill:var(--muted-text)">計算的時候，盒子還沒有被動過</text>
  <path d="M635 110 H695" stroke="var(--muted-text)" stroke-width="2.5" marker-end="url(#ah7)"/>
  <text x="665" y="92" text-anchor="middle" style="font-size:19px; font-weight:700">② 放回</text>
  <rect x="710" y="60" width="170" height="100" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2.5"/>
  <rect x="730" y="30" width="100" height="32" rx="6" fill="#fff" stroke="var(--primary)" stroke-width="2"/>
  <text x="780" y="53" text-anchor="middle" style="font-size:22px; font-weight:700" font-family="JetBrains Mono, Consolas, monospace">count</text>
  <text x="795" y="128" text-anchor="middle" style="font-size:46px; font-weight:700">4</text>
  <text x="795" y="198" text-anchor="middle" style="font-size:19px; fill:var(--muted-text)">執行後：舊的 3 被換成 4</text>
</svg>

<div class="takeaway mt-2">不是數學的等式（count 不可能等於 count + 1）。是<strong>先算出新的值，再放進 count</strong>。</div>

<div class="src">下一頁練習 <code>score = score + bonus</code>，用同樣的兩步驟追蹤。</div>

<!--
★ 學員最常卡在這裡：把 = 當成數學的等號，覺得 count = count + 1 不可能成立。用三步驟講：①盒子裡現在是 3；②先把右邊算完，得到 4，這時盒子還沒動；③把 4 放進 count，舊的 3 被換掉。念法不要念「等於」，念「算出右邊，放進左邊」。可請學員用手遮住左邊，先只看右邊。
-->
````

---

## 範例 3：練習頁附「照著做」示範（單元 05 第 15 頁）

**概念**：預測運算結果的練習頁。學員第一次自己動手，先看一個**題目不同的完整示範**，再做表格。

**為什麼學員做得出來**

1. **示範用不同的題目**：`9 / 2`、`"hi" * 2` 不在表格裡，學員學得到方法，又不會直接抄到答案。
2. **一個檔案走完全程**：程式碼（`practice.py`）、輸出（寫在 `#` 註解）、執行指令（`python practice.py`）三樣齊全，學員知道要在哪裡寫、怎麼跑、去哪裡看結果。
3. **不用 Python 互動模式（`>>>`）**：初學者容易搞不清楚自己在哪裡輸入。一律改檔案、存檔、執行，和後面做專案的流程一致。
4. **只有三個步驟**，一步一行，右邊編號清單，左邊程式碼，視線不用來回找。
5. **示範輸出經過實際執行**，不憑空編造。
6. 練習頁本身保持極簡：灰色斜體提示、可直接輸入的空白欄位，不收回，答案頁 hostOnly。

**注意事項**

- 示範區放在表格**上方**，並縮小表格列高，整頁要在 1280×720 內放得下：在該頁加 `<style>.slidev-layout table.tight td.blank { height: 30px; }</style>`。
- 步驟文字要短，每步一行，避免換行把表格擠出頁面。
- 其他練習頁（第 21、30 頁）用同一個版型，只換程式碼與步驟。

````markdown
<div class="eyebrow">03 · 運算</div>

# 練習：預測運算結果

<style>
.slidev-layout table.tight td.blank { height: 30px; }
</style>

<div class="grid grid-cols-[1fr_1.2fr] gap-5 items-start mb-1">
<div>

```python
# practice.py
print(9 / 2)       # 輸出 4.5
print("hi" * 2)    # 輸出 hihi
```

</div>
<div class="muted" style="font-size:17px">

**示範：照著做**（題目不同）

1. 新增 `practice.py`，每題一行 `print(...)`
2. 存檔，執行 `python practice.py`
3. 每行輸出對應一題，和「我預測」比對

</div>
</div>

<table class="fill tight">
<thead><tr><th style="width:36%">運算式</th><th>我預測</th><th>實際</th></tr></thead>
<tbody>
<tr><td><code>10 / 4</code></td><td class="blank"><span class="hint">例：有小數嗎……</span></td><td class="blank"></td></tr>
<tr><td><code>10 // 4</code></td><td class="blank"></td><td class="blank"></td></tr>
<tr><td><code>10 % 4</code></td><td class="blank"></td><td class="blank"></td></tr>
<tr><td><code>2 ** 5</code></td><td class="blank"></td><td class="blank"></td></tr>
<tr><td><code>"ab" * 3</code></td><td class="blank"><span class="hint">例：字串乘數字……</span></td><td class="blank"></td></tr>
<tr><td><code>type(10 / 5)</code></td><td class="blank"></td><td class="blank"></td></tr>
</tbody>
</table>

<!--
★ 目標：發現 / 一定給 float、字串可以乘整數（重複）。給 4 分鐘，不收回。下一頁是答案，學員網站不含。
-->
````

---

## 範例 4：用中文白話解釋程式碼（單元 05 第 19 頁）⭐ 非常有幫助

**概念**：邏輯運算 `and`、`or`、`not`，以及 `passed = average >= 60 and attendance >= 0.8` 這種條件式。

> **重點：用中文把程式碼「念出來」，對初學者的理解幫助非常大。** 之後每個語法、運算式、條件，都請先給中文白話說法，再給程式寫法。

**為什麼學員看得懂**

1. **每個關鍵字配一個中文口語**：`and`＝「而且」、`or`＝「或是」、`not`＝「不是」。學員看到程式碼就能自己在心裡念成一句話。
2. **例子用生活語言，不用 `True and False`**：「國文及格」**而且**「英文及格」，學員不用先懂布林運算就能判斷成立與否。`True and False` 這種純符號的例子對初學者太抽象。
3. **先設定情境**：頁面頂端一行「國文 80 分、英文 55 分，60 分及格」，三個例子共用同一組數字，學員可以自己推算結果。
4. **推理過程寫出來**：「→ 英文 55 不成立 → `False`」，讓學員看見為什麼是 `False`，不是只給答案。
5. **關鍵詞用粗體標出**（**而且**、**或是**、**不是**），把中文和程式關鍵字對應起來。
6. **把中文翻譯貼到真實的程式碼**：藍色框裡的 `passed = ...` 下面一行寫「『平均及格』而且『出席率夠』，兩個都要成立才算及格」，學員看到的是自己專案的程式。
7. **括號小提示放在旁邊**：`(average >= 60) and (attendance >= 0.8)`，用括號把兩個條件圈起來，一眼看出 `and` 連接哪兩個，字級比主內容小，不搶焦點。

**可以套用到其他頁面的做法**

- 運算子、比較、條件式、迴圈、函式……凡是有符號或關鍵字的地方，都加一欄「中文怎麼念」。
- 例子的情境與專案（成績單）一致，同一組數字貫穿整頁。
- 中文說法放在程式碼旁邊或正下方，不要藏在講師備註。

**注意事項**

- 表格欄位寬度要預留，避免 `True`／`False` 換行；「意思」欄文字要短。
- 補充提示（括號）用 15px 左右的灰色小字，放在藍色框的右側，不要壓過主要內容。
- 中文白話說法不能和程式行為不一致（例如 `or` 是「至少一個成立」，不是「二選一」）。

````markdown
<div class="eyebrow">04 · 判斷</div>

# 邏輯運算（logic）：and、or、not

<div class="muted" style="font-size:18px">假設國文 80 分、英文 55 分，60 分及格：</div>

<table class="compact">
<thead><tr><th style="width:16%">寫法</th><th style="width:26%">意思</th><th>中文例子</th></tr></thead>
<tbody>
<tr><td><code>A and B</code></td><td>「而且」：兩個都要成立</td><td>「國文及格」<strong>而且</strong>「英文及格」→ 英文 55 不成立 → <code>False</code></td></tr>
<tr><td><code>A or B</code></td><td>「或是」：一個成立就好</td><td>「國文及格」<strong>或是</strong>「英文及格」→ 國文成立 → <code>True</code></td></tr>
<tr><td><code>not A</code></td><td>「不是」：反過來</td><td><strong>不是</strong>「國文及格」→ 國文及格成立，反過來 → <code>False</code></td></tr>
</tbody>
</table>

<div class="grid grid-cols-[1.35fr_1fr] gap-4 mt-3 items-center">
<div class="node node--primary">
  <code>passed = average >= 60 and attendance >= 0.8</code>
  <small>「平均及格」<strong>而且</strong>「出席率夠」，兩個都要成立才算及格</small>
</div>
<div class="muted" style="font-size:15px; line-height:1.5">
  小提示：加括號更好懂<br>
  <code style="font-size:13px">passed = (average >= 60) and (attendance >= 0.8)</code><br>
  括號把每個條件圈起來，一眼看出 <code>and</code> 連接哪兩個。結果相同。
</div>
</div>

<div class="takeaway mt-3">用 <code>and</code> 還是 <code>or</code>，是<strong>需求</strong>的問題，不是語法問題。需求沒寫清楚，Agent 就會猜。</div>

<div class="src">表中結果為本機實際執行 Python 3.12.10。條件複雜時，用括號 <code>( )</code> 讓意思清楚。</div>
````

---

## 範例 5：一整段「帶著做」的實作練習（單元 05 第 27–31 頁）⭐ 學員喜歡

**概念**：把 Specify → Generate → Execute → Audit → Iterate 這條開發迴圈，拆成五頁連續的引導練習，學員從頭到尾做完一個小程式（`grades.py`），每一步都知道**做什麼、寫在哪裡、做完長什麼樣子**。

### 全貌

| 頁 | 階段 | 學員做什麼 | 這頁給了什麼引導 |
|---|---|---|---|
| 27 | Specify（說明需求） | 在 `spec.txt` 寫欄位與型別、規則、驗收標準 | 三個編號步驟＋每步一行「為什麼」＋**提示骨架**（【欄位】【規則】【驗收標準】【限制】）＋三組驗收標準表格 |
| 28 | Generate → Execute | 把需求貼給 Agent、看差異、執行 | 要貼的**那一句話**、要檢查的東西（有沒有 `def`、`for`、`input`）、執行指令、**預期輸出**（實際執行過）、沒有額度的備案 |
| 29 | Audit → Iterate | 逐項稽核，挑一個問題修正 | 表格：**稽核問題 ＋ 具體動作 ＋ 應該是什麼**；修正三步驟；一個真實的修正例子（`72.33333333333333` → 一位小數） |
| 30 | 練習：邊界值 | 先預測，再用 `practice.py` 驗證 | 「照著做」示範（題目不同）、灰色斜體提示、不收回 |
| 31 | 練習解答（hostOnly） | 對答案 | 學員網站不含；說明為什麼只有邊界值測得出 `>=` 與 `>` 的差別 |

### 為什麼有效

1. **一條線串到底**：同一份資料（王小明的成績單）、同一個檔案（`grades.py`）、同一份驗收標準，從第 27 頁寫下，第 28 頁比對輸出，第 29 頁逐組驗證，第 30 頁再加邊界值。學員不用每頁重新理解情境。
2. **前一頁的產出就是下一頁的輸入**：`spec.txt` → 提示骨架 → Agent 的程式 → 預期輸出 → 稽核表。頁面上直接寫「第 27 頁」「第 29 頁用」，學員知道現在做的事會用在哪裡。
3. **每一步都有具體動作，不是抽象口號**：不寫「檢查型別」，而是「在檔案最後加 `print(type(chinese))`，存檔再執行」。不寫「驗證數字」，而是「把變數改成表格的數字，一組一組執行」。
4. **先決定標準答案，再執行**：驗收標準（給這組數字，應該印出什麼）在第 27 頁、程式還沒寫的時候就先寫好，學員才有東西可以比對，也才分得清「跑完」和「正確」。
5. **回答「為什麼要做這步」**：每個步驟下方一行灰色小字（例如「沒有 `input()` 也要寫型別：沒寫，Agent 可能把成績存成 `"80"`」），消除學員心中的疑問，不用等講師口頭補。
6. **給「骨架」而不是空白頁**：提示骨架把三個步驟組合成一個完整提示，寫不出來的人照著填。
7. **預期輸出與表格都是實際執行過的**，學員比對時不會被不存在的輸出誤導。
8. **有備案**：沒有 Agent 額度時，從第 28 頁第 3 步用講師提供的 `materials/grades.py` 繼續，學習目標不受影響。
9. **邊界值留給最後的練習**：前面三組是一般情況，邊界值（剛好 60、剛好 0.8）單獨拉出來練習，讓學員親眼看到「`>=` 寫成 `>` 才測得出來」。

### 設計模式（之後做其他實作可以照用）

- 一個實作 ＝ 3 頁引導（Specify／Generate→Execute／Audit→Iterate）＋ 1 頁獨立練習＋ 1 頁 hostOnly 解答。需要資料檔時，最前面再加 1 頁「先拿到資料檔」（範例見單元 06、07 的第 22 頁；規則見 `demo-and-practice` §3b）。
- 每頁固定結構：**編號步驟 → 一行為什麼 → 範本或預期結果**。
- 一個頁面只出現一個新檔案或一個新動作（`spec.txt`、`grades.py`、`practice.py`）。
- 任何「寫需求」的步驟，都附上提示骨架與一組可以直接抄的範例。
- 引導要具體到「輸入什麼指令、改哪一行、輸出應該長怎樣」。

### 第 27 頁原始碼（骨架版型）

其他頁的原始碼請直接看 `05-variables-types-expressions/slides.md` 的「實作 2／3」「實作 3／3」「練習：邊界值」。

````markdown
<div class="eyebrow">06 · 資料模型</div>

# 實作 1／3：Specify（說明需求）

<div class="task-meta">
  <b>任務</b><span>為「學生成績單」寫一份需求，<strong>先不要寫程式</strong>。寫在 VS Code 的新檔案 <code>spec.txt</code>。</span>
</div>

<div class="steps mt-2" style="font-size:17px; gap:6px">
  <div><span class="num">1</span><strong>欄位與型別</strong>：<code>name</code> <code>student_id</code> 是 <code>str</code>；<code>chinese</code> <code>english</code> <code>math</code> 是 <code>int</code>（0–100）；<code>attendance</code> 是 <code>float</code>（0–1）
  <div style="font-size:15px; color:var(--muted-text); text-indent:0; margin-top:2px">沒有 <code>input()</code> 也要寫型別：程式裡每個值都有型別。沒寫，Agent 可能把成績存成 <code>"80"</code>（字串，算不出平均），或把出席率寫成 <code>85</code>（規則 ≥ 0.8 永遠成立）。</div></div>
  <div><span class="num">2</span><strong>規則</strong>：<code>average</code> ＝ 三科平均；<code>passed</code> ＝ 平均 ≥ 60 <strong>而且</strong>出席率 ≥ 0.8
  <div style="font-size:15px; color:var(--muted-text); text-indent:0; margin-top:2px">「≥」還是「&gt;」、「而且」還是「或」，都要寫出來，Agent 不會替你猜對。</div></div>
  <div><span class="num">3</span><strong>驗收標準</strong>：先決定「給這組數字，應該印出什麼」，至少三組
  <div style="font-size:15px; color:var(--muted-text); text-indent:0; margin-top:2px">驗收標準＝程式寫好後，拿來比對的標準答案。先寫，執行時才有東西可以比（第 29 頁用）。</div></div>
</div>

<table class="compact mt-2" style="font-size:16px">
<thead><tr><th>國文／英文／數學</th><th>出席率</th><th>應該印出：平均</th><th>應該印出：及格</th></tr></thead>
<tbody>
<tr><td>80／72／65</td><td>0.85</td><td>72.33…</td><td><code>True</code></td></tr>
<tr><td>50／50／50</td><td>1.0</td><td>50.0</td><td><code>False</code>（分數不夠）</td></tr>
<tr><td>80／80／80</td><td>0.5</td><td>80.0</td><td><code>False</code>（出席率不夠）</td></tr>
</tbody>
</table>

<div class="src">剛好等於門檻的邊界值（平均 60、出席率 0.8），留到第 30 頁練習。</div>
````

---

## 範例 6：實作的思考流程「問題 → 分工 → 每個部分做什麼 → 四個檢查點」（單元 09 第 26–30 頁）⭐ 講師指定的規則

**概念**：在寫需求之前，先帶學員想三件事：**我們想知道什麼？怎麼分工？每個部分該做什麼？** 這三步剛好就是單元 01 的 Prompt 四個檢查點的前兩點（① 目標、② 輸入與輸出），Specify 頁只要補上 ③ 限制、④ 驗收。規則全文在 `demo-and-practice` §3c，適用單元 09–14（單元 05–08 仍用範例 5）。

### 全貌

| 頁 | 標題 | 學員做什麼 | 對應檢查點 |
|---|---|---|---|
| 26 | 實作 1／5：資料在手，我們想知道什麼？ | 拿到 `grades.csv`，讀兩個用白話寫的問題：全班數學、國文平均？誰及格？ | ① 目標 |
| 27 | 實作 2／5：怎麼分工？把問題拆成函式 | 看拆解圖：問題 ① → `subject_average()`；問題 ② → `passed_names()` → `is_passed()` → `average()`；提示框給四個函式名 | （思考） |
| 28 | 練習：每個函式該做什麼？ | 在表格打字：每個函式「做什麼（一句話）」「交回什麼」，第一列是示範 | ② 輸入與輸出 |
| 29 | 練習解答（hostOnly） | 對答案 | |
| 30 | 實作 3／5：Specify（用四個檢查點寫需求） | 骨架【目標】【輸入與輸出】【限制】【驗收】寫成 `spec.txt` | ③ 限制、④ 驗收 |
| 31 | 實作 4／5：Generate → Execute | 貼提示詞（點名四個函式）、看差異、執行 | |
| 32 | 實作 5／5：Audit → Iterate | 稽核表：資料抄對了嗎、兩個問題答對了嗎…… | |

### 為什麼有效

1. **從問題出發，不是從程式出發**：學員先說得出「要回答什麼」，才知道需要哪些函式；不會一開始就叫 Agent「寫一個程式」。
2. **分工圖讓「一個函式只做一件事」變成看得見的動作**：由上往下拆（要知道誰及格 → 要一個一個判斷 → 判斷前要先算平均），由下往上組。
3. **提示給名字，練習給責任**：函式名由講師給（之後會出現在提示詞與答案程式裡，必須一致）；「做什麼、交回什麼」留給學員寫，這正是需求裡最容易漏掉的部分。
4. **把思考接回已經學過的框架**：每頁都說出這是四個檢查點的哪一點，Specify 頁的四個步驟名稱與單元 01 一字不差，學員不用學新的骨架。
5. **練習的「想一想」直接變成限制**：空資料時 `subject_average` 該交回什麼？→ Specify 的限制「空資料回傳 None」。

### 注意事項

- 問題用白話寫（「誰及格？」），不要寫成程式（「寫 passed_names」）。
- 拆出來的部分必須和答案程式完全一致（名字、參數）。答案程式沒有函式時（單元 12、14 的主程式），改拆成**步驟**（讀檔 → 計算 → 存檔），不要發明程式裡沒有的函式。
- 練習表第一列一定先填好當示範；提示文字一行內，以「……」結尾。

### 原始碼（第 26–30 頁）

Generate／Audit 兩頁的原始碼請直接看 `09-functions-scope-clean-code/slides.md` 的「實作 4／5」「實作 5／5」。

````markdown
<div class="eyebrow">05 · 實作</div>

# 實作 1／5：資料在手，我們想知道什麼？

<div class="grid grid-cols-[1.1fr_1fr] gap-5 mt-1 items-start">
<div>

<div class="muted" style="font-size:17px"><strong>資料</strong>：<code>grades.csv</code>，單元 08 已放進資料夾（沒有：點 <code>materials/grades.csv</code> 下載，放進 VS Code 開著的資料夾）。內容應該是：</div>

```text
name,student_id,chinese,english,math
王小明,S1001,80,72,65
林小華,S1002,92,88,95
陳小美,S1003,65,70,58
張小強,S1004,45,50,52
李小雅,S1005,78,85,90
```

</div>
<div class="flex flex-col gap-3" style="font-size:18px">
  <div class="node node--primary"><strong>問題 ①</strong><small>全班的<strong>數學平均</strong>和<strong>國文平均</strong>各是多少？</small></div>
  <div class="node node--primary"><strong>問題 ②</strong><small><strong>誰及格？</strong>（三科平均 ≥ 60 才及格，剛好 60 也算）</small></div>
  <div class="node node--secondary"><strong>這就是四個檢查點的 ① 目標</strong><small>先說清楚「要回答什麼」，再想怎麼寫</small></div>
</div>
</div>

<div class="takeaway mt-3">先別急著叫 Agent 寫。<strong>問題想清楚，才知道要哪些函式。</strong></div>

<!--
★ 實作的起點是問題，不是程式。資料和單元 08 相同（grades.csv，5 位），分數是數字。四個檢查點（目標、輸入與輸出、限制、驗收）是單元 01 學過的寫 Prompt 方法，這個實作照順序走一次：這頁是 ① 目標，下兩頁想出 ② 輸入與輸出，Specify 頁補上 ③ 限制 和 ④ 驗收。
-->

---

<div class="eyebrow">05 · 實作</div>

# 實作 2／5：怎麼分工？把問題拆成函式

<svg viewBox="0 0 900 270" style="width:100%; max-height:270px" class="mt-1">
  <defs><marker id="ahd" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="var(--muted-text)"/></marker></defs>
  <rect x="20" y="20" width="390" height="56" rx="10" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="215" y="55" text-anchor="middle" style="font-size:20px" font-weight="700">問題 ① 全班數學、國文平均</text>
  <rect x="490" y="20" width="390" height="56" rx="10" fill="var(--soft-amber)" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="685" y="55" text-anchor="middle" style="font-size:20px" font-weight="700">問題 ② 誰及格</text>
  <path d="M215 80 V118" stroke="var(--muted-text)" stroke-width="2.5" marker-end="url(#ahd)"/>
  <path d="M685 80 V118" stroke="var(--muted-text)" stroke-width="2.5" marker-end="url(#ahd)"/>
  <rect x="40" y="122" width="350" height="56" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2.5"/>
  <text x="215" y="157" text-anchor="middle" style="font-size:20px" font-family="JetBrains Mono, Consolas, monospace" font-weight="700">subject_average()</text>
  <text x="215" y="205" text-anchor="middle" style="font-size:17px; fill:var(--muted-text)">呼叫兩次：一次 "math"、一次 "chinese"</text>
  <rect x="510" y="122" width="350" height="56" rx="10" fill="var(--soft-blue)" stroke="var(--primary)" stroke-width="2.5"/>
  <text x="685" y="157" text-anchor="middle" style="font-size:20px" font-family="JetBrains Mono, Consolas, monospace" font-weight="700">passed_names()</text>
  <path d="M685 182 V202" stroke="var(--muted-text)" stroke-width="2.5" marker-end="url(#ahd)"/>
  <rect x="510" y="206" width="160" height="50" rx="10" fill="var(--soft-teal)" stroke="var(--secondary)" stroke-width="2"/>
  <text x="590" y="238" text-anchor="middle" style="font-size:18px" font-family="JetBrains Mono, Consolas, monospace" font-weight="700">is_passed()</text>
  <path d="M674 231 H696" stroke="var(--muted-text)" stroke-width="2.5" marker-end="url(#ahd)"/>
  <rect x="700" y="206" width="160" height="50" rx="10" fill="var(--soft-teal)" stroke="var(--secondary)" stroke-width="2"/>
  <text x="780" y="238" text-anchor="middle" style="font-size:18px" font-family="JetBrains Mono, Consolas, monospace" font-weight="700">average()</text>
</svg>

<div class="grid grid-cols-2 gap-4 mt-2" style="font-size:17px">
  <div class="node node--primary"><strong>提示：四個函式就夠</strong><small><code>average()</code>、<code>is_passed()</code>、<code>subject_average()</code>、<code>passed_names()</code></small></div>
  <div class="node node--primary"><strong>由上往下拆，由下往上組</strong><small>要知道誰及格 → 要一個一個判斷 → 判斷前要先算平均</small></div>
</div>

<div class="takeaway mt-3">拆到<strong>每個函式一句話說得完</strong>為止（Clean Code 的「只做一件事」）。</div>

<!--
★ 用問句帶：「問題 ② 誰及格，要先知道什麼？」→ 每一位有沒有及格（is_passed）→ 要先算出這一位的平均（average）。箭頭的意思是「會用到」：passed_names 裡面呼叫 is_passed，is_passed 裡面呼叫 average。問題 ① 只要一個函式，因為數學和國文是同一件事，只差科目，所以把科目做成參數 subject，呼叫兩次。這就是 04 段「一個函式只做一件事」用在真的問題上。
-->

---

<div class="eyebrow">05 · 實作 · 練習</div>

# 練習：每個函式該做什麼？

<style>
.slidev-layout table.tight td.blank { height: 28px; }
</style>

<div class="muted" style="font-size:17px; margin-bottom:4px">每個函式用<strong>一句話</strong>說它做什麼，再寫它<strong>交回什麼</strong>。第一列是示範。這張表就是四個檢查點的 <strong>② 輸入與輸出</strong>。</div>

<table class="fill tight">
<thead><tr><th style="width:36%">函式（括號裡是輸入）</th><th>做什麼（一句話）</th><th style="width:24%">交回什麼</th></tr></thead>
<tbody>
<tr><td><code>average(student)</code></td><td>算一位學生的三科平均</td><td>一個小數（float）</td></tr>
<tr><td><code>is_passed(student, line=60)</code></td><td class="blank"><FillIn id="split.passed-do" hint="例：判斷……" /></td><td class="blank"><FillIn id="split.passed-ret" hint="例：……" /></td></tr>
<tr><td><code>subject_average(students, subject)</code></td><td class="blank"><FillIn id="split.subject-do" hint="例：算全班……" /></td><td class="blank"><FillIn id="split.subject-ret" /></td></tr>
<tr><td><code>passed_names(students)</code></td><td class="blank"><FillIn id="split.names-do" /></td><td class="blank"><FillIn id="split.names-ret" /></td></tr>
</tbody>
</table>

<FillClear group="split" />

<div class="takeaway mt-3">想一想：<code>subject_average([], "math")</code> 遇到<strong>沒有學生</strong>時，應該交回什麼？</div>

<!--
★ 目標：在叫 Agent 寫之前，自己先決定每個函式的輸入、做什麼、輸出。這張表會直接放進 spec.txt。注意 student（一位）和 students（全班）只差一個 s，意思完全不同。最後一行問題留給 Specify 頁的限制：空資料時回傳 None，不要除以零（單元 08 的 ZeroDivisionError）。給 5 分鐘，不收回。答案在下一頁，學員網站不含。
-->

---
hostOnly: true
---

<div class="eyebrow">05 · 實作 · 練習解答</div>

# 練習：每個函式該做什麼？

<table class="fill tight">
<thead><tr><th style="width:36%">函式（括號裡是輸入）</th><th>做什麼（一句話）</th><th style="width:24%">交回什麼</th></tr></thead>
<tbody>
<tr><td><code>average(student)</code></td><td>算一位學生的三科平均</td><td>float</td></tr>
<tr><td><code>is_passed(student, line=60)</code></td><td>判斷這一位的平均是否 ≥ line（用 <code>average</code>）</td><td>bool（True／False）</td></tr>
<tr><td><code>subject_average(students, subject)</code></td><td>算全班某一科的平均</td><td>float；沒有學生時 <code>None</code></td></tr>
<tr><td><code>passed_names(students)</code></td><td>挑出及格的人的名字（用 <code>is_passed</code>）</td><td>名字的 list</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">分辨方法：<strong>一位</strong>（student）的算個人，<strong>全班</strong>（students）的算整班或挑名單。</div>

<!--
★ 說法不必一字不差。交回什麼一定要寫對型別，因為 Specify 和 docstring 的 Returns 都會用到。空資料回傳 None 是本課的決定，單元 10 會再討論。
-->

---

<div class="eyebrow">05 · 實作</div>

# 實作 3／5：Specify（用四個檢查點寫需求）

<div class="task-meta">
  <b>任務</b><span>把前面三頁寫成需求，存成 <code>spec.txt</code>。<strong>先不要寫程式</strong>。骨架：【目標】【輸入與輸出】【限制】【驗收】</span>
</div>

<div class="steps mt-2" style="font-size:17px; gap:5px">
  <div><span class="num">1</span><strong>目標</strong>：回答兩個問題：全班數學、國文平均；誰及格（三科平均 ≥ 60）</div>
  <div><span class="num">2</span><strong>輸入與輸出</strong>：把 <code>grades.csv</code> 的 5 位照抄進 <code>students.py</code>（分數是數字）；四個函式照練習表；印出下表四行</div>
  <div><span class="num">3</span><strong>限制</strong>：每個函式用 <code>return</code>、有 Google 格式 docstring；不改傳進來的 <code>students</code>；空資料回傳 <code>None</code>；只用 <code>for</code>、<code>if</code>
  <div style="font-size:15px; color:var(--muted-text); text-indent:0; margin-top:2px">不要寫讀檔程式（<code>open</code>），也不要改 <code>grades.csv</code>；讀檔是單元 12。</div></div>
  <div><span class="num">4</span><strong>驗收</strong>：先決定「應該印出什麼」（下表）</div>
</div>

<table class="compact mt-2" style="font-size:16px">
<thead><tr><th>印出的項目</th><th>應該是</th><th>印出的項目</th><th>應該是</th></tr></thead>
<tbody>
<tr><td>全班數學平均</td><td>72.0</td><td>及格名單</td><td>王小明、林小華、陳小美、李小雅</td></tr>
<tr><td>全班國文平均</td><td>72.0</td><td>空資料的數學平均</td><td>None（不除以零）</td></tr>
</tbody>
</table>

<div class="src">表中數字為本機 Python 3.12 實測講師版程式（資料同 grades.csv）；數學與國文總分都是 360，除以 5 得 72.0。</div>

<!--
★ Specify。四個檢查點照順序：① 目標（實作 1）、② 輸入與輸出（實作 2 與練習表）、③ 限制、④ 驗收。學員在 VS Code 新增 spec.txt，不用繳交。驗收標準先寫，才分得出「跑完」和「正確」。數學 65+95+58+52+90、國文 80+92+65+45+78 都是 360，剛好都是 72.0，可以請學員心算。只有張小強不及格（平均 49.0）。
-->
````

---

## 這些範例共同的設計原則

- **一頁一個概念**，用一個貫穿的比喻（盒子）連到後面的頁面。
- **用中文白話解釋程式碼**（範例 4）：每個關鍵字配一個中文口語說法，非常有幫助。
- **實作先想問題與分工**（範例 6，單元 09 起）：問題 → 分工 → 每個部分做什麼 → 四個檢查點。
- **實作練習要帶著做**（範例 5）：每一步都有具體動作、為什麼、預期結果；前一頁的產出是下一頁的輸入。
- **先看圖，再看程式碼，最後一句結論**，三者使用同一組數字。
- **把「動作」畫出來**：箭頭、劃掉、編號，讓學員看見變化的過程，而不是只看到結果。
- **直接點出常見誤解**（`=` 不是等號），並在講師備註寫出怎麼講。
- **版面**：灰色說明文字 18px、圖寬 100%、`max-height` 控制高度，整頁在 1280×720 內不溢出；投影和筆電螢幕上都要看得清楚。
- **畫完一定要實際渲染檢查**（`npm run dev` 或截圖），確認沒有文字重疊、超出框、被截掉。

## 新增範例的方式

講師說某一頁「學員很好懂」時，把它加進這份檔案：概念、為什麼有效、注意事項、可複製的原始碼。

## 本課程範例

（尚無。講師說某頁「學員很好懂」時加入：概念、為什麼有效、注意事項、可複製的原始碼。）
