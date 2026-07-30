"""db_raw.json に表データの手当てを加えて最終データ db.json を出力する。"""
import json, re

DB = json.load(open('db_raw.json'))
BY = {q['id']: q for q in DB}

# --- 図表問題は PDF の段組みが崩れるため、表を構造化して持たせる ---
TABLES = {
 'K15-48': {
   'title': '損益計算書',
   'caption': '自平成31年4月1日 至令和2年3月31日（単位：百万円）',
   'head': ['科目', '金額'],
   'rows': [['売上高','3,850'], ['売上原価','2,950'], ['（ａ）','900'],
            ['販売費及び一般管理費','730'], ['（ｂ）','170'],
            ['営業外費用','20'], ['営業外収益','3'], ['（ｃ）','153'],
            ['特別利益','0'], ['特別損失','1'],
            ['税引前当期純利益','152'], ['法人税等','80'], ['当期純利益','72']],
   # 表以降の平坦化されたテキストを問題文から取り除く
   'cut': '損益計算書自平成31年',
 },
 'K19-48': {
   'title': '損益計算書',
   'caption': '（単位：百万円）',
   'head': ['科目', '金額'],
   'rows': [['売上高','2,000'], ['売上原価','1,000'], ['販売費及び一般管理費','400'],
            ['営業外収益','80'], ['営業外費用','100'],
            ['特別利益','40'], ['特別損失','60']],
   'cut': '損益計算書売上高',
 },
}

for qid, t in TABLES.items():
    q = BY[qid]
    i = q['stem'].find(t['cut'])
    assert i > 0, qid
    q['stem'] = q['stem'][:i].strip()
    q['table'] = {k: t[k] for k in ('title', 'caption', 'head', 'rows')}

# --- 出題形式の判定（アプリの表示・絞り込み用） ---
for q in DB:
    if re.search(r'個数を', q['stem']):
        q['format'] = 'count'          # 適切なものの個数を選ぶ
    elif re.search(r'組み合わせを', q['stem']):
        q['format'] = 'combo'          # ａｂ 等の組み合わせを選ぶ
    else:
        q['format'] = 'single'         # 単純択一
    # 「適切でないもの」を選ばせる問題は取り違えが多いので目印を付ける
    q['negative'] = bool(re.search(r'適切でないもの|合致しないもの|該当しないもの|含まれないもの', q['stem']))

json.dump(DB, open('db.json', 'w'), ensure_ascii=False, indent=1)

import collections
print('総問題数', len(DB))
print('形式  ', dict(collections.Counter(q['format'] for q in DB)))
print('否定形 ', sum(1 for q in DB if q['negative']))
print('分野  ', dict(collections.Counter(q['sectionShort'] for q in DB)))
print('年度  ', dict(collections.Counter(q['era'] for q in DB)))
