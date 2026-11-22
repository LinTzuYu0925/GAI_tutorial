---
theme: default
title: 從 Keras 到 PyTorch
info: |
  生成式AI原理 · D1-3
  把 DL 課跑過的 CIFAR-10 CNN 從 Keras 搬到 PyTorch：Tensor、nn.Module、DataLoader、五行訓練迴圈、state_dict。
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
exportFilename: 03-keras-to-pytorch
layout: center
class: cover
---

<div class="eyebrow">生成式AI原理 · D1-3</div>

# 從 Keras 到 PyTorch

<p class="subtitle">同一個 CIFAR-10 CNN，換一個框架，自己寫訓練迴圈</p>

<div class="chain flex flex-nowrap items-center gap-2 mt-8">
  <span class="chip">為什麼搬</span><span class="arrow">→</span>
  <span class="chip">對照表</span><span class="arrow">→</span>
  <span class="chip">Tensor</span><span class="arrow">→</span>
  <span class="chip">nn.Module</span><span class="arrow">→</span>
  <span class="chip">五行迴圈</span><span class="arrow">→</span>
  <span class="chip">移植與驗收</span>
</div>

<!--
★ 開場（2 分）：這是一堂「橋接課」：不教新的 AI 概念，只把你會的東西換成 PyTorch 的寫法。之後每一個生成模型都用今天的迴圈訓練。
-->

---

<div class="eyebrow">00 · Frame（定義問題）</div>

# 工廠資訊組：分類器要搬家

<div class="ticket mt-2">
  <div class="ticket-head">【需求單 #D1-3】部門：工廠資訊組<span>公司：曜嶼電子 <span class="fiction" style="color:#fff;border-color:#fff">虛構</span></span></div>
  <dl>
    <dt>問題</dt><dd>瑕疵分類器是 Keras 寫的，要接 Hugging Face 生態系得先搬到 PyTorch</dd>
    <dt>現況痛點</dt><dd>生成式工具（transformers、diffusers、peft、trl）都以 PyTorch 為主</dd>
    <dt>成功指標（KPI）</dt><dd>PyTorch 版測試準確率和 Keras 版差距在 ±2 個百分點內；存成 state_dict</dd>
    <dt>可用資料</dt><dd>CIFAR-10（代替公司的瑕疵影像；DL 課 LabDay3-2 用過）</dd>
    <dt>限制與法規</dt><dd>Colab T4；一堂課內訓練完</dd>
    <dt>為何現有工具不夠</dt><dd>Keras 的 <code>fit()</code> 把訓練迴圈藏起來；生成模型需要自己寫迴圈</dd>
  </dl>
</div>

<!--
★ 需求單（2 分）：KPI 是「和 Keras 版一樣好」，不是「越高越好」。搬家的驗收標準是行為一致。
-->

---

<div class="eyebrow">學習目標</div>

# 今天結束時，你能夠……

1. **對照** Keras 的每一步在 PyTorch 叫什麼
2. **預測**卷積網路每一層的輸出 shape（[B, C, H, W]），不靠 AI
3. **寫出並解釋**訓練一步的五行程式
4. **移植** LabDay3-2 的 CNN，比較準確率，存成 <code>state_dict</code>

<!--
★ 目標（1 分）。不教：PyTorch Lightning、分散式訓練、自訂 CUDA。
-->

---

<div class="eyebrow">00 · Frame</div>

# 為什麼要搬到 PyTorch？

<div class="grid grid-cols-4 gap-3 mt-4" style="font-size:18px">
  <div class="node node--primary"><strong>transformers</strong><small>LLM、Tokenizer（D1-2、D5）</small></div>
  <div class="node node--primary"><strong>diffusers</strong><small>擴散模型（D3、D4）</small></div>
  <div class="node node--primary"><strong>peft</strong><small>LoRA 微調（D4-3、D5-4）</small></div>
  <div class="node node--primary"><strong>trl</strong><small>LLM 微調（D5-4）</small></div>
</div>

<div class="node mt-5" style="font-size:18px"><strong>PyTorch</strong><small>這四個套件的模型都是 <code>torch.nn.Module</code>；訓練、微調都寫 PyTorch 迴圈</small></div>

<div class="takeaway mt-5">不是 Keras 不好，而是這門課要用的生成式工具都建在 PyTorch 上。</div>

