import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from youtube.uploader import get_youtube_service

yt = get_youtube_service()

# 1. Datos generales del canal
res = yt.channels().list(part='snippet,statistics', mine=True).execute()
channel = res['items'][0]
stats = channel['statistics']

print("=== 📊 ESTADO ACTUAL DEL CANAL ===")
print("Nombre:", channel['snippet']['title'])
print("Suscriptores:", stats.get('subscriberCount'))
print("Total Videos:", stats.get('videoCount'))
print("Vistas totales registradas por YouTube:", stats.get('viewCount'))

# 2. Obtener todos los videos subidos
search = yt.search().list(part='id', forMine=True, type='video', maxResults=50, order='date').execute()
v_ids = [item['id']['videoId'] for item in search.get('items', [])]

if v_ids:
    v_res = yt.videos().list(part='snippet,statistics,status', id=','.join(v_ids)).execute()
    print("\n=== 🎬 DETALLE DE VIDEOS PUBLICADOS ===")
    total_views = 0
    total_likes = 0
    total_comments = 0
    for idx, v in enumerate(v_res.get('items', []), 1):
        st = v['statistics']
        sn = v['snippet']
        status = v['status']
        views = int(st.get('viewCount', 0))
        likes = int(st.get('likeCount', 0))
        comments = int(st.get('commentCount', 0))
        total_views += views
        total_likes += likes
        total_comments += comments
        privacy = status.get('privacyStatus', 'unknown')
        pub = sn['publishedAt'][:16].replace('T', ' ')
        title = sn['title'][:48]
        print(f"{idx:2d}. [{pub}] {views:5d} vistas | {likes:3d} likes | {comments:2d} com | [{privacy.upper()}] | {title}")
    
    print("\n=========================================")
    print(f"Total vistas reales sumadas: {total_views}")
    print(f"Total likes reales sumados: {total_likes}")
    print(f"Total comentarios: {total_comments}")
    print("=========================================")
