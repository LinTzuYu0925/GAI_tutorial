---
theme: default
title: 雲端 API 還是自架模型
info: |
  生成式AI原理 · L19
  資訊部和法務要決定客服單分流用雲端 API 還是自架開放模型：同一個 JSON 分流任務做三次（Gemini API、Qwen fp16、Qwen 4-bit），比成本、延遲、品質、個資與授權。
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
exportFilename: 19-api-vs-self-host
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · L19</div>

# 雲端 API 還是自架模型

<p class="subtitle">同一個客服單分流任務做三次：Gemini API、Qwen fp16、Qwen 4-bit，用數字填決策表</p>

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-8">
  <span class="chip">決策表</span><span class="arrow">→</span>
  <span class="chip">SDK 呼叫</span><span class="arrow">→</span>
  <span class="chip">usage → 成本</span><span class="arrow">→</span>
  <span class="chip">JSON 驗證＋重試</span><span class="arrow">→</span>
  <span class="chip">transformers generate</span><span class="arrow">→</span>
  <span class="chip">4-bit 量化</span><span class="arrow">→</span>
  <span class="chip">分流助理</span>
</div>

<!--
★ 開場（2 分）：L02 呼叫過一次 API。今天要回答真實的採購問題：同樣的工作，交給雲端還是自己跑？答案不是技術偏好，是一張有數字的表。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 資訊部／法務：客服單分流要用雲端 API 還是自架？

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #L19】部門：資訊部／法務<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>客服單自動分類（類別、緊急程度、摘要）要用雲端 API 還是自架開放模型？</dd>
    <dt>現況痛點</dt><dd>法務擔心個資外流；資訊部擔心成本與延遲</dd>
    <dt>成功指標（KPI）</dt><dd>每 1,000 張的成本、每張秒數、分類正確率；有效 JSON 比例</dd>
    <dt>可用資料</dt><dd>40 張合成繁中客服單（附正確類別、緊急程度）</dd>
    <dt>限制與法規</dt><dd>個資法、資料存放地區；免費方案的輸入可能被拿去改進模型；開放權重的授權依大小不同</dd>
    <dt>為何現有工具不夠</dt><dd>L02 只做過一次呼叫，沒有比較，也沒有結構化輸出</dd>
  </dl>
</div>

<!--
★ 需求單（3 分）：合成資料是今天能放心送到雲端的前提。強調 KPI 有四個面向，不只是「哪個比較準」。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **讀懂**一次 SDK（軟體開發套件：官方提供的 Python 函式庫）呼叫：model、系統提示詞、輸入、max_output_tokens，以及回傳的 usage
2. **算出**每 1,000 張客服單的成本（雲端用 usage、自架用秒數 × GPU 租金）
3. **要求** JSON 輸出，用 <code>json.loads</code> 驗證，失敗就重試
4. **用** <code>transformers</code> 和 chat template 自架同一個任務，並載入 4-bit 版本
5. **填寫**開放 vs 封閉模型的決策表

<div class="takeaway mt-4">今天的分流助理就是第五天要交付（Ship）的作品。</div>

<!--
★ 目標（1 分）。不教（Agent 模組）：串流、schema 強制輸出（structured outputs）、tool calling、MCP。只認名字：Ollama／GGUF、NF4／GPTQ／AWQ。
-->

---

<div class="eyebrow">00 · Frame · 一把尺</div>

# 決策表：五個欄位，今天結束時填滿

<table class="mt-2" style="font-size:18px">
<thead><tr><th style="width:18%">準則</th><th>雲端 API</th><th>自架開放模型</th></tr></thead>
<tbody>
<tr><td><b>成本</b></td><td>按 token 付費，用多少付多少</td><td>按 GPU 時數付費，閒著也要付</td></tr>
<tr><td><b>個資</b></td><td>資料送出公司；看服務條款與存放地區；<b>免費額度的輸入可能被拿去改進產品</b></td><td>資料不出公司</td></tr>
<tr><td><b>授權</b></td><td>服務條款</td><td>模型卡的 license，<b>同一家族不同大小可能不同</b></td></tr>
<tr><td><b>延遲</b></td><td>網路往返＋排隊</td><td>看你的 GPU</td></tr>
<tr><td><b>品質</b></td><td>通常較強的大模型</td><td>T4 放得下的小模型</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">每一格都要有證據：成本、延遲、品質用 lab 量，個資、授權讀條款。</div>

<!--
★ Frame（4 分）：先讓學員憑直覺在心裡選一邊，下課前用 lab 的數字再選一次，看有沒有改變。這張表的格式來自 L01 的價值地圖：每個主張都要有證據。
-->

---

<div class="eyebrow">01 · Try（先看結果）· SDK 呼叫</div>

# 一次 SDK 呼叫長什麼樣子