<div class="src">回顧：DL pp.36–37（TF 與 PyTorch 比較）、pp.94–97（PyTorch 附錄）；套件文件見 research/sources.md S1–S4</div>

<!--
★ 為什麼（3 分）：D1-2 已經用過 transformers 和 diffusers，學員看過 torch_dtype、.to("cuda")——今天把這些看懂。
-->

---

<div class="eyebrow">01 · Try（先用現成的）</div>

# 先回顧：你在 DL 課跑過的 Keras 版

```python
model = keras.Sequential([
    keras.Input((32, 32, 3)),
    layers.Conv2D(32, 3, padding="same", activation="relu"),
    layers.Conv2D(32, 3, activation="relu"), layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding="same", activation="relu"),
    layers.Conv2D(64, 3, activation="relu"), layers.MaxPooling2D(),
    layers.Flatten(), layers.Dense(512, activation="relu"), layers.Dense(10)])
model.compile(optimizer="adam", loss=..., metrics=["accuracy"])
model.fit(x_train, y_train, batch_size=64, epochs=10)
```

<div class="takeaway mt-3">你已經會每一步；只是 <code>fit()</code> 一行把「訓練迴圈」藏起來了。</div>

<div class="src">回顧：DL pp.38–55（CNN）、LabDay3-2。實際層數以 DL 課筆記本為準（待講師核對），Dropout 省略未列</div>

<!--
★ 回顧（4 分）：請學員打開自己 DL 課的 LabDay3-2，對照層數。若不同，筆記本的 Net 與 Keras 參考版要一起改。
這一頁是「已經會的」，不要重講 CNN（R-C11）。
-->

---

<div class="eyebrow">02 · Open（打開黑盒子）</div>

# Keras ↔ PyTorch 對照表

<table style="font-size:18px">
<thead><tr><th style="width:26%">要做的事</th><th style="width:34%">Keras</th><th>PyTorch</th></tr></thead>
<tbody>
<tr><td>資料</td><td>NumPy 陣列 <code>x_train</code></td><td><code>Dataset</code> ＋ <code>DataLoader</code></td></tr>
<tr><td>定義模型</td><td><code>Sequential</code>／繼承 <code>keras.Model</code></td><td>繼承 <code>nn.Module</code></td></tr>
<tr><td>損失函數</td><td><code>compile(loss=...)</code></td><td><code>loss_fn = nn.CrossEntropyLoss()</code></td></tr>
<tr><td>優化器</td><td><code>compile(optimizer="adam")</code></td><td><code>torch.optim.Adam(model.parameters())</code></td></tr>
<tr><td>訓練</td><td><code>fit()</code></td><td><strong>自己寫迴圈</strong>（五行）</td></tr>
<tr><td>評估</td><td><code>evaluate()</code></td><td><code>model.eval()</code> ＋ <code>torch.no_grad()</code></td></tr>
<tr><td>存檔</td><td><code>model.save()</code></td><td><code>torch.save(model.state_dict())</code></td></tr>
</tbody>
</table>

<div class="takeaway mt-3">只有「訓練」那一列差最多：Keras 一行，PyTorch 自己寫。</div>

<div class="src">回顧：DL pp.16–33（Keras 訓練流程）</div>

<!--
★ 對照表（5 分）：這張表就是今天的地圖，後面每一頁對應一列。Lab 的稽核也照這張表一列一列檢查。
-->

---

<div class="eyebrow">02 · Open · Tensor</div>

# Tensor：資料和模型要在同一個 device

<div class="grid grid-cols-[1.15fr_1fr] gap-6 mt-1">
<div>

```python
x = torch.rand(64, 3, 32, 32)
x.dtype, x.device     # float32, cpu
x = x.to("cuda")      # 搬到 GPU
model = Net().to("cuda")
y = model(x)          # 兩個都在 cuda 才能算
```

</div>
<div style="font-size:18px">

- **dtype**：每個數字怎麼存（float32、float16）
- **device**：放在哪裡算（cpu、cuda）
- <code>.to(...)</code> 讀作「搬到……」

<div class="node node--warm mt-3"><strong>最常見的錯誤</strong><small>Expected all tensors to be on the same device → 有東西忘了 <code>.to(device)</code></small></div>

