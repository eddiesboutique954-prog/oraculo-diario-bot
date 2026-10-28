import sys
sys.stdout.reconfigure(encoding='utf-8')
from youtube.uploader import get_youtube_service

yt = get_youtube_service()
search = yt.search().list(part='id', forMine=True, type='video', maxResults=8, order='date').execute()
v_ids = [item['id']['videoId'] for item in search.get('items', [])]

v_res = yt.videos().list(part='snippet,status,contentDetails', id=','.join(v_ids)).execute()
for v in v_res.get('items', []):
    sn = v['snippet']
    st = v['status']
    cd = v['contentDetails']
    print(f"ID: {v['id']}")
    print(f"Título: {sn['title']}")
    print(f"Duración: {cd.get('duration')}")
    print(f"Privacy: {st.get('privacyStatus')} | UploadStatus: {st.get('uploadStatus')} | RejectionReason: {st.get('rejectionReason')}")
    print(f"Publicado: {sn['publishedAt']}")
    print("-" * 50)
