# 04-colab-hub-gradio 查證紀錄

**2026-11-23 製作時沒有上網核對；下列標「待確認」。**

| id | 主張 | 來源 | 狀態 | 日期 |
|---|---|---|---|---|
| S1 | 免費 Colab 有連線時間上限、閒置中斷、GPU 不保證 | Colab FAQ（research.google.com/colaboratory/faq.html） | 待確認（不在投影片寫數字） | 2026-11-23 |
| S2 | 檢查點存 model、optimizer state_dict 與 epoch 以續訓 | PyTorch 教學 *Saving and Loading a General Checkpoint* | 待確認 | 2026-11-23 |
| S3 | `from_pretrained`、Hub 倉庫結構、`~/.cache/huggingface` | Hugging Face Hub 文件 | 待確認 | 2026-11-23 |
| S4 | pickle 載入可執行任意程式碼；safetensors 只存張量 | Python `pickle` 文件警告；safetensors 文件 | 待確認 | 2026-11-23 |
| S5 | T4 為 Turing、compute capability 7.5、16 GB；無原生 bf16 | NVIDIA T4 規格書；CUDA GPU 列表 | 待確認 | 2026-11-23 |
| S6 | FlashAttention-2 支援 Ampere 以上 | Dao-AILab/flash-attention README | 待確認 | 2026-11-23 |
| S7 | Gradio `Interface`、`share=True` 公開網址（有效期限依版本） | Gradio 文件 *Sharing Your App* | 待確認 | 2026-11-23 |
| S8 | 授權家族說明；MusicGen 權重 NC；SD1.5 OpenRAIL-M | 各模型卡與授權全文 | 待確認 | 2026-11-23 |
