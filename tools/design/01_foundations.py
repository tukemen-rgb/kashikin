# -*- coding: utf-8 -*-
"""app/template.html のトークンをそのまま切り出して、
   Claude Design（claude.ai/design）に push できるコンポーネント集を組む。

   各ファイルは1行目の <!-- @dsCard ... --> でペインのカードになる。
   トークンは template.html から機械的に写すので、二重管理にならない。
"""
import re, os, pathlib

SRC = open('app/template.html', encoding='utf-8').read()
CSS = SRC.split('<style>', 1)[1].split('</style>', 1)[0]
# :root 一式（ライト・ダーク・data-theme）と、サイズ指定までを丸ごと持ってくる
TOKENS = CSS.split('*{box-sizing:border-box}')[0].strip()

FRAME = """<!-- @dsCard group="{group}" name="{name}" subtitle="{sub}" -->
<style>
{tokens}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
     font-family:var(--gothic);font-size:14.5px;line-height:1.8;
     -webkit-text-size-adjust:100%}}
button,select{{font:inherit;color:inherit;cursor:pointer}}
:focus-visible{{outline:2px solid var(--pri-2);outline-offset:2px}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
.ds{{padding:20px 18px;display:flex;flex-direction:column;gap:18px;max-width:820px}}
.ds-h{{font-size:11px;letter-spacing:.06em;color:var(--ink-3);
      border-left:3px solid var(--pri);padding-left:8px;line-height:1.5}}
.ds-note{{font-size:11.5px;color:var(--ink-3);line-height:1.75}}
{css}
</style>
<div class="ds">
{body}
</div>
"""

def card(path, group, name, sub, css, body):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    open(path, 'w', encoding='utf-8').write(
        FRAME.format(group=group, name=name, sub=sub, tokens=TOKENS, css=css, body=body))
    return path


# ---------------------------------------------------------------- 色
SW = """
.pal{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:10px}
.sw{border:1px solid var(--rule);border-radius:var(--r);overflow:hidden;background:var(--surface)}
.sw .chip{height:70px;display:grid;place-items:center;font-size:12px;font-weight:700}
.sw .t{padding:9px 11px;display:flex;flex-direction:column;gap:2px}
.sw .nm{font-size:13.5px;font-weight:700}
.sw .hx{font-family:var(--mono);font-size:11px;color:var(--ink-3)}
.sw .us{font-size:11px;color:var(--ink-2);line-height:1.65}
.neu{display:flex;flex-wrap:wrap;gap:1px;border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.neu i{flex:1;min-width:74px;height:52px;display:grid;place-items:end center;
       font-family:var(--mono);font-size:9.5px;padding-bottom:4px;color:var(--ink-3)}
.secs4{display:flex;flex-direction:column;border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.secs4 div{display:grid;grid-template-columns:5px 1fr auto;gap:11px;align-items:center;
           background:var(--surface);padding:9px 13px;border-top:1px solid var(--rule-2);font-size:13.5px}
.secs4 div:first-child{border-top:none}
.secs4 i{width:5px;height:26px;display:block}
.secs4 b{font-weight:700}
.secs4 em{font-style:normal;font-family:var(--mono);font-size:11.5px;color:var(--ink-3)}
"""
FOUR = [('--pri', '深緑', '#0F7A3C', '操作するもの', 'ヘッダー・ボタン・リンク・選択中／法令'),
        ('--acc', '朱', '#C6402A', '先へ進む／誤り', '「次へ」「学習をはじめる」・不正解・着目語の下線・連続日数／貸付実務'),
        ('--ok', '紺', '#134E8C', 'できた', '正解・段位・XP・実績・到達度／資金需要者保護'),
        ('--vio', '紫', '#6A4A9C', 'あとで見直す', '復習の期日・付箋・頻出／財務会計')]
body = '<div class="ds-h">使う色は4つだけ</div><div class="pal">'
for v, nm, hx, mean, use in FOUR:
    body += (f'<div class="sw"><div class="chip" style="background:var({v});'
             f'color:var(--on-pri)">{mean}</div><div class="t"><span class="nm">{nm}</span>'
             f'<span class="hx">var({v})　{hx}</span><span class="us">{use}</span></div></div>')
body += '</div>'
body += ('<p class="ds-note">主色の深緑は、同ジャンル上位（宅建 #01843A・行政書士 #03843A・'
         'ITパスポート #279F00・公務員 #01602F）の実測値に合わせている。'
         '<code>--ng</code>（不正解）は朱、<code>--gold</code>（段位・実績）は紺の別名で、実体は4色。</p>')
body += '<div class="ds-h">4分野への割り当て</div><div class="secs4">'
for v, s, q in [('--sec1', '法令', '551問'), ('--sec2', '貸付実務', '290問'),
                ('--sec3', '資金需要者保護', '99問'), ('--sec4', '財務会計', '60問')]:
    body += f'<div><i style="background:var({v})"></i><b>{s}</b><em>{q}</em></div>'
body += '</div>'
body += '<div class="ds-h">地と文字</div><div class="neu">'
for v in ['--bg', '--surface', '--sunken', '--rule', '--rule-2', '--ink-4', '--ink-3', '--ink-2', '--ink']:
    body += f'<i style="background:var({v})">{v[2:]}</i>'
body += '</div><p class="ds-note">灰は主色の深緑にわずかに寄せた寒色。純粋な中間灰は使っていない。</p>'
card('design/foundations/color.html', 'Foundations', '配色', '深緑・朱・紺・紫の4色と4分野への割り当て', SW, body)


