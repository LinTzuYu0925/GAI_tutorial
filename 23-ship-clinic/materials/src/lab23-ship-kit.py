# Source of lab23-ship-kit(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L6-3：期末專題打包工具箱（D6-3）
#
# **需求單 #D6-3**（虛構公司：曜嶼電子，法遵部）：每個原型上線展示前，都要過合規檢查表，並且打包好。
#
# | 部分 | 做什麼 | 輸出 |
# |---|---|---|
# | 1 | 合規檢查表：六項，每項寫證據 | 檢查表 |
# | 2 | 成本與延遲預算：量你的模型一次要多久 | 秒數、每千次成本 |
# | 3 | Gradio Blocks 介面：輸入、輸出、AI 生成標示、免責聲明 | 介面 |
# | 4 | 模型卡（model card）：用途、資料、評估、限制、授權 | `README.md` |
# | 5 | 推上 Hugging Face Hub（有 token 才跑）；GitHub 指令 | 網址 |
#
# 執行階段：CPU 就可以（你的專題需要 GPU 時再換）。
# 把 `my_model()` 換成你的專題（例如 D5-3 的分流、D4-2 的生圖、D6-2 的搜尋）。

# %%
# 第 1 格：環境
%pip install -q gradio huggingface_hub python-dotenv
import os, time, json, platform, datetime
import gradio as gr
print("gradio", gr.__version__, "| python", platform.python_version())

# %% [markdown]
# ## 0. 你的專題（換成自己的）
# 先用一個最簡單的例子讓整個流程跑通：關鍵字分流。之後把 `my_model()` 換成真的模型。

# %%
PROJECT = {
    "name": "曜嶼客服分流助理（示範）",
    "ticket": "D5-3 客服中心：客服單自動分類",
    "owner": "你的名字",
    "base_model": "（沒有：示範用關鍵字規則）",   # 換成你用的模型，例：Qwen/Qwen2.5-1.5B-Instruct
    "license": "apache-2.0",   # 換成你的專題授權的 Hugging Face 授權識別名稱（例：mit、apache-2.0、other）
}

def my_model(text):
    """示範用的假模型：用關鍵字分類。換成你的專題時，保持「文字進、結果出」"""
    rules = {"退": "退換貨", "修": "維修", "扣款": "帳單", "包裹": "物流", "密碼": "帳號"}
    for k, v in rules.items():
        if k in text:
            return v
    return "產品諮詢"

print(my_model("我的包裹一直沒到"))

# %% [markdown]
# ## 1. 合規檢查表
# 每一項都要寫**證據**（連結、截圖、數字），不是只打勾。

# %%
CHECKLIST = {
    "1. 授權：程式、權重、資料各是什麼授權？能商用嗎？": "",
    "2. 著作權與同意：訓練／輸入的圖片、聲音、文字，有權利使用嗎？人臉、人聲有同意書嗎？": "",
    "3. AI 生成標示：介面上有寫「AI 生成，可能有誤」嗎？生成的圖或聲音有標示嗎？": "",
    "4. 個資：會不會處理到姓名、電話、地址？資料存在哪裡？": "",
    "5. 提示注入：使用者輸入能不能改變系統行為？試過哪一句攻擊？": "",
    "6. 成本與延遲：一次多久、每 1,000 次多少錢？（第 2 部分）": "",
}
# 示範專題（關鍵字分流）的證據：看格式就好
CHECKLIST["1. 授權：程式、權重、資料各是什麼授權？能商用嗎？"] = "程式：自己寫的（MIT）；沒有用到模型權重；資料：課程合成客服單"
CHECKLIST["2. 著作權與同意：訓練／輸入的圖片、聲音、文字，有權利使用嗎？人臉、人聲有同意書嗎？"] = "只用合成文字，沒有圖片和聲音"
CHECKLIST["3. AI 生成標示：介面上有寫「AI 生成，可能有誤」嗎？生成的圖或聲音有標示嗎？"] = "介面上方有標示（第 3 部分）"
CHECKLIST["4. 個資：會不會處理到姓名、電話、地址？資料存在哪裡？"] = "示範只用合成資料；正式版要先去識別化"
CHECKLIST["5. 提示注入：使用者輸入能不能改變系統行為？試過哪一句攻擊？"] = "關鍵字規則不受指令影響；換成 LLM 後要重測（D5-4 的攻擊句）"
CHECKLIST["6. 成本與延遲：一次多久、每 1,000 次多少錢？（第 2 部分）"] = "見第 2 部分"
# >>> TODO: 換成你自己的專題後，把六項改寫成你的證據（一兩句＋連結或數字）；先保留示範的也可以跑
pass
# <<< TODO
missing = [k for k, v in CHECKLIST.items() if not v.strip()]
for k, v in CHECKLIST.items():
    print(("✅ " if v.strip() else "⬜ ") + k + "\n    → " + (v or "（還沒寫）"))
print("\n還沒寫的項目：", len(missing))

# %% [markdown]
# ## 2. 成本與延遲預算

# %%
SAMPLES = ["我的包裹一直沒到", "可以退貨嗎？", "信用卡被扣款兩次", "忘記密碼了"]
N = 50
t0 = time.time()
for i in range(N):
    my_model(SAMPLES[i % len(SAMPLES)])
