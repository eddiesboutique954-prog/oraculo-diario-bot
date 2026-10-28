import sys
sys.stdout.reconfigure(encoding='utf-8')
from youtube.uploader import get_youtube_service

yt = get_youtube_service()
search = yt.search().list(part='id', forMine=True, type='video', maxResults=10, order='date').execute()
v_ids = [item['id']['videoId'] for item in search.get('items', [])]
if v_ids:
    v_res = yt.videos().list(part='snippet', id=','.join(v_ids)).execute()
    print("VIDEOS PUBLICADOS:")
    for idx, v in enumerate(v_res.get('items', []), 1):
        sn = v['snippet']
        # Convertir a hora Colombia (UTC-5)
        pub_utc = sn['publishedAt']
        print(f"{idx}. {pub_utc} UTC | {sn['title']}")
