# 講師導覽（D1-1 第 6 頁）最後一格：10 秒片頭音樂。
# 貼在 02-genai-tour/materials/lab02-genai-tour-solution.ipynb 最後一格執行（Colab T4）。
# MusicGen-small 權重為 CC-BY-NC 4.0（非商用），只由講師示範，學員不跑。
# 注意：2026-11-24 的 tour-jingle.wav 是講師當時在 Colab 直接輸入的格子產生；本檔是可重現的版本，
#       抽樣有隨機性，重跑的音樂不會和 wav 完全相同（見 research/lab-runs.md）。
import torch, scipy.io.wavfile
from transformers import AutoProcessor, MusicgenForConditionalGeneration

torch.manual_seed(0)
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
DEV = "cuda" if torch.cuda.is_available() else "cpu"   # CPU 也能跑（約 100 秒）
mg = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(DEV)
inputs = proc(text=["upbeat electronic jingle, 10 seconds"], padding=True, return_tensors="pt").to(DEV)
audio = mg.generate(**inputs, max_new_tokens=500)   # 約 50 個 token／秒 → 約 10 秒；長度由這裡決定，不是提示詞
rate = mg.config.audio_encoder.sampling_rate        # 32 kHz
scipy.io.wavfile.write("outputs/tour-jingle.wav", rate=rate, data=audio[0, 0].cpu().numpy())
