import sys, json, os, requests
sys.stdout.reconfigure(encoding='utf-8')

# 1. YouTube Stats
from youtube.uploader import get_youtube_service

yt = get_youtube_service()
res = yt.channels().list(part='snippet,statistics', mine=True).execute()
channel = res['items'][0]
stats = channel['statistics']

print("=========================================")
print("📊 REPORTE EN VIVO DEL CANAL YOUTUBE")
print("=========================================")
print(f"Canal: {channel['snippet']['title']}")
print(f"Suscriptores actuales: {stats.get('subscriberCount')}")
print(f"Total Videos: {stats.get('videoCount')}")
print(f"Vistas totales registradas: {stats.get('viewCount')}")

search = yt.search().list(part='id', forMine=True, type='video', maxResults=15, order='date').execute()
v_ids = [item['id']['videoId'] for item in search.get('items', [])]
if v_ids:
    v_res = yt.videos().list(part='snippet,statistics', id=','.join(v_ids)).execute()
    print("\nDesglose de Videos:")
    total_views = 0
    total_likes = 0
    for v in v_res.get('items', []):
        st = v['statistics']
        sn = v['snippet']
        views = int(st.get('viewCount', 0))
        likes = int(st.get('likeCount', 0))
        total_views += views
        total_likes += likes
        print(f" - [{sn['publishedAt'][:16].replace('T', ' ')}] {sn['title'][:45]}... | 👁️ {views} vistas | 👍 {likes} likes")
    print(f"\nSuma total real de vistas en los videos: {total_views}")
    print(f"Suma total real de likes: {total_likes}")

# 2. GitHub Actions Cron Check (12:00 PM Colombia)
print("\n=========================================")
print("🤖 ESTADO DE GITHUB ACTIONS (12:00 PM)")
print("=========================================")
token = os.environ.get("GITHUB_TOKEN", "")
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
repo = 'eddiesboutique954-prog/oraculo-diario-bot'

r_runs = requests.get(f'https://api.github.com/repos/{repo}/actions/runs', headers=headers)
runs = r_runs.json().get('workflow_runs', [])[:5]
for r in runs:
    print(f"Run #{r['id']} | Creado: {r['created_at'][:19].replace('T', ' ')} UTC | Estado: {r['status']} | Conclusión: {r['conclusion']}")
