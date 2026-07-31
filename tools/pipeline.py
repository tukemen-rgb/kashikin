# -*- coding: utf-8 -*-
"""公開の1歩手前まで、全部を作り直して検証する。

   このスクリプトは公開しない。dist/ に公開できる状態のものを置いて、
   何が通って何が落ちたかを dist/REPORT.md に書くところで止める。

     python3 tools/pipeline.py              全段
     python3 tools/pipeline.py --only app   1段だけ
     python3 tools/pipeline.py --skip docx  重い段を飛ばす
     python3 tools/pipeline.py --quiet      要約だけ

   終了コードは 0（全部通った）／1（1つでも落ちた）。ループから叩ける。
"""
from __future__ import annotations
import argparse, json, os, re, shutil, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = lambda *p: os.path.join(ROOT, *p)
DIST = D('dist')

# 検証で「これだけは落ちてはいけない」ものを、出力から拾う条件で書く。
#   name, 実行するコマンド, 出力に必ず含まれる文字列, 出てはいけない文字列
CHECKS = [
    ('verbatim', ['node', 'tools/test/t7.mjs'],
     ['不一致: 0件（完全一致）'], ['ERRORS: [']),
    ('exam',     ['node', 'tools/test/t8.mjs'],  ['ERRORS: none'], []),
    ('practice', ['node', 'tools/test/t9.mjs'],  ['ERRORS: none'], []),
    ('history',  ['node', 'tools/test/t10.mjs'], ['ERRORS: none'], []),
    ('mobile',   ['node', 'tools/test/t11.mjs'], ['ERRORS: none', '横溢れ: false'], []),
    ('themes',   ['node', 'tools/test/t12.mjs'], ['ERRORS: none'], []),
    ('diagnose', ['node', 'tools/test/t13.mjs'], ['ERRORS: none'], []),
]


class Stage:
    def __init__(self, key, title, fn, heavy=False):
        self.key, self.title, self.fn, self.heavy = key, title, fn, heavy
        self.status, self.detail, self.secs = 'skip', '', 0.0


def run(cmd, cwd=ROOT):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


# ---------------------------------------------------------------- 各段
def st_data():
    """公式PDFがあれば抽出からやり直す。無ければ data/ をそのまま使う。"""
    if not os.path.isdir(D('official')) or not [f for f in os.listdir(D('official')) if f.endswith('.pdf')]:
        n = len(json.load(open(D('data', 'questions.json'), encoding='utf-8')))
        return 'skip', f'official/ にPDFなし。既存の data/questions.json（{n}問）を使う'
    for s in ['parse.py', 'build.py', 'enrich.py', 'themes.py', 'traps.py']:
        code, out = run(['python3', D('tools', s)])
        if code:
            return 'fail', f'{s}: {out.strip().splitlines()[-1] if out.strip() else "異常終了"}'
    return 'ok', 'PDFから再抽出'


def st_integrity():
    """データそのものの筋が通っているか。アプリを作る前に落とす。"""
    Q = json.load(open(D('data', 'questions.json'), encoding='utf-8'))
    bad = []
    if len(Q) != 1000:
        bad.append(f'問題数が{len(Q)}（1000であるべき）')
    kai = {}
    for q in Q:
        kai[q['kai']] = kai.get(q['kai'], 0) + 1
    off = {k: v for k, v in kai.items() if v != 50}
    if off:
        bad.append(f'50問でない回: {off}')
    for q in Q:
        if not (isinstance(q['answer'], int) and 1 <= q['answer'] <= 4):
            bad.append(f'{q["id"]} の正答が不正')
        if len(q['options']) != 4:
            bad.append(f'{q["id"]} の選択肢が{len(q["options"])}個')
        if not q['stem'].strip():
            bad.append(f'{q["id"]} の設問が空')
    ids = [q['id'] for q in Q]
    if len(set(ids)) != len(ids):
        bad.append('IDが重複')
    themes = {t['name'] for t in json.load(open(D('data', 'themes.json'), encoding='utf-8'))}
    lost = {q['theme'] for q in Q} - themes
    if lost:
        bad.append(f'themes.json に無いテーマ: {sorted(lost)[:3]}')
    if bad:
        return 'fail', ' ／ '.join(bad[:4])
    return 'ok', f'{len(Q)}問・20回×50問・正答と選択肢と設問すべて充足'


