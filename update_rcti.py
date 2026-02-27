import requests
import re
import os
import sys

API_KEY = "jFFhGYfZzrEgaPIGmFOVttQzCNbvqJHb"

CHANNELS = [
    {"id": "1", "name": "RCTI", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/RCTI_logo_2015.svg/512px-RCTI_logo_2015.svg.png"},
    {"id": "2", "name": "MNCTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"},
    {"id": "3", "name": "GTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"},
    {"id": "4", "name": "iNews", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/iNews.png"}
]

def get_fresh_token():
    """Fungsi ajaib untuk mengambil token RCTI terbaru secara otomatis"""
    print("[*] Mencoba mengambil token baru secara otomatis dari web...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
    }
    try:
        session = requests.Session()
        res = session.get('https://m.rctiplus.com/', headers=headers, timeout=10)
        
        # 1. Coba ambil dari Cookies
        token = session.cookies.get('visitor_token')
        if token:
            print("    [✓] Token berhasil didapatkan dari Cookie!")
            return token
            
        # 2. Coba ambil dari dalam teks HTML (sebagai cadangan)
        match = re.search(r'(eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+)', res.text)
        if match:
            print("    [✓] Token berhasil diekstrak dari HTML!")
            return match.group(1)
            
        print("    [!] Gagal menemukan token secara otomatis.")
        return None
    except Exception as e:
        print(f"    [X] Error saat mengambil token: {e}")
        return None

def update_m3u_file():
    print("🚀 Memulai proses update token MNC Group via API...")
    
    # 1. AMBIL TOKEN OTOMATIS
    AUTH_TOKEN = get_fresh_token()
    
    if not AUTH_TOKEN:
        print("\n❌ FATAL: Tidak dapat mengambil token baru. Proses dihentikan.")
        sys.exit(1)
    
    user_agent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
    
    headers = {
        'accept': 'application/json',
        'apikey': API_KEY,
        'authorization': AUTH_TOKEN,
        'user-agent': user_agent
    }
    
    playlist_content = "#EXTM3U\n"
    links_found = 0 
    
    for ch in CHANNELS:
        print(f"[*] Menghubungi API untuk {ch['name']}...")
        api_url = f"https://toutatis.rctiplus.com/video/live/api/v1/live/{ch['id']}/url?appierid=8d357e4a-f0b7-432f-ad9f-9610ac2f3afc"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            match = re.search(r'(https://[^"\'\s]+\.m3u8[^"\'\s]*)', response.text)
            
            if match:
                stream_url = match.group(1)
                print(f"    [✓] Sukses mendapatkan link!")
                links_found += 1
                
                # Merakit format M3U
                playlist_content += f'#EXTINF:-1 tvg-id="{ch["name"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="TV Nasional", {ch["name"]}\n'
                
                # Memasukkan Referer DAN User-Agent agar terbaca oleh App.js kamu
                playlist_content += f'#EXTVLCOPT:http-referrer=https://m.rctiplus.com/\n'
                playlist_content += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
                
                playlist_content += f'{stream_url}\n'
            else:
                print(f"    [!] Gagal. Response API menolak token.")
                
        except Exception as e:
            print(f"    [X] Error: {e}")
    
    # SAFETY CHECK
    if links_found > 0:
        os.makedirs('streams', exist_ok=True)
        with open('streams/id.m3u', 'w', encoding='utf-8') as file:
            file.write(playlist_content)
        print("\n✅ Berhasil memperbarui playlist!")
    else:
        print("\n❌ GAGAL TOTAL: API menolak request. File m3u lama tidak dihapus.")
        sys.exit(1)

if __name__ == "__main__":
    update_m3u_file()
