"""db.json に、本文から機械的に導ける情報を足す。
   生成AIで文章を作るのではなく、原文からの抽出と統計だけを使う。
     - 根拠となる法令・条文の抽出
     - 論点（条文）ごとの出題頻度
     - 類題（文字3-gramのコサイン類似度）
"""
import json, re, math, collections

DB = json.load(open('db.json'))

# ---------- 1. 法令・条文の抽出 ----------
LAWS = [
    ('貸金業法', r'貸金業法'), ('貸金業法施行規則', r'貸金業法施行規則|施行規則'),
    ('貸金業法施行令', r'貸金業法施行令'), ('監督指針', r'監督指針'),
    ('利息制限法', r'利息制限法'), ('出資法', r'出資法|出資の受入れ'),
    ('民法', r'民法'), ('民事執行法', r'民事執行法'), ('民事訴訟法', r'民事訴訟法'),
    ('民事保全法', r'民事保全法'), ('民事再生法', r'民事再生法'), ('破産法', r'破産法'),
    ('会社法', r'会社法'), ('商法', r'商法'), ('手形法', r'手形法'),
    ('電子記録債権法', r'電子記録債権法'), ('個人情報保護法', r'個人情報の保護に関する法律|個人情報保護法'),
    ('消費者契約法', r'消費者契約法'), ('景品表示法', r'不当景品類及び不当表示防止法|景品表示法'),
    ('特定商取引法', r'特定商取引法'), ('犯罪収益移転防止法', r'犯罪による収益の移転防止に関する法律|犯罪収益移転防止法'),
    ('暴力団対策法', r'暴力団員による不当な行為の防止等に関する法律|暴力団対策法'),
    ('自主規制基本規則', r'自主規制基本規則'), ('紛争解決等業務に関する規則', r'紛争解決等業務に関する規則'),
    ('企業会計原則', r'企業会計原則'), ('会社計算規則', r'会社計算規則'),
    ('財務諸表等規則', r'財務諸表等の用語'), ('不動産登記法', r'不動産登記法'),
    ('特定調停法', r'特定調停'),
]
ART = re.compile(r'第(\d+)条(?:の(\d+))?(?:の(\d+))?')


def articles(text):
    """『貸金業法第13条の2』のような参照を拾って正規化する。"""
    found = []
    for m in ART.finditer(text):
        # 直前240字のなかで最後に現れた法令名をその条文の所属とみなす
        head = text[max(0, m.start() - 240):m.start()]
        law = None
        for name, pat in LAWS:
            for mm in re.finditer(pat, head):
                law = (mm.start(), name)
        law = law[1] if law else None
        if not law:
            continue
        num = '第' + m.group(1) + '条'
        if m.group(2): num += 'の' + m.group(2)
        if m.group(3): num += 'の' + m.group(3)
        found.append(law + num)
    return found


for q in DB:
    body = q['stem'] + ''.join(q['statements'].values()) + ''.join(q['options'].values()) + q['note']
    laws = [n for n, p in LAWS if re.search(p, body)]
    arts = articles(body)
    q['laws'] = laws
    # 出現回数が多い順に代表的な条文を最大4つ
    q['articles'] = [a for a, _ in collections.Counter(arts).most_common(4)]

# ---------- 2. 論点（条文）ごとの出題頻度 ----------
freq = collections.Counter()
kai_of = collections.defaultdict(set)
for q in DB:
    for a in q['articles']:
        freq[a] += 1
        kai_of[a].add(q['kai'])
TOPICS = [{'article': a, 'count': c, 'kaiCount': len(kai_of[a])}
          for a, c in freq.most_common() if c >= 3]
for q in DB:
    # その問題の論点が過去何回分の試験で出ているか（いちばん頻出の条文で代表させる）
    q['topicRank'] = max([len(kai_of[a]) for a in q['articles']], default=0)

# ---------- 3. 類題（文字3-gramのコサイン類似度） ----------
STOP = re.compile(r'[、。「」『』（）()［］\[\]0-9０-９\s]')


def grams(q):
    t = STOP.sub('', q['stem'] + ''.join(q['statements'].values()))
    return collections.Counter(t[i:i + 3] for i in range(len(t) - 2))


G = [grams(q) for q in DB]
df = collections.Counter()
for g in G:
    for k in g:
        df[k] += 1
N = len(DB)
V = []
for g in G:
    v = {}
    for k, c in g.items():
        if df[k] < 2 or df[k] > N * 0.3:      # 稀すぎる／ありふれすぎる断片は落とす
            continue
        v[k] = (1 + math.log(c)) * math.log(N / df[k])
    nrm = math.sqrt(sum(x * x for x in v.values())) or 1
    V.append({k: x / nrm for k, x in v.items()})

# 転置索引で候補を絞ってから内積
inv = collections.defaultdict(list)
for i, v in enumerate(V):
    for k in sorted(v, key=v.get, reverse=True)[:60]:   # 各問の特徴的な断片だけ索引に
        inv[k].append(i)
for i, q in enumerate(DB):
    score = collections.Counter()
    for k, w in V[i].items():
        for j in inv.get(k, ()):
            if j != i:
                score[j] += w * V[j].get(k, 0)
    top = [j for j, s in score.most_common(6) if s > 0.06][:5]
    q['similar'] = [DB[j]['id'] for j in top]

json.dump(DB, open('db.json', 'w'), ensure_ascii=False)
json.dump(TOPICS, open('topics.json', 'w'), ensure_ascii=False)

print('法令タグ付き問題:', sum(1 for q in DB if q['laws']), '/', len(DB))
print('条文タグ付き問題:', sum(1 for q in DB if q['articles']), '/', len(DB))
print('類題が付いた問題:', sum(1 for q in DB if q['similar']), '/', len(DB))
print('頻出論点（3回以上）:', len(TOPICS))
print('\n■ 出題頻度 上位15論点')
for t in TOPICS[:15]:
    print(f"  {t['count']:3d}問 / {t['kaiCount']:2d}回分   {t['article']}")