```python
it = client.interactions.create(
    model="gemini-3.5-flash-lite",              # 用哪個模型（有免費額度）
    system_instruction=SYSTEM,                  # 系統提示詞：角色、格式規則
    input=ticket_text,                          # 這張客服單
    generation_config={"max_output_tokens": 1024},   # 回覆最多幾個 token
)
print(it.output_text)                           # 模型的文字回覆
print(it.usage.total_input_tokens, it.usage.total_output_tokens)   # 這次用了多少 token
```

<div class="grid grid-cols-2 gap-5 mt-2" style="font-size:17px">
<div class="node"><strong>金鑰從哪來</strong><small>到 Google AI Studio 申請免費金鑰；Colab 的「🔑 密鑰」或 <code>.env</code>（Vibe 11–12），SDK 自動讀 <code>GEMINI_API_KEY</code>；不要寫進程式</small></div>
<div class="node node--warm"><strong>免費額度的代價</strong><small>有每分鐘／每天的請求上限（被擋就等一下再試）；輸入可能被拿去改進產品，所以只送合成資料。新版 Gemini 會忽略 <code>temperature</code>；開放模型（今天的 Qwen）還是用溫度</small></div>
</div>

<div class="takeaway mt-2">一次呼叫＝模型＋系統提示詞＋這張單；回來的 usage 就是帳單（付費層才真的收費）。</div>

<!--
★ SDK 剖析（6 分）：一行一行讀：model、system_instruction、input、max_output_tokens。output_text 是模型的文字；usage 是 token 計數，付費層就是帳單的依據。
免費額度不收錢，但有限流、輸入可能被拿去改進產品（S2）；所以成本欄用「若改付費層」的單價換算。temperature 被忽略是新版模型的事（S2），昨天學的溫度概念沒有過時：開放模型還有。
SDK 的呼叫形式（interactions.create）依官方文件（S1），講師 2026-11-27 已在 Colab T4 跑過整本，呼叫形式可用（金鑰設定見筆記本第 1 部分）。
-->

---

<div class="eyebrow">01 · Try · usage → 成本</div>

# 從 usage 算每 1,000 張的成本

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2 items-start" style="font-size:18px">
<div>

**照著算（token 數是假設的例子）**

- 每張平均：輸入 300 token（系統提示詞＋客服單）、輸出 60 token
- <code>gemini-3.5-flash-lite</code> 付費層：輸入 0.30、輸出 2.50 美元／百萬 token
- 每張 ＝ 300 × 0.30 ÷ 10⁶ ＋ 60 × 2.50 ÷ 10⁶ ＝ 0.00024 美元
- 每 1,000 張 ≈ **0.24 美元**；每天 2,000 張、一個月約 **14.4 美元**（免費額度內是 0，但有上限、輸入會被再利用）

</div>
<div class="node node--primary"><strong>三個常被忘記的地方</strong><small>① 系統提示詞每次都要送，每張都算一次<br>② 模型的內部思考也算輸出 token<br>③ 重試一次就多付一次<br>→ 所以要用 lab 量到的 usage 平均，不要用估的</small></div>
</div>

<div class="takeaway mt-3">成本 ＝ usage × 單價：L17 的算式，換成 API 直接回報的 token 數。</div>

<div class="src">單價：Google AI Studio 價格頁（2026-11-26 讀取，S3）；上線前請再查一次</div>

<!--
★ 成本（5 分）：和 L17 的差別：L17 用 tokenizer 自己數，今天用 API 回傳的 usage，包含系統提示詞和思考。免費額度不收錢，但成本欄要寫「若改付費層」的單價，否則自架的比較沒有意義。lab 裡可以換成別的 Gemini 模型：便宜的是否夠準，要量。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）· JSON</div>

# JSON：在提示詞裡要求，用 json.loads 驗證，失敗就重試

<div class="grid grid-cols-[1.15fr_1fr] gap-5 mt-1">
<div>

```python
def parse_reply(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        d = json.loads(text)                 # 不是 JSON → 例外
    except json.JSONDecodeError:
        return None
    if not isinstance(d, dict) or d.get("category") not in CATEGORIES:
        return None                          # 類別不在清單 → 不收
    if d.get("urgency") not in URGENCY:      # 緊急程度不在清單 → 不收
        return None
    return d
```

</div>
<div style="font-size:17px">

- **提示詞**：寫清楚格式與可填的值
- **解析**：<code>json.loads</code> 讀作「照 JSON 規則變成 dict，不合就丟例外」
- **檢查**：欄位齊、值在清單
- **重試**：不合格再問（最多 2 次）

</div>
</div>

<div class="takeaway mt-2">模型給的是「看起來像 JSON 的文字」：驗證，不要相信。</div>

