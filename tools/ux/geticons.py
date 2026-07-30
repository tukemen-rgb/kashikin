"""アイコンを 128px で落とす。色を見るだけなので小さくてよい。"""
import json, os, urllib.request, concurrent.futures as cf

ART = json.load(open('art.json'))
os.makedirs('icons', exist_ok=True)

def grab(kv):
    i, u = kv
    p = f'icons/{i}.jpg'
    if os.path.exists(p) and os.path.getsize(p) > 500:
        return 0
    u = u.replace('512x512bb', '128x128bb').replace('100x100bb', '128x128bb')
    try:
        d = urllib.request.urlopen(u, timeout=25).read()
        open(p, 'wb').write(d)
        return 1
    except Exception:
        return -1

with cf.ThreadPoolExecutor(16) as ex:
    r = list(ex.map(grab, [(k, v) for k, v in ART.items() if v]))
print('取得', r.count(1), '既存', r.count(0), '失敗', r.count(-1))
