# Source of lab19-triage(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L5-3：雲端 API 還是自架模型？客服單分流三種做法（D5-3）
#
# **需求單 #D5-3**（虛構公司：曜嶼電子，資訊部／法務）：客服單分類要用雲端 API，還是自架開放模型？
#
# 同一個任務做三次：把 40 張**合成**客服單分成「類別＋緊急程度＋一句摘要」，要求模型輸出 JSON。
#
# | 部分 | 做什麼 | 輸出 |
# |---|---|---|
# | 0 | 資料、提示詞、JSON 驗證（`json.loads` ＋ 重試） | `parse_reply()` |
# | 1 | 雲端：Gemini API 免費額度（沒有金鑰就跳過） | usage、每 1,000 張成本（付費單價換算） |
# | 2 | 自架：Qwen2.5-1.5B-Instruct，fp16 | 延遲、VRAM |
# | 3 | 自架：同一個模型，4-bit（bitsandbytes） | 延遲、VRAM |
# | 4 | 比較表 → 決策表 | 有效 JSON 比例、正確率、秒數、成本 |
# | 5 | 交付：Gradio 分流助理 | 分享連結 |
#
# 執行階段：**T4 GPU**（4-bit 需要 GPU）。資料是講師製作的合成客服單，可以送到雲端 API。

# %%
# 第 1 格：環境
%pip install -q google-genai python-dotenv bitsandbytes gradio
import json, os, re, time, platform, urllib.request, gc
import torch, transformers
print("torch", torch.__version__, "| transformers", transformers.__version__, "| python", platform.python_version())
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    free, total = torch.cuda.mem_get_info()
    print("GPU:", torch.cuda.get_device_name(0), f"| 可用 VRAM {free/1e9:.1f} / {total/1e9:.1f} GB")

RAW = "https://raw.githubusercontent.com/LinTzuYu0925/GAI_tutorial/day5-done/19-api-vs-self-host/materials/data"
def load_jsonl(name):
    local = os.environ.get("LAB_DATA_DIR")          # 只有講師本機測試會設定；Colab 一律從網址下載
    text = open(os.path.join(local, name), encoding="utf-8").read() if local else \
        urllib.request.urlopen(f"{RAW}/{name}").read().decode("utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]

tickets = load_jsonl("tickets.jsonl")
N = len(tickets)
print(N, "張合成客服單")

# %% [markdown]
# ## 0. 提示詞與 JSON 驗證
# 模型輸出的是「看起來像 JSON 的文字」。**驗證，不要相信**：`json.loads` 解析、檢查欄位和值，失敗就重試。

# %%
CATEGORIES = ["退換貨", "維修", "帳單", "物流", "帳號", "產品諮詢"]
URGENCY = ["高", "中", "低"]
SYSTEM = (
    "你是曜嶼電子的客服分流助理。讀一張客服單，只輸出一個 JSON 物件，不要任何其他文字。\n"
    '格式：{"category": "...", "urgency": "...", "summary": "..."}\n'
    f"category 只能是：{'、'.join(CATEGORIES)}\n"
    "urgency 只能是：高、中、低（有安全疑慮、重複扣款、帳號被盜用＝高）\n"
    "summary：20 字以內的繁體中文摘要。"
)
print(SYSTEM)

def parse_reply(text):
    """把模型的文字變成 dict；不合格就回傳 None"""
    # >>> TODO: 先去掉 ```json … ``` 圍欄，再 json.loads；解析失敗、欄位不齊、值不在清單內都回傳 None
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        d = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(d, dict) or d.get("category") not in CATEGORIES or d.get("urgency") not in URGENCY:
        return None
    if not isinstance(d.get("summary"), str):
        return None
    return d
    # <<< TODO

# 練習頁的四個例子：哪些會被接受？
for s in ['{"category": "維修", "urgency": "高", "summary": "手錶充電發燙"}',
          '```json\n{"category": "物流", "urgency": "中", "summary": "包裹未到"}\n```',
          "{'category': '帳單', 'urgency': '高', 'summary': '重複扣款'}",
          '{"category": "退貨", "urgency": "低", "summary": "想退貨"}']:
    print("接受" if parse_reply(s) else "拒絕", "｜", s.replace("\n", " "))

def triage(generate_fn, ticket, retries=2):
    """呼叫模型、驗證；失敗最多重試 retries 次。回傳 (dict 或 None, 試了幾次, 秒數)"""
    t0 = time.time()
    for attempt in range(1, retries + 2):
        out = generate_fn(ticket["zh"])
        d = parse_reply(out)
        if d is not None:
            return d, attempt, time.time() - t0
    return None, attempt, time.time() - t0

def evaluate(name, generate_fn, n=N):
    rows = [(t, *triage(generate_fn, t)) for t in tickets[:n]]
    ok = [r for r in rows if r[1] is not None]
    first = sum(r[2] == 1 for r in rows if r[1] is not None)
    res = {
        "方法": name,
        "第一次就有效": first / n,
        "重試後有效": len(ok) / n,
        "類別正確": sum(r[1]["category"] == r[0]["category"] for r in ok) / n,
        "緊急正確": sum(r[1]["urgency"] == r[0]["urgency"] for r in ok) / n,
        "秒／張": sum(r[3] for r in rows) / n,
    }
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in res.items()})
    return res, rows

