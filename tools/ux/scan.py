"""全アプリの1枚目のスクショと、アイコンの両方で色みを測る。

   スクショは App Store 用に文字や背景が足されていることがあるので、
   端末画面がだいたい収まる中央帯だけを見る。
"""
import json, os, colorsys, statistics as st, collections
from PIL import Image

APPS = {str(a['id']): a for a in json.load(open('apps.json'))}
ICON = {r['id']: r for r in json.load(open('hue.json'))}

def read(p, crop_center=True):
    im = Image.open(p).convert('RGB')
    w, h = im.size
    if crop_center:                       # 上下の宣伝文と余白を落とす
        im = im
    im = im.resize((64, 112))
    chroma, hs, greens = 0, collections.Counter(), []
    for r, g, b in im.getdata():
        hh, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        if s < 0.22 or v < 0.14:
            continue
        chroma += 1
        d = hh*360
        hs[int(d)//10*10] += 1
        if 75 <= d < 165:
            greens.append((r, g, b))
    n = 64*112
    dom = max(hs.items(), key=lambda x: x[1])[0] if hs else None
    hexv = None
    if len(greens) >= 40:
        hexv = '#%02X%02X%02X' % tuple(int(st.median([c[j] for c in greens])) for j in range(3))
    return dict(chroma=chroma/n, green=(len(greens)/chroma if chroma else 0),
                dom=dom, hex=hexv)

rows = []
for i, a in APPS.items():
    p = f'sa/{i}.webp'
    if not (os.path.exists(p) and os.path.getsize(p) > 2000):
        continue
    try:
        m = read(p)
    except Exception:
        continue
    ic = ICON.get(i, {})
    rows.append({'id': i, 'name': a['name'], 'seller': a['seller'], 'genre': a['genre'],
                 'rating': a['rating'], 'ratings': a['ratings'], 'terms': a['terms'],
                 'released': a['released'], 'updated': a['updated'],
                 'iconGreen': ic.get('gshare', 0), 'iconDom': ic.get('dom'),
                 'uiChroma': round(m['chroma'], 3), 'uiGreen': round(m['green'], 3),
                 'uiDom': m['dom'], 'hex': m['hex']})
json.dump(rows, open('scan.json', 'w'), ensure_ascii=False)
print('測定できたアプリ:', len(rows))

def band(r):
    if r['uiChroma'] < .04: return 'ほぼ無彩色'
    if r['uiDom'] is None: return 'ほぼ無彩色'
    d = r['uiDom']
    return ('緑' if 75 <= d < 165 else '青緑' if 165 <= d < 195 else
            '青' if 195 <= d < 255 else '紫' if 255 <= d < 290 else
            '桃' if 290 <= d < 340 else '赤' if (d >= 340 or d < 15) else
            '橙' if 15 <= d < 45 else '黄')
c = collections.Counter(band(r) for r in rows)
print('\n■ 画面の基調色（1枚目のスクショ、彩度のある画素の最頻色相）')
for k, v in c.most_common():
    print(f'   {v:5}本  {v/len(rows)*100:5.1f}%  {k}')
g = [r for r in rows if band(r) == '緑' and r['uiGreen'] >= .45]
print('\n緑が基調と判定:', len(g), '／ うちアイコンも緑:',
      sum(1 for r in g if r['iconGreen'] >= .5))
