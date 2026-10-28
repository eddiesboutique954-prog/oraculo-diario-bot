import sys
sys.stdout.reconfigure(encoding='utf-8')
from youtube.uploader import get_youtube_service

yt = get_youtube_service()
search = yt.search().list(part='id', forMine=True, type='video', maxResults=50, order='date').execute()
v_ids = [item['id']['videoId'] for item in search.get('items', [])]

v_res = yt.videos().list(part='snippet,statistics,contentDetails', id=','.join(v_ids)).execute()

print(f"{'FECHA':<16} | {'VISTAS':<7} | {'DUR':<6} | TÍTULO")
print("-" * 80)
for v in v_res.get('items', []):
    sn = v['snippet']
    st = v['statistics']
    cd = v['contentDetails']
    views = int(st.get('viewCount', 0))
    pub = sn['publishedAt'][:16].replace('T', ' ')
    dur = cd.get('duration', '').replace('PT', '').replace('S', 's').replace('M', 'm')
    title = sn['title']
    print(f"{pub:<16} | {views:<7} | {dur:<6} | {title}")