RESULTS = []

# %% [markdown]
# ## 1. 雲端：Gemini API（免費額度）
# 到 Google AI Studio 申請免費金鑰。
# 金鑰**不寫在程式裡**。兩種放法，下面這格都會試：
# 1. **Colab 網頁版**：左側 🔑「密鑰（Secrets）」→ 新增 `GEMINI_API_KEY` → 打開「筆記本存取權」。
# 2. **`.env` 檔**（VS Code 連 Colab）：檔案內容一行 `GEMINI_API_KEY=你的金鑰`；在 VS Code 檔案總管對 `.env` 按右鍵 →「Upload to Colab」。VS Code 連 Colab **不支援**方法 1。
# 注意：免費額度的輸入可能被 Google 拿去改進產品，所以今天只送**合成**客服單。免費額度有每分鐘／每天的請求上限，下面的程式遇到就等一下再試。
# 沒有金鑰：這一部分會自動跳過，其他部分照常。

# %%
try:                                              # 方法 1：Colab 網頁版的密鑰
    from google.colab import userdata
    if userdata.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = userdata.get("GEMINI_API_KEY")
except Exception:
    pass
from dotenv import load_dotenv                    # 方法 2：.env 檔（VS Code 連 Colab 時上傳）
load_dotenv()
HAS_KEY = bool(os.environ.get("GEMINI_API_KEY"))
MODEL = "gemini-3.5-flash-lite"    # 免費額度可用；想換別的模型，到 AI Studio 的價格頁確認
PRICE = {"gemini-3.5-flash-lite": (0.30, 2.50)}   # 美元／百萬 token（輸入, 輸出），付費層單價（2026-11 價格頁，用前請再查）；免費額度本身不收費，這裡換算的是「若改用付費層」的成本
print("有金鑰" if HAS_KEY else "沒有金鑰：跳過第 1 部分")

if HAS_KEY:
    from google import genai
    client = genai.Client()                       # 自動讀 GEMINI_API_KEY
    USAGE = []
    def cloud_generate(ticket_text):
        for wait in (0, 15, 45):                  # 免費額度被限流時，等一下再試
            time.sleep(wait)
            try:
                it = client.interactions.create(
                    model=MODEL,
                    system_instruction=SYSTEM,                    # 系統提示詞：角色與格式
                    input=ticket_text,                            # 這張客服單
                    generation_config={"max_output_tokens": 1024},   # 回覆最多幾個 token
                )
                break
            except Exception as e:
                print("API 錯誤（可能是限流）：", str(e)[:80])
        else:
            return ""
        u = it.usage                              # 這次用了多少 token
        USAGE.append((u.total_input_tokens, u.total_output_tokens))
        return it.output_text

    one = cloud_generate(tickets[2]["zh"])
    print("客服單：", tickets[2]["zh"]); print("模型回覆：", one); print("usage：", USAGE[-1] if USAGE else "（無）")

# %%
def cost_per_1000(in_tok, out_tok, price_in, price_out):
    """平均每張的輸入、輸出 token → 每 1,000 張多少美元"""
    # >>> TODO: 每張成本＝輸入 token × 輸入單價 ÷ 100 萬 ＋ 輸出 token × 輸出單價 ÷ 100 萬；再乘 1,000
    return (in_tok * price_in / 1e6 + out_tok * price_out / 1e6) * 1000
    # <<< TODO

if HAS_KEY:
    USAGE.clear()
    res, rows_api = evaluate(f"雲端 {MODEL}", cloud_generate)
    ins = sum(u[0] for u in USAGE) / len(USAGE); outs = sum(u[1] for u in USAGE) / len(USAGE)
    res["每千張美元"] = cost_per_1000(ins, outs, *PRICE[MODEL]); res["VRAM GB"] = 0.0
    print(f"平均每次：輸入 {ins:.0f}、輸出 {outs:.0f} token（含重試）→ 每 1,000 張 {res['每千張美元']:.2f} 美元")
    RESULTS.append(res)

# %% [markdown]
# ## 2. 自架：Qwen2.5-1.5B-Instruct（fp16）
# 同一個系統提示詞，用 `transformers` 自己跑。聊天模型要先套 **chat template**：把 system／user 包成模型訓練時看過的格式。

# %%
from transformers import AutoTokenizer, AutoModelForCausalLM
HF_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
tok = AutoTokenizer.from_pretrained(HF_MODEL)
msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": tickets[2]["zh"]}]
print(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True))

