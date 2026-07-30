"""公式PDF（日本貸金業協会 第14〜20回）から全350問を構造化して抽出する。"""
from pypdf import PdfReader
import re, json

ANSWERS = {
1:"3 2 1 1 4 1 3 4 4 3 1 4 1 4 4 2 1 2 4 3 1 2 2 3 4 2 4 4 3 1 3 4 2 1 2 3 1 3 2 2 3 4 3 2 2 1 4 1 3 3",
2:"3 1 4 3 1 2 2 3 3 4 4 1 4 4 1 2 3 1 2 4 4 1 4 3 1 2 3 2 2 3 2 3 2 3 4 1 4 3 1 2 1 4 3 1 4 2 2 3 1 1",
3:"2 4 4 2 3 3 3 4 2 4 1 4 4 2 1 1 3 2 2 1 1 1 2 3 1 3 3 2 1 1 3 1 2 4 2 3 4 4 2 1 2 3 2 3 4 4 3 4 3 1",
4:"1 2 4 3 4 4 2 1 4 3 2 3 2 3 2 2 3 4 3 1 1 3 2 1 1 3 4 4 1 4 2 1 2 1 3 4 1 2 1 4 2 2 4 3 4 3 1 4 2 3",
5:"3 3 3 2 1 2 1 4 2 1 3 4 1 4 4 3 2 2 3 3 2 3 2 1 1 4 4 3 2 1 2 4 1 2 1 3 2 3 4 3 3 2 1 4 1 4 2 2 4 4",
6:"2 4 1 3 2 3 3 4 1 1 1 2 4 1 3 2 4 4 4 3 2 4 3 2 1 2 3 3 3 2 4 4 4 2 3 1 3 4 4 1 1 2 2 2 1 4 3 1 2 3",
7:"3 4 1 4 2 1 1 4 4 4 1 3 2 3 2 3 2 1 1 1 4 3 3 4 2 3 2 3 3 4 1 2 2 1 3 2 3 4 2 1 4 3 2 2 1 4 3 3 4 4",
8:"4 3 1 3 1 1 1 4 2 3 4 2 3 2 4 4 2 2 4 1 3 4 3 4 4 1 2 2 2 3 4 4 3 1 1 2 3 2 2 4 3 3 1 3 2 2 1 1 1 3",
9:"2 4 3 4 2 1 2 3 2 2 1 2 2 1 4 4 1 1 3 2 2 1 3 4 1 1 3 4 3 1 4 4 1 3 1 2 1 3 4 3 2 3 2 4 2 4 3 3 4 1",
10:"1 3 3 1 4 3 1 2 2 1 2 3 2 4 4 2 1 2 1 3 1 3 4 1 4 4 4 1 4 3 2 4 2 2 4 3 3 2 3 4 1 4 1 4 2 3 3 2 1 3",
11:"1 3 2 2 4 4 3 2 3 4 1 3 4 1 2 1 4 2 3 1 4 3 1 4 2 1 3 2 4 4 1 3 1 3 2 3 1 2 1 4 3 2 2 4 4 3 2 3 1 4",
12:"4 3 2 2 3 4 2 4 1 3 4 2 4 1 3 4 1 4 2 4 2 4 1 3 3 2 3 3 1 3 1 1 2 4 2 1 1 4 2 3 4 1 3 4 3 2 1 2 1 4",
13:"2 1 4 3 2 4 1 3 3 3 1 3 1 1 2 4 4 2 4 3 1 3 4 3 4 2 2 3 1 4 3 1 4 3 2 1 3 2 4 1 4 3 2 4 2 1 1 4 2 4",
14:"2 2 2 3 4 1 4 3 3 3 1 1 2 2 1 4 4 1 1 1 3 4 2 3 4 3 4 1 3 2 4 3 4 3 2 2 1 3 1 4 3 2 4 4 3 3 2 4 1 2",
15:"1 2 4 1 3 2 2 4 1 4 3 1 2 4 3 2 1 3 2 4 3 3 4 3 1 1 4 4 1 2 3 1 4 3 4 3 1 3 1 2 4 2 4 3 1 2 3 1 3 2",
16:"1 3 2 3 2 4 3 1 4 1 2 4 2 4 2 4 2 4 1 4 2 1 1 4 3 1 3 2 4 2 4 3 1 1 4 2 4 2 3 1 3 4 2 4 1 3 3 1 3 2",
17:"1 3 4 4 3 1 2 4 4 3 2 3 4 3 2 2 1 1 3 4 1 3 2 1 4 1 4 3 2 1 4 2 4 4 1 4 4 2 1 3 4 3 1 4 2 3 1 3 2 3",
18:"2 3 3 1 4 3 2 2 4 3 2 1 4 4 1 1 4 1 2 2 3 3 1 1 3 3 4 3 4 4 1 3 2 1 2 4 3 2 1 4 1 4 3 1 3 1 2 3 4 2",
19:"1 2 2 4 3 4 1 4 3 2 1 3 3 4 3 2 4 4 2 3 1 2 1 4 1 1 2 3 4 4 1 3 1 4 2 4 1 1 3 2 2 3 4 2 2 1 3 3 2 1",
20:"1 4 2 2 4 1 4 3 2 2 4 1 3 3 2 2 3 1 2 3 4 2 3 1 4 4 1 3 3 2 4 1 1 4 2 3 3 4 3 4 2 4 3 2 3 4 1 1 2 2"}
ANSWERS = {k: [int(x) for x in v.split()] for k, v in ANSWERS.items()}

