"""pypdfium2（pypdf とは別の抽出エンジン）で公式PDFを読み直し、
   数字を除いた本文が完全に一致するかを全1000問で確認する。"""
import pypdfium2 as pdfium, json, re
DB=json.load(open('db.json')); BY={}
for q in DB: BY.setdefault(q['kai'],{})[q['num']]=q
def fold(s):
    s=re.sub(r'[\x00-\x1f]','',s)              # 未対応字形が制御文字で出る
    s=re.sub(r'/c269\d','',s); s=re.sub(r'/c\d+','',s)
    s=re.sub(r'[０-９Ａ-Ｚａ-ｚ]',lambda m:chr(ord(m.group())-0xFEE0),s)
    s=re.sub(r'[\s　]','',s)
    for a,b in [('〜','～'),('（','('),('）',')'),('，','、'),('％','%'),('−','-'),('–','-')]:
        s=s.replace(a,b)
    s=re.sub(r'[。、「」『』]','',s)
    return re.sub(r'[\d,.]','',s)              # 数字は別途検証するので除く
tot=hit=0; miss=[]
for kai in range(1,21):
    pdf=pdfium.PdfDocument(f'official/exam_paper_{kai}th.pdf')
    # 【問題…】を含むページは問1〜問50の順に並ぶので、順序で対応付ける
    pages=[]
    for i in range(len(pdf)):
        raw=pdf[i].get_textpage().get_text_range()
        if '【問題' in raw: pages.append(fold(raw))
    if len(pages)!=50: print(f'  !! 第{kai}回 問題ページ {len(pages)}枚')
    for n,q in BY[kai].items():
        if n>len(pages): miss.append((q['id'],'page','ページなし')); continue
        hay=pages[n-1]
        for k,v in list(q['options'].items())+list(q['statements'].items())+[('stem',q['stem'])]:
            f=fold(v)
            if len(f)<8: continue
            tot+=1
            if f in hay: hit+=1
            else: miss.append((q['id'],k,f[:60]))
print(f'pypdfium2 との照合：{hit}/{tot} 一致 ({hit/tot*100:.2f}%)   ※数字を除いた本文')
print(f'不一致 {len(miss)}件')
for m in miss[:15]: print('  ',m)
json.dump(miss,open('miss_pdfium.json','w'),ensure_ascii=False)
