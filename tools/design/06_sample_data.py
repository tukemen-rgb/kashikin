# -*- coding: utf-8 -*-
"""Claude Design に渡す見本データを選ぶ。

   1000問すべては要らない。要るのは「レイアウトが壊れる条件を網羅した見本」なので、
   出題形式・分野・長さの極端・注記・図表・引っかけの有無を必ず1つずつ含める。
"""
import json, collections

DB = json.load(open('data/questions.json'))
BY = {q['id']: q for q in DB}
pick, why = [], {}

def take(qid, reason):
    if qid in why:
        why[qid] += ' ／ ' + reason
        return
    why[qid] = reason
    pick.append(qid)

L = sorted(DB, key=lambda q: len(q['stem']))
take(L[-1]['id'], f"設問がいちばん長い（{len(L[-1]['stem'])}字・9文）")
take(L[0]['id'],  f"設問がいちばん短い（{len(L[0]['stem'])}字）")
take(max(DB, key=lambda q: max([len(v) for v in q['options'].values()] + [0]))['id'], '選択肢がいちばん長い（499字）')
take(max(DB, key=lambda q: max([len(v) for v in q['statements'].values()] + [0]))['id'], '記述ａ〜ｄがいちばん長い（357字）')
take('K15-48', '図表問題（表を構造化して保持）')
take('K19-48', '図表問題（表を構造化して保持）')

# 出題形式3種 × 否定形あり／なし
for fmt, lbl in [('single', '単純択一'), ('combo', '組合せ'), ('count', '個数')]:
    for neg in (True, False):
        c = [q for q in DB if q['format'] == fmt and q['negative'] == neg
             and 150 < len(q['stem']) < 420 and q['id'] not in why]
        if c:
            take(sorted(c, key=lambda q: -q['topicRank'])[0]['id'],
                 f"{lbl}・{'否定形' if neg else '肯定形'}")

# 4分野を必ず1つずつ（頻出テーマの代表を選ぶ）
for sec in ['法令', '貸付実務', '資金需要者保護', '財務会計']:
    c = [q for q in DB if q['sectionShort'] == sec and q['id'] not in why and q['traps']]
    if c:
        take(sorted(c, key=lambda q: -q['topicRank'])[0]['id'], f'分野の代表：{sec}')

take(sorted([q for q in DB if q['note'] and q['id'] not in why],
            key=lambda q: -len(q['note']))[0]['id'], '注記つき（注の定義文が本文と別に付く）')
take(sorted([q for q in DB if len(q['traps']) >= 3 and q['id'] not in why],
            key=lambda q: -q['topicRank'])[0]['id'], '引っかけの型が3つ以上')
take(sorted([q for q in DB if not q['traps'] and q['arts'] and q['id'] not in why],
            key=lambda q: -q['topicRank'])[0]['id'], '引っかけなし・条文名あり')
take(sorted([q for q in DB if q['id'] not in why],
            key=lambda q: -q['topicRank'])[0]['id'], '頻出度がいちばん高い')

# 直近の回から4問（現在の出題傾向）
for q in sorted([q for q in DB if q['kai'] == 20 and q['id'] not in why],
                key=lambda q: q['num'])[:4]:
    take(q['id'], '第20回（令和7年度）から')

OUT = []
for qid in pick:
    q = BY[qid]
    OUT.append({
        'id': q['id'], 'label': q['label'], 'era': q['era'], 'num': q['num'],
        'section': q['sectionShort'], 'theme': q['theme'],
        'format': q['format'], 'negative': q['negative'],
        'stem': q['stem'], 'statements': q['statements'], 'options': q['options'],
        'note': q['note'], 'table': q.get('table'),
        'answer': q['answer'],
        'articles': [f"{a['a']}（{a['n']}）" for a in q['arts']],
        'traps': q['traps'], 'topicRank': q['topicRank'],
        'sampleFor': why[qid],
        'len': {'stem': len(q['stem']),
                'maxStatement': max([len(v) for v in q['statements'].values()] + [0]),
                'maxOption': max(len(v) for v in q['options'].values())},
    })

TRAPS = {t['id']: t for t in json.load(open('data/traps.json'))}
META = {
    '見本の件数': len(OUT),
    '全体': {'問題数': len(DB), '回': 20, '分野': 4, 'テーマ': 47, '引っかけの型': len(TRAPS)},
    '分野の内訳': dict(collections.Counter(q['sectionShort'] for q in DB)),
    '出題形式': {'single': '単純択一', 'combo': '組合せ', 'count': '個数'},
    '文字数の実測': {
        '設問': {'最短': min(len(q['stem']) for q in DB),
                 '中央': sorted(len(q['stem']) for q in DB)[len(DB)//2],
                 '最長': max(len(q['stem']) for q in DB)},
        '選択肢': {'最短': min(min(len(v) for v in q['options'].values()) for q in DB),
                   '中央': sorted(len(v) for q in DB for v in q['options'].values())[len(DB)*2],
                   '最長': max(max(len(v) for v in q['options'].values()) for q in DB)},
        '記述ａ〜ｄ': {'最長': max([len(v) for q in DB for v in q['statements'].values()] or [0])},
    },
    '引っかけの型': {k: {'表示名': v['name'], '着眼点': v['tip']} for k, v in TRAPS.items()},
    '注意': '問題文・記述・選択肢・注記は公式PDFの原文そのままです。'
            '表示上の改行や強調は加えてかまいませんが、文字を足す・削る・置き換えることはできません。',
}
json.dump({'meta': META, 'questions': OUT},
          open('design/data/sample-questions.json', 'w'), ensure_ascii=False, indent=1)
print(len(OUT), '問')
for o in OUT:
    print(f"  {o['id']}  {o['section'][:6]:<6} {o['format']:<6} {o['len']['stem']:>4}字  {o['sampleFor']}")