</div>
</div>

<div class="takeaway mt-3">Keras 自動決定 GPU；PyTorch 要你自己把模型和每個 batch 搬過去。</div>

<div class="src">回顧：Vibe 12a（shape、dtype）</div>

<!--
★ Tensor（5 分）：tensor 和 NumPy 陣列幾乎一樣，多了 device 與自動微分。現場故意示範錯誤：模型在 cuda、資料在 cpu，看錯誤訊息。
-->

---

<div class="eyebrow">02 · Open · 通道順序</div>

# 通道放哪裡？Keras 放最後，PyTorch 放前面

<div class="grid grid-cols-2 gap-8 mt-4" style="font-size:19px">
<div class="node"><strong>Keras：[B, H, W, C]</strong><small>[64, 32, 32, 3]：64 張、32×32、3 個顏色通道</small></div>
<div class="node node--primary"><strong>PyTorch：[B, C, H, W]</strong><small>[64, 3, 32, 32]：通道排在高寬前面</small></div>
</div>

```python
x = x.permute(0, 3, 1, 2)   # [B,H,W,C] → [B,C,H,W]：把第 3 維搬到第 1 維
```

<div class="node mt-3" style="font-size:18px"><strong><code>transforms.ToTensor()</code> 一次做兩件事</strong><small>HWC → CHW，0–255 → 0–1（等於 Keras 版的 <code>/255.0</code>）</small></div>

<div class="takeaway mt-3">同一張圖，只是軸的順序不同；看到 shape 先問「通道在哪一維」。</div>

<!--
★ 通道（4 分）：B 讀作 batch、C 通道、H 高、W 寬。之後所有影像模型（AE、U-Net、擴散）都用 [B, C, H, W]。
-->

---

<div class="eyebrow">02 · Open · nn.Module</div>

# nn.Module：和繼承 keras.Model 一樣

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1">
<div>

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(),
            nn.Conv2d(32, 32, 3), nn.ReLU(), ...)
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(64*6*6, 512),
            nn.ReLU(), nn.Linear(512, 10))
    def forward(self, x):
        return self.classifier(self.features(x))