def st_palette():
    """4分野の色が見分けられるか。目視では気づけないので機械で通す。"""
    code, out = run(['python3', D('tools', 'build', 'palette.py')])
    lines = [l.rstrip() for l in out.strip().splitlines() if l.strip()]
    if code:
        return 'fail', '\n'.join(lines)
    return 'ok', '\n'.join(lines)


def st_app():
    code, out = run(['python3', D('tools', 'build', 'inject.py')])
    if code:
        return 'fail', out.strip().splitlines()[-1] if out.strip() else '異常終了'
    kb = os.path.getsize(D('app', 'index.html')) // 1024
    return 'ok', f'app/index.html {kb}KB　（{out.strip()}）'


def st_design():
    for s in ['01_foundations.py', '02_chrome.py', '03_content.py', '04_state.py',
              '05_viewer.py', '06_sample_data.py', '07_sample_xlsx.py']:
        code, out = run(['python3', D('tools', 'design', s)])
        if code:
            return 'fail', f'{s}: {out.strip().splitlines()[-1] if out.strip() else "異常終了"}'
    n = len([f for g in ('foundations', 'components') for f in os.listdir(D('design', g))
             if f.endswith('.html')])
    return 'ok', f'カード{n}枚＋ビューア＋見本データ（JSON・XLSX）'


def st_docx():
    code, out = run(['node', D('tools', 'restore', 'make_docx.mjs')])
    if code:
        return 'fail', out.strip().splitlines()[-1] if out.strip() else '異常終了'
    code, out = run(['python3', D('tools', 'restore', 'verify.py')])
    if code or '不一致: 0件' not in out:
        return 'fail', out.strip().splitlines()[-1] if out.strip() else '検証に失敗'
    m = re.search(r'照合した項目: (\d+)', out)
    return 'ok', f'5年分250問／{m.group(1) if m else "?"}項目を照合、不一致0件'


def st_test():
    os.makedirs(D('dist', 'shots'), exist_ok=True)
    lines, ng = [], 0
    for name, cmd, need, forbid in CHECKS:
        t0 = time.time()
        code, out = run(cmd)
        okay = code == 0 and all(s in out for s in need) and not any(s in out for s in forbid)
        lines.append(('  ✓ ' if okay else '  ✗ ') + f'{name}　{time.time() - t0:.1f}s')
        if not okay:
            ng += 1
            tail = [l for l in out.strip().splitlines() if l.strip()][-3:]
            lines.append('      ' + ' / '.join(tail))
    detail = '\n'.join(lines)
    if ng:
        return 'fail', f'{len(CHECKS) - ng}/{len(CHECKS)} 通過\n{detail}'
    return 'ok', f'{len(CHECKS)}/{len(CHECKS)} 通過\n{detail}'


def st_shots():
    code, out = run(['node', D('tools', 'build', 'shots.mjs')])
    if code:
        return 'fail', out.strip().splitlines()[-1] if out.strip() else '異常終了'
    return 'ok', out.strip()


def st_stage():
    """公開できる一式を dist/ にそろえる。公開そのものはしない。"""
    os.makedirs(DIST, exist_ok=True)
    pairs = [(D('app', 'index.html'), 'app.html'),
             (D('design', 'index.html'), 'design-system.html'),
             (D('data', 'questions.json'), 'questions.json'),
             (D('data', 'questions.csv'), 'questions.csv'),
             (D('design', 'data', 'sample-questions.json'), 'sample-questions.json'),
             (D('design', 'data', 'sample-questions.xlsx'), 'sample-questions.xlsx')]
    put = []
    for src, dst in pairs:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DIST, dst))
            put.append(f'{dst} {os.path.getsize(src)//1024}KB')
    rd = D('restored')
    if os.path.isdir(rd):
        os.makedirs(os.path.join(DIST, 'restored'), exist_ok=True)
        for f in os.listdir(rd):
            shutil.copy2(os.path.join(rd, f), os.path.join(DIST, 'restored', f))
        put.append(f'restored/ {len(os.listdir(rd))}点')
    return 'ok', '　'.join(put)


