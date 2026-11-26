# Source of lab17-tokens-attention(.ipynb / -solution.ipynb). Build: python -X utf8 scripts/py2nb.py <this file>

# %% [markdown]
# # Lab L5-1：客服單要花多少 token？注意力從哪裡來（D5-1）
#
# **需求單 #D5-1**（虛構公司：曜嶼電子，客服中心）：每天 2,000 張繁中客服單，交給 LLM 處理每月要花多少？為什麼字序很重要？
#
# | 部分 | 做什麼 | 輸出 |
# |---|---|---|
# | 1 | 同一張客服單，用 3 種 tokenizer 切 token；繁中 vs 英文 | token 表、每月成本 |
# | 2 | 自己寫 BPE：最常一起出現的兩個片段合併 | 前 10 次合併 |
# | 3 | 嵌入（embedding）＝查表；字序為什麼重要 | 相似度表、詞袋比較 |
# | 4 | 從零寫注意力（Q、K、V、softmax、÷√d），再看真實模型的注意力 | 3×3 權重、熱力圖 |
#
# 執行階段：**CPU 就可以**（Colab 預設執行階段）。資料是講師製作的**合成**客服單，沒有真實個資。

# %%
# 第 1 格：環境與資料
%pip install -q tiktoken
import json, math, os, platform, glob, subprocess, urllib.request
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import torch, transformers, tiktoken
from matplotlib import font_manager
# Colab 預設沒有中文字型：安裝 Noto CJK，否則圖上的中文會變成方框
NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
if not glob.glob(NOTO) and platform.system() == "Linux":
    subprocess.run("apt-get -qq install -y fonts-noto-cjk > /dev/null", shell=True)
for f in glob.glob(NOTO):
    font_manager.fontManager.addfont(f)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name()
print("torch", torch.__version__, "| transformers", transformers.__version__, "| tiktoken", tiktoken.__version__, "| python", platform.python_version())

