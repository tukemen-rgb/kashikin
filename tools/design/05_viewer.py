# -*- coding: utf-8 -*-
"""design/ の各カードを1枚のページから見られるようにする。
   Claude Design の Design System ペインに並ぶのと同じ単位で切ってある。"""
import os, re, json, html

CARDS = []
for grp in ['foundations', 'components']:
    for f in sorted(os.listdir(f'design/{grp}')):
        src = open(f'design/{grp}/{f}', encoding='utf-8').read()
        m = re.match(r'<!--\s*@dsCard\s+(.*?)\s*-->', src)
        at = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1))) if m else {}
        CARDS.append({'path': f'{grp}/{f}', 'group': at.get('group', grp),
                      'name': at.get('name', f), 'sub': at.get('subtitle', ''),
                      'html': src})

DATA = json.dumps(CARDS, ensure_ascii=False)
nav = ''
last = None
for i, c in enumerate(CARDS):
    if c['group'] != last:
        nav += f'<div class="grp">{html.escape(c["group"])}</div>'
        last = c['group']
    nav += (f'<button class="nv" data-i="{i}"><span class="n">{html.escape(c["name"])}</span>'
            f'<span class="s">{html.escape(c["sub"])}</span></button>')

OUT = f'''<title>貸金業務取扱主任者 デザインシステム</title>
<style>
:root{{
  --pri:#0F7A3C; --hdr:#0A5A2C;
  --bg:#F1F2F4; --surface:#FFFFFF; --sunken:#EDEFF2;
  --ink:#14181D; --ink-2:#4E5560; --ink-3:#7C838F;
  --rule:#D4D8DE; --rule-2:#E3E6EA;
  --f:Meiryo,"メイリオ","Meiryo UI","Hiragino Sans","Noto Sans JP",sans-serif;
}}
@media (prefers-color-scheme:dark){{:root{{
  --pri:#4FC182; --hdr:#0B2318;
  --bg:#111419; --surface:#191D23; --sunken:#22272F;
  --ink:#E9ECF1; --ink-2:#A6ADB9; --ink-3:#79808C;
  --rule:#2E343D; --rule-2:#242931;
}}}}
:root[data-theme="dark"]{{
  --pri:#4FC182; --hdr:#0B2318;
  --bg:#111419; --surface:#191D23; --sunken:#22272F;
  --ink:#E9ECF1; --ink-2:#A6ADB9; --ink-3:#79808C;
  --rule:#2E343D; --rule-2:#242931;
}}
:root[data-theme="light"]{{
  --pri:#0F7A3C; --hdr:#0A5A2C;
  --bg:#F1F2F4; --surface:#FFFFFF; --sunken:#EDEFF2;
  --ink:#14181D; --ink-2:#4E5560; --ink-3:#7C838F;
  --rule:#D4D8DE; --rule-2:#E3E6EA;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--f);
     font-size:14px;line-height:1.7;-webkit-text-size-adjust:100%}}
button{{font:inherit;color:inherit;cursor:pointer}}
:focus-visible{{outline:2px solid var(--pri);outline-offset:2px}}
.top{{position:sticky;top:0;z-index:5;background:var(--hdr);color:#fff;
     border-bottom:2px solid #C6402A;display:flex;align-items:center;gap:10px;
     padding:8px 14px;min-height:48px}}
.top h1{{font-size:15.5px;font-weight:700;margin:0}}
.top .sub{{font-size:10.5px;opacity:.72;font-weight:400;display:block;margin-top:1px}}
.top .sp{{flex:1}}
.tb{{background:transparent;border:1px solid rgba(255,255,255,.34);border-radius:3px;
    padding:5px 9px;font-size:12.5px;color:#fff;white-space:nowrap}}
.tb:hover{{background:rgba(255,255,255,.12)}}
.lay{{display:grid;grid-template-columns:246px minmax(0,1fr);
     height:calc(100vh - 50px);height:calc(100dvh - 50px)}}
nav{{border-right:1px solid var(--rule);background:var(--surface);overflow-y:auto;padding-bottom:20px}}
.grp{{font-size:10.5px;color:var(--ink-3);padding:14px 14px 6px;letter-spacing:.06em}}
.nv{{display:block;width:100%;text-align:left;background:none;border:none;
    border-top:1px solid var(--rule-2);padding:9px 14px}}
.nv:hover{{background:var(--sunken)}}
.nv[aria-current="true"]{{background:var(--sunken);
    box-shadow:inset 4px 0 0 var(--pri)}}
.nv .n{{display:block;font-size:13.5px;font-weight:700;line-height:1.45}}
.nv .s{{display:block;font-size:10.5px;color:var(--ink-3);line-height:1.55;margin-top:1px}}
main{{overflow:hidden;background:var(--bg);display:flex;flex-direction:column}}
.meta{{padding:11px 16px;border-bottom:1px solid var(--rule);background:var(--surface)}}
.meta b{{font-size:14.5px}}
.meta code{{font-family:ui-monospace,monospace;font-size:11px;color:var(--ink-3);margin-left:9px}}
iframe{{flex:1;width:100%;border:none;background:var(--bg)}}
@media (max-width:720px){{
  .lay{{grid-template-columns:1fr;height:auto}}
  nav{{border-right:none;border-bottom:1px solid var(--rule);max-height:210px}}
  iframe{{height:78vh;flex:none}}
}}
</style>
<header class="top">
  <h1>貸金業務取扱主任者<span class="sub">デザインシステム ／ 過去問1000</span></h1>
  <div class="sp"></div>
  <button class="tb" id="tg" type="button">表示</button>
</header>
<div class="lay">
  <nav id="nav">{nav}</nav>
  <main><div class="meta" id="meta"></div><iframe id="fr" title="プレビュー"></iframe></main>
</div>
<script>
const CARDS={DATA};
const fr=document.getElementById('fr'),meta=document.getElementById('meta');
const btns=[...document.querySelectorAll('.nv')];
function show(i){{
  const c=CARDS[i];
  btns.forEach(b=>b.setAttribute('aria-current',String(+b.dataset.i===i)));
  meta.innerHTML='<b>'+c.name+'</b><code>'+c.path+'</code>';
  const t=document.documentElement.getAttribute('data-theme');
  fr.srcdoc=(t?'<script>document.documentElement.setAttribute("data-theme","'+t+'")<\\/script>':'')+c.html;
  try{{location.hash=c.path}}catch(e){{}}
}}
fr.addEventListener('load',()=>{{
  const t=document.documentElement.getAttribute('data-theme');
  const d=fr.contentDocument;
  if(d){{ if(t) d.documentElement.setAttribute('data-theme',t);
          else d.documentElement.removeAttribute('data-theme'); }}
}});
btns.forEach(b=>b.onclick=()=>show(+b.dataset.i));
const tg=document.getElementById('tg');
tg.onclick=()=>{{
  const cur=document.documentElement.getAttribute('data-theme')
    ||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light');
  document.documentElement.setAttribute('data-theme',cur==='dark'?'light':'dark');
  show(btns.findIndex(b=>b.getAttribute('aria-current')==='true')||0);
}};
const h=decodeURIComponent(location.hash.slice(1));
show(Math.max(0,CARDS.findIndex(c=>c.path===h)));

'''
OUT = OUT.rstrip() + '\n' + chr(60) + '/script' + chr(62) + '\n'
open('design/index.html', 'w', encoding='utf-8').write(OUT)
print('design/index.html', len(OUT), 'chars /', len(CARDS), 'cards')