<!--
★ JSON（6 分）：常見誤解：「提示詞說了只輸出 JSON，它就一定會」。小模型常加上 ```json 圍欄、說明文字、單引號，或發明清單外的類別（例如把「退換貨」寫成「退貨」）。
schema 強制輸出（structured outputs）能從 API 端保證格式，留到 Agent 模組。
-->

---

<div class="eyebrow">02 · Open · JSON · 練習</div>

# 練習：這四個回覆，parse_reply 會不會接受？

<div class="grid grid-cols-[1fr_1.5fr] gap-5 mt-1" style="font-size:17px">
<div class="node"><strong>照著做</strong><small><code>{"category": "帳號", "urgency": "高", "summary": "帳號被盜"}</code><br>→ 雙引號、欄位齊、帳號在清單、高在清單 → <b>接受</b></small></div>
<div>

<table class="fill tight vlines">
<thead><tr><th>模型回覆</th><th style="width:22%">接受？</th></tr></thead>
<tbody>
<tr><td><code>{"category": "維修", "urgency": "高", "summary": "手錶充電發燙"}</code></td><td class="blank"><FillIn id="parse.a" hint="例：接受／拒絕，因為……" /></td></tr>
<tr><td><code>```json</code> 包住的 <code>{"category": "物流", …}</code></td><td class="blank"><FillIn id="parse.b" /></td></tr>
<tr><td><code>{'category': '帳單', 'urgency': '高', …}</code>（單引號）</td><td class="blank"><FillIn id="parse.c" /></td></tr>
<tr><td><code>{"category": "退貨", "urgency": "低", …}</code></td><td class="blank"><FillIn id="parse.d" /></td></tr>
</tbody>
</table>

<div class="muted" style="font-size:15px">「…」代表其他欄位都正確</div>

<FillClear group="parse" />

</div>
</div>

<div class="muted mt-2" style="font-size:16px">做完後：lab 第 0 部分會印出這四個的結果，對一下。</div>

<!--
★ 練習（7 分）：個人、不收回。關鍵發現：單引號在 Python 是合法的 dict，但不是合法的 JSON；「退貨」看起來對，卻不在我們的類別清單。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · JSON · 練習解答</div>

# 練習解答：兩個接受、兩個拒絕

<table class="vlines" style="font-size:18px">
<thead><tr><th>回覆</th><th style="width:14%">結果</th><th>為什麼</th></tr></thead>
<tbody>
<tr><td>維修／高</td><td>接受</td><td>格式、欄位、值都對</td></tr>
<tr><td>```json 圍欄</td><td>接受</td><td><code>parse_reply</code> 先去掉圍欄再解析</td></tr>
<tr><td>單引號</td><td>拒絕</td><td>JSON 規定雙引號；<code>json.loads</code> 丟例外</td></tr>
<tr><td>退貨</td><td>拒絕</td><td>能解析，但「退貨」不在類別清單（應是「退換貨」）</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：lab 第 0 部分印出「接受、接受、拒絕、拒絕」。</div>

<!--
★ 解答（2 分）：第 4 個最危險：如果沒有檢查清單，錯的類別會被當成正確資料寫進系統。
-->

---

<div class="eyebrow">02 · Open · 自架</div>

# 自架：transformers 的 generate ＋ chat template

```python
m = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": ticket_text}]
ids = tok.apply_chat_template(m, add_generation_prompt=True,
                              return_tensors="pt", return_dict=True).to(model.device)