YEARS = {
 1:('平成21年度',2009,'第1回'),  2:('平成21年度',2009,'第2回'),
 3:('平成21年度',2009,'第3回'),  4:('平成21年度',2010,'第4回'),
 5:('平成22年度',2010,'第5回'),  6:('平成23年度',2011,'第6回'),
 7:('平成24年度',2012,'第7回'),  8:('平成25年度',2013,'第8回'),
 9:('平成26年度',2014,'第9回'), 10:('平成27年度',2015,'第10回'),
11:('平成28年度',2016,'第11回'),12:('平成29年度',2017,'第12回'),
13:('平成30年度',2018,'第13回'),14:('令和元年度',2019,'第14回'),
15:('令和2年度',2020,'第15回'),16:('令和3年度',2021,'第16回'),
17:('令和4年度',2022,'第17回'),18:('令和5年度',2023,'第18回'),
19:('令和6年度',2024,'第19回'),20:('令和7年度',2025,'第20回')}

SECTIONS = ['法及び関係法令に関すること',
            '貸付け及び貸付けに付随する取引に関する法令及び実務に関すること',
            '資金需要者等の保護に関すること',
            '財務及び会計に関すること']
SHORT = {SECTIONS[0]:'法令', SECTIONS[1]:'貸付実務',
         SECTIONS[2]:'資金需要者保護', SECTIONS[3]:'財務会計'}

OPTSTART  = re.compile(r'^①(?![～~])')
# ａ〜ｄの記述の見出し。「ａ～ｄの…」のような本文の折り返しや、
# 引用文中の箇条書き「ａ．…」は見出しではないので除外する。
STMT      = re.compile(r'^([ａ-ｄ])(?![～~．.])\s*(.*)$')
WRAPPED   = re.compile(r'[ａ-ｄ][～~]$')   # 前の行が「…次のａ～」で終わっている
NOTEDEF   = re.compile(r'^\(\s*注\s*\d*\s*\)'
                       r'(?:\s*[^。]{1,40}?とは[、，]'      # 「〜とは、」は空白なしでも注と判定
                       r'|\s+[^。]{1,40}?は[、，])')        # 「〜は、」は字下げがある場合のみ
BARE_NOTE = re.compile(r'^\(\s*注\s*\d*\s*\)?\s*$')


def norm(s):
    s = re.sub(r'/c269(\d)', r'\1', s)      # 埋め込みフォントの数字
    s = re.sub(r'/c\d+', '', s)
    s = s.replace(' ', ' ').replace('　', ' ').replace('\xa0', ' ')
    s = re.sub(r'[０-９]', lambda m: chr(ord(m.group()) - 0xFEE0), s)
    return s.replace('〜', '～')


SEP = ''   # 保護した区切り空白の一時記号


def tidy(s):
    s = re.sub(r'[ \t]+', ' ', s)
    # 括弧に隣接する空白は先に落とす（「（ ア ）」→「（ア）」）
    s = re.sub(r'([（(]) +', r'\1', s)
    s = re.sub(r' +([）)])', r'\1', s)
    # 「ア 50万円 イ 100万円 ウ 40万円」のような対応表形式の選択肢は、
    # 項目の区切り空白を残さないと読めなくなるので保護する。
    # 誤検出を避けるため、区切りが2箇所以上ある場合に限る。
    LIST = r'(?<=[^\s（(]) (?=[アイウエオａ-ｄ] ?[^\s])'
    if len(re.findall(LIST, s)) >= 2:
        s = re.sub(LIST, SEP, s)
    for _ in range(3):
        s = re.sub(r'(?<=\d) (?=\d)', '', s)
        s = re.sub(r'(?<=[^\x00-\x7F]) (?=\d)', '', s)
        s = re.sub(r'(?<=\d) (?=[^\x00-\x7F])', '', s)
        s = re.sub(r'(?<=[^\x00-\x7F]) (?=[^\x00-\x7F])', '', s)
        s = re.sub(r'(?<=[^\x00-\x7F]) (?=[A-Za-z])', '', s)
        s = re.sub(r'(?<=[A-Za-z]) (?=[^\x00-\x7F])', '', s)
        s = re.sub(r'(?<=[^\x00-\x7F]) (?=[-–—])', '', s)
        s = re.sub(r'(?<=[-–—]) (?=[^\x00-\x7F])', '', s)
        s = re.sub(r'(?<=[-–—]) (?=\d)', '', s)        # Ⅱ- 2
        s = re.sub(r'(?<=\d) (?=[-–—])', '', s)
        s = re.sub(r'(?<=[A-Za-z]) (?=\d)', '', s)      # Z 8305
        s = re.sub(r'(?<=\d) (?=[A-Za-z])', '', s)
        s = re.sub(r'(?<=,) (?=\d)', '', s)             # 1, 000
        s = re.sub(r'(?<=\d) (?=,)', '', s)             # 1 ,000
        s = re.sub(r'(?<=[^\x00-\x7F]) (?=\()', '', s)  # 書面等 (注)
    s = re.sub(r'\(\s*注\s*(\d*)\s*\)', lambda m: f'(注{m.group(1)})', s)
    s = re.sub(r'（ +', '（', s); s = re.sub(r' +）', '）', s)
    s = re.sub(r'\( +', '(', s);  s = re.sub(r' +\)', ')', s)
    return s.replace(SEP, ' ').strip()


