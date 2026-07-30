"""4,554本のアプリのアイコンURLを iTunes Lookup で引き直す。"""
import json, urllib.request, time, os

APPS = json.load(open('apps.json'))
ids = [str(a['id']) for a in APPS]
out = {}
if os.path.exists('art.json'):
    out = json.load(open('art.json'))

for i in range(0, len(ids), 180):
    chunk = [x for x in ids[i:i+180] if x not in out]
    if not chunk:
        continue
    u = 'https://itunes.apple.com/lookup?country=jp&id=' + ','.join(chunk)
    for attempt in range(4):
        try:
            r = json.loads(urllib.request.urlopen(u, timeout=40).read())
            break
        except Exception as e:
            print('retry', i, e); time.sleep(2 * (attempt + 1))
    else:
        continue
    for a in r.get('results', []):
        out[str(a['trackId'])] = a.get('artworkUrl512') or a.get('artworkUrl100') or ''
    print(i, len(out), flush=True)
    time.sleep(0.35)

json.dump(out, open('art.json', 'w'))
print('アイコンURL取得:', len(out), '/', len(ids))
