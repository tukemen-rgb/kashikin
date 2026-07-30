# -*- coding: utf-8 -*-
import re, pathlib
exec(open('/tmp/claude-0/-home-user-kashikin/34f9ab86-5115-5c62-bcf8-a7df9b057b68/scratchpad/mkds.py',
          encoding='utf-8').read().split('# ------')[0])
def pull(*sel):
    out=[]
    for rule in re.findall(r'(?:^|\})\s*([^{}@/]+?)\{([^{}]*)\}', CSS, re.M):
        s=rule[0].strip()
        if any(s==x or s.startswith(x+' ') or s.startswith(x+':') or s.startswith(x+'[')
               or s.startswith(x+',') or (','+x) in ','+s.replace(' ','') for x in sel):
            out.append(f'{s}{{{rule[1]}}}')
    return '\n'.join(out)

# --------------------------------------------------- 診断
css = pull('.dlist', '.dcard', '.dh', '.dk', '.dt', '.dv', '.dbar', '.dm', '.dtip', '.dgo')
def dcard(kind, title, pc, n, ng, avg, tip, weak=True):
    c = 'var(--acc)' if weak else 'var(--ok)'
    return (f'<div class="dcard{"" if weak else " good"}"><div class="dh">'
            f'<span class="dk">{kind}</span><span class="dt">{title}</span>'
            f'<span class="dv" style="color:{c}">{pc}<small>%</small></span></div>'
            f'<div class="dbar"><i style="width:{pc}%;background:{c}"></i>'
            f'<b style="left:{avg}%"></b></div>'
            f'<div class="dm">{n}回解答／{ng}回不正解　全体平均は {avg}%</div>'
            f'<p class="dtip">{tip}</p><button class="dgo">この型だけ演習する</button></div>')
body = ('<div class="ds-h">足を引っ張っているところ</div><div class="dlist">'
        + dcard('引っかけ', '義務か任意か', 27, 56, 41, 61,
                '「しなければならない」と「することができる」の入れ替えです。'
                '条文が義務を課しているのか、できる規定にすぎないのかを分けて覚えてください。')
        + dcard('読み方', '「適切でないもの」を選ぶ問題', 52, 149, 72, 61,
                '否定形の設問で落としています。設問の最後まで読んでから選択肢に入ってください。')
        + dcard('テーマ', '契約締結時の書面', 88, 34, 4, 61,
                'このテーマは過去20回中20回・計52問出ています。根拠は貸金業法第17条'
                '（契約締結時の書面の交付）です。ここは維持できています。', weak=False)
        + '</div>'
        '<p class="ds-note">縦の細い棒が全体平均。自分の値が平均の左にあるものだけを'
        '「足を引っ張っているところ」として、差の大きい順に並べる。'
        '文章は生成せず、引っかけの型ごとに用意した固定の着眼点と、'
        '自分の正誤の集計だけで組み立てている。</p>')
card('design/components/diagnosis.html', 'Components', '弱点診断', '引っかけの型・テーマ・読み方の5軸', css, body)

# --------------------------------------------------- 進み具合
css = pull('.rankbar', '.rankseal', '.xpbar', '.badges', '.badge', '.matrix', '.cell',
           '.pass', '.gauge', '.days', '.day', '.srow', '.weeks', '.wk', '.streak')
cells = ''
import itertools
for kai, row in [(1, [(1,100),(2,100),(3,100),(4,100),(0,None)]),
                 (2, [(1,72),(2,55),(3,80),(4,0),(0,64)]),
                 (3, [(1,48),(2,33),(3,None),(4,None),(0,41)])]:
    cells += f'<tr><th class="row">{kai}</th>'
    for sec, p in row:
        v = f'var(--sec{sec})' if sec else 'var(--pri)'
        if p is None:
            cells += '<td><button class="cell">10</button></td>'
        else:
            pf = ' perfect' if p == 100 else ''
            cells += (f'<td><button class="cell has{pf}" style="background:{v};'
                      f'opacity:{0.28+0.72*p/100:.2f}">{p}%</button></td>')
    cells += '</tr>'