out = model.generate(**ids, max_new_tokens=120, do_sample=False)
reply = tok.decode(out[0, ids["input_ids"].shape[1]:], skip_special_tokens=True)
```

<div class="grid grid-cols-3 gap-4 mt-2" style="font-size:16px">
<div class="node"><strong>chat template（對話範本）</strong><small>把 system／user 包成模型訓練時看過的格式（特殊 token 標出誰在說話）</small></div>
<div class="node"><strong>generate</strong><small>就是 L18 的接龍迴圈；<code>do_sample=False</code>＝每次選機率最高的（貪婪）</small></div>
<div class="node"><strong>decode</strong><small>切掉提示詞那一段，只留新生成的文字</small></div>
</div>

<div class="takeaway mt-2">雲端和自架用同一個系統提示詞、同一個 <code>parse_reply</code>：比較才公平。</div>

<!--
★ 自架（5 分）：lab 第 2 部分會印出套完範本的樣子，讓學員看到 &lt;|im_start|&gt;system 這種特殊標記。明天 L20 的微調資料也要用同一個範本，否則模型學到的格式和用的時候不一樣。
-->

---

<div class="eyebrow">02 · Open · 量化</div>

# 量化（quantization）：每個權重用更少的位元

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2 items-center">
<div>

<svg viewBox="0 0 400 170" style="width:100%" aria-label="一把尺上只有 16 個刻度；連續的權重值被移到最近的刻度上">
  <line x1="20" y1="80" x2="380" y2="80" stroke="var(--text)" stroke-width="2"/>
  <g stroke="var(--primary)" stroke-width="2">
  <line x1="20" y1="68" x2="20" y2="92"/><line x1="44" y1="68" x2="44" y2="92"/><line x1="68" y1="68" x2="68" y2="92"/><line x1="92" y1="68" x2="92" y2="92"/><line x1="116" y1="68" x2="116" y2="92"/><line x1="140" y1="68" x2="140" y2="92"/><line x1="164" y1="68" x2="164" y2="92"/><line x1="188" y1="68" x2="188" y2="92"/>
  <line x1="212" y1="68" x2="212" y2="92"/><line x1="236" y1="68" x2="236" y2="92"/><line x1="260" y1="68" x2="260" y2="92"/><line x1="284" y1="68" x2="284" y2="92"/><line x1="308" y1="68" x2="308" y2="92"/><line x1="332" y1="68" x2="332" y2="92"/><line x1="356" y1="68" x2="356" y2="92"/><line x1="380" y1="68" x2="380" y2="92"/></g>
  <circle cx="103" cy="40" r="6" fill="var(--warm-accent)"/><line x1="103" y1="46" x2="94" y2="66" stroke="var(--warm-accent)" stroke-width="2"/>
  <circle cx="247" cy="40" r="6" fill="var(--warm-accent)"/><line x1="247" y1="46" x2="238" y2="66" stroke="var(--warm-accent)" stroke-width="2"/>
  <text x="20" y="125" style="font-size:16px" fill="var(--primary)">4 bit ＝ 2⁴ ＝ 16 個刻度</text>
  <text x="20" y="155" style="font-size:16px" fill="var(--warm-accent)">橘點：原本的權重 → 移到最近的刻度</text>
</svg>

</div>
<div>

<table style="font-size:18px">
<thead><tr><th>格式</th><th>每個權重</th><th>1.5B 模型</th></tr></thead>
<tbody>
<tr><td>fp32</td><td>4 bytes</td><td>6 GB</td></tr>
<tr><td>fp16</td><td>2 bytes</td><td>3 GB</td></tr>
<tr><td>4-bit</td><td>≈ 0.5 byte</td><td>≈ 0.75 GB</td></tr>
</tbody>
</table>
<div class="shot-cap">只算權重；實際 VRAM 還要加上 KV cache 和計算空間（lab 實測）</div>

</div>
</div>

<div class="takeaway mt-2">和 L08 的 VQ 同一招：「移到最近的刻度」；省下記憶體，換一些精度（多少，lab 量）。</div>

<!--
★ 量化（5 分）：L04 學過「參數量 × 每個參數幾 byte」的估算，今天只是把 byte 數變小。DL 課第 67–72 頁提過模型壓縮。真正的 4-bit 方法每一小組權重有自己的尺（縮放係數），所以誤差比一把共用的尺小。
-->

---

<div class="eyebrow">02 · Open · 量化 · 練習</div>

# 練習：7B 模型放得進 T4 嗎？

<div class="grid grid-cols-[1fr_1.4fr] gap-5 mt-1" style="font-size:17px">
<div class="node"><strong>照著做：1.5B</strong><small>fp16：1.5 × 2 ＝ 3 GB<br>4-bit：1.5 × 0.5 ≈ 0.75 GB<br>T4 可用約 15 GB → 都放得下</small></div>
<div>

<table class="fill tight vlines">
<thead><tr><th style="width:20%">模型</th><th>fp16 權重（GB）</th><th>4-bit 權重（GB）</th><th>T4 放得下哪個？</th></tr></thead>
<tbody>
<tr><td>7B</td><td class="blank"><FillIn id="vram.7f" hint="例：參數量 × 2……" /></td><td class="blank"><FillIn id="vram.74" /></td><td class="blank"><FillIn id="vram.7ok" /></td></tr>
<tr><td>14B</td><td class="blank"><FillIn id="vram.14f" /></td><td class="blank"><FillIn id="vram.144" /></td><td class="blank"><FillIn id="vram.14ok" /></td></tr>
</tbody>
</table>

<FillClear group="vram" />

</div>
</div>

<div class="muted mt-2" style="font-size:16px">提醒：權重之外還要留空間給 KV cache 和計算（L18）。</div>

<!--
★ 練習（7 分）：個人作業，和 L04 的 VRAM 練習同一個算法。發現：7B 在 fp16 剛好卡在邊緣（14 GB，沒空間給 KV cache），4-bit 就輕鬆放得下。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · 量化 · 練習解答</div>

# 練習解答：4-bit 讓 7B「放得下」

<table class="vlines" style="font-size:19px">
<thead><tr><th>模型</th><th>fp16</th><th>4-bit</th><th>T4（約 15 GB）</th></tr></thead>
<tbody>
<tr><td>7B</td><td>14 GB</td><td>≈ 3.5 GB</td><td>fp16 幾乎沒空間給 KV cache → 實務上用 4-bit</td></tr>
<tr><td>14B</td><td>28 GB</td><td>≈ 7 GB</td><td>只有 4-bit 放得下</td></tr>
</tbody>
</table>

<div class="takeaway mt-4">怎麼判斷：參數量（十億）× 每個權重幾 byte ＝ GB；再留幾 GB 給 KV cache 和計算。</div>

<!--
★ 解答（2 分）：實際 4-bit 檔案會比 0.5 byte × 參數量稍大：嵌入層、輸出層常保留較高精度。lab 量到的 VRAM 會說明這一點。
-->

---

<div class="eyebrow">03 · 延伸 · 講師示範</div>

# 筆電上跑：Ollama 與 GGUF

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:19px">
<div class="node"><strong>GGUF</strong><small>一種存放「已量化模型」的檔案格式，CPU 也能跑</small></div>
<div class="node node--secondary"><strong>Ollama</strong><small>在筆電上下載並執行 GGUF 模型的工具，一行指令就能對話；適合離線示範</small></div>
</div>

<div class="takeaway mt-4">同一個 4-bit 的想法，搬到筆電上：資料完全不出這台電腦。</div>

<!--
○ 示範（2 分）：講師筆電示範 `ollama run qwen2.5:1.5b`（課前先下載）。指令與版本待講師確認。學員不必操作。
-->

---

<div class="eyebrow">附錄 · 只認名字</div>

# NF4、GPTQ、AWQ：三種 4-bit 做法（選讀）

<div class="mt-4" style="font-size:19px">

- **NF4**（bitsandbytes）：刻度依常態分布排，載入時直接量化，不需要校準資料；今天的 lab 和明天的 QLoRA 用它
- **GPTQ**：用一小批校準資料，逐層找讓輸出誤差最小的量化方式
- **AWQ**：先找出最重要的權重（看激勵值 activation 的大小），保護它們再量化

</div>

<div class="takeaway mt-4">差別在「刻度怎麼排、要不要校準資料」；選哪個看部署工具支援什麼。</div>

<div class="src">S7（待確認）</div>

<!--
△ 附錄（1 分）：只認名字。看到模型名稱後面的 -GPTQ、-AWQ、-GGUF，知道是「已經量化好的版本」。
-->

---

<div class="eyebrow">04 · 交接</div>

# 留給 Agent 模組：串流、schema 強制輸出、tool calling

<div class="grid grid-cols-3 gap-4 mt-4" style="font-size:17px">
<div class="node"><strong>串流（streaming）</strong><small>邊生成邊顯示，降低使用者感覺到的等待</small></div>
<div class="node node--secondary"><strong>schema 強制輸出</strong><small>由 API 保證輸出符合 JSON schema（欄位與型別的規格），不必自己重試</small></div>
<div class="node node--primary"><strong>tool calling、MCP</strong><small>讓模型呼叫你的函式與外部系統</small></div>
</div>

<div class="takeaway mt-4">今天停在「提示詞要求 JSON ＋ 自己驗證」：先懂為什麼需要驗證，Agent 模組再用工具自動化。</div>

<!--
★ 交接（2 分）：課程地圖 §13：GAI 教到一次 SDK 呼叫、token 成本、JSON＋json.loads；Agent 模組 #3、#4 接手。今天自己寫的 parse_reply，就是之後那些功能在背後替你做的事。
-->

---

<div class="eyebrow">05 · Lab L5-3</div>

# Lab 1／7：我們要做出什麼？

<div class="grid grid-cols-2 gap-6 mt-2" style="font-size:18px">
<div>

**打開筆記本**：<code>lab19-triage.ipynb</code>（在 <code>materials/</code>）→ Open in Colab；執行階段：**T4 GPU**

1. 同一張客服單，三種做法分得一樣嗎？
2. 哪一種最常吐出壞掉的 JSON？
3. 每 1,000 張各要多少錢、多少秒？

</div>
<div>

<table class="vlines" style="font-size:14px;text-align:center">
<thead><tr><th></th><th>有效 JSON<br><small>重試後</small></th><th>類別</th><th>緊急</th><th>秒／張</th><th>VRAM</th><th>每千張</th></tr></thead>
<tbody>
<tr><td style="text-align:left">雲端 Gemini</td><td>100%</td><td>85%</td><td>78%</td><td>4.21</td><td>—</td><td>$0.12</td></tr>
<tr><td style="text-align:left">自架 fp16</td><td>100%</td><td>85%</td><td>60%</td><td>1.31</td><td>3.11 GB</td><td>$0.18</td></tr>
<tr><td style="text-align:left">自架 4-bit</td><td>100%</td><td>82%</td><td>55%</td><td>2.41</td><td>1.26 GB</td><td>$0.33</td></tr>
</tbody>
</table>
<div class="shot-cap">講師 T4 實跑（40 張合成客服單；自架成本假設 GPU 每小時 0.5 美元）</div>

</div>
</div>

<div class="muted mt-1" style="font-size:14px">Colab：<code>colab.research.google.com/github/LinTzuYu0925/GAI_tutorial/blob/day5-done/19-api-vs-self-host/materials/lab19-triage.ipynb</code></div>

<div class="takeaway mt-1">交付給資訊部和法務：填滿的決策表，加上你的建議與理由。</div>

<!--
★ Lab 開始（3 分）：沒有 API 金鑰的學員（Gemini 金鑰免費申請，但需要 Google 帳號）：第 1 部分自動跳過，用講師的數字填雲端那一欄（課堂上公布）。
-->

---

<div class="eyebrow">05 · Lab L5-3</div>

# Lab 2／7：筆記本拆成哪幾塊？

<div class="steps mt-2" style="font-size:18px">
  <div><span class="num">0</span><strong>共用</strong>：<code>SYSTEM</code> 提示詞、<code>parse_reply()</code>、<code>triage()</code>（呼叫＋驗證＋重試）、<code>evaluate()</code>（40 張）</div>
  <div><span class="num">1</span><strong>雲端</strong>：<code>cloud_generate()</code>（Gemini 免費額度）；<code>USAGE</code> 記錄每次 token；<code>cost_per_1000()</code></div>
  <div><span class="num">2</span><strong>自架 fp16</strong>：<code>Qwen/Qwen2.5-1.5B-Instruct</code>；<code>make_hf_generate()</code>；成本 ＝ 秒數 × GPU 租金</div>
  <div><span class="num">3</span><strong>自架 4-bit</strong>：同一個模型 ＋ <code>BitsAndBytesConfig(load_in_4bit=True)</code></div>
  <div><span class="num">4</span><strong>比較表</strong>，<span class="num" style="margin-left:6px">5</span><strong>Gradio</strong> 分流助理</div>
</div>

<div class="takeaway mt-3">三種做法都走同一個 <code>triage()</code>：只有「產生文字的函式」不同。</div>

<!--
★ 拆塊（3 分）：這是比較實驗的基本設計：控制變因（提示詞、驗證、資料）相同，只換一個東西。
-->

---

<div class="eyebrow">05 · Lab L5-3</div>

# Lab 3／7：Specify

<div style="font-size:18px" class="mt-2">

<strong>【目標】</strong>40 張合成客服單，三種做法各分類一次，填決策表<br>
<strong>【輸入與輸出】</strong>客服單文字 → 模型文字 → <code>parse_reply</code> → <code>&#123;category, urgency, summary&#125;</code> 或 None<br>
<strong>【限制】</strong>同一個 <code>SYSTEM</code>、同一個驗證；最多重試 2 次；只用合成資料；金鑰放 Colab 密鑰或 <code>.env</code>（GEMINI_API_KEY）<br>
<strong>【驗收】</strong>① 練習的四個例子：接受、接受、拒絕、拒絕　② 每種做法都有一列完整數字　③ 4-bit 的 VRAM 峰值比 fp16 低　④ 成本欄寫出你用的單價與 GPU 租金

</div>

<!--
★ Specify（3 分）：驗收門檻是課前定的。強調 ④：沒寫單價的成本數字，沒辦法拿去跟主管討論。
-->

---

<div class="eyebrow">05 · Lab L5-3</div>

# Lab 4／7：Generate → Execute

<PromptBox>
這是分流筆記本，請只填兩個 # TODO：<br>
① parse_reply()：先去掉 ```json 圍欄，再 json.loads；解析失敗、欄位不齊、category 或 urgency 不在清單，都回傳 None<br>
② cost_per_1000()：每張成本＝輸入 token × 輸入單價 ÷ 100 萬 ＋ 輸出 token × 輸出單價 ÷ 100 萬；再乘 1,000<br>
不要改 SYSTEM、CATEGORIES、資料。每一行加中文註解。
</PromptBox>