sec = (time.time() - t0) / N
GPU_PER_HOUR = 0.0      # 示範模型不用 GPU；換成你的專題時填你的 GPU 或 API 成本假設
print(f"平均每次 {sec*1e6:.1f} 微秒；每 1,000 次約 {sec*1000/3600*GPU_PER_HOUR:.4f} 美元（假設 GPU 每小時 {GPU_PER_HOUR} 美元）")
CHECKLIST["6. 成本與延遲：一次多久、每 1,000 次多少錢？（第 2 部分）"] = f"每次 {sec*1e6:.1f} 微秒；不需要 GPU"

# %% [markdown]
# ## 3. Gradio Blocks 介面
# `gr.Blocks` 比 D1-4 的 `gr.Interface` 自由：可以排版、加說明、加多個分頁。

# %%
DISCLAIMER = "⚠️ 本系統的結果由 AI 產生，可能有誤；請勿輸入真實個資。僅供課堂示範（虛構公司：曜嶼電子）。"
with gr.Blocks(title=PROJECT["name"]) as demo:
    gr.Markdown(f"# {PROJECT['name']}\n{DISCLAIMER}")
    with gr.Row():
        inp = gr.Textbox(label="客服單", lines=4, placeholder="輸入一張客服單……")
        out = gr.Textbox(label="分類結果（AI 生成）")
    btn = gr.Button("分類")
    btn.click(my_model, inputs=inp, outputs=out)
    gr.Examples(SAMPLES, inputs=inp)
    with gr.Accordion("模型卡摘要", open=False):
        gr.Markdown(f"需求單：{PROJECT['ticket']}｜基礎模型：{PROJECT['base_model']}｜授權：{PROJECT['license']}")
print("介面建立完成；第 5 部分最後會用 share=True 啟動")

# %% [markdown]
# ## 4. 模型卡（model card）
# Hugging Face 的模型卡＝`README.md`：最上面是 YAML（給機器讀的授權、語言、標籤），下面是給人讀的說明。

# %%
EVAL = "（寫你的指標與數字，例如：類別正確率、有效 JSON 比例、每次延遲）"
# >>> TODO: 把 EVAL 改成你專題量到的數字（D5-4 的前後對照表、D4-2 的 CLIP 分數……）
EVAL = "示範專題：4 張測試單全部分對；每次約幾微秒（第 2 部分）"
# <<< TODO

def model_card(p, checklist):
    """回傳模型卡文字：YAML 區塊＋用途、資料、評估、限制與風險、授權五個小節"""
    lines = [
        "---",
        f"license: {p['license']}",
        "language:\n- zh",
        "tags:\n- course-project\n- generative-ai",
        "---",
        f"# {p['name']}",
        "## 用途", f"解決的需求單：{p['ticket']}。只供課堂示範，不可用於真實客服決策。",
        "## 資料", "課程合成資料（沒有真實個資）。",
        "## 評估", EVAL,
        "## 限制與風險", "\n".join(f"- {k}：{v}" for k, v in checklist.items()),
        "## 授權", f"程式與權重：{p['license']}；基礎模型：{p['base_model']}（依其模型卡授權）。",
        f"\n_最後更新：{datetime.date.today()}，作者：{p['owner']}_",
    ]
    return "\n\n".join(lines)

os.makedirs("ship", exist_ok=True)
card = model_card(PROJECT, CHECKLIST)
open("ship/README.md", "w", encoding="utf-8").write(card)
print(card[:800])

# %% [markdown]
# ## 5. 推上去
# **Hugging Face Hub**：需要 `HF_TOKEN`（write 權限）。沒有 token 就跳過。
# 金鑰**不寫在程式裡**。兩種放法，下面這格都會試：
# 1. **Colab 網頁版**：左側 🔑「密鑰（Secrets）」→ 新增 `HF_TOKEN` → 打開「筆記本存取權」。
# 2. **`.env` 檔**（VS Code 連 Colab）：檔案內容一行 `HF_TOKEN=你的金鑰`；在 VS Code 檔案總管對 `.env` 按右鍵 →「Upload to Colab」。VS Code 連 Colab **不支援**方法 1。
# **GitHub**：建議在自己的電腦用 Vibe Coding 學過的 git（02、07a 單元）；下面印出要打的指令。

# %%
try:                                              # 方法 1：Colab 網頁版的密鑰
    from google.colab import userdata
    if userdata.get("HF_TOKEN"):
        os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN")
except Exception:
    pass
from dotenv import load_dotenv                    # 方法 2：.env 檔（VS Code 連 Colab 時上傳）
load_dotenv()
if os.environ.get("HF_TOKEN"):
    from huggingface_hub import HfApi
    api = HfApi()
    user = api.whoami()["name"]
    repo = f"{user}/course-capstone-demo"
    api.create_repo(repo, private=True, exist_ok=True)           # 私人，自己決定何時公開
    api.upload_folder(folder_path="ship", repo_id=repo)          # 有轉接器（D5-4 的 adapter/）就先複製進 ship/ 一起上傳
    print("已上傳到：https://huggingface.co/" + repo)
else:
    print("沒有 HF_TOKEN：跳過 Hugging Face 上傳")

print("""GitHub（在自己的電腦）：
  git init                                   # 第一次才需要
  git add README.md app.py requirements.txt
  git commit -m "Capstone: 第一版"
  git branch -M main                          # 把分支名稱改成 main
  git remote add origin https://github.com/<你的帳號>/<專案名>.git
  git push -u origin main""")

# %%
# 最後：啟動分享連結（期限看執行時的輸出；只放合成資料）
if not os.environ.get("LAB_NO_LAUNCH"):
    demo.launch(share=True)
