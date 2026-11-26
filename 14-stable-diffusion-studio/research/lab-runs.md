# 14-stable-diffusion-studio 實跑紀錄

投影片上的數字、圖片、VRAM 和時間都要來自這裡記錄的執行。

## 本機檢查（2026-11-25）

- `python -X utf8 scripts/py2nb.py …/lab14-sd-studio.py`：學員版與解答版都建出來，解答版語法檢查通過。
- 依 /goal 指示，SD 筆記本不在本機 CPU 實跑；T4 實跑才是真正的測試。

## Colab T4 實跑

### 第 1 次（2026-11-25，commit 5eb368f，部分完成）

- 環境：Colab T4（15.5／15.6 GB 可用）；torch 2.14.1+cu130、diffusers 0.43.0、transformers 5.24.1、Python 3.13.16（`pip -U` 當天版本）。
- 第 1 部分：SD1.5 下載 3.94 GB、載入 57 秒；U-Net 860M 參數、in_channels 4、潛在 64 × 64；文字編碼器輸出 (1, 77, 768)；512 × 512、25 步 4.8 秒，VRAM 峰值 2.81 GB。圖：`public/lab14-run-brief.png`。
- 第 2 部分（CLIP，seed 0）：3 × 3 表 圖1 0.293／0.181／0.227；圖2 0.236／0.299／0.208；圖3 0.272／0.209／0.344（對角線最大）。tricky：white wireless 0.293、black wireless 0.270、white wired headphones 0.263、中文 0.170。
- 第 3 部分：參數網格（`public/lab14-run-param-grid.png`）：10 步 1.2–1.7 秒、25 步 2.5–5.4 秒、50 步 7.2–7.7 秒；w＝1 全部糊。負面提示詞（seed 1）：瓶身文字消失（`lab14-run-negative.png`）。
- 第 4 部分：img2img 實際步數 7／12／17／22；「冬天」在 0.3、0.5 幾乎沒變，0.7 只多光點，0.9 換掉構圖（`lab14-run-img2img.png`）。
- 第 5 部分：**失敗**。生成的「白底」其實是淺灰，`(arr > 235)` 只選到耳機亮面（背景佔約 5%）；換背景後幾乎沒變，產品區改變 5.3／255、背景區 2.2／255（驗收 ② 不通過）。圖：`lab14-run-mask-fail.png`。inpainting 模型下載 3.94 GB，in_channels 9，換背景 4.2 秒，VRAM 峰值 3.43 GB。
- 第 6a 部分：CLIP 分數 w＝1／3／5／7.5／10／14：29.0±2.2、30.1±0.9、30.8±1.0、32.3±1.2、30.6±1.0、31.0±2.1，共 81 秒。
- 第 6b、7 部分有執行，但 Colab 在講師離開期間因閒置中斷，偏差網格與 Gradio 畫面沒有截圖。
- **修正**：遮罩改成「和邊框中位數顏色相差 < 30」＋中值濾波（本機用第一次實跑的產品照截圖測試：背景約 57%）。

### 第 2 次

- [ ] 待執行（修正後的遮罩、偏差網格、Gradio）。

### 第 3 次（2026-11-26，講師 T4，解答筆記本存有輸出）

- 環境：torch 2.14.1+cu130、diffusers 0.43.0、transformers 5.24.1、Python 3.13.16。
- 第 1 部分：512 × 512、25 步 6.1 秒，VRAM 峰值 2.81 GB。
- 第 5 部分：換背景 5.0 秒，VRAM 峰值 3.41 GB；輸出圖和投影片上的 `lab14-inpaint-swap.png` 逐像素相同（seed 固定）。
- 附錄（講師示範，不發給學員）：ControlNet Canny（`lllyasviel/sd-controlnet-canny`）＋SD1.5，UniPC 25 步、seed 0：6.6 秒，VRAM 峰值 4.18 GB；圖 `public/lab14-controlnet-demo.png`。耳機、手機的位置和角度保留，背景變成木紋桌。
- Gradio（第 7 部分）有執行，沒有截圖；Ship 頁改成不放截圖。