# ---------------------------------------------------------------- 文字
TY = """
.ty{display:flex;flex-direction:column;gap:13px;background:var(--surface);
    border:1px solid var(--rule);border-radius:var(--r);padding:16px 18px}
.ty>div{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
.ty .k{font-family:var(--mono);font-size:10.5px;color:var(--ink-3);width:112px;flex-shrink:0}
.qbox{background:var(--surface);border:1px solid var(--rule);border-radius:var(--r);padding:15px 17px}
.stem{font-family:var(--disp);font-size:var(--qsize);line-height:var(--qlh);
      letter-spacing:.015em;display:flex;flex-direction:column;gap:.42em}
.stem .s{text-indent:1em} .stem .s.lead{text-indent:0}
.stem .cue{border-bottom:2px solid var(--acc);font-weight:700;padding-bottom:1px}
.dim{color:var(--ink-4)}
"""
SPEC = [('h1 / 25px 700', '<span style="font-family:var(--disp);font-size:22px;font-weight:700">弱点診断</span>'),
        ('h2 / 13.5px 700', '<span style="font-size:13.5px;font-weight:700">足を引っ張っているところ</span>'),
        ('本文 / 14.5px', '<span>解答履歴から弱点と復習期日を見て出題します</span>'),
        ('設問 / 15.5px 1.95', '<span style="font-family:var(--disp);font-size:var(--qsize)">貸金業法第13条の2第2項に規定する</span>'),
        ('補足 / 11.5px', '<span style="font-size:11.5px;color:var(--ink-3)">20回中19回・計33問出ています</span>'),
        ('数字 / tabular', '<span style="font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:22px">0/1000</span>')]
body = ('<div class="ds-h">メイリオ1本。表示・本文・数字を書体で分けない</div><div class="ty">'
        + ''.join(f'<div><span class="k">{k}</span>{v}</div>' for k, v in SPEC) + '</div>'
        + '<p class="ds-note">日本語の資格試験アプリで確実に入っている書体がメイリオなので、'
        'ヒラギノ・Noto Sans JP へ落ちる場合も含めて1系統に統一している。'
        '数字が縦に揃う箇所はすべて <code>font-variant-numeric: tabular-nums</code>。</p>'
        '<div class="ds-h">長文の組み方（本文は一字も変えない）</div>'
        '<div class="qbox"><div class="stem">'
        '<span class="s lead">貸金業者であるＡ社は、Ｂとの間で貸付けに係る契約'
        '<span class="dim">（以下、本問において「本件貸付契約」という。）</span>を締結するに当たり、'
        'その内容が<span class="cue">適切でないもの</span>を1つだけ選びなさい。</span>'
        '<span class="s">なお、本問におけるすべての貸付けに係る契約は、住宅資金貸付契約ではないものとする。</span>'
        '</div></div>'
        '<p class="ds-note">括弧の外にある「。」で文を割って改行し、字下げする。'
        '定義の括弧書きは濃度を落とす。着目語は朱の下線。'
        '足す・削る・置き換えるは一切していない（全1000問で自動検証、不一致0件）。</p>')
card('design/foundations/type.html', 'Foundations', '文字', 'メイリオ1本のスケールと、長文設問の組み方', TY, body)


# ---------------------------------------------------------------- 形
SH = """
.sh{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.sh>div{background:var(--surface);border:1px solid var(--rule);padding:13px;
        display:flex;flex-direction:column;gap:5px}
.sh .box{height:44px;background:var(--pri-soft);border:1px solid var(--pri)}
.sh .k{font-family:var(--mono);font-size:10.5px;color:var(--ink-3)}
.sh .d{font-size:11.5px;color:var(--ink-2);line-height:1.6}
.dens{display:flex;flex-direction:column;background:var(--surface);
      border:1px solid var(--rule);border-radius:var(--r);overflow:hidden}
.dens div{padding:9px 13px;border-top:1px solid var(--rule-2);font-size:13.5px;
          display:flex;justify-content:space-between;align-items:center}
.dens div:first-child{border-top:none}
.dens em{font-style:normal;font-family:var(--mono);font-size:11.5px;color:var(--ink-3)}
"""
body = ('<div class="ds-h">角丸は2段階だけ</div><div class="sh">'
        '<div><div class="box" style="border-radius:var(--r)"></div>'
        '<span class="k">--r　4px</span><span class="d">面・カード・一覧の外枠</span></div>'
        '<div><div class="box" style="border-radius:var(--rs)"></div>'
        '<span class="k">--rs　3px</span><span class="d">ボタン・選択肢・入力</span></div>'
        '<div><div class="box" style="border-radius:0"></div>'
        '<span class="k">0</span><span class="d">一覧の行・分野の色帯</span></div>'
        '<div><div class="box" style="border-radius:50%;width:44px;margin:0 auto"></div>'
        '<span class="k">50%</span><span class="d">曜日の丸だけ</span></div></div>'
        '<p class="ds-note"><code>box-shadow</code> は全廃。面は1pxの罫線だけで区切る。'
        'グラデーションも使わない。実在の過去問アプリを並べて確認した共通点に合わせている。</p>'
        '<div class="ds-h">一覧の密度</div><div class="dens">'
        + ''.join(f'<div><span>{a}</span><em>{b}</em></div>' for a, b in
                  [('行の上下余白', '9px'), ('行の左右余白', '13px'), ('行の区切り', '1px / --rule-2'),
                   ('分野の色帯', '5×26px'), ('カードの内側', '13px 15px')])
        + '</div><p class="ds-note">テーマ47件が1画面に流し込める密度を上限として決めた。</p>')
card('design/foundations/shape.html', 'Foundations', '形と密度', '角丸2段階・影なし・一覧の行の詰め方', SH, body)
print('foundations 3枚')
