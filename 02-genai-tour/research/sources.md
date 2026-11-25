# 02-genai-tour 查證紀錄

**本次製作（2026-11-23）沒有上網核對；下列各項依作者既有知識撰寫，標「待確認」。** 筆記本最後一格會從 Hugging Face 讀出授權欄位，實跑時以其輸出為準。

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | Colab 可選 T4 GPU 執行階段 | Colab 說明文件 | 待確認 | 2026-11-23 |
| S2 | Qwen2.5-0.5B-Instruct：約 0.5B 參數、Apache-2.0 | https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct | 授權已確認：2026-11-26 T4 實跑最後一格從模型卡讀出 apache-2.0／creativeml-openrail-m／openrail++（參數量、步數仍依模型卡） | 2026-11-26 |
| S3 | SD1.5 鏡像 `stable-diffusion-v1-5/stable-diffusion-v1-5`（原 runwayml 倉庫已移除），CreativeML OpenRAIL-M | Hugging Face 模型卡 | 授權已確認：2026-11-26 T4 實跑最後一格從模型卡讀出 apache-2.0／creativeml-openrail-m／openrail++（參數量、步數仍依模型卡） | 2026-11-26 |
| S4 | LCM-LoRA `latent-consistency/lcm-lora-sdv1-5`，約 4 步，guidance_scale 約 1 | Luo et al. arXiv 2311.05556；diffusers LCM 文件 | 授權已確認：2026-11-26 T4 實跑最後一格從模型卡讀出 apache-2.0／creativeml-openrail-m／openrail++（參數量、步數仍依模型卡） | 2026-11-26 |
| S5 | （已改用 Gemini，見 S9）Anthropic Python SDK `client.messages.create(model, max_tokens, system, messages)`；回應為內容區塊列表，可能包含 thinking 區塊，所以只取 `type == "text"` | Claude API 文件（作者工具內建參考，2026-11） | 已依參考文件撰寫，待實跑 | 2026-11-23 |
| S6 | 不同 GPU、版本下相同 seed 不保證相同結果 | PyTorch 文件 *Reproducibility* | 待確認 | 2026-11-23 |
| S7 | 免費方案提示詞可能被用於改進服務；AI 生成物著作權保護在台灣仍在討論 | 各服務條款；經濟部智慧財產局相關函釋 | 待確認 | 2026-11-23 |
| S8 | Google Colab VS Code 擴充功能（發行者 Google，`google.colab`）：Select Kernel → Colab → Auto Connect／New Colab Server；第一次要 Google 登入授權；`Colab: Remove Server`；檔案總管右鍵「Upload to Colab」；Contents 檢視可看 `/content`。**`userdata.get` 目前會出錯**（"Secrets can only be fetched when running from the Colab UI"） | https://github.com/googlecolab/colab-vscode README、wiki User Guide、wiki Known Issues and Workarounds、issue #215（2026-11-26 讀）；擴充功能 0.9.7 本機 README 與 package.json（displayName「Colab」、publisher google、extensionDependencies：ms-toolsai.jupyter） | 已讀；講師 2026-11-26 依此流程連上 T4（第 1 格印出 Tesla T4）；GPU 選單確切字樣待截圖 | 2026-11-26 |
| S9 | Gemini API（2026-11-26 實跑確認 `generate_content`、`usage_metadata` 與模型 `gemini-3.5-flash-lite`）：金鑰在 aistudio.google.com/apikey 按「Create API key」；新使用者同意條款後自動建立專案；免費層不需帳單；SDK `pip install google-genai`，客戶端自動讀 `GEMINI_API_KEY`／`GOOGLE_API_KEY` | aistudio.google.com/docs/api-key、/docs/get-started（2026-11-26 讀） | 已讀；`generate_content` 寫法與模型名稱以實跑為準 | 2026-11-26 |
| S10 | 免費層「Content used to improve our products：Yes」，付費層 No；速率限制以專案計、每日額度太平洋時間午夜重設 | aistudio.google.com/docs/pricing、/docs/rate-limits（2026-11-26 讀） | 已讀（免費層 RPM／RPD 數字頁面未列） | 2026-11-26 |
| S11 | Hugging Face Hub 模型名稱「組織／模型」對應網址 huggingface.co/組織/模型；未設限（ungated）模型不需登入即可下載 | huggingface.co 模型頁 | 實跑佐證：2026-11-26 T4 run 沒有 HF_TOKEN（讀取逾時）仍下載成功 | 2026-11-26 |
| S12 | diffusers：guidance_scale ≤ 1 時不做 classifier-free guidance，負面提示被忽略 | diffusers 0.43.0 原始碼 `StableDiffusionPipeline.do_classifier_free_guidance`：`return self._guidance_scale > 1 and self.unet.config.time_cond_proj_dim is None`（本機 inspect 讀出） | 已確認 | 2026-11-26 |