```

</div>
<div style="font-size:18px">

- `__init__`：**建**好每一層
- `forward`：**接**線，資料怎麼流
- `Conv2d(3, 32, 3)` 讀作「輸入 3 通道、輸出 32 通道、3×3 卷積核」
- `padding=1` ＝ Keras 的 `"same"`

</div>
</div>

<div class="takeaway mt-2">PyTorch 的卷積要寫「輸入通道數」；Keras 會自己推。</div>

<div class="src">回顧：DL p.20（繼承 keras.Model）、Vibe 13（類別）</div>

<!--
★ nn.Module（6 分）：64*6*6 從哪來？下一頁的練習自己推。Dropout 在投影片省略，筆記本有。
常見誤解：以為呼叫 model.forward(x)——應該寫 model(x)，PyTorch 會自動呼叫 forward。
-->

---

<div class="eyebrow">02 · Open · nn.Module · 練習</div>

# 練習：預測每一層的輸出 shape

<div class="muted" style="font-size:17px">不用 AI、先不執行。3×3 卷積：<code>padding=1</code> 大小不變；沒有 padding 每邊少 1。池化 2×2：高寬除以 2（無條件捨去）</div>

<table class="fill tight vlines mt-1">
<thead><tr><th style="width:36%">層</th><th>我預測的輸出 shape</th><th>實際（筆記本印出）</th></tr></thead>
<tbody>
<tr><td>輸入</td><td>[64, 3, 32, 32]</td><td>[64, 3, 32, 32]</td></tr>
<tr><td><code>Conv2d(3, 32, 3, padding=1)</code></td><td class="blank"><FillIn id="shape.c1" hint="例：[64, ?, ?, ?]……" /></td><td class="blank"><FillIn id="shape.c1-real" /></td></tr>
<tr><td><code>Conv2d(32, 32, 3)</code></td><td class="blank"><FillIn id="shape.c2" /></td><td class="blank"><FillIn id="shape.c2-real" /></td></tr>
<tr><td><code>MaxPool2d(2)</code></td><td class="blank"><FillIn id="shape.p1" /></td><td class="blank"><FillIn id="shape.p1-real" /></td></tr>
<tr><td>第二個卷積區塊（同樣 3 層）</td><td class="blank"><FillIn id="shape.p2" /></td><td class="blank"><FillIn id="shape.p2-real" /></td></tr>
<tr><td><code>Flatten()</code></td><td class="blank"><FillIn id="shape.flat" hint="例：[64, 某個乘積]……" /></td><td class="blank"><FillIn id="shape.flat-real" /></td></tr>
<tr><td><code>Linear(…, 512)</code> → <code>Linear(512, 10)</code></td><td class="blank"><FillIn id="shape.out" /></td><td class="blank"><FillIn id="shape.out-real" /></td></tr>
</tbody>
</table>

<FillClear group="shape" corner />

<!--
★ 無 AI 檢核點（10 分）：先手算，再執行筆記本「nn.Module」那一格，它會逐層印出 shape。不收回。
目的：自己推出 64*6*6 = 2304 從哪裡來——這是移植時最常寫錯的數字。
-->

---
hostOnly: true
---

<div class="eyebrow">02 · Open · nn.Module · 練習解答</div>

# 練習解答：64 × 6 × 6 ＝ 2304 是這樣來的

<table class="tight vlines" style="font-size:18px">
<thead><tr><th style="width:40%">層</th><th>輸出 shape</th><th>為什麼</th></tr></thead>
<tbody>
<tr><td>輸入</td><td>[64, 3, 32, 32]</td><td>—</td></tr>
<tr><td><code>Conv2d(3, 32, 3, padding=1)</code></td><td>[64, 32, 32, 32]</td><td>通道 3→32；padding 保持 32</td></tr>
<tr><td><code>Conv2d(32, 32, 3)</code></td><td>[64, 32, 30, 30]</td><td>沒有 padding：32−2</td></tr>
<tr><td><code>MaxPool2d(2)</code></td><td>[64, 32, 15, 15]</td><td>30÷2</td></tr>
<tr><td>第二個卷積區塊</td><td>[64, 64, 6, 6]</td><td>15 → 15 → 13 → 6（13÷2 捨去）</td></tr>
<tr><td><code>Flatten()</code></td><td>[64, 2304]</td><td>64×6×6</td></tr>
<tr><td>兩個 <code>Linear</code></td><td>[64, 10]</td><td>10 類的分數</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">怎麼對答案：筆記本逐層 <code>print(h.shape)</code>；Flatten 的數字寫錯，第一個 Linear 就會報 shape 錯誤。</div>

<!--
★ 解答（3 分）：這些是由卷積規則算出來的，執行筆記本會印出同樣的 shape（講師實跑時再確認一次）。
-->

---

<div class="eyebrow">02 · Open · 資料</div>

# Dataset 與 DataLoader：取代 <code>fit(batch_size=…)</code>

<div class="grid grid-cols-[1.25fr_1fr] gap-5 mt-1">
<div>

```python
tf = transforms.ToTensor()
train_ds = datasets.CIFAR10("data", train=True,
                            download=True, transform=tf)
train_loader = DataLoader(train_ds, batch_size=64,
                          shuffle=True)
x, y = next(iter(train_loader))
x.shape, y.shape   # [64, 3, 32, 32], [64]
```

</div>
<div style="font-size:18px">

- **Dataset**：第 i 筆資料是什麼（一張圖＋標籤）
- **DataLoader**：一次拿一批、打亂順序
- <code>shuffle=True</code> 只給訓練集

</div>
</div>

<div class="takeaway mt-3">Dataset 回答「一筆」，DataLoader 負責「一批一批、打亂地給」。</div>

<!--
★ DataLoader（5 分）：Vibe 13 寫過 Dataset 類別，這裡用 torchvision 現成的。之後 D2 會自己寫一個讀 PCB 影像的 Dataset。
-->

---

<div class="eyebrow">03 · Adapt（調成我們的）· 訓練迴圈</div>

# 訓練一步＝五行程式

<div class="grid grid-cols-[1.05fr_1.2fr] gap-5 mt-1">
<div>

```python
for x, y in train_loader:
    x, y = x.to(device), y.to(device)
    logits = model(x)            # ①
    loss = loss_fn(logits, y)    # ②
    optimizer.zero_grad()        # ③
    loss.backward()              # ④
    optimizer.step()             # ⑤
