"""data/*.json を app/template.html に流し込んで app/index.html を作る。
   単体で走らせても、tools/pipeline.py から呼んでも同じ結果になる。"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = lambda *p: os.path.join(ROOT, *p)
DB = json.load(open(D('data', 'questions.json'), encoding='utf-8'))

PASS={1:(30,'70.1%'),2:(30,'65.2%'),3:(33,'65.4%'),4:(31,'61.7%'),5:(30,'32.9%'),
      6:(27,'21.8%'),7:(29,'25.8%'),8:(30,'28.1%'),9:(30,'24.5%'),10:(31,'31.2%'),
      11:(30,'30.5%'),12:(34,'32.5%'),13:(32,'31.5%'),14:(29,'30.0%'),15:(33,'33.9%'),
      16:(31,'32.2%'),17:(28,'26.6%'),18:(31,'31.0%'),19:(30,'32.4%'),20:(31,'32.5%')}
seen={}
for q in DB: seen.setdefault(q['kai'],(q['era'],q['year'],q['label']))
META={'years':[{'kai':k,'era':seen[k][0],'year':seen[k][1],'label':seen[k][2],
                'pass':PASS[k][0],'rate':PASS[k][1]} for k in sorted(seen)]}
TOPICS=json.load(open(D('data','themes.json'),encoding='utf-8'))
TRAPS=json.load(open(D('data','traps.json'),encoding='utf-8'))
slim=[{k:v for k,v in q.items() if k not in ('section','era','year','label','laws')} for q in DB]
t=open(D('app','template.html'),encoding='utf-8').read()
j=lambda o: json.dumps(o,ensure_ascii=False,separators=(',',':'))
assert '/*__DATA__*/' in t and '/*__META__*/' in t
assert '/*__TOPICS__*/' in t
t=t.replace('/*__DATA__*/',j(slim)).replace('/*__META__*/',j(META)).replace('/*__TOPICS__*/',j(TOPICS)).replace('/*__TRAPS__*/',j(TRAPS))
open(D('app','index.html'),'w',encoding='utf-8').write(t)
print('questions',len(slim),'| topics',len(TOPICS),'| html chars',len(t))