def page_lines(raw):
    """ページ本文の行リストと、そのページで宣言された分野を返す。"""
    out, sec = [], None
    for line in norm(raw).split('\n'):
        s = line.strip()
        if not s: continue
        if re.fullmatch(r'[-−–]\s*\d+\s*[-−–]', s): continue        # ノンブル
        if re.match(r'DKIH-\d+\.(indd|smd)', s): continue           # 印刷用フッタ
        if re.match(r'^\d{4}/\d{1,2}/\d{1,2}', s): continue
        if s in SECTIONS: sec = s; continue
        out.append(s)
    if out and re.fullmatch(r'\d{1,3}', out[-1]):   # 旧版面はノンブルが裸の数字
        out.pop()
    return out, sec


def find_note_start(lines):
    """「(注N) XXXとは、…」という注の定義が始まる行。無ければ None。"""
    for i in range(len(lines)):
        if NOTEDEF.match(''.join(lines[i:i + 3])):
            return i
    return None


def merge_superscripts(lines):
    """本文中に単独行で現れる上付きの (注) を直前の行に吸収する。"""
    merged = []
    for s in lines:
        if BARE_NOTE.match(s) and merged:
            merged[-1] += s
        else:
            merged.append(s)
    return merged


def split_blocks(lines):
    """本文を 前段（問題文＋ａ〜ｄ）／選択肢／注 の3ブロックに分ける。"""
    note_at = find_note_start(lines)
    anchor = None
    for i, l in enumerate(lines):
        if OPTSTART.match(l):
            anchor = i
    if anchor is None:
        return merge_superscripts(lines), [], []
    if note_at is None:
        return merge_superscripts(lines[:anchor]), lines[anchor:], []
    if note_at < anchor:                       # 注が選択肢より前にある版面
        return merge_superscripts(lines[:note_at]), lines[anchor:], lines[note_at:anchor]
    return merge_superscripts(lines[:anchor]), lines[anchor:note_at], lines[note_at:]


def parse_exam(kai):
    reader = PdfReader(f'official/exam_paper_{kai}th.pdf')
    questions, section = {}, None
    for page in reader.pages:
        raw = page.extract_text()
        if '【問題' not in raw: continue
        lines, sec = page_lines(raw)
        if sec: section = sec
        body = '\n'.join(lines)
        m = re.search(r'【問題\s*(\d{1,2})\s*】', body)
        if not m: continue
        num = int(m.group(1))
        rest = [l for l in body[m.end():].split('\n') if l.strip()]
        pre, optlines, notelines = split_blocks(rest)

        opts, buf = {}, None
        for part in re.split(r'([①②③④])', ''.join(optlines)):
            if part and part in '①②③④':
                buf = part; opts.setdefault(buf, '')
            elif buf is not None:
                opts[buf] += part

        stem, stmts, cur, prev = [], {}, None, ''
        for s in pre:
            g = STMT.match(s)
            wrapped = WRAPPED.search(prev)      # 直前の行が「…次のａ～」で切れている
            prev = s
            if g and not wrapped and g.group(1) not in stmts:
                cur = g.group(1); stmts[cur] = g.group(2)
            elif cur:
                stmts[cur] += s
            else:
                stem.append(s)

        questions[num] = dict(
            section=section,
            stem=tidy(''.join(stem)),
            statements={k: tidy(v) for k, v in sorted(stmts.items())},
            options={k: tidy(v) for k, v in sorted(opts.items())},
            note=tidy(''.join(notelines)))
    return questions


if __name__ == '__main__':
    db = []
    for kai, (era, year, label) in YEARS.items():
        qs = parse_exam(kai)
        for n in range(1, 51):
            q = qs[n]
            db.append(dict(id=f'K{kai:02d}-{n:02d}', kai=kai, era=era, year=year, label=label, num=n,
                           section=q['section'], sectionShort=SHORT[q['section']],
                           stem=q['stem'], statements=q['statements'],
                           options=q['options'], note=q['note'],
                           answer=ANSWERS[kai][n - 1]))
    json.dump(db, open('db_raw.json', 'w'), ensure_ascii=False, indent=1)
    print('total', len(db))
