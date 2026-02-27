import requests
import re
import os
import sys

# Daftar channel dan link halamannya
CHANNELS = [
    {"id": "rcti", "name": "RCTI", "url": "https://m.rctiplus.com/tv/rcti", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/RCTI_logo_2015.svg/512px-RCTI_logo_2015.svg.png"},
    {"id": "mnctv", "name": "MNCTV", "url": "https://m.rctiplus.com/tv/mnctv", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"},
    {"id": "gtv", "name": "GTV", "url": "https://m.rctiplus.com/tv/gtv", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"},
    {"id": "inews", "name": "iNews", "url": "https://m.rctiplus.com/tv/inews", "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/iNews.png"}
]

def update_m3u_file():
    print("🚀 Memulai proses update token via Web Scraping (Versi Update)...")
    
    # Header user-agent Android yang diperbarui agar lebih natural
    user_agent = 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
    
    headers = {
        'User-Agent': user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/' # Pura-pura datang dari pencarian Google
    }
    
    playlist_content = "#EXTM3U\n"
    links_found = 0
    
    for ch in CHANNELS:
        print(f"[*] Membedah halaman web {ch['name']}...")
        try:
            response = requests.get(ch['url'], headers=headers, timeout=15)
            # Tampilkan status HTTP untuk mengecek apakah koneksi berhasil atau diblokir
            print(f"    [-] Status HTTP: {response.status_code}")
            
            html_text = response.text.replace('\\/', '/')
            
            # Regex Fleksibel: Mengambil seluruh URL m3u8 dan segala parameter di belakangnya
            match = re.search(r'(https://[^"\'\s<>]+\.m3u8[^"\'\s<>]*)', html_text)
            
            if match:
                stream_url = match.group(1)
                print(f"    [✓] Sukses menemukan link m3u8!")
                links_found += 1
                
                playlist_content += f'#EXTINF:-1 tvg-id="{ch["name"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="TV Nasional", {ch["name"]}\n'
                playlist_content += f'#EXTVLCOPT:http-referrer=https://m.rctiplus.com/\n'
                playlist_content += f'#EXTVLCOPT:http-user-agent={user_agent}\n'
                playlist_content += f'{stream_url}\n'
            else:
                print(f"    [!] Gagal menemukan link m3u8. Struktur web mungkin berubah.")
                # Cetak 200 karakter pertama dari HTML untuk bahan analisa kita nanti
                print(f"    [!] Cuplikan HTML: {html_text[:200]}...")
                
        except Exception as e:
            print(f"    [X] Error koneksi saat memproses {ch['name']}: {e}")
            
    if links_found > 0:
        os.makedirs('streams', exist_ok=True)
        with open('streams/id.m3u', 'w', encoding='utf-8') as file:
            file.write(playlist_content)
        print(f"\n✅ Selesai! Berhasil mengekstrak {links_found} channel.")
    else:
        print("\n❌ GAGAL TOTAL: Tidak ada link yang ditemukan. File m3u lama aman.")
        sys.exit(1)

if __name__ == "__main__":
    update_m3u_file()