```

</div>
<div style="font-size:18px">

1. **forward**：「模型看這批圖，給 10 類分數」
2. **loss**：「和正確答案差多少」
3. **zero_grad**：「把上一批的梯度清掉」
4. **backward**：「算出每個參數該往哪裡調、調多少」
5. **step**：「照梯度真的調一點」

</div>
</div>

<div class="takeaway mt-3">Keras 的 <code>fit()</code> 每一批都在做這五件事；PyTorch 讓你看見、也讓你改。</div>

<div class="src">回顧：DL pp.25–27（損失與反向傳播）</div>

<!--
★ 五行（8 分）：一行一行用中文唸。強調：生成模型的訓練只會改①②（模型和損失不同），③④⑤永遠一樣。D2-1 的 AE 會直接重用這個迴圈。
-->

---

<div class="eyebrow">03 · Adapt · 常見錯誤</div>

# 忘了 <code>zero_grad()</code>：梯度會一直加上去

<div class="flex items-center gap-4 mt-4" style="font-size:19px">
  <div class="node" style="width:30%"><strong>第一次 backward</strong><small>某個參數的梯度 ＝ g</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:30%"><strong>沒清，再 backward</strong><small>梯度 ＝ g ＋ g ＝ 2g</small></div><span class="arrow">→</span>
  <div class="node node--warm" style="width:30%"><strong>結果</strong><small>每一步都走太大、loss 亂跳</small></div>
</div>

<div class="placeholder mt-4" style="height:90px">筆記本「常見錯誤」格印出的兩個梯度值<small>講師實跑後替換（第二個約為第一個的 2 倍）</small></div>

<div class="takeaway mt-3">PyTorch 預設把梯度「累加」；每一批開始前都要清空。</div>

<!--
★ 常見錯誤（4 分）：筆記本會用同一批資料做兩次 backward 印出梯度。這個設計是故意的（有時要累加梯度來模擬大 batch），所以不會報錯——更危險。
-->

---

<div class="eyebrow">03 · Adapt · 評估</div>

# 評估前：<code>model.eval()</code> ＋ <code>torch.no_grad()</code>

<div class="grid grid-cols-[1.2fr_1fr] gap-5 mt-1">
<div>

```python
@torch.no_grad()          # 整個函式不記錄梯度
def evaluate(model, loader):
    model.eval()          # 關掉 Dropout
    correct = 0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        correct += (model(x).argmax(1) == y).sum().item()
    return correct / len(loader.dataset)
```

</div>
<div style="font-size:18px">

- <code>model.eval()</code>：Dropout 不再隨機丟、BatchNorm 用固定統計值
- <code>no_grad()</code>：不記錄計算過程 → 省記憶體、較快
- <code>@</code> 是**裝飾器**（decorator）：把整個函式包在 <code>no_grad</code> 裡

</div>
</div>

<div class="takeaway mt-3">忘了 <code>eval()</code>：準確率會忽高忽低；訓練時記得切回 <code>model.train()</code>。</div>

<!--
★ 評估（5 分）：裝飾器第一次出現，就照右邊那句解釋，不展開語法細節。
-->

---

<div class="eyebrow">04 · Ship（交付）</div>

# 存檔：只存權重（state_dict）

```python
torch.save(model.state_dict(), "cifar_cnn.pt")       # 存：一包「層名稱 → 權重」

model2 = Net().to(device)                            # 先建同樣的類別
model2.load_state_dict(torch.load("cifar_cnn.pt"))   # 再把權重放進去
```

<div class="takeaway mt-4">state_dict 只有數字，沒有程式；載入時要先有同樣的 <code>Net</code> 類別。</div>

<!--
★ 存檔（3 分）：對照 Keras 的 model.save() 會連架構一起存。D1-4 會再加上「優化器狀態＋epoch」，做成可以斷線續訓的檢查點。
-->

---

<div class="eyebrow">附錄 · 選修</div>

# Broadcasting：shape 不同也能相減

```python
x = torch.rand(64, 3, 32, 32)
mean = torch.tensor([0.49, 0.48, 0.45]).view(3, 1, 1)   # [3, 1, 1]
x_norm = x - mean     # [64, 3, 32, 32]：mean 自動「複製」到每張圖、每個像素
```

<div class="takeaway mt-4">從最後一維往前對齊；大小是 1 的維度會自動延伸。</div>

<!--
○ Broadcasting（3 分）：NumPy 規則相同（Vibe 12a）。0.49 等數字只是示範用的平均值，不是 CIFAR-10 的實際統計。
-->

---

<div class="eyebrow">附錄 · 選修</div>

# 暖身：用梯度下降找平均值

<div class="grid grid-cols-[1.2fr_1fr] gap-5 mt-1">
<div>

```python
data = torch.randn(1000) * 2 + 5
mu = torch.zeros(1, requires_grad=True)
opt = torch.optim.SGD([mu], lr=0.1)
for step in range(100):
    loss = ((data - mu) ** 2).mean()
    opt.zero_grad(); loss.backward(); opt.step()