def make_hf_generate(model):
    @torch.no_grad()
    def gen(ticket_text):
        m = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": ticket_text}]
        ids = tok.apply_chat_template(m, add_generation_prompt=True, return_tensors="pt", return_dict=True).to(model.device)
        out = model.generate(**ids, max_new_tokens=120, do_sample=False)       # 貪婪解碼：每次選機率最高的
        return tok.decode(out[0, ids["input_ids"].shape[1]:], skip_special_tokens=True)
    return gen

def load_and_eval(name, **kw):
    if device == "cuda":
        torch.cuda.empty_cache(); torch.cuda.reset_peak_memory_stats()
    model = AutoModelForCausalLM.from_pretrained(HF_MODEL, **kw).eval()
    if device == "cuda":
        print(f"{name}：載入後 VRAM {torch.cuda.memory_allocated()/1e9:.2f} GB")
    gen = make_hf_generate(model)
    print("範例：", gen(tickets[2]["zh"]))
    res, rows = evaluate(name, gen)
    res["VRAM GB"] = torch.cuda.max_memory_allocated() / 1e9 if device == "cuda" else float("nan")
    return model, res, rows

GPU_PER_HOUR = 0.50    # 假設：一張 T4 等級 GPU 每小時 0.5 美元（請換成你查到的雲端報價）
def selfhost_cost_per_1000(sec_per_ticket):
    return sec_per_ticket * 1000 / 3600 * GPU_PER_HOUR

model16, res16, rows16 = load_and_eval("自架 fp16", dtype=torch.float16 if device == "cuda" else torch.float32,
                                       device_map=device)
RESULTS.append(res16)
del model16; gc.collect()
if device == "cuda":
    torch.cuda.empty_cache()

# %% [markdown]
# ## 3. 自架：同一個模型，4-bit
# 每個權重從 16 bit（2 bytes）變成 4 bit（約 0.5 byte）。**需要 GPU**（bitsandbytes）。

# %%
if device == "cuda":
    from transformers import BitsAndBytesConfig
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.float16)
    model4, res4, rows4 = load_and_eval("自架 4-bit", quantization_config=bnb, device_map="cuda")
    RESULTS.append(res4)
else:
    print("沒有 GPU：跳過 4-bit（bitsandbytes 需要 CUDA）")

# %% [markdown]
# ## 4. 比較表 → 決策表

# %%
GPU_PER_HOUR = 0.50    # 想看敏感度：改成 0.2 或 2.0，只重跑這一格
for r in RESULTS:
    if r["方法"].startswith("自架"):
        r["每千張美元"] = selfhost_cost_per_1000(r["秒／張"])
cols = ["方法", "第一次就有效", "重試後有效", "類別正確", "緊急正確", "秒／張", "VRAM GB", "每千張美元"]
print(" | ".join(cols))
for r in RESULTS:
    print(" | ".join(f"{r[c]:.2f}" if isinstance(r[c], float) else str(r[c]) for c in cols))
print("\n自架成本只算 GPU 租金（假設每小時", GPU_PER_HOUR, "美元），沒算人力與維運。")

# %%
# 看錯在哪：自架 fp16 分錯的單（最多 5 張）
wrong = [(t, d) for t, d, att, sec in rows16 if d is None or d["category"] != t["category"]]
for t, d in wrong[:5]:
    print(t["id"], t["zh"][:30], "| 正解", t["category"], "| 模型", None if d is None else d["category"])

# %% [markdown]
# ## 5. 交付：Gradio 分流助理（第五天的 Ship）
# 用 4-bit 模型（沒有 GPU 時用 fp32 重新載入）。`share=True` 會給一個暫時的公開網址（期限看執行時的輸出），只用合成資料示範。

# %%
import gradio as gr
app_model = model4 if device == "cuda" else AutoModelForCausalLM.from_pretrained(HF_MODEL, dtype=torch.float32).eval()
app_gen = make_hf_generate(app_model)

def app(ticket_text):
    d, attempts, sec = triage(app_gen, {"zh": ticket_text})
    if d is None:
        return "（模型輸出不是有效 JSON，請人工處理）", "", "", f"{attempts} 次、{sec:.1f} 秒"
    return d["category"], d["urgency"], d["summary"], f"{attempts} 次、{sec:.1f} 秒"

demo = gr.Interface(fn=app, inputs=gr.Textbox(label="客服單", lines=4),
                    outputs=[gr.Textbox(label="類別"), gr.Textbox(label="緊急程度"), gr.Textbox(label="摘要"), gr.Textbox(label="嘗試／時間")],
                    title="曜嶼客服分流助理（示範，合成資料）", examples=[[t["zh"]] for t in tickets[:3]])
if not os.environ.get("LAB_NO_LAUNCH"):
    demo.launch(share=True)
