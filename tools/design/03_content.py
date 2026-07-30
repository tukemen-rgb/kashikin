# -*- coding: utf-8 -*-
import re, pathlib
exec(open('/tmp/claude-0/-home-user-kashikin/34f9ab86-5115-5c62-bcf8-a7df9b057b68/scratchpad/mkds.py',
          encoding='utf-8').read().split('# ------')[0])
exec(open('/tmp/claude-0/-home-user-kashikin/34f9ab86-5115-5c62-bcf8-a7df9b057b68/scratchpad/mkds2.py',
          encoding='utf-8').read().split('# ---------------------------------------------------')[0]
     .split('exec(')[0])

def pull(*sel):
    out = []
    for rule in re.findall(r'(?:^|\})\s*([^{}@/]+?)\{([^{}]*)\}', CSS, re.M):
        s = rule[0].strip()
        if any(s == x or s.startswith(x + ' ') or s.startswith(x + ':')
               or s.startswith(x + '[') or s.startswith(x + ',') or (',' + x) in ',' + s.replace(' ', '')
               for x in sel):
            out.append(f'{s}{{{rule[1]}}}')
    return '\n'.join(out)

# --------------------------------------------------- 一覧の行
css = pull('.secs', '.secrow', '.topics', '.trow', '.list', '.li')
body = ('<div class="ds-h">分野別</div><div class="secs">'
        + ''.join(f'''<button class="secrow"><span class="swatch" style="background:var(--sec{i})"></span>
        <span class="body"><span class="nm">{s}</span>
        <span class="track"><i style="width:{p}%;background:var(--sec{i})"></i></span></span>
        <span class="val">{d}/{t}<br><em>{a}</em></span></button>'''
                  for i, s, d, t, p, a in [(1, '法令', 355, 551, 64, '68%'), (2, '貸付実務', 170, 290, 59, '67%'),
                                           (3, '資金需要者保護', 59, 99, 60, '70%'), (4, '財務会計', 36, 60, 60, '63%')])
        + '</div>'
        '<div class="ds-h">テーマ（全47件）</div><div class="topics">'
        + ''.join(f'''<button class="trow"><span class="tsec" style="background:var(--sec{i})"></span>
        <span class="tbody"><span class="tn">{n}</span><span class="tart">{art}</span></span>
        <span class="f">{q}問<br><em>{k}回で出題</em></span>
        <span class="acc" style="color:var(--{c})">{a}</span>
        <span class="tbar"><i style="width:{w}%;background:var(--sec{i})"></i></span></button>'''
                  for i, n, art, q, k, a, c, w in [
                      (1, '総量規制・過剰貸付けの禁止', '貸金業法第13条の2（過剰貸付け等の禁止）', 72, 20, '63%', 'acc', 78),
                      (1, '契約締結時の書面', '貸金業法第17条（契約締結時の書面の交付）', 52, 20, '70%', 'ok', 66),
                      (2, '意思表示・代理・行為能力', '', 53, 19, '67%', 'acc', 48),
                      (4, '貸借対照表', '', 12, 11, '86%', 'ok', 34)])
        + '</div>'
        '<div class="ds-h">解答の履歴</div><div class="list">'
        + ''.join(f'<div class="li"><span class="id">{i}</span>'
                  f'<span class="ans"><span class="{c}">{m}</span></span>'
                  f'<span class="tx">{t}</span></div>'
                  for i, c, m, t in [('第7回 問22', 'no', '誤 ②→④', '個人顧客の利益の保護に支障を生ずることが…'),
                                     ('第3回 問30', 'yes', '正 ①', '期限に関する次の①〜④の記述のうち…')])
        + '</div>'
        '<p class="ds-note">行は角を立てたまま1pxの罫線で区切る。左端の5px帯が分野で、'
        '行の下端の細い帯が到達度。カードを浮かせず、1画面に入る件数を稼ぐ。</p>')
card('design/components/list-rows.html', 'Components', '一覧の行', '分野別・テーマ47件・解答履歴', css, body)

# --------------------------------------------------- 設問
css = pull('.stem', '.dim', '.opts', '.opt', '.mark', '.verdict', '.note', '.qtable', '.traps') + """
:root[data-dim="off"] .dim{color:inherit}
"""
STEM = ('<div class="stem"><span class="s lead">貸金業法第13条の2第2項に規定する個人顧客の利益の保護に'
        '支障を生ずることがない契約として内閣府令で定めるもの'
        '<span class="dim">（以下、本問において「個人顧客の利益の保護に支障を生ずることがない契約」という。）</span>'
        'に該当するか否かに関する次の①〜④の記述のうち、その内容が'
        '<span class="cue">適切でないもの</span>を1つだけ選び、解答欄にその番号をマークしなさい。</span></div>')
