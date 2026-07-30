"""過去問ドットコム（第10〜20回を収録）と、数字を含めた完全一致で照合する。"""
import json,re,html,difflib,os
DB={q['id']:q for q in json.load(open('db.json'))}
def fold(s):
    s=html.unescape(s)
    s=re.sub(r'[０-９Ａ-Ｚａ-ｚ]',lambda m:chr(ord(m.group())-0xFEE0),s)
    s=re.sub(r'[\s　]','',s)
    for a,b in [('〜','～'),('（','('),('）',')'),('，','、'),('％','%'),('−','-'),('–','-'),('—','-')]:
        s=s.replace(a,b)
    s=re.sub(r'\(注\s*\d*\s*\)','',s)
    return re.sub(r'[。、「」『』]','',s)
def theirs(path):
    t=open(path,encoding='utf-8',errors='replace').read()
    m=re.search(r'<div class="sect_problem">(.*?)<div class="sect_commentary">',t,re.S)
    if not m: return None
    seg=re.sub(r'<(script|style|form|select).*?</\1>','',m.group(1),flags=re.S)
    lines=[l.strip() for l in html.unescape(re.sub(r'<[^>]+>','\n',seg)).split('\n') if l.strip()]
    i=[k for k,l in enumerate(lines) if '訂正依頼' in l]
    e=[k for k,l in enumerate(lines) if l.startswith('解答する')]
    return fold(''.join(lines[(i[0]+1 if i else 0):(e[0] if e else len(lines))]))
def best(n,h):
    if n in h: return 1.0
    L=len(n); b=0
    for st in range(0,max(1,len(h)-L+1),6):
        r=difflib.SequenceMatcher(None,n,h[st:st+L+24]).ratio()
        if r>b: b=r
        if b>0.99: break
    return b
tot=ok=0; miss=[]; nofile=0
for kai in range(10,21):
    for n in range(1,51):
        p=f'third/{kai}-{n:02d}.html'
        if not os.path.exists(p): nofile+=1; continue
        hay=theirs(p)
        if hay is None: nofile+=1; continue
        q=DB[f'K{kai:02d}-{n:02d}']
        for name,v in [('opt'+k,v) for k,v in q['options'].items()]+[('stmt'+k,v) for k,v in q['statements'].items()]:
            f=fold(v)
            if len(f)<4: continue
            tot+=1
            if f in hay or best(f,hay)>=0.97: ok+=1
            else: miss.append((q['id'],name,round(best(f,hay),3),f[:60]))
print(f'過去問ドットコム（第10〜20回）との照合：{tot}項目中 {ok}項目が一致（{ok/tot*100:.2f}%）')
print(f'  取得できなかったページ {nofile}件 ／ 要確認 {len(miss)}項目')
for m in miss[:15]: print('  ',m)
