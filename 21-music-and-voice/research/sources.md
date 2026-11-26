# 21-music-and-voice 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | `facebook/musicgen-small` 權重 CC-BY-NC 4.0；程式 MIT；transformers 4.31 起支援；單聲道 32 kHz | HF 模型卡 license 欄位（Hugging Face API 讀取：cc-by-nc-4.0）；程式 MIT 依 audiocraft 說明 | 權重授權已確認；程式授權待確認 | 2026-11-26 |
| S2 | `hexgrad/Kokoro-82M-v1.1-zh` Apache-2.0；`misaki[zh]`；`lang_code="z"`、聲音 zf_001 | HF 模型卡 license 欄位（API 讀取：apache-2.0）；本機實跑成功 | 已確認 | 2026-11-26 |
| S3 | BreezyVoice（MediaTek Research）Apache-2.0，台灣華語、注音輸入、基於 CosyVoice、可聲音複製 | HF 模型卡 license 欄位（API：BreezyVoice、BreezyVoice-300M 皆 apache-2.0）；功能描述來自搜尋摘要與 arXiv 2501.17790 | 授權已確認；功能待確認 | 2026-11-26 |
| S4 | MusicNet 是古典音樂錄音＋音符標註的資料集 | Thickstun et al., *Learning Features of Music from Scratch*, ICLR 2017 | 待確認 | 2026-11-26 |
| S5 | MusicGen：EnCodec 32 kHz、4 本碼本、50 Hz；delay pattern 約快 4 倍、品質相近；2 萬小時授權音樂 | Copet et al., *Simple and Controllable Music Generation*, 2023；audiocraft MUSICGEN.md | 碼本數與時間點數本機實跑吻合（4 × 247／4.9 秒）；其餘待確認 | 2026-11-26 |
| S6 | Stable Audio Open 等其他音樂模型的授權條款 | 各模型卡 | 待確認 | 2026-11-26 |
| S7 | 碼本大小 2048 | 本機載入時 transformers 警告「vocabulary between 0 and 2047」 | 已觀察 | 2026-11-26 |