body = ('<div class="ds-h">解答前</div>' + STEM +
        '<div class="opts">'
        '<button class="opt"><span class="m">①</span><span class="bd">'
        '個人顧客を相手方とする不動産の建設もしくは購入に必要な資金に係る契約は、'
        '個人顧客の利益の保護に支障を生ずることがない契約に該当しない。</span></button>'
        '<button class="opt"><span class="m">②</span><span class="bd">'
        '売却を予定している個人顧客の不動産の売却代金により弁済される貸付けに係る契約であって、'
        '当該個人顧客の返済能力を超えないと認められるもの。</span></button></div>'
        '<div class="ds-h">解答後</div>'
        '<div class="verdict ng"><span class="r">不正解</span>'
        '<span class="a">正答 ①　選択 ②　0:41</span></div>'
        '<div class="opts">'
        '<button class="opt correct" disabled><span class="m">①</span><span class="bd">'
        '個人顧客を相手方とする不動産の建設もしくは購入に必要な資金に係る契約。</span>'
        '<svg class="mark" viewBox="0 0 40 40" style="--len:100">'
        '<circle cx="20" cy="20" r="15"/></svg></button>'
        '<button class="opt wrong picked" disabled><span class="m">②</span><span class="bd">'
        '売却を予定している個人顧客の不動産の売却代金により弁済される貸付けに係る契約。</span>'
        '<svg class="mark" viewBox="0 0 40 40" style="--len:40">'
        '<path d="M9 9 L31 31"/><path class="s2" d="M31 9 L9 31"/></svg></button></div>'
        '<div class="ds-h">この問題で狙われている点</div>'
        '<div class="traps"><div class="tl">この問題で狙われている点</div>'
        '<div class="ti"><b>含む・含まない</b>「含まれる」と「含まれない」の入れ替えです。'
        '定義に何が入って何が入らないかを、境界の例で押さえてください。</div></div>'
        '<p class="ds-note">正解は紺、不正解は朱。〇と✕はどちらも朱で手書き風に引く'
        '（日本の採点は〇も✕も赤ペンなので、色では区別しない）。'
        '本文は原文のまま。改行・濃度・下線だけで読みやすさを作る。</p>')
card('design/components/question.html', 'Components', '設問', '解答前・解答後・引っかけの提示', css, body)

# --------------------------------------------------- 記述ａ〜ｄ
css = pull('.stmts', '.stmt', '.tally', '.stem', '.dim')
body = ('<div class="ds-h">記述ａ〜ｄに○×を付けながら整理する</div>'
        '<div class="stmts">'
        '<div class="stmt" data-v="o"><button class="mk" data-stmt="ａ">○</button>'
        '<span class="bd">貸金業者は、貸付けに係る契約について、保証業者と保証契約を締結しようとする場合には、'
        'あらかじめ、当該保証業者に対し、書面を交付しなければならない。</span></div>'
        '<div class="stmt" data-v="x"><button class="mk" data-stmt="ｂ">×</button>'
        '<span class="bd">貸金業者は、その営業所ごとに、当該営業所に置かれる'
        '貸金業務取扱主任者の氏名を掲示することを要しない。</span></div>'
        '<div class="stmt"><button class="mk" data-stmt="ｃ">ｃ</button>'
        '<span class="bd">貸金業者は、極度方式基本契約を締結したときは、遅滞なく、'
        '内閣府令で定める事項を記載した書面を相手方に交付しなければならない。</span></div>'
        '<div class="stmt"><button class="mk" data-stmt="ｄ">ｄ</button>'
        '<span class="bd">個人顧客と連絡することができないことにより'
        '返済能力の調査を行うことができないときは、その旨を記録することを要しない。</span></div>'
        '</div><div class="tally">○ <b>1</b> ／ × 1 ／ 未 2</div>'
        '<p class="ds-note">個数問題・組合せ問題では、記述を1枚ずつのカードにして'
        '○×を切り替えられるようにしている。○の数がその場で出るので、'
        '「適切なものの個数」を数え直さずに済む。</p>')
card('design/components/statements.html', 'Components', '記述カード', 'ａ〜ｄに○×を付ける（個数・組合せ問題）', css, body)
print('components +3')
