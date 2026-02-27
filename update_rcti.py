import requests
import re
import os
import sys

API_KEY = "jFFhGYfZzrEgaPIGmFOVttQzCNbvqJHb"

# ================================================================
# ⚠️ PENTING: KAMU WAJIB MENGGANTI TOKEN DI BAWAH INI DENGAN YANG BARU
# Buka web m.rctiplus.com di browser, inspect element, cari visitor_token baru
# ================================================================
AUTH_TOKEN = "eyJ0eXAiOiJK... (GANTI DENGAN TOKEN KAMU YANG MASIH HIDUP)"

CHANNELS = [
    {"id": "1", "name": "RCTI", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/RCTI_logo_2015.svg/512px-RCTI_logo_2015.svg.png"},
    {"id": "2", "name": "MNCTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"},
    {"id": "3", "name": "GTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"},
    {"id": "4", "name": "iNews", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/iNews.png"}
]

def update_m3u_file():
    print("🚀 Memulai proses update token MNC Group via API...")
    
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
                
                # 💡 TAMBAHAN BARU: Memasukkan Referer DAN User-Agent agar terbaca oleh App.js kamu
                playlist_content += f'#EXTVLCOPT:http-referrer=https://m.rctiplus.com/\n'
                playlist_content += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
                
                playlist_content += f'{stream_url}\n'
            else:
                print(f"    [!] Gagal. Token mungkin expired!")
                
        except Exception as e:
            print(f"    [X] Error: {e}")
    
    # SAFETY CHECK
    if links_found > 0:
        os.makedirs('streams', exist_ok=True)
        with open('streams/id.m3u', 'w', encoding='utf-8') as file:
            file.write(playlist_content)
        print("\n✅ Berhasil memperbarui playlist!")
    else:
        print("\n❌ GAGAL TOTAL: Token kedaluwarsa. File m3u lama tidak dihapus.")
        sys.exit(1)

if __name__ == "__main__":
    update_m3u_file()