<div class="steps mt-2" style="font-size:17px">
  <div><span class="num">1</span>預期第 0 部分：四行「接受、接受、拒絕、拒絕」</div>
  <div><span class="num">2</span>沒有金鑰：印出「沒有金鑰：跳過第 1 部分」，繼續往下</div>
  <div><span class="num">3</span>沒有 Agent 額度：<code>parse_reply</code> 照 JSON 那一頁的程式；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ 執行（約 22 分，含下載 1.5B 模型約 3 GB）：時間待講師 T4 實跑後填入。最常見錯誤：忘了 return None，讓不合格的 dict 溜過去。
-->

---

<div class="eyebrow">05 · Lab L5-3</div>

# Lab 5／7：讀比較表

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

跑完第 4 部分後：

1. 「第一次就有效」和「重試後有效」差多少？重試值得嗎？
2. 4-bit 比 fp16 省多少 VRAM？正確率掉多少？
3. 自架每 1,000 張的成本，對 GPU 租金的假設有多敏感？

</div>
<div>

<table class="vlines" style="font-size:14px;text-align:center">
<thead><tr><th></th><th>有效 JSON<br><small>重試後</small></th><th>類別</th><th>緊急</th><th>秒／張</th><th>VRAM</th><th>每千張</th></tr></thead>
<tbody>
<tr><td style="text-align:left">雲端 Gemini</td><td>100%</td><td>85%</td><td>78%</td><td>4.21</td><td>—</td><td>$0.12</td></tr>
<tr><td style="text-align:left">自架 fp16</td><td>100%</td><td>85%</td><td>60%</td><td>1.31</td><td>3.11 GB</td><td>$0.18</td></tr>
<tr><td style="text-align:left">自架 4-bit</td><td>100%</td><td>82%</td><td>55%</td><td>2.41</td><td>1.26 GB</td><td>$0.33</td></tr>
</tbody>
</table>
<div class="shot-cap">講師 T4 實跑（40 張合成客服單；自架成本假設 GPU 每小時 0.5 美元）</div>

