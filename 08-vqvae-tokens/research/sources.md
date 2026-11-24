# 08-vqvae-tokens 查證紀錄

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | 國語朗讀錄音「畢業（演藝界）」，CC BY-SA 4.0 | Wikimedia Commons：File:Zh-tw-畢業(演藝界).wav（Commons API 授權欄位） | 已確認（授權）；檔案下載待補（429） | 2026-11-24 |
| S2 | EnCodec 24 kHz：每秒 75 步、每本 1024 格；bandwidth 1.5／3／6／12／24 → 2／4／8／16／32 本 | facebook/encodec_24khz；講師本機試跑印出本數與 750 步／10 秒。權重授權：模型卡沒有標示，GitHub README 只寫程式碼 MIT | 已確認（本數）；權重授權待確認 | 2026-11-24 |
| S3 | VQ-VAE、編碼簿損失、承諾損失 β ＝ 0.25、直通估計器 | van den Oord et al., arXiv 1711.00937：式 3 的三項損失（sg 位置與投影片相同）；「We use β = 0.25 in all our experiments」；直通估計器引用 [3] Bengio et al. 2013 | 已確認 | 2026-11-24 |
| S4 | EnCodec 用殘差向量量化、24 kHz 每秒 75 步 | Défossez et al., *High Fidelity Neural Audio Compression*, arXiv 2210.13438；數字由 S2 本機試跑印出 | 部分確認（數字已由實跑確認；論文未逐字核對） | 2026-11-24 |
| S5 | SoundStream 殘差向量量化：每一層量化前一層剩下的殘差；用幾層決定位元率（quantizer dropout） | Zeghidour et al., arXiv 2107.03312 §III-C、Algorithm 1 | 已確認 | 2026-11-24 |
| S6 | VQGAN：感知損失＋patch 鑑定師的對抗損失 | Esser et al., arXiv 2012.09841 §3.1（「replace the L2 loss … by a perceptual loss and introduce an adversarial training procedure with a patch-based discriminator」） | 已確認 | 2026-11-24 |
| S7 | 個人資料保護法 | 全國法規資料庫 | 待確認（條號） | 2026-11-24 |
| S8 | VisA pcb2、capsules，CC BY 4.0 | spot-diff README | 已確認 | 2026-11-24 |
| S9 | 直通估計器 | Bengio, Léonard, Courville, *Estimating or propagating gradients through stochastic neurons for conditional computation*, arXiv 1308.3432 (2013)（VQ-VAE 論文的參考文獻 [3]） | 已確認（引用） | 2026-11-24 |
