import json, os, urllib.request, concurrent.futures as cf
UA = {'User-Agent': 'Mozilla/5.0 (design research)'}
URLS = json.load(open('shoturl_v3.json'))
jobs = [(i, us[0]) for i, us in URLS.items()]
def grab(j):
    i, u = j
    p = f'sa/{i}.webp'
    if os.path.exists(p) and os.path.getsize(p) > 2000: return 0
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as x:
            open(p, 'wb').write(x.read())
        return 1
    except Exception: return -1
with cf.ThreadPoolExecutor(16) as ex:
    r = list(ex.map(grab, jobs))
print('取得', r.count(1), '既存', r.count(0), '失敗', r.count(-1))
