# D1-4 · 斷線不怕、主管點得到

> 依據：`planning/slide-plan/D1-value-and-tooling.md` 的 D1-4。**狀態：講師以 /goal 指示自動核准（2026-11-23）**。
> 時間：2 小時。**不教**：HF Spaces 部署（D6-3）、量化（D5-3）、多 GPU。

## 1. 學員假設與學習目標

- **學員**：Colab GPU（ML pp.5–6、DL pp.34–35）、pickle 風險（Vibe 12）、Dash 網頁（數據代理人 pp.50–61）、D1-3 的 PyTorch 迴圈與 state_dict。**沒用過** HF Hub、Gradio（curriculum-analysis K10）。

學完後，學員能夠：

1. **存與接續**訓練（Drive 檢查點）。
2. **說明**模型倉庫內容與 safetensors 的理由。
3. **估算並實測** VRAM。
4. **處理** CUDA out of memory。
5. **交付** Gradio 網頁（第一天成品）。

## 2. 概念地圖

| 概念 | 白話定義 | 解決的問題 | 先備 | 例子 | 常見誤解 |
|---|---|---|---|---|---|
| 檢查點 | 權重＋優化器＋epoch | 斷線續訓 | D1-3 state_dict | Drive 上的 .pt | 只存權重就能續訓 |
| HF Hub | 放模型的倉庫 | 下載預訓練模型 | Vibe Git | from_pretrained | 能下載就能商用 |
| safetensors | 只存數字的權重格式 | 安全載入 | Vibe 12 pickle | model.safetensors | — |
| VRAM 估算 | 參數×位元組 | 跑不跑得動 | — | 0.5B fp16 ≈ 1 GB | 權重＝全部記憶體 |
| T4 限制 | fp16 可、bf16 與 FA2 不行 | 避免報錯 | — | — | 網路範例都能直接跑 |
| Gradio | 函式 → 網頁 | 主管能點 | Dash | Interface | 要先學網頁程式 |
| 授權家族 | Apache／MIT／OpenRAIL／NC | 能否商用 | D1-2 模型卡 | MusicGen NC | 同家族授權都一樣 |

## 3. 投影片順序

