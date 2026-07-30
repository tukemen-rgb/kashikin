# -*- coding: utf-8 -*-
"""生成した .docx を開き直して、原文と正解が保たれているかを確かめる。

   pandoc も LibreOffice も使わず、document.xml の <w:t> を直接読む。
"""
import zipfile, re, json, os, unicodedata

DB = json.load(open('data/questions.json'))
MARK = ['①', '②', '③', '④']
YEARS = [(14, '令和元年_2019_第14回.docx'), (15, '令和2年_2020_第15回.docx'),
         (16, '令和3年_2021_第16回.docx'), (17, '令和4年_2022_第17回.docx'),
         (18, '令和5年_2023_第18回.docx')]

def text_of(path):
    x = zipfile.ZipFile(path).read('word/document.xml').decode('utf-8')
    x = re.sub(r'</w:p>', '\n', x)
    x = re.sub(r'<w:tab[^>]*/>', '\t', x)
    runs = re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>|(\n)', x, re.S)
    out = []
    for a, b in runs:
        out.append(b if b else a)
    s = ''.join(out)
    for a, b in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")]:
        s = s.replace(a, b)
    return s

bad, checked = [], 0
for kai, fn in YEARS:
    path = os.path.join('restored', fn)
    T = text_of(path)
    flat = T.replace('\n', '')
    qs = sorted([q for q in DB if q['kai'] == kai], key=lambda q: q['num'])
    assert len(qs) == 50, (kai, len(qs))
    for q in qs:
        for label, s in ([('stem', q['stem'])]
                         + [('stmt' + k, v) for k, v in q['statements'].items()]
                         + [('opt' + k, v) for k, v in q['options'].items()]
                         + ([('note', q['note'])] if q['note'] else [])):
            checked += 1
            if s not in flat:
                bad.append((fn, q['id'], label))
        # 正解行
        want = f"問題 {q['num']}　正解 {MARK[q['answer'] - 1]}"
        if want not in T.replace('\n', ''):
            bad.append((fn, q['id'], 'answer'))
        checked += 1
    # 問題番号が50個そろっているか
    n = len(re.findall(r'【問題 \d+】', T))
    if n != 50:
        bad.append((fn, '-', f'問題見出しが{n}個'))

print('照合した項目:', checked)
print('原文・正解との不一致:', bad if bad else '0件')
