"""4,554本すべての商品ページを取得する。アイコンが白でも画面が緑のことがあるため。"""
import json, os, re, urllib.request, concurrent.futures as cf, sys
UA = {'User-Agent': 'Mozilla/5.0 (design research)'}
IDS = [str(a['id']) for a in json.load(open('apps.json'))]
def page(i):
    p = f'pages/{i}.html'
    if os.path.exists(p) and os.path.getsize(p) > 20000:
        return 'skip'
    try:
        with urllib.request.urlopen(urllib.request.Request(
                f'https://apps.apple.com/jp/app/id{i}', headers=UA), timeout=30) as x:
            open(p, 'wb').write(x.read())
        return 'ok'
    except Exception:
        return 'err'
with cf.ThreadPoolExecutor(12) as ex:
    res = list(ex.map(page, IDS))
print({k: res.count(k) for k in set(res)}, flush=True)

SHOT = re.compile(r'https://is\d-ssl\.mzstatic\.com/image/thumb/[^"\\]+?/\d+x\d+bb\.(?:png|jpg|webp)')
urls = {}
for i in IDS:
    p = f'pages/{i}.html'
    if not os.path.exists(p): continue
    h = open(p, encoding='utf-8', errors='ignore').read()
    seen, keep = set(), []
    for m in SHOT.findall(h):
        b = m.rsplit('/', 1)[0]
        if b in seen: continue
        seen.add(b); keep.append(b + '/500x0w.webp')
    if keep: urls[i] = keep[:2]
json.dump(urls, open('shoturl_all.json', 'w'))
print('スクショURL:', len(urls), '/', len(IDS))
