import requests
import json
import re
import os
import sys
import uuid

# 1. CHANNEL DINAMIS (Scraping API RCTI+)
CHANNELS = [
    {"api_id": 1, "name": "RCTI", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/RCTI.png"},
    {"api_id": 2, "name": "MNCTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"},
    {"api_id": 3, "name": "GTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"},
    {"api_id": 4, "name": "iNews", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/iNews.png"}
]

# 2. CHANNEL STATIS (Link Alternatif yang sudah dites jalan)
STATIC_CHANNELS = [
    {
        "name": "Indosiar",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Indosiar_2014.svg/512px-Indosiar_2014.svg.png",
        "url": "https://warningfm.github.io/v3/live/str/id/575eeb9f08dc8db.m3u8"
    }
    # SCTV sementara kita nonaktifkan karena link komunitasnya mati (404)
]

def update_m3u_file():
    print("🚀 Memulai proses update token (Sistem Hybrid)...")
    
    user_agent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
    session = requests.Session()
    playlist_content = "#EXTM3U\n"
    links_found = 0

    # ==========================================
    # TAHAP 1: SCRAPING API RCTI+
    # ==========================================
    print("\n[*] TAHAP 1: Memproses Channel Grup RCTI+ ...")
    jwt_token = None
    try:
        session.get("https://m.rctiplus.com/", headers={'User-Agent': user_agent}, timeout=15)
        jwt_token = session.cookies.get('visitor_token')
        if not jwt_token:
            jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aWQiOjAsInRva2VuIjoiMjM0OTM2NGE5ZTgzMjQ1NyIsInBsIjoibXdlYiIsImRldmljZV9pZCI6IjJkYmQwZDJiLWRjMTYtNGIwOS1iYTA1LWUwYjQzNzc5NDhkOSIsImx0eXBlIjoiIiwiaWF0IjoxNzcyMTU5NDMyfQ.F_CwnDc1Bpen9o7uJNTP1lCqwcHMbY48rZOftlRYLC0"
    except Exception:
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aWQiOjAsInRva2VuIjoiMjM0OTM2NGE5ZTgzMjQ1NyIsInBsIjoibXdlYiIsImRldmljZV9pZCI6IjJkYmQwZDJiLWRjMTYtNGIwOS1iYTA1LWUwYjQzNzc5NDhkOSIsImx0eXBlIjoiIiwiaWF0IjoxNzcyMTU5NDMyfQ.F_CwnDc1Bpen9o7uJNTP1lCqwcHMbY48rZOftlRYLC0"

    api_headers = {
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://m.rctiplus.com',
        'Referer': 'https://m.rctiplus.com/',
        'apikey': 'jFFhGYfZzrEgaPIGmFOVttQzCNbvqJHb',
        'authorization': jwt_token
    }

    dummy_device_id = str(uuid.uuid4())

    for ch in CHANNELS:
        print(f"    [-] Menembus API: {ch['name']}...")
        api_url = f"https://toutatis.rctiplus.com/video/live/api/v1/live/{ch['api_id']}/url?appierid={dummy_device_id}"
        try:
            res_api = session.get(api_url, headers=api_headers, timeout=15)
            if res_api.status_code == 200:
                match = re.search(r'(https://[^"\'\s<>]+\.m3u8[^"\'\s<>]*)', json.dumps(res_api.json()))
                if match:
                    stream_url = match.group(1).replace('\\/', '/')
                    playlist_content += f'#EXTINF:-1 tvg-id="{ch["name"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="TV Nasional", {ch["name"]}\n'
                    playlist_content += f'#EXTVLCOPT:http-referrer=https://m.rctiplus.com/\n'
                    playlist_content += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
                    playlist_content += f'{stream_url}\n'
                    links_found += 1
        except Exception as e:
            print(f"    [X] Error koneksi: {e}")

    # ==========================================
    # TAHAP 2: INJECT CHANNEL STATIS (Indosiar)
    # ==========================================
    print("\n[*] TAHAP 2: Menyuntikkan Channel Statis Alternatif...")
    for static_ch in STATIC_CHANNELS:
        print(f"    [+] Menambahkan: {static_ch['name']}")
        playlist_content += f'#EXTINF:-1 tvg-id="{static_ch["name"]}" tvg-name="{static_ch["name"]}" tvg-logo="{static_ch["logo"]}" group-title="TV Nasional", {static_ch["name"]}\n'
        playlist_content += f'{static_ch["url"]}\n'
        links_found += 1

    # ==========================================
    # TAHAP 3: SIMPAN HASIL AKHIR
    # ==========================================
    if links_found > 0:
        os.makedirs('streams', exist_ok=True)
        with open('streams/id.m3u', 'w', encoding='utf-8') as file:
            file.write(playlist_content)
        print(f"\n✅ BERHASIL! File id.m3u telah diupdate dengan {links_found} total channel.")
    else:
        print("\n❌ GAGAL TOTAL: Tidak ada satupun link yang berhasil diproses.")
        sys.exit(1)

if __name__ == "__main__":
    update_m3u_file()