</div>
</div>

<div class="takeaway mt-3">看錯的單：第 4 部分列出 fp16 分錯的單（最多 5 張），判斷是模型錯，還是題目本來就模糊。</div>

<!--
★ 讀表（6 分）：講師實跑的數字課堂上公布。第 3 題：在第 4 部分的比較表格上面改 GPU_PER_HOUR（0.2、2.0），只重跑比較表那一格，看結論會不會翻轉。
-->

---

<div class="eyebrow">05 · Lab L5-3</div>

# Lab 6／7：Audit → Iterate

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:32%">應該是</th></tr></thead>
<tbody>
<tr><td>驗證真的擋住壞輸出？</td><td>看練習四個例子的結果</td><td>接受、接受、拒絕、拒絕</td></tr>
<tr><td>比較公平嗎？</td><td>三種做法的 <code>SYSTEM</code>、資料、重試次數</td><td>完全相同</td></tr>
<tr><td>成本有算重試嗎？</td><td>雲端：<code>USAGE</code> 筆數 vs 40</td><td>筆數 ≥ 40（重試也算）</td></tr>
<tr><td>延遲有暖機嗎？</td><td>第一張通常比較慢</td><td>報告時說明，或去掉第一張</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">一次只改一件事：例如把 <code>MODEL</code> 換成另一個 Gemini 模型（記得在 <code>PRICE</code> 表加上它的單價），看正確率和成本怎麼變。</div>

