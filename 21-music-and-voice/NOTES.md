# D6-1 · 活動影片的配樂與旁白 · 工作筆記

最後更新：2026-11-26。

## 1. 檔案

| 檔案 | 用途 |
|---|---|
| `outline.md`、`slides.md`（24 頁，其中 2 頁 hostOnly）、`teaching-plan.md` | 大綱、投影片、時間表 |
| `materials/src/lab21-music-voice.py` | 筆記本原始檔（不需要資料檔） |
| `public/jingle.wav`、`voiceover.wav`、`waveform_spectrogram.png`、`length_vs_time.png` | 講師本機 CPU 實跑輸出（配樂只能課堂播放：CC-BY-NC） |

## 2. 進度

- [x] 大綱、投影片、筆記本
- [x] 本機 CPU 實跑（全部格子）
- [ ] 講師 Colab T4 實跑：生成秒數、VRAM
- [x] build、PNG 檢視、`check-order.cjs`、`scan-zh.py`
- [x] slide-reviewer 審查（22 FAIL：0 blocker、7 major；已修正；授權改以 HF API 讀模型卡確認）

## 3. 決定

| 日期 | 內容 |
|---|---|
| 2026-11-26 | TTS 用 Kokoro-82M-v1.1-zh（Apache-2.0、CPU 可跑）；台灣口音的 BreezyVoice（Apache-2.0）安裝較複雜，改為講師示範 |
| 2026-11-26 | 配樂提示詞用英文（MusicGen 的文字編碼器是英文 T5） |
| 2026-11-26 | 每段聲音都附授權說明；MusicGen 輸出只在課堂播放 |

## 4. 本單元詞彙（中文統一）

| 英文 | 中文 | 首次出現頁 |
|---|---|---|
| sample rate | 取樣率 | 3、6 |
| waveform / spectrogram | 波形／頻譜圖 | 3、6 |
| codebook | 編碼簿（D2-4） | 7 |
| TTS | 文字轉語音 | 3、12 |
| vocoder | 聲碼器 | 12 |
| melody conditioning | 旋律條件 | 15 |
| delay pattern | 延遲排列 | 16 |
| deepfake audio | 深偽語音 | 22 |