RAW = "https://raw.githubusercontent.com/LinTzuYu0925/GAI_tutorial/day5-done/17-tokens-attention-bridge/materials/data"
def load_jsonl(name):
    local = os.environ.get("LAB_DATA_DIR")          # 只有講師本機測試會設定；Colab 一律從網址下載
    text = open(os.path.join(local, name), encoding="utf-8").read() if local else \
        urllib.request.urlopen(f"{RAW}/{name}").read().decode("utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]

tickets = load_jsonl("tickets.jsonl")
print(len(tickets), "張合成客服單；第一張：", tickets[0]["zh"])

# %% [markdown]
# ## 1. 同一張客服單，三種 tokenizer
# - `o200k_base`、`cl100k_base`：OpenAI 公開的兩套 tokenizer（tiktoken）
# - `Qwen2.5`：開放模型 Qwen2.5 的 tokenizer（只下載 tokenizer，幾 MB）
#
# Claude 的 tokenizer 沒有公開；要算 Claude 的 token 數，用 API 的 token 計數功能（D5-3）。

# %%
from transformers import AutoTokenizer
QWEN = "Qwen/Qwen2.5-0.5B-Instruct"
qwen_tok = AutoTokenizer.from_pretrained(QWEN)
enc_o200k = tiktoken.get_encoding("o200k_base")
enc_cl100k = tiktoken.get_encoding("cl100k_base")
TOKENIZERS = {
    "o200k_base": lambda s: enc_o200k.encode(s),
    "cl100k_base": lambda s: enc_cl100k.encode(s),
    "Qwen2.5": lambda s: qwen_tok.encode(s, add_special_tokens=False),
}

def show_pieces(name, text):
    """把一句話切成的 token 一個一個印出來；半個中文字（只有部分位元組）印成 ▯"""
    ids = TOKENIZERS[name](text)
    if name == "Qwen2.5":
        pieces = [qwen_tok.decode([i]) for i in ids]
    else:
        enc = enc_o200k if name == "o200k_base" else enc_cl100k
        pieces = [enc.decode_single_token_bytes(i).decode("utf-8", errors="replace").replace("�", "▯") for i in ids]
    print(f"{name:12s} {len(ids):3d} 個 token：", "｜".join(pieces))

t = tickets[0]
print("字數：", len(t["zh"]))
for name in TOKENIZERS:
    show_pieces(name, t["zh"])

# %%
# 全部 40 張：繁中 vs 英文，平均每張幾個 token
rows = []
for name, f in TOKENIZERS.items():
    zh = np.mean([len(f(t["zh"])) for t in tickets])
    en = np.mean([len(f(t["en"])) for t in tickets])
    chars = np.mean([len(t["zh"]) for t in tickets])
    rows.append((name, zh, en, zh / en, chars / zh))
print(f"{'tokenizer':12s} {'繁中':>6s} {'英文':>6s} {'繁中/英文':>8s} {'每個token幾個字':>10s}")
for r in rows:
    print(f"{r[0]:12s} {r[1]:6.1f} {r[2]:6.1f} {r[3]:8.2f} {r[4]:10.2f}")

# %% [markdown]
# ### 每月成本＝token 數 × 單價
# 單價請到廠商的價格頁查（每 100 萬 token 多少美元，輸入和輸出分開算）。下面的單價是**假設值**，只為了練習算式。

# %%
TICKETS_PER_DAY = 2000
DAYS = 30
PRICE_IN = 1.00     # 假設：每 100 萬個輸入 token 1 美元（請換成你查到的價格）
PRICE_OUT = 5.00    # 假設：每 100 萬個輸出 token 5 美元
REPLY_RATIO = 2      # 假設：回覆長度約是客服單的 2 倍，而且用同一種語言寫

def monthly_cost(ticket_tokens):
    # >>> TODO: 每張單：輸入＝客服單的 token 數，輸出＝REPLY_RATIO 倍；乘上單價（每 100 萬 token），再乘一個月的張數
    per_ticket = ticket_tokens * PRICE_IN / 1e6 + ticket_tokens * REPLY_RATIO * PRICE_OUT / 1e6
    return per_ticket * TICKETS_PER_DAY * DAYS
    # <<< TODO

for name, zh, en, _, _ in rows:
    print(f"{name:12s} 繁中 {monthly_cost(zh):6.2f} 美元／月　英文 {monthly_cost(en):6.2f} 美元／月")
print("（真實系統還要加上每次都送的系統提示詞：D5-3 會從 API 回傳的 usage 讀到）")

# %% [markdown]
# ## 2. 自己寫 BPE：最常一起出現的兩個片段，合併成一個
# BPE（Byte Pair Encoding，位元組對編碼）的訓練只有一個動作，重複很多次：
# 數「相鄰兩個片段」出現幾次 → 最多的那一對合併成新片段 → 再數一次。
# 這裡用 40 張客服單、從「一個字一個片段」開始（真正的 tokenizer 從位元組開始、合併幾萬次）。

# %%
def pair_counts(seqs):
    """數每一對相鄰片段出現幾次；seqs 是很多個「片段串列」"""
    c = Counter()
    for s in seqs:
        for a, b in zip(s, s[1:]):
            c[(a, b)] += 1
    return c

def merge(seqs, pair):
    """把每一串裡的 pair 換成合併後的新片段"""
    out = []
    for s in seqs:
        new, i = [], 0
        while i < len(s):
            if i < len(s) - 1 and (s[i], s[i + 1]) == pair:
                new.append(s[i] + s[i + 1]); i += 2
            else:
                new.append(s[i]); i += 1
        out.append(new)
    return out

seqs = [list(t["zh"]) for t in tickets]
for step in range(1, 11):
    best, n = pair_counts(seqs).most_common(1)[0]
    seqs = merge(seqs, best)
    print(f"第 {step:2d} 次合併：{best[0]} ＋ {best[1]} → {best[0] + best[1]}（出現 {n} 次）")
print("第一張單現在切成：", "｜".join(seqs[0]))

# %% [markdown]
# ## 3. 嵌入＝查表；字序為什麼重要
# 模型拿到的是 token 編號。第一層是一張大表（嵌入矩陣）：**編號 → 那一列**，一列就是一個向量。
# 訓練後，意思相近的詞，向量也會比較接近（用 cosine 相似度量）。

# %%
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(QWEN, dtype=torch.float32, attn_implementation="eager")
model.eval()
E = model.get_input_embeddings().weight.detach()          # 嵌入矩陣
print("嵌入矩陣 shape：", tuple(E.shape), "＝（詞彙表大小, 每個向量的長度）")

WORDS = ["退貨", "退款", "換貨", "耳機", "手錶", "發票"]
ids = []
for w in WORDS:
    i = qwen_tok.encode(w, add_special_tokens=False)
    print(f"{w} → token 編號 {i}")
    ids.append(i)
vecs = torch.stack([E[i].mean(0) for i in ids])          # 若一個詞被切成多個 token，取平均
vecs = torch.nn.functional.normalize(vecs, dim=1)
sim = (vecs @ vecs.T).numpy()
fig, ax = plt.subplots(figsize=(5, 4))
ax.imshow(sim, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(len(WORDS)), WORDS); ax.set_yticks(range(len(WORDS)), WORDS)
for a in range(len(WORDS)):
    for b in range(len(WORDS)):
        ax.text(b, a, f"{sim[a, b]:.2f}", ha="center", va="center", fontsize=9,
                color="white" if sim[a, b] > 0.6 else "black")
ax.set_title("Qwen2.5 嵌入的 cosine 相似度"); plt.tight_layout(); plt.savefig("embed_sim.png", dpi=150); plt.show()

# %%
# 詞袋（bag of words）：只數每個字出現幾次，不管順序
a, b = "先退款再寄回", "先寄回再退款"
print(a, "vs", b)
print("詞袋一樣嗎？", Counter(a) == Counter(b), "← 一樣，但對客服來說是相反的流程")

# %% [markdown]
# ## 4. 從零寫注意力
# 一個字（query，查詢）去和每個字的「標籤」（key，鍵）比對：
# 1. 分數＝q · k（內積，越像越大）
# 2. 除以 √d（d＝向量長度），避免分數太大
# 3. softmax 變成加起來等於 1 的權重
# 4. 用權重把每個字的「內容」（value，值）加起來

# %%
def attention(Q, K, V):
    """Q: [n, d]、K: [n, d]、V: [n, d_v] → 輸出 [n, d_v]、權重 [n, n]"""
    d = Q.shape[-1]
    # >>> TODO: 分數＝Q 乘 K 的轉置再除以 √d；權重＝每一列做 softmax；輸出＝權重乘 V
    scores = Q @ K.T / math.sqrt(d)
    weights = torch.softmax(scores, dim=-1)
    out = weights @ V
    # <<< TODO
    return out, weights

# 投影片「練習：注意力手算」的 3 個字（d＝4，所以 √d＝2）
words = ["螢幕", "破了", "退貨"]
Q = torch.tensor([[1., 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0]])
K = torch.tensor([[1., 0, 0, 0], [0, 0, 2, 0], [1, 0, 1, 0]])
V = torch.tensor([[1., 0], [0, 1], [1, 1]])
out, w = attention(Q, K, V)
torch.set_printoptions(precision=3, sci_mode=False)
print("權重（每一列加起來＝1）：\n", w)
print("「退貨」那一列：", dict(zip(words, w[2].tolist())))
print("輸出：\n", out)

# %%
# 為什麼要除以 √d：d＝64 的隨機向量，分數很大，softmax 幾乎變成 one-hot
torch.manual_seed(0)
q, k = torch.randn(1, 64), torch.randn(8, 64)
raw = torch.softmax(q @ k.T, dim=-1)
scaled = torch.softmax(q @ k.T / math.sqrt(64), dim=-1)
print("不除 √d，最大的權重：", round(raw.max().item(), 3))
print("除以 √d，最大的權重：", round(scaled.max().item(), 3))

# %% [markdown]
# ### 真實模型的注意力：「換」在看哪些字？
# 用 Qwen2.5-0.5B 讀一句客服單，取第 12 層、所有注意力頭的平均。
# 模型常把很多注意力放在第一個 token（像一個「休息站」），所以先把第一欄拿掉、其餘重新加總成 1 再畫。

# %%
SENT = "錶帶太短戴不上，可以只換錶帶嗎？"
LAYER = 12
inputs = qwen_tok(SENT, return_tensors="pt")
with torch.no_grad():
    att = model(**inputs, output_attentions=True).attentions      # 每一層一個 [1, 頭數, n, n]
toks = [qwen_tok.decode([i]).replace("�", "＊") for i in inputs["input_ids"][0]]   # 半個字（只有部分位元組）印成 ＊
A = att[LAYER][0].mean(0)                     # 所有頭平均 → [n, n]
print("第一個 token 平均拿到的注意力：", round(A[1:, 0].mean().item(), 3))
A2 = A[:, 1:] / A[:, 1:].sum(-1, keepdim=True)  # 拿掉第一欄、重新加總成 1
fig, ax = plt.subplots(figsize=(8.5, 7.5))
ax.imshow(A2[1:].numpy(), cmap="Oranges")
ax.tick_params(labelsize=20)
ax.set_xticks(range(len(toks) - 1), toks[1:]); ax.set_yticks(range(len(toks) - 1), toks[1:])
ax.set_xlabel("被看的字（key）", fontsize=20); ax.set_ylabel("正在讀的字（query）", fontsize=20)
ax.set_title(f"Qwen2.5-0.5B 第 {LAYER} 層注意力（頭平均）"); plt.tight_layout(); plt.savefig("attention_heatmap.png", dpi=150); plt.show()
q_idx = next(i for i, s in enumerate(toks) if "換" in s)
top = torch.topk(A2[q_idx, :q_idx], k=min(3, q_idx))
print(f"「{toks[q_idx]}」最注意的字：", [(toks[1 + j], round(v, 3)) for v, j in zip(top.values.tolist(), top.indices.tolist())])

# %% [markdown]
# ## 交付：成本估算便條
# 在下面寫三行，交給客服中心主管：
# 1. 用哪一個 tokenizer 的數字、平均每張幾個 token
# 2. 每月成本（寫出你用的單價和查價日期）
# 3. 一個風險：真實客服單有個資，不能直接送到免費 API
