import json,re,html,difflib
DB={q['id']:q for q in json.load(open('db.json'))}
def fold(s):
    s=html.unescape(s)
    s=re.sub(r'[０-９Ａ-Ｚａ-ｚ]',lambda m:chr(ord(m.group())-0xFEE0),s)
    s=re.sub(r'[\s　]','',s)
    s=s.replace('〜','～').replace('（','(').replace('）',')').replace('，','、').replace('％','%')
    s=re.sub(r'\(注\s*\d*\s*\)','',s)
    s=re.sub(r'[。、「」『』]','',s)
    return s
def theirs_text(path):
    t=open(path,encoding='utf-8',errors='replace').read()
    m=re.search(r'<div class="sect_problem">(.*?)<div class="sect_commentary">',t,re.S)
    seg=re.sub(r'<(script|style|form|select).*?</\1>','',m.group(1),flags=re.S)
    lines=[l.strip() for l in html.unescape(re.sub(r'<[^>]+>','\n',seg)).split('\n') if l.strip()]
    i=[k for k,l in enumerate(lines) if '訂正依頼' in l]
    e=[k for k,l in enumerate(lines) if l.startswith('解答する')]
    return fold(''.join(lines[(i[0]+1 if i else 0):(e[0] if e else len(lines))]))
def best(needle,hay):
    if needle in hay: return 1.0
    L=len(needle); bestr=0
    for st in range(0,max(1,len(hay)-L+1),8):
        r=difflib.SequenceMatcher(None,needle,hay[st:st+L+20]).ratio()
        if r>bestr: bestr=r
        if bestr>0.99: break
    return bestr
miss=[]; tot=0; exact=0
for kai in [14,15,16,17,18,19,20]:
    for n in range(1,51):
        qid=f'R{kai}-{n:02d}'; q=DB[qid]
        hay=theirs_text(f'third/{kai}-{n:02d}.html')
        fields=[('opt'+k,v) for k,v in q['options'].items()]+[('stmt'+k,v) for k,v in q['statements'].items()]
        for name,v in fields:
            f=fold(v)
            if len(f)<4: continue
            tot+=1
            if f in hay: exact+=1; continue
            r=best(f,hay)
            if r<0.97: miss.append((qid,name,round(r,3),f[:70]))
            else: exact+=1
print(f'選択肢・ａ〜ｄ記述 計{tot}項目を他社データ内に照合')
print(f'  完全一致または0.97以上で一致: {exact}項目 ({exact/tot*100:.2f}%)')
print(f'  要確認: {len(miss)}項目')
for m in miss[:15]: print('   ',m)
