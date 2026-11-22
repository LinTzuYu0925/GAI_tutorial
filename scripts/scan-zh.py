"""Scan a deck (or any folder/file) for Simplified Chinese characters and Mainland vocabulary.

Usage:  python -X utf8 scripts/scan-zh.py <deck-dir-or-file> [...]
Scans .md .vue .ts .ipynb .py .txt files, skipping node_modules, dist and .slidev.
Hits are candidates, not verdicts: a few characters are valid in both scripts in some
words (for example 干 in 干擾, 后 in 皇后), so read each hit in context.
Exit code 1 if anything is found.
"""
import pathlib
import sys

# Common Simplified-only forms (Traditional counterpart in the comment block below).
SIMPLIFIED = set(
    "们这个为说时会对来过还进动现样么开关头问题间东车长门马见气书买卖读写听说话语词计认让论设"
    "记许证识译该详误调谈请这级给统维绝练组织经结红约纸线终细级纪纯两并业丛专严丧个临丽举义乌乐"
    "习乡买乱亏亚产亲亿仅从仓仪价众优伙传伤伦伪体佣侠侣侧侦俭债倾偿储儿兑兰关兴养兽内冈册写军农"
    "冯冲决况冻净凉减凤凭凯击凿刘则刚创删别刮制刹剂剑剧劝办务动励劲劳势勋区医华协单卖卫却厂厅历"
    "压厌县参双发变叙叶号叹吓吕吗启员呜咏响哑唤啸喷团园围图圆圣场坏块坚坛坟坠垄垒垦堕墙壮声壳处"
    "备复够头夸夹夺奋奖妆妇妈娱婴学宁宝实宠审宪宫宽宾对寻导寿将尔尘尝层属岁岂岗岛岭峡币师帐带帮"
    "库应庙废开异弃张弹强归当录彻径忆忧怀态怜总恋恶惊惧惨惯愤愿戏战户扑执扩扫扬抢护报担拟拥择挂"
    "挡挤挥损换据掷揽搁摄摆摇撑数斋断无旧时旷昼显晋晒晓晕暂术机杀杂权条来杨极构枪柜标栏树样桥档"
    "梦检楼横欢欧歼毁毕毙气汇汉汤没沟泪泽洁浅测济浏浓涂涛润涨渊渐渔湾湿满滚滞滤灭灯灵灾灿炉点炼"
    "烂热焕爱爷牵犹状独狭猎猪献环现玛琐电画畅疗疮疯痒症盏盐监盖盘着矫矿码砖础硕确碍礼祸离种积称"
    "稳穷窃窍竞笔笼筑简签篮类粮紧纠纤约级纪纬纯纱纲纳纵纷纸纹纺线练组细织终绍经绑绕绘给络绝统继"
    "绩续维综绿缆缓编缘缩缴网罗罚罢职联聪肃肠肤肾肿胀胁胜脉脏脑脚脱腾舰舱艺节芦苏苹范荐药莱获萝营"
    "蓝虑虽蚀蛮补装见观规视览觉触誉计订认讨让训议讯记讲许论设访证评识诉诊词译试诗诚话诞询该详语"
    "误说请诸诺读课谁调谈谊谋谓谢谱贝负贡财责贤败货质贩贪贫购贯贱贴贵贷贸费贺资赋赌赏赔赖赚赛赞"
    "赠赵赶趋跃践踪轨轮软轰轴轻载较辅辆辈辉辑输辖边达迁过运还这进远违连迟适选递逻遗邮邻郑释针钉"
    "钓钟钢钥钱钻铁铃铜铭银铺链销锁锅错锦键镇镜长门闪闭问闯闲间闹闻阀阁阅队阳阴阵阶际陆陈陕险随"
    "隐隶难雾静页顶项顺须顾顿预领颇频题颜额风飞饥饭饮饰饱饼馆首马驱驶驻驾验骑骗骤髅鱼鲁鸟鸡鸣鸭鹰"
    "麦黄齐齿龙龟"
)
# Remove characters that are also standard Traditional forms in common Taiwan usage.
SIMPLIFIED -= set("才面里后干只台系发首伙佣刮制咏症")

MAINLAND_TERMS = [
    "程序", "代码", "软件", "数据", "函数", "变量", "对象", "网络", "接口", "默认", "运行", "服务器",
    "文件夹", "信息", "质量", "视频", "屏幕", "鼠标", "硬件", "内存", "缓存", "调用", "打印", 
    "用户", "优化", "模块", "项目", "博客", "激活函数", "卷积", "数据集", "训练集",
    "回调", "迭代器", "字符串", "布尔", "实例", "源代码", "编程", "笔记本电脑", "U盘",
]
# Mainland terms written in Traditional characters (Taiwan uses 程式, 物件, 執行, 資訊, 使用者, 呼叫…).
# Not listed on purpose: 數據 (course name 數據代理人), 函數 (math: 機率密度函數), 實例, 項目, 演算法.
MAINLAND_TRAD = ["程序", "對象", "運行", "信息", "用戶", "調用", "默認", "視頻", "內存", "軟件",
                 "代碼", "變量", "網絡", "接口", "文件夾", "質量", "屏幕", "鼠標",
                 "字符串", "編程", "緩存", "激活函數"]

EXTS = {".md", ".vue", ".ts", ".ipynb", ".py", ".txt", ".html"}
SKIP = {"node_modules", "dist", ".slidev", "__pycache__", ".git"}


def files(paths):
    for p in map(pathlib.Path, paths):
        if p.is_file():
            yield p
        else:
            for f in p.rglob("*"):
                if f.is_file() and f.suffix in EXTS and not (SKIP & set(f.parts)):
                    yield f


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    hits = 0
    for f in files(argv):
        if f.name == "scan-zh.py":
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            chars = sorted({c for c in line if c in SIMPLIFIED})
            terms = [t for t in MAINLAND_TERMS + MAINLAND_TRAD if t in line]
            if chars or terms:
                hits += 1
                what = []
                if chars:
                    what.append("簡體字 " + "".join(chars))
                if terms:
                    what.append("用語 " + "、".join(dict.fromkeys(terms)))
                print(f"{f}:{n}: {'; '.join(what)} | {line.strip()[:80]}")
    print(f"{hits} line(s) flagged" if hits else "clean: no Simplified characters or Mainland terms found")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
