# 01-genai-value-map 查證紀錄

依 `technical-research-fact-checking`：只列實際讀過的來源。2026-11-23 初稿全部標「待確認」；2026-11-26 已上網核對 S3–S6、S8–S13（arXiv、OpenAI、Stability AI、Hugging Face API）與 S14–S18。仍待確認：S1（McKinsey 頁面連線逾時）、S2。

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | 生成式 AI 約 75% 價值集中在客服、行銷與銷售、軟體工程、研發 | McKinsey Global Institute, *The economic potential of generative AI: The next productivity frontier* (June 2023) | 待確認（頁碼） | 2026-11-23 |
| S2 | LLM 會產生流暢但錯誤的內容（幻覺） | 一般知識；可引用 Ji et al., *Survey of Hallucination in NLG* (2023) | 待確認 | 2026-11-23 |
| S3 | Qwen2.5-0.5B-Instruct 為 Apache-2.0 | https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct 模型卡 | 已確認：HF API cardData.license＝apache-2.0（2026-11-26）；02 deck T4 實跑也讀出同值 | 2026-11-26 |
| S4 | SD1.5 鏡像 `stable-diffusion-v1-5/stable-diffusion-v1-5`，CreativeML OpenRAIL-M | Hugging Face 模型卡 | 已確認：02 deck 2026-11-26 T4 實跑從模型卡讀出 creativeml-openrail-m | 2026-11-26 |
| S5 | LCM-LoRA `latent-consistency/lcm-lora-sdv1-5`，少步數取樣 | Luo et al., *LCM-LoRA* (arXiv 2311.05556)；模型卡 | 已確認：02 deck 2026-11-26 T4 實跑從模型卡讀出 openrail++ | 2026-11-26 |
| S6 | MusicGen-small 權重 CC-BY-NC 4.0 | https://huggingface.co/facebook/musicgen-small | 已確認：HF API cardData.license＝cc-by-nc-4.0（2026-11-26） | 2026-11-26 |
| S8 | VAE 2013 | Kingma & Welling, arXiv 1312.6114 (Dec 2013) | 已確認（VAE：arXiv 1312.6114 首次投稿 2013-12-20，2026-11-26 讀 abs／發布頁） | 2026-11-26 |
| S9 | GAN 2014 | Goodfellow et al., arXiv 1406.2661 | 已確認（GAN：arXiv 1406.2661 首次投稿 2014-06-10，2026-11-26 讀 abs／發布頁） | 2026-11-26 |
| S10 | Transformer 2017 | Vaswani et al., arXiv 1706.03762 | 已確認（Transformer：arXiv 1706.03762 首次投稿 2017-06-12，2026-11-26 讀 abs／發布頁） | 2026-11-26 |
| S11 | DDPM 2020 | Ho et al., arXiv 2006.11239 | 已確認（DDPM：arXiv 2006.11239 首次投稿 2020-06-19，2026-11-26 讀 abs／發布頁） | 2026-11-26 |
| S12 | Stable Diffusion 2022 公開 | Rombach et al., arXiv 2112.10752；Stability AI 2022-08 發布 | 已確認：Stability AI「Stable Diffusion Public Release」頁日期 Aug 22；HF API CompVis/stable-diffusion-v1-4 createdAt 2022-08-20，年份為 2022；LDM 論文 arXiv 2112.10752 首投 2021-12-20 | 2026-11-26 |
| S13 | ChatGPT 2022-11-30 發布 | OpenAI 部落格 *Introducing ChatGPT* | 已確認（ChatGPT：openai.com/index/chatgpt 日期 2022-11-30，2026-11-26 讀 abs／發布頁） | 2026-11-26 |
| S14 | 第 7 頁左圖：藍眼虎斑貓照片，作者 AdinaVoicu，授權 CC0（Pixabay 原圖，Commons 已審核）；取 500 px 縮圖並裁成正方形 | https://commons.wikimedia.org/wiki/File:Tabby_cat_with_blue_eyes-3336579.jpg（檔案頁與授權欄位已讀） | 已讀檔案頁 | 2026-11-24 |
| S15 | 第 7 頁右圖：GAN 生成的貓，Commons 標示 PD-algorithm（公有領域）、來源 thiscatdoesnotexist.com、作者欄為 StyleGAN2；取 500 px 縮圖 | https://commons.wikimedia.org/wiki/File:GAN_Katze_StyleGAN2.png（檔案頁已讀）。公有領域是 Commons 的標示，不是法律意見；StyleGAN2 之說採 Commons 標註，未另查網站 | 已讀檔案頁（StyleGAN 版本待確認） | 2026-11-24 |
| S16 | 練習 1 左圖：戴耳機走在斯德哥爾摩街頭的男子，攝影 Yingchou Han（Unsplash），Commons 標示 CC0；取 800 px 縮圖（`public/scene-commuter.jpg`） | https://commons.wikimedia.org/wiki/File:Stockholm_man_with_headphones_(Unsplash).jpg（API 讀取 LicenseShortName＝CC0、Artist 欄） | 已讀檔案頁資料 | 2026-11-26 |
| S17 | 練習 2 左圖：VisA PCB1 良品與不良品 001（彎針腳，綠線為講師描邊），CC BY 4.0；從 05 deck `public/` 複製 | 05-ae-anomaly-detection/research/sources.md S1、S6（spot-diff README 授權句） | 已確認（沿用 05） | 2026-11-26 |
| S18 | 「照片變成點」「p_data／p_θ」兩頁的貓圖：S14 同一張照片，以 Pillow `ImageEnhance.Color`（0–3.0）與 `ImageEnhance.Brightness`（0.3–2.1）調整後排成 5×5 格；是教學示意，不是模型輸出 | 講師本機產生（2026-11-26） | 已產生 | 2026-11-26 |
| S19 | use-case canvas（用例畫布）是顧問業常用的一頁式 AI 用例評估格式；課堂改稱「需求評估表」 | 課程用語決定（polish_note01，2026-11-26）；未引用特定版本 | 用語決定 | 2026-11-26 |
