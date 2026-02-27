import requests
import re
import os
import sys

# ==========================================
# KONFIGURASI API (SAMA SEPERTI TERMUX)
# ==========================================
API_KEY = "jFFhGYfZzrEgaPIGmFOVttQzCNbvqJHb"

# PENTING: Pastikan Token ini adalah token yang masih aktif!
AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aWQiOjAsInRva2VuIjoiMjM0OTM2NGE5ZTgzMjQ1NyIsInBsIjoibXdlYiIsImRldmljZV9pZCI6IjJkYmQwZDJiLWRjMTYtNGIwOS1iYTA1LWUwYjQzNzc5NDhkOSIsImx0eXBlIjoiIiwiaWF0IjoxNzcyMTU5NDMyfQ.F_CwnDc1Bpen9o7uJNTP1lCqwcHMbY48rZOftlRYLC0"

# Daftar ID Channel MNC Group
CHANNELS = [
    {"id": "1", "name": "RCTI", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/RCTI_logo_2015.svg/512px-RCTI_logo_2015.svg.png"},
    {"id": "2", "name": "MNCTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"},
    {"id": "3", "name": "GTV", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"},
    {"id": "4", "name": "iNews", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/iNews.png"}
]

def update_m3u_file():
    print("🚀 Memulai proses update token MNC Group via API...")
    
    headers = {
        'accept': 'application/json',
        'apikey': API_KEY,
        'authorization': AUTH_TOKEN,
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
    }
    
    playlist_content = "#EXTM3U\n"
    links_found = 0 # Penghitung keberhasilan
    
    for ch in CHANNELS:
        print(f"[*] Menghubungi API untuk {ch['name']} (ID: {ch['id']})...")
        api_url = f"https://toutatis.rctiplus.com/video/live/api/v1/live/{ch['id']}/url?appierid=8d357e4a-f0b7-432f-ad9f-9610ac2f3afc"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            
            # Mencari URL m3u8 dari response JSON/Teks API
            match = re.search(r'(https://[^"\'\s]+\.m3u8[^"\'\s]*)', response.text)
            
            if match:
                stream_url = match.group(1)
                print(f"    [✓] Sukses mendapatkan link {ch['name']}!")
                links_found += 1
                
                # Merakit format M3U
                playlist_content += f'#EXTINF:-1 tvg-id="{ch["name"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="TV Nasional", {ch["name"]}\n'
                playlist_content += f'#EXTVLCOPT:http-referrer=https://m.rctiplus.com/\n'
                playlist_content += f'{stream_url}\n'
            else:
                print(f"    [!] Gagal menemukan link untuk {ch['name']}. Apakah token expired?")
                print(f"    [Debug] Respons API: {response.text[:100]}...")
                
        except Exception as e:
            print(f"    [X] Terjadi error koneksi saat memproses {ch['name']}: {e}")
    
    # ==========================================
    # SAFETY CHECK: Jangan timpa file kalau gagal total!
    # ==========================================
    if links_found > 0:
        os.makedirs('streams', exist_ok=True)
        m3u_path = 'streams/id.m3u'
        with open(m3u_path, 'w', encoding='utf-8') as file:
            file.write(playlist_content)
        print(f"\n✅ Selesai! Berhasil memperbarui {links_found} channel ke dalam {m3u_path}.")
    else:
        print("\n❌ GAGAL TOTAL: Tidak ada satu pun link yang ditemukan!")
        print("📁 File id.m3u yang lama TIDAK dihapus/ditimpa untuk mencegah playlist kosong.")
        print("⚠️ Solusi: Silakan update variabel AUTH_TOKEN di skrip ini dengan token terbaru dari browser Anda.")
        sys.exit(1) # Memaksa GitHub Actions berhenti dengan status Error

if __name__ == "__main__":
    update_m3u_file()