<!-- slide-table:start -->
| # | 標題 | 區塊 | 一句話重點 | ★/○/△ | 學員看得到 |
|---|---|---|---|---|---|
| 1 | 斷線不怕、主管點得到 | 生成式AI原理 · D1-4 |  | ★ | 是 |
| 2 | 資訊部：白訓練一天，主管只看到截圖 | 00 · Frame（定義問題） |  | ★ | 是 |
| 3 | 今天結束時，你能夠…… | 學習目標 |  | ★ | 是 |
| 4 | 免費 Colab 的三個限制 | 00 · Frame | 斷線時，記憶體裡的變數和模型全部消失；只有存到 Drive 的檔案會留下。 | ★ | 是 |
| 5 | 檢查點要存三樣：權重、優化器、epoch | 01 · Adapt（調成我們的）· 檢查點 | 只存權重＝能用模型；存三樣＝能接著訓練。 | ★ | 是 |
| 6 | 斷線後：載入檢查點，從下一個 epoch 接著跑 | 01 · Adapt · 續訓 | 斷線最多損失「一個 epoch」，不是一整天。 | ★ | 是 |
| 7 | <code>from_pretrained</code>：一行下載別人訓練好的模型 | 02 · Try（先用現成的）· Hub | Hugging Face Hub 就像「放模型的 GitHub」。 | ★ | 是 |
| 8 | 模型倉庫裡有什麼？ | 02 · Open（打開黑盒子）· 模型倉庫 | 架構（config）＋權重（safetensors）＝能用的模型；授權寫在模型卡。 | ★ | 是 |
| 9 | 為什麼用 safetensors，不用 pickle？ | 02 · Open · 安全 | 別人的模型優先選 safetensors；自己的檢查點用 torch.load 時只載自己存的檔案。 | ★ | 是 |
| 10 | VRAM 估算：參數量 × 每個參數的位元組 | 03 · Measure（量化驗收）· VRAM | 這只是權重；訓練還要梯度、優化器狀態、中間結果，實際會大好幾倍。 | ★ | 是 |
| 11 | 練習：T4（16 GB）跑得動嗎？ | 03 · Measure · VRAM · 練習 |  | ★ | 是 |
| 12 | 練習解答：7B 要等到 D5-3 的 4-bit | 03 · Measure · VRAM · 練習解答 | 怎麼判斷：權重 ≤ 約一半 VRAM 才算舒服；接近上限就要量化（D5-3）。 | ★ | 否（hostOnly） |
| 13 | T4 的三件事 | 03 · Measure · T4 | 網路上的範例常為新 GPU 寫；搬到 T4 前先檢查這三項。 | ★ | 是 |
| 14 | CUDA out of memory：照這個順序處理 | 04 · Adapt · 記憶體不足 | 先改設定，再清記憶體，最後才重新啟動；重新啟動後從檢查點接著跑。 | ★ | 是 |
| 15 | 一張圖看一批樣本：matplotlib 網格 | 05 · Ship（交付）· 網格 | 之後判斷 AE、GAN、擴散模型的好壞，第一步都是「印一張網格來看」。 | ★ | 是 |
| 16 | Gradio：幾行做出網頁 | 05 · Ship · Gradio | 把模型包成「一個函式」，Gradio 就能把它變成網頁。 | ★ | 是 |
| 17 | HF 快取與磁碟空間 | 05 · Ship · 選修 | 模型越下載越多，Colab 磁碟會滿；用不到的模型從快取刪掉。 | ○ | 是 |
| 18 | HF Spaces：網頁長期掛在網路上 | 附錄 · 預告 | 課堂上預設用 Colab 的 share 網址；期末專題再考慮 Spaces。 | △ | 是 |
| 19 | Lab 1／6：我們要做出什麼？ | 06 · Lab L1-4 | 這就是四個檢查點的 ① 目標。 | ★ | 是 |
| 20 | Lab 2／6：拆成哪幾塊？ | 06 · Lab L1-4 | 名稱和筆記本一樣：CKPT、train_one_epoch、measure、predict、demo。 | ★ | 是 |
| 21 | 練習：<code>predict</code> 裡每一步的輸入與輸出 | 06 · Lab L1-4 · 練習 |  | ★ | 是 |
| 22 | 練習解答：<code>predict</code> 的每一步 | 06 · Lab L1-4 · 練習解答 | 怎麼對答案：在 predict 裡每一步後面加 print(x.shape)，上傳一張圖看輸出。 | ★ | 否（hostOnly） |
| 23 | Lab 4／6：Specify | 06 · Lab L1-4 |  | ★ | 是 |
| 24 | Lab 5／6：Generate → Execute | 06 · Lab L1-4 |  | ★ | 是 |
| 25 | Lab 6／6：Audit → Iterate | 06 · Lab L1-4 | 常見錯誤：predict 沒呼叫 model.eval()，同一張圖每次機率都不一樣（Dropout 還開著）。 | ★ | 是 |
| 26 | 授權家族：這個模型可以拿來賺錢嗎？ | 07 · Measure & Risk | 授權寫在模型卡，而且同一家族不同大小可能不同；用之前讀，交付時寫下來。 | ★ | 是 |
| 27 | 第一天：從「能做什麼」到「做出能點的東西」 | 第一天總整理 | 明天開始打開生成模型的黑盒子：先從「只看過良品」的自編碼器開始。 | ★ | 是 |
| 28 | 選擇題（iPAS 題型） | 第一天隨堂檢核 |  | ★ | 是 |
| 29 | 回家作業（不收回，下次上課開頭對答案） | 第一天作業 | 每一題都對應今天的一個交付物：畫布、移植、VRAM 表。 | ★ | 是 |
| 30 | 下一堂 D2-1：找出從沒看過的瑕疵 | 下一步 |  | ★ | 否（hostOnly） |
<!-- slide-table:end -->

## 4. Lab

| Lab | 筆記本 | 模型／資料 | T4 VRAM 峰值 | 時間 | 備案 |
|---|---|---|---|---|---|
| L1-4 | `materials/lab04-checkpoint-gradio.ipynb`（解答：`-solution.ipynb`） | CIFAR-10、D1-3 的 CNN；Qwen2.5-0.5B-Instruct | 待實測 | 約 45 分（待實測） | 無 Drive：存 /content；無 GPU：Part B 只估算；share 打不開：內嵌介面 |

**本機 CPU 煙霧測試（2026-11-23，不是 T4 實跑）**：用 FakeData 代替 CIFAR-10，Part A 續訓流程（第二次執行印出「從 epoch 3 接著訓練」）與 `predict`（灰階 800×600 圖）可以執行。Part B、Gradio 網頁未測。

## 5. 常見誤解

- 只存權重就能續訓（第 5 頁）。
- 估算＝實際用量（第 10 頁）。
- 網路範例在 T4 都能直接跑（第 13 頁）。
- `predict` 忘了 `model.eval()`（第 25 頁）。

## 6. 隨堂檢核

第 28 頁：第一天六題（iPAS 題型）；第 29 頁作業。

## 7. 待查證

- Colab 連線上限、閒置中斷時間（S1）。
- Gradio share 網址有效期限（S7）。
- T4 compute capability 7.5、FlashAttention-2 需 Ampere 以上（S5、S6）。
- `torch.load` 的 `weights_only` 預設值與版本。

## 8. 待講師決定

- 作業第 3 題的 1.5B 模型（授權需確認）。