STAGES = [
    Stage('data',      'データ（公式PDF → JSON）', st_data),
    Stage('integrity', 'データの整合性',            st_integrity),
    Stage('palette',   '分野色の識別性',            st_palette),
    Stage('app',       'アプリのビルド',            st_app),
    Stage('design',    'デザインシステムと見本データ', st_design),
    Stage('docx',      '5年分の .docx',             st_docx, heavy=True),
    Stage('test',      '回帰テスト',                st_test, heavy=True),
    Stage('shots',     'スクリーンショット',        st_shots, heavy=True),
    Stage('stage',     'dist/ にそろえる',          st_stage),
]


def report(stages, secs):
    ok = sum(1 for s in stages if s.status == 'ok')
    ng = [s for s in stages if s.status == 'fail']
    icon = {'ok': '✓', 'fail': '✗', 'skip': '—'}
    L = ['# ビルド結果', '',
         f'- 判定　**{"公開可" if not ng else "公開不可"}**',
         f'- 実行　{time.strftime("%Y-%m-%d %H:%M:%S")}　（{secs:.1f}秒）',
         f'- 段　　{ok} 通過 ／ {len(ng)} 失敗 ／ {len(stages) - ok - len(ng)} 省略', '',
         '| | 段 | 結果 |', '|---|---|---|']
    for s in stages:
        head = s.detail.split('\n')[0]
        if len(head) > 90:
            head = head[:88] + '…'
        L.append(f'| {icon[s.status]} | {s.title} | {head} |')
    for s in stages:
        if '\n' in s.detail:
            L += ['', f'### {s.title}', '```', s.detail, '```']
    L += ['', '## 公開の手順', '',
          '`dist/` の中身がそのまま公開できる状態です。**このスクリプトは公開しません。**', '',
          '| 出力 | 公開先 |', '|---|---|',
          '| `dist/app.html` | 学習アプリ（Artifact） |',
          '| `dist/design-system.html` | デザインシステム（Artifact） |',
          '| `dist/questions.json` `dist/questions.csv` | データセット |',
          '| `dist/sample-questions.*` | Claude Design に渡す見本 |',
          '| `dist/restored/` | 5年分の .docx |',
          '| `dist/shots/` | 実機サイズのスクリーンショット |', '']
    if ng:
        L += ['## 落ちた段', ''] + [f'- **{s.title}** — {s.detail.splitlines()[0]}' for s in ng] + ['']
    os.makedirs(DIST, exist_ok=True)
    open(os.path.join(DIST, 'REPORT.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', nargs='*', help='この段だけ走らせる')
    ap.add_argument('--skip', nargs='*', default=[], help='この段を飛ばす')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()

    todo = [s for s in STAGES
            if (not a.only or s.key in a.only) and s.key not in a.skip]
    t0 = time.time()
    for s in todo:
        st = time.time()
        if not a.quiet:
            print(f'▶ {s.title}', flush=True)
        try:
            s.status, s.detail = s.fn()
        except Exception as e:
            s.status, s.detail = 'fail', f'{type(e).__name__}: {e}'
        s.secs = time.time() - st
        if not a.quiet:
            print({'ok': '  ✓', 'fail': '  ✗', 'skip': '  —'}[s.status],
                  s.detail.split('\n')[0], f'（{s.secs:.1f}s）', flush=True)
            if '\n' in s.detail:
                print('\n'.join(s.detail.split('\n')[1:]), flush=True)
    secs = time.time() - t0
    report(todo, secs)

    ng = [s for s in todo if s.status == 'fail']
    print()
    print('判定:', '公開可' if not ng else f'公開不可（{len(ng)}段が失敗）',
          f'／ {secs:.1f}秒 ／ dist/REPORT.md')
    return 1 if ng else 0


if __name__ == '__main__':
    sys.exit(main())
