"""スクショは縦長（高さ／幅 ≧ 1.4）。アイコンや宣伝画像は正方形か横長なので、
   縦横比だけで確実に分けられる。"""
import json, os, re
IDS = [str(a['id']) for a in json.load(open('apps.json'))]
PAT = re.compile(r'https://is\d-ssl\.mzstatic\.com/image/thumb/([^"\\\s]+?)/(\d+)x(\d+)[a-z]{1,3}\.(?:png|jpg|jpeg|webp)')
out = {}
for i in IDS:
    p = f'pages/{i}.html'
    if not os.path.exists(p):
        continue
    h = open(p, encoding='utf-8', errors='ignore').read()
    seen, keep = set(), []
    for base, w, hh in PAT.findall(h):
        w, hh = int(w), int(hh)
        if w == 0 or hh/w < 1.4:            # 正方形＝アイコン、横長＝宣伝画像
            continue
        if base in seen:
            continue
        seen.add(base)
        keep.append(f'https://is1-ssl.mzstatic.com/image/thumb/{base}/460x0w.webp')
    if keep:
        out[i] = keep[:2]
json.dump(out, open('shoturl_v3.json', 'w'))
print('スクショURLあり:', len(out), '/', len(IDS))