```

</div>
<div style="font-size:18px">

- 讓平方誤差最小的 μ，就是資料平均
- 也是「讓資料出現機率最大」（最大概似）的最簡單例子
- D5-2 的交叉熵是同一個想法

</div>
</div>

<div class="takeaway mt-3">「找參數讓資料最像模型會產生的」——這就是訓練生成模型的核心。</div>

<!--
○ 最大概似的直覺（4 分）：不推導。筆記本最後一格會印出找到的 μ 和資料平均，兩者應該很接近（以實跑為準）。
-->

---

<div class="eyebrow">05 · Lab L1-3</div>

# Lab 1／3：Specify

<div class="grid grid-cols-[1.15fr_1fr] gap-5 mt-1" style="font-size:18px">
<div>

<strong>【目標】</strong>把 LabDay3-2 的 CNN 搬到 PyTorch<br>
<strong>【輸入與輸出】</strong>CIFAR-10 [B, 3, 32, 32] → 10 類分數 [B, 10]<br>
<strong>【限制】</strong>架構、epoch 數、batch 大小和 Keras 版一樣；Colab T4<br>
<strong>【驗收】</strong>① 逐層 shape 和練習頁一致　② loss 每個 epoch 下降　③ 準確率和 Keras 差距 ≤ 2 個百分點　④ 存檔載回後準確率不變

</div>
<div>

**打開**：`materials/lab03-keras-to-pytorch.ipynb` → Open in Colab<br>
執行階段：**T4 GPU**

<div class="muted mt-2" style="font-size:16px">Keras 參考值：填你 DL 課的準確率，或把 <code>RUN_KERAS</code> 改成 True 現場訓練（多花幾分鐘，時間待實測）</div>

</div>
</div>

<!--
★ Specify（4 分）：驗收寫在執行前。橋接課用三頁版（demo-and-practice §3c）：Specify → Generate/Execute → Audit/Iterate。
-->

---

<div class="eyebrow">05 · Lab L1-3</div>

# Lab 2／3：Generate → Execute

<PromptBox>
這是一個 PyTorch 筆記本，請只填寫標有 # TODO 的三格：<br>
① DataLoader（batch_size=BATCH，訓練集要打亂）<br>
② Net 的 features 與 classifier，要和第 2 格的 Keras 模型完全一樣（含 Dropout）<br>
③ train_one_epoch 裡的五行訓練步驟<br>
不要改其他格。每一格填完說明每一行在做什麼。
</PromptBox>

<div class="steps mt-3" style="font-size:17px">
  <div><span class="num">1</span>把 Agent 的程式貼進對應的 TODO 格，<strong>逐行讀懂</strong>再執行</div>
  <div><span class="num">2</span>執行到訓練格，觀察每個 epoch 的 loss 與準確率（每 epoch 時間待實測）</div>
  <div><span class="num">3</span>沒有 Agent 額度：照投影片第 9、12、13 頁自己填；卡住開 <code>-solution.ipynb</code></div>
</div>

<!--
★ Generate＋Execute（約 20 分，含訓練）：訓練時讓學員對照練習頁的 shape 輸出。CPU 備案：把 EPOCHS 改成 1。
-->

---

<div class="eyebrow">05 · Lab L1-3</div>

# Lab 3／3：Audit → Iterate——「跑得動」不等於「搬對了」

<table style="font-size:17px">
<thead><tr><th style="width:30%">稽核問題</th><th>具體動作</th><th style="width:30%">應該是</th></tr></thead>
<tbody>
<tr><td>架構一樣嗎？</td><td>對照 Keras 版每一層；比參數量</td><td>層數、通道、Dropout 都一樣</td></tr>
<tr><td>輸入範圍一樣嗎？</td><td>印出一個 batch 的最小、最大值</td><td>0 到 1（和 <code>/255.0</code> 一樣）</td></tr>
<tr><td>loss 有下降嗎？</td><td>看訓練曲線</td><td>每個 epoch 往下</td></tr>
<tr><td>評估有關 Dropout 嗎？</td><td>找 <code>model.eval()</code></td><td>在 <code>evaluate</code> 裡</td></tr>
<tr><td>準確率差距？</td><td>看 Audit 格印出的差距</td><td>±2 個百分點內</td></tr>
</tbody>
</table>

<div class="takeaway mt-3">差太多時一次只改一件事（例如補上 Dropout），再跑一次比較。</div>

<!--
★ 稽核（10 分）：常見原因：Agent 少寫 Dropout、正規化方式不同（例如多做了 Normalize）、優化器學習率不同。
-->

---

<div class="eyebrow">附錄 · 只認名字</div>

# PyTorch Lightning、Accelerate

<div class="grid grid-cols-2 gap-6 mt-4" style="font-size:18px">
<div class="node"><strong>PyTorch Lightning</strong><small>把訓練迴圈包起來，像 Keras 的 <code>fit()</code></small></div>
<div class="node"><strong>Accelerate</strong><small>同一份迴圈在多張 GPU 或混合精度下執行</small></div>
</div>

<div class="takeaway mt-6">先會自己寫迴圈，再用工具省事；這門課不用它們。</div>

<!--
△ 備用（1 分）。
-->

---

<div class="eyebrow">總整理</div>

# 今天學到的概念鏈

<div class="chain flex flex-nowrap items-center gap-2 mt-4">
  <span class="chip">Tensor／device</span><span class="arrow">→</span>
  <span class="chip">[B, C, H, W]</span><span class="arrow">→</span>
  <span class="chip">nn.Module</span><span class="arrow">→</span>
  <span class="chip">DataLoader</span><span class="arrow">→</span>
  <span class="chip">五行迴圈</span><span class="arrow">→</span>
  <span class="chip">eval／no_grad</span><span class="arrow">→</span>
  <span class="chip">state_dict</span>
</div>

<div class="takeaway mt-6">之後每個生成模型都用同一個迴圈，只換模型和損失函數。</div>

<!--
★ 總整理（2 分）。風險回顧：Agent 寫的移植版「跑得動」不代表「搬對了」，一定要跑稽核表。
-->

---

<div class="eyebrow">隨堂檢核</div>

# 選擇題（iPAS 題型）

<div class="mcq">

1. PyTorch 影像 tensor 的慣用排列？（　）<br><span class="opts">A. [B, H, W, C]　B. [B, C, H, W]　C. [C, B, H, W]　D. [H, W, C, B]</span>
2. 每一批訓練開始前要呼叫哪一個，避免梯度累加？（　）<br><span class="opts">A. <code>loss.backward()</code>　B. <code>optimizer.step()</code>　C. <code>optimizer.zero_grad()</code>　D. <code>model.eval()</code></span>
3. <code>model.eval()</code> 的作用？（　）<br><span class="opts">A. 開始訓練　B. 關閉 Dropout 等訓練專用行為　C. 刪除梯度　D. 存檔</span>
4. 載入 <code>state_dict</code> 前必須先做什麼？（　）<br><span class="opts">A. 建立同樣架構的模型　B. 重新訓練　C. 安裝 Keras　D. 把資料轉成 NumPy</span>

</div>

<!--
★ 檢核（4 分）。答案：1 B、2 C、3 B、4 A。
-->

---
hostOnly: true
---

<div class="eyebrow">下一步</div>

# 下一堂 D1-4：斷線不怕、主管點得到

<div class="node node--primary mt-2">今天的分類器只存在 Colab 的記憶體裡。下一堂把它做成「斷線可以續訓」的檢查點，從 Hugging Face Hub 載模型、估算 VRAM，最後用 Gradio 做成主管點得到的網頁。</div>

<!--
★ 只給講師的託管版看。請學員保留 cifar_cnn.pt（下載或存到 Drive）。
-->
