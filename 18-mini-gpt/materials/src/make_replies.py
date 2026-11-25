"""Generate the course's synthetic 繁中 customer-service reply corpus (Taiwan usage).

Usage: python -X utf8 make_replies.py  → ../data/replies.txt (one reply per line)
Everything is template-made by the course; no real customer data. Seeded, so it is reproducible.
"""
import random
from pathlib import Path

random.seed(2026)
PRODUCTS = ["藍牙耳機", "行動電源", "智慧手錶", "掃地機器人", "電熱水壺", "筆電散熱座"]
GREET = ["您好，", "您好，感謝您的來信。", "您好，謝謝您聯絡曜嶼客服。", "親愛的顧客您好，", "您好，收到您的訊息了。"]
SORRY = ["造成您的不便，我們深感抱歉。", "很抱歉讓您遇到這樣的狀況。", "非常抱歉，讓您久等了。", "了解您的困擾，真的很抱歉。", ""]
CLOSE = ["如有其他問題，歡迎隨時與我們聯絡。", "祝您有美好的一天。", "謝謝您的耐心與支持。", "再次感謝您的來信。", "有任何問題都可以直接回覆這封信。"]
ACT = {
    "退換貨": [
        "{p}在七天鑑賞期內可以辦理退貨，請保留完整包裝與配件。",
        "我們會先寄出新的{p}給您，收到後再請您把舊的寄回。",
        "請在訂單頁面點選「申請退換貨」，系統會通知物流到府收件。",
        "退貨運費由本公司負擔，您不需要另外付費。",
        "{p}收到退件後，我們會在三到五個工作天內完成退款。",
    ],
    "維修": [
        "{p}還在保固期內，維修不需要任何費用。",
        "請先停止使用{p}，並拔掉電源，避免發生危險。",
        "請將{p}寄到台北維修中心，維修時間大約七個工作天。",
        "我們已經為您建立維修單，工程師會在兩天內與您聯絡。",
        "如果{p}有發燙或焦味，請不要再充電，我們會優先處理。",
    ],
    "帳單": [
        "我們已確認重複扣款，多扣的金額會退回您的信用卡。",
        "退款通常需要七到十四個工作天才會出現在帳單上。",
        "電子發票可以在會員中心下載，統一編號請在結帳時填寫。",
        "分期付款的設定已經幫您更正，下一期帳單就會生效。",
        "折價券的差額會以購物金的方式退還到您的帳號。",
    ],
    "物流": [
        "包裹目前在轉運中心，預計明天就會送達。",
        "我們已經請物流公司協助查詢，有消息會立刻通知您。",
        "訂單還沒出貨，可以幫您把收件地址改成新的地址。",
        "您可以選擇超商取貨，到貨時會收到簡訊通知。",
        "缺少的{p}會在今天補寄，並附上新的出貨單號。",
    ],
    "帳號": [
        "為了保護您的安全，我們已經暫時凍結您的帳號。",
        "請到登入頁面點選「忘記密碼」，重設信件會在五分鐘內寄出。",
        "會員點數的到期日可以在會員中心的「我的點數」查詢。",
        "手機號碼變更需要先驗證舊號碼，再輸入新的號碼。",
        "兩個帳號的點數可以合併，請提供兩個帳號的註冊信箱。",
    ],
    "產品諮詢": [
        "{p}的使用說明可以在官網的支援頁面下載。",
        "{p}支援 iPhone 和 Android，安裝 App 後就能設定。",
        "行動電源容量 20000mAh，可以隨身帶上飛機，但不能托運。",
        "智慧手錶的防水等級是 5ATM，游泳時可以配戴。",
        "電熱水壺有保溫功能，可以設定 40 到 100 度。",
    ],
}

def reply():
    cat = random.choice(list(ACT))
    p = random.choice(PRODUCTS)
    acts = random.sample(ACT[cat], k=random.choice([1, 2, 2, 3]))
    body = "".join(a.format(p=p) for a in acts)
    return random.choice(GREET) + random.choice(SORRY) + body + random.choice(CLOSE)

lines = sorted({reply() for _ in range(6000)})
random.shuffle(lines)
out = Path(__file__).resolve().parent.parent / "data" / "replies.txt"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(len(lines), "replies,", sum(map(len, lines)), "characters,", len(set("".join(lines))), "distinct characters →", out)