<!--
★ 稽核（6 分）：換模型的實驗只在有金鑰的學員做；免費額度有每日上限，跑兩次可能被擋。
-->

---

<div class="eyebrow">05 · Lab L5-3 · 延伸</div>

# Lab 7／7：延伸：改提示詞，正確率會變嗎？

<div class="grid grid-cols-[1.1fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

1. 新增一格：<code>SYSTEM = SYSTEM + "帳單＝扣款、退款、發票；……"</code>（不要重跑第 0 部分，否則比較表會清空）
2. 再重跑自架 4-bit 那一格
3. 預測：類別正確率會升還是降？有效 JSON 比例呢？

</div>
<div class="node node--warm"><strong>L20 的伏筆</strong><small>提示詞能修一部分；修不好的（例如簡體字、格式不穩），L20 用微調（QLoRA）</small></div>
</div>

<div class="takeaway mt-3">改提示詞是最便宜的修法：先改提示詞、量一次，再決定要不要微調。</div>

<!--
★ 延伸（3 分）：不給答案頁：結果依模型而定，請學員把前後數字寫進交付的決策表。
-->

---

<div class="eyebrow">05 · Ship</div>

# 交付：客服分流助理（第五天的 Ship）

<div class="grid grid-cols-[1.2fr_1fr] gap-6 mt-2" style="font-size:18px">
<div>

<img class="photo" src="/lab19-gradio-ui.png" alt="Gradio 客服分流助理畫面：左邊客服單輸入框與三個範例，右邊類別、緊急程度、摘要、嘗試／時間四個輸出欄" style="width:100%">
<div class="shot-cap">Part 5 的 Gradio 畫面（Colab T4 實跑，尚未送出客服單）</div>

</div>
<div>

- 用 4-bit 模型，同一個 <code>triage()</code>
- 驗證失敗時顯示「請人工處理」，不亂猜
- <code>share=True</code>：暫時的公開網址（期限看執行時的輸出），只放合成資料示範（L04）

</div>
</div>

<div class="takeaway mt-2">好的分流助理知道自己什麼時候不確定：失敗就交給人。</div>

<!--
★ Ship（4 分）：這是第五天的交付作品，也可以發展成期末專題。分享網址不要貼到公開地方。
-->

---

<div class="eyebrow">06 · 風險（Risk）</div>

# 風險：資料存放地區、服務條款、授權依大小不同

<table class="mt-2" style="font-size:17px">
<thead><tr><th style="width:22%">風險</th><th>例子</th><th style="width:34%">怎麼做</th></tr></thead>
<tbody>
<tr><td>資料存放地區</td><td>客服單送到海外伺服器處理</td><td>和法務確認個資法與合約要求</td></tr>
<tr><td>輸入被再利用</td><td>部分免費方案的條款允許用輸入改進模型</td><td>讀服務條款；只送去識別化或合成資料</td></tr>
<tr><td>授權依大小不同</td><td>Qwen2.5-1.5B 是 Apache-2.0；同家族的 3B 是另一種研究用授權</td><td>每一個大小都去讀模型卡的 license</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">「開放模型」不等於「什麼都能做」：換大小就要重讀授權。</div>

<div class="src">授權：HF 模型卡 license 欄位（S5，待確認）；課程地圖 §9.2</div>