body = ('<div class="ds-h">段位とXP</div>'
        '<div class="rankbar"><div class="rankseal"><span>五級</span></div>'
        '<div class="meta"><div class="x"><span><b>1180</b> XP</span>'
        '<span>次は 四級 まであと <b>220</b></span><span>解答済 <b>340</b>/1000</span>'
        '<span>正答率 <b>62%</b></span></div>'
        '<span class="xpbar"><i style="width:62%"></i></span></div></div>'
        '<div class="ds-h">続ける</div><div class="streak">'
        '<div class="days">'
        + ''.join(f'<div class="day"><div class="w">{w}</div>'
                  f'<div class="d{" on" if o else ""}{" today" if t else ""}">{"✓" if o else ""}</div></div>'
                  for w, o, t in [('金',1,0),('土',1,0),('日',1,0),('月',1,0),('火',1,0),('水',1,0),('木',1,1)])
        + '</div><div class="srow">'
        '<div><div class="n">9</div><div class="l">連続日数</div></div>'
        '<div><div class="n">14</div><div class="l">自己ベスト</div></div>'
        '<div><div class="n">8<span style="font-size:12px;color:var(--ink-3)">/20</span></div>'
        '<div class="l">今日</div></div></div>'
        '<div class="weeks">'
        + ''.join(f'<div class="wk"><i style="height:{h}px"></i><span class="t">{l}</span></div>'
                  for h, l in [(6,'6/11'),(14,'6/18'),(28,'6/25'),(33,'7/2'),(24,'7/9'),(38,'7/16'),(30,'7/23'),(40,'7/30')])
        + '</div></div>'
        '<div class="ds-h">合格可能性の目安</div>'
        '<div class="pass"><div class="hd">'
        '<span class="pc" style="color:var(--ok)">62<span style="font-size:16px">%</span></span>'
        '<span class="lb">今の実力で50問なら 推定 32.4点</span></div>'
        '<span class="gauge"><i style="width:62%;background:var(--ok)"></i></span>'
        '<p class="note">分野別の正答率（延べ679回の解答）をもとに、本番の分野構成 27/15/5/3 で'
        '50問解いたときの得点分布を推定し、合格基準点31問を超える確率を計算しています。</p></div>'
        '<div class="ds-h">到達度</div>'
        '<table class="matrix"><colgroup><col class="lab"><col><col><col><col>'
        '<col class="tot"></colgroup><thead><tr><th class="row"></th>'
        '<th>法令</th><th>貸付<br>実務</th><th>資金<br>需要者</th><th>財務<br>会計</th><th>計</th>'
        f'</tr></thead><tbody>{cells}</tbody></table>'
        '<div class="ds-h">実績</div><div class="badges">'
        + ''.join(f'<div class="badge{" on" if o else ""}"><div class="bt">{t}</div>'
                  f'<div class="bd">{d}</div></div>'
                  for t, d, o in [('初挑戦','1問目に解答',1),('百問','100問に解答',1),
                                  ('一回完答','ある回の50問すべてに解答',1),
                                  ('千問走破','全1000問に解答',0),('模試五冠','5回分の模試に合格',0)])
        + '</div>'
        '<p class="ds-note">「できた」はすべて紺で統一している（段位の印・XPバー・実績・到達度・正解）。'
        '到達度の全問一発正解だけは4色すべての上に乗るため、色ではなく地色の縁取りで示す。</p>')
card('design/components/progress.html', 'Components', '進み具合', '段位・連続日数・合格可能性・到達度・実績', css, body)

# --------------------------------------------------- 初回起動
css = pull('.hero', '.why', '.ring', '.cta', '.setrow', '.streak', '.days', '.day',
           '.srow', '.secs', '.secrow', '.rankbar', '.rankseal', '.xpbar', '.h2')
body = ('<div class="ds-h">一度も解いていないとき</div>'
        '<div class="rankbar"><div class="rankseal"><span>十級</span></div>'
        '<div class="meta"><div class="x"><span><b>0</b> XP</span>'
        '<span>次は 九級 まであと <b>100</b></span><span>解答済 <b>0</b>/1000</span>'
        '<span>正答率 <b>—</b></span></div>'
        '<span class="xpbar"><i style="width:0%"></i></span></div></div>'
        '<div class="hero"><div class="why start">'
        '<svg class="ring" viewBox="0 0 60 60" aria-hidden="true">'
        '<circle class="bgc" cx="30" cy="30" r="26"/>'
        '<circle class="fg" cx="30" cy="30" r="26" transform="rotate(-90 30 30)"'
        ' stroke-dasharray="163.4 163.4"/><text x="30" y="36">20</text></svg>'
        '<div><div class="msg">まずは <b>20</b> 問から始めましょう</div>'
        '<div class="sub">解答履歴から弱点と復習期日を見て出題します</div></div></div>'
        '<button class="cta">学習をはじめる</button></div>'
        '<h2 class="h2">続ける</h2><div class="streak"><div class="days">'
        + ''.join(f'<div class="day"><div class="w">{w}</div>'
                  f'<div class="d{" today" if t else ""}"></div></div>'
                  for w, t in [('金',0),('土',0),('日',0),('月',0),('火',0),('水',0),('木',1)])
        + '</div><p class="hint">解いた日にチェックが付きます。今日が1日目です。</p></div>'
        '<div class="ds-h">今日の目標を達成したとき</div>'
        '<div class="hero"><div class="why start met">'
        '<svg class="ring" viewBox="0 0 60 60" aria-hidden="true">'
        '<circle class="bgc" cx="30" cy="30" r="26"/>'
        '<circle class="fg" cx="30" cy="30" r="26" transform="rotate(-90 30 30)"'
        ' stroke-dasharray="163.4 163.4"/><text x="30" y="37" style="font-size:22px">✓</text></svg>'
        '<div><div class="msg">今日の目標 <b>20</b> 問は達成済みです</div>'
        '<div class="sub">そのまま続けることもできます</div></div></div></div>'
        '<div class="ds-h">復習の期日が来ているとき</div>'
        '<div class="hero"><div class="why">'
        '<svg class="ring" viewBox="0 0 60 60" aria-hidden="true">'
        '<circle class="bgc" cx="30" cy="30" r="26"/>'
        '<circle class="fg" cx="30" cy="30" r="26" transform="rotate(-90 30 30)"'
        ' stroke-dasharray="163.4 163.4"/><text x="30" y="36">340</text></svg>'
        '<div><div class="msg">復習の期日が来た問題が <b>340</b> 問あります</div>'
        '<div class="sub">忘れかけた頃に出し直すのがいちばん定着します</div></div></div></div>'
        '<p class="ds-note">記録がないときは、0 を朱で出したり空の棒グラフを立てたりしない。'
        'これから始める状態は主色の深緑、復習が溜まっている状態だけ紫にする。'
        '達成したときはリングを閉じて 0 ではなく ✓ を出す。</p>')
card('design/components/empty-state.html', 'Components', '状態', '初回起動・目標達成・復習が溜まったとき', css, body)
print('components +3')
