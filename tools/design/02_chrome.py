# -*- coding: utf-8 -*-
"""コンポーネント側。CSSは app/template.html の該当ルールをそのまま抜いて使う。"""
import re, pathlib
exec(open('/tmp/claude-0/-home-user-kashikin/34f9ab86-5115-5c62-bcf8-a7df9b057b68/scratchpad/mkds.py',
          encoding='utf-8').read().split('# ------')[0])

def pull(*sel):
    """template.html の CSS から、指定セレクタで始まるルールだけを抜き出す。"""
    out = []
    for rule in re.findall(r'(?:^|\})\s*([^{}@/]+?)\{([^{}]*)\}', CSS, re.M):
        s = rule[0].strip()
        if any(s == x or s.startswith(x + ' ') or s.startswith(x + ':')
               or s.startswith(x + '[') or s.startswith(x + ',') or (',' + x) in ',' + s.replace(' ', '')
               for x in sel):
            out.append(f'{s}{{{rule[1]}}}')
    return '\n'.join(out)

# --------------------------------------------------- ヘッダー
css = pull('.top', '.brand', '.tbtn', '.counter', '.timer', '.combo') + """
.top{position:static}
"""
body = ('<div class="ds-h">ホーム</div>'
        '<header class="top"><button class="brand" type="button">貸金業務取扱主任者'
        '<span class="sub">過去問1000 ／ 第1〜20回</span></button>'
        '<div class="spacer"></div><button class="tbtn" type="button">表示</button></header>'
        '<div class="ds-h">演習中</div>'
        '<header class="top"><button class="brand" type="button">貸金業務取扱主任者</button>'
        '<div class="spacer"></div><span class="counter"><b>7</b> / 20</span>'
        '<span class="combo">4連正解</span>'
        '<button class="tbtn" type="button">読みやすさ</button>'
        '<button class="tbtn" type="button">中断</button></header>'
        '<div class="ds-h">模試（残り時間つき）</div>'
        '<header class="top"><button class="brand" type="button">貸金業務取扱主任者</button>'
        '<div class="spacer"></div><span class="timer">残り 12:04</span>'
        '<span class="timer warn">残り 0:48</span>'
        '<button class="tbtn" type="button">中断</button></header>'
        '<p class="ds-note">ヘッダーは主色より一段濃い深緑のベタ塗り（<code>--hdr</code>）に朱の下罫。'
        '中の操作は枠線だけの透明ボタンで、白抜き文字を主役から外さない。</p>')
card('design/components/header.html', 'Components', 'ヘッダーバー', 'ホーム／演習中／模試の3状態', css, body)

# --------------------------------------------------- ボタン
css = pull('.cta', '.next', '.ghost', '.tbtn', '.dgo', '.after', '.setrow') + """
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.bar-demo{background:var(--surface);border:1px solid var(--rule);border-radius:var(--r);padding:8px 14px}
.bar-demo .inner{display:flex;gap:8px;align-items:center}
.bar-demo .spacer{flex:1}
"""
body = ('<div class="ds-h">主動線（1画面に1つだけ）</div>'
        '<button class="cta">学習をはじめる</button>'
        '<div class="ds-h">演習中の下部バー</div>'
        '<div class="bar-demo"><div class="inner">'
        '<button class="ghost">前へ</button><button class="ghost" aria-pressed="true">付箋</button>'
        '<span class="spacer"></span><button class="next">次へ</button></div></div>'
        '<div class="ds-h">解答後の枝分かれ</div>'
        '<div class="after"><button>似ている問題 5問</button>'
        '<button>「総量規制・過剰貸付けの禁止」をまとめて</button>'
        '<button disabled>貸金業法第13条の2</button></div>'
        '<div class="ds-h">診断からの導線</div><div class="row"><button class="dgo">この型だけ演習する</button></div>'
        '<div class="ds-h">出題条件</div>'
        '<div class="setrow">'
        '<label><span class="lb">問題数</span><select><option>20問</option></select></label>'
        '<label><span class="lb">出題の狙い</span><select><option>おまかせ（弱点＋復習）</option></select></label>'
        '<label><span class="lb">範囲</span><select><option>全1000問</option></select></label></div>'
        '<p class="ds-note">朱は「先へ進む」だけに使う。ホームの「学習をはじめる」と演習中の「次へ」が'
        'それに当たり、同じ画面に2つ出ることはない。'
        '付箋は押されているあいだ紫（あとで見直す）。</p>')
card('design/components/buttons.html', 'Components', 'ボタン', '主動線・下部バー・解答後の枝分かれ・出題条件', css, body)

# --------------------------------------------------- タグ
css = pull('.tag', '.qmeta', '.dk') + """
.dk{display:inline-block}
"""
body = ('<div class="ds-h">設問の見出しに付くもの</div>'
        '<div class="qmeta"><span class="tag sec" style="background:var(--sec1)">法令</span>'
        '<span class="tag">第7回 問22</span><span class="tag">単純択一</span>'
        '<span class="tag neg">否定形</span></div>'
        '<div class="qmeta"><span class="tag theme">総量規制・過剰貸付けの禁止</span>'
        '<span class="tag hot">頻出</span><span class="tag">2回目・誤1</span></div>'
        '<div class="ds-h">4分野</div><div class="qmeta">'
        + ''.join(f'<span class="tag sec" style="background:var(--sec{i})">{s}</span>'
                  for i, s in [(1, '法令'), (2, '貸付実務'), (3, '資金需要者保護'), (4, '財務会計')])
        + '</div>'
        '<div class="ds-h">診断カードの種別</div><div class="qmeta">'
        '<span class="dk">テーマ</span>　<span class="dk">引っかけ</span>　'
        '<span class="dk">読み方</span>　<span class="dk">形式</span></div>'
        '<p class="ds-note">分野のタグだけがベタ塗り。ほかは枠線のみで、'
        '否定形は朱、頻出は紫。ベタ塗りを1種類に絞ることで、'
        'どれが分野なのかを色を覚えなくても判別できる。</p>')
card('design/components/tags.html', 'Components', 'タグ', '分野・出題形式・否定形・頻出・診断の種別', css, body)
print('components 3枚')