<!--
★ 風險（4 分）：授權依大小不同是最容易踩到的坑：測試時用 1.5B，上線時想換 3B 提升品質，授權就變了。法條細節由法務判斷。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-wrap items-center gap-x-2 gap-y-3 mt-4">
  <span class="chip">決策表五欄</span><span class="arrow">→</span>
  <span class="chip">SDK 呼叫＋usage</span><span class="arrow">→</span>
  <span class="chip">每千張成本</span><span class="arrow">→</span>
  <span class="chip">json.loads＋重試</span><span class="arrow">→</span>
  <span class="chip">chat template＋generate</span><span class="arrow">→</span>
  <span class="chip">4-bit：0.5 byte／權重</span><span class="arrow">→</span>
  <span class="chip">分流助理</span>
</div>

<div class="takeaway mt-6">雲端或自架沒有標準答案：用同一個任務量成本、延遲、品質，再讀條款與授權，才填得出決策表。</div>

<!--
★ 總整理（2 分）：請學員說出自己的選擇和一個數字證據。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 1／2（iPAS 題型）：點選答案

<Mcq id="quiz1.q1" :n="1" :answer="1"
  :options="['回覆的字數', '回傳的 usage（輸入、輸出 token 數）', '呼叫花的秒數', '提示詞的行數']"
  :why="['字數不是計費單位，計費看 token。', '', '秒數是延遲，不是費用。', '行數和費用無關。']"
  explain="API 回傳 usage：輸入、輸出各幾個 token，乘以單價就是這次的費用（付費層才真的收費）。">
呼叫雲端 LLM API 後，計算這次費用最直接的依據是？
</Mcq>

<Mcq id="quiz1.q2" :n="2" :answer="3"
  :options="['成功', '自動改成雙引號', '回傳空字串', '丟出例外，因為 JSON 要用雙引號']"
  :why="['JSON 標準只接受雙引號，單引號是 Python 字典的寫法。', 'json.loads 不會幫你修，所以 lab 才需要 parse_reply 做保護。', '解析失敗是丟出例外，不是回傳空字串。', '']"
  explain="單引號不是合法 JSON，json.loads 會丟出 JSONDecodeError；所以 parse_reply 要 try／except，並計入「有效 JSON」的比例。">
模型回覆 <code>&#123;'category': '帳單'&#125;</code>（單引號），用 <code>json.loads</code> 解析會？
</Mcq>

<FillClear group="quiz1" corner />

<!--
★ 檢核 1／2（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：1 B、2 D。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 隨堂檢核 2／2（iPAS 題型）：點選答案

<Mcq id="quiz2.q3" :n="3" :answer="2"
  :options="['28 GB', '14 GB', '3.5 GB', '0.7 GB']"
  :why="['28 GB 是 fp32（每個參數 4 bytes）。', '14 GB 是 fp16（每個參數 2 bytes）。', '', '0.7 GB 比 4-bit 實際需要的少了十倍。']"
  explain="4-bit ＝ 0.5 byte／參數，7B × 0.5 ＝ 3.5 GB（還要另加 KV cache 等額外開銷）。">
7B 參數的模型用 4-bit 載入，權重大約需要？
</Mcq>

<Mcq id="quiz2.q4" :n="4" :answer="0"
  :options="['在公司內部 GPU 自架開放模型', '用最便宜的雲端 API', '提高 max_output_tokens', '用 json.loads 驗證']"
  :why="['', '再便宜，資料還是送到外部服務商（免費額度的輸入還可能被拿去改進產品）。', 'max_output_tokens 管回覆長度，不管資料去哪。', 'json.loads 只管格式，不管資料去哪。']"
  explain="自架開放模型，資料只在公司內部的機器上處理，不會送出去。">
下列何者最能保護個資「不離開公司」？
</Mcq>

<FillClear group="quiz2" corner />

<!--
★ 檢核 2／2（2 分）：學員自己點；點錯會出現「再想想」和該選項錯在哪，可再點一次。答案：3 C、4 A。
全部答案與理由：
1 B：API 回傳 usage：輸入、輸出各幾個 token，乘以單價就是這次的費用（付費層才真的收費）。
2 D：單引號不是合法 JSON，json.loads 會丟出 JSONDecodeError；所以 parse_reply 要 try／except，並計入「有效 JSON」的比例。
3 C：4-bit ＝ 0.5 byte／參數，7B × 0.5 ＝ 3.5 GB（還要另加 KV cache 等額外開銷）。
4 A：自架開放模型，資料只在公司內部的機器上處理，不會送出去。
-->


---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 L20：模型回覆混進簡體字，格式也不聽話

<div style="font-size:19px" class="mt-4">

- 客服中心：開放模型常冒出簡體字和大陸用語，JSON 也不穩
- LLM 怎麼訓練出來的：預訓練 → SFT → 偏好調整 → 推理 RL
- 用 QLoRA（4-bit ＋ 今天的量化 ＋ L15 的 LoRA）在 T4 上微調，前後對照評估

</div>

<!--
★ 下一步（1 分）：預告。請學員保留今天的比較表：明天微調完要用同一組客服單再量一次。
-->
