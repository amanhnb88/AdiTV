import requests
import re
import os

# Daftar lengkap channel MNC Group beserta halamannya
CHANNELS = [
    {
        "name": "RCTI",
        "page_url": "https://m.rctiplus.com/tv/rcti",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/RCTI_logo_2015.svg/512px-RCTI_logo_2015.svg.png"
    },
    {
        "name": "MNCTV",
        "page_url": "https://m.rctiplus.com/tv/mnctv",
        "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/MNCTV.png"
    },
    {
        "name": "GTV",
        "page_url": "https://m.rctiplus.com/tv/gtv",
        "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/GTV.png"
    },
    {
        "name": "iNews",
        "page_url": "https://m.rctiplus.com/tv/inews",
        "logo": "https://static.rctiplus.id/media/300/files/fta_rcti/Channel_Logo/iNews.png"
    }
]

def update_m3u_file():
    print("🚀 Memulai proses update token MNC Group (RCTI, MNCTV, GTV, iNews)...")
    
    # Menyamar sebagai browser HP agar tidak diblokir
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://m.rctiplus.com/'
    }
    
    # Kerangka awal file M3U
    playlist_content = "#EXTM3U\n"
    
    # Looping / Iterasi untuk setiap channel
    for ch in CHANNELS:
        print(f"[*] Mengekstrak link untuk {ch['name']}...")
        try:
            response = requests.get(ch['page_url'], headers=headers, timeout=10)
            
            # Sangat Penting: Seringkali URL di dalam HTML di-escape (misal: https:\/\/1s1...). 
            # Kita bersihkan dulu garis miring terbalik (\) nya.
            html_text = response.text.replace('\\/', '/')
            
            # Regex Sapu Jagat: Mencari link yang berawalan https, berakhiran m3u8, dan memiliki parameter auth_key
            match = re.search(r'(https://[^"\'\s]+\.m3u8\?auth_key=[a-zA-Z0-9\-]+)', html_text)
            
            if match:
                stream_url = match.group(1)
                print(f"    [✓] Berhasil menemukan token baru!")
                
                # Merakit format M3U
                playlist_content += f'#EXTINF:-1 tvg-id="{ch["name"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="TV Nasional", {ch["name"]}\n'
                
                # Menambahkan tag VLC untuk mengirim referer (berguna untuk beberapa pemutar video)
                playlist_content += f'#EXTVLCOPT:http-referrer=https://m.rctiplus.com/\n'
                
                # Menambahkan URL streaming
                playlist_content += f'{stream_url}\n'
            else:
                print(f"    [!] Gagal menemukan link m3u8 untuk {ch['name']}. Struktur web mungkin berubah.")
                
        except Exception as e:
            print(f"    [X] Terjadi error saat memproses {ch['name']}: {e}")
    
    # Memastikan folder 'streams' ada
    os.makedirs('streams', exist_ok=True)
    m3u_path = 'streams/id.m3u'
    
    # Menyimpan dan menimpa file id.m3u dengan data terbaru
    with open(m3u_path, 'w', encoding='utf-8') as file:
        file.write(playlist_content)
        
    print(f"\n✅ Selesai! File {m3u_path} berhasil diperbarui dengan 4 channel.")

if __name__ == "__main__":
    update_m3u_file()
