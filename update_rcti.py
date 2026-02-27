import requests
import json
import re
import os
import sys
import uuid

# Daftar channel dengan ID API yang baru kita temukan dan Logo Resmi yang sudah diperbaiki
CHANNELS = [
    {"api_id": 1, "name": "RCTI", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/RCTI.png"},
    {"api_id": 2, "name": "MNCTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"},
    {"api_id": 3, "name": "GTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"},
    {"api_id": 4, "name": "iNews", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/iNews.png"}
]

def update_m3u_file():
    print("🚀 Memulai proses update token via API Internal (Jalur VIP)...")
    
    user_agent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
    
    # Menggunakan Session() agar bot kita bisa menyimpan "Cookie" layaknya browser HP
    session = requests.Session()
    
    # 1. Langkah Pertama: Memancing Server untuk memberikan Token JWT
    print("[*] Memancing Token JWT (Surat Izin) dari server...")
    jwt_token = None
    try:
        session.get("https://m.rctiplus.com/", headers={'User-Agent': user_agent}, timeout=15)
        # Ambil token dari cookie yang tersimpan otomatis
        jwt_token = session.cookies.get('visitor_token')
        
        if not jwt_token:
            print("    [!] Cookie tidak ditemukan, menggunakan token cadangan...")
            jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aWQiOjAsInRva2VuIjoiMjM0OTM2NGE5ZTgzMjQ1NyIsInBsIjoibXdlYiIsImRldmljZV9pZCI6IjJkYmQwZDJiLWRjMTYtNGIwOS1iYTA1LWUwYjQzNzc5NDhkOSIsImx0eXBlIjoiIiwiaWF0IjoxNzcyMTU5NDMyfQ.F_CwnDc1Bpen9o7uJNTP1lCqwcHMbY48rZOftlRYLC0"
        else:
            print("    [✓] Sukses mendapatkan Token JWT baru!")
    except Exception as e:
        print(f"    [X] Error saat mengambil token: {e}")
        jwt_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aWQiOjAsInRva2VuIjoiMjM0OTM2NGE5ZTgzMjQ1NyIsInBsIjoibXdlYiIsImRldmljZV9pZCI6IjJkYmQwZDJiLWRjMTYtNGIwOS1iYTA1LWUwYjQzNzc5NDhkOSIsImx0eXBlIjoiIiwiaWF0IjoxNzcyMTU5NDMyfQ.F_CwnDc1Bpen9o7uJNTP1lCqwcHMbY48rZOftlRYLC0"

    # 2. Menyiapkan Kunci untuk Membuka Pintu API
    api_headers = {
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://m.rctiplus.com',
        'Referer': 'https://m.rctiplus.com/',
        'apikey': 'jFFhGYfZzrEgaPIGmFOVttQzCNbvqJHb', # Kunci statis dari hasil intaianmu
        'authorization': jwt_token # Kunci dinamis (KTP)
    }

    playlist_content = "#EXTM3U\n"
    links_found = 0
    # Membuat ID perangkat palsu agar terlihat natural
    dummy_device_id = str(uuid.uuid4())

    for ch in CHANNELS:
        print(f"[*] Menembus API untuk channel {ch['name']} (ID: {ch['api_id']})...")
        api_url = f"https://toutatis.rctiplus.com/video/live/api/v1/live/{ch['api_id']}/url?appierid={dummy_device_id}"
        
        try:
            res_api = session.get(api_url, headers=api_headers, timeout=15)
            
            if res_api.status_code == 200:
                data = res_api.json()
                
                # Menggunakan regex untuk mencari m3u8 di dalam tumpukan JSON
                match = re.search(r'(https://[^"\'\s<>]+\.m3u8[^"\'\s<>]*)', json.dumps(data))
                
                if match:
                    # Bersihkan jika ada format \/
                    stream_url = match.group(1).replace('\\/', '/')
                    print(f"    [✓] Berhasil mengekstrak link video {ch['name']}!")
                    links_found += 1
                    
                    # Menyusun M3U untuk dibaca di aplikasimu
                    playlist_content += f'#EXTINF:-1 tvg-id="{ch["name"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="TV Nasional", {ch["name"]}\n'
                    playlist_content += f'#EXTVLCOPT:http-referrer=https://m.rctiplus.com/\n'
                    playlist_content += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
                    playlist_content += f'{stream_url}\n'
                else:
                    print(f"    [!] Pintu terbuka, tapi link m3u8 tidak ada di dalam data JSON.")
            else:
                print(f"    [X] Gagal. API Menolak. Status HTTP: {res_api.status_code}")
                print(f"    [X] Pesan dari server: {res_api.text}")
                
        except Exception as e:
            print(f"    [X] Error koneksi saat memproses {ch['name']}: {e}")

    # 3. Tahap Akhir: Simpan file id.m3u
    if links_found > 0:
        os.makedirs('streams', exist_ok=True)
        with open('streams/id.m3u', 'w', encoding='utf-8') as file:
            file.write(playlist_content)
        print(f"\n✅ Selesai! Berhasil meretas {links_found} channel lewat API.")
    else:
        print("\n❌ GAGAL TOTAL: Tidak ada satupun link yang berhasil di-extract.")
        sys.exit(1)

if __name__ == "__main__":
    update_m3u_file()
