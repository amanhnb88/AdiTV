import requests
import re
import os

def ambil_token(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://m.rctiplus.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
    }
    cookies = {
        'device_uuid': '2dbd0d2b-dc16-4b09-ba05-e0b4377948d9',
        'visitor_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aWQiOjAsInRva2VuIjoiMjM0OTM2NGE5ZTgzMjQ1NyIsInBsIjoibXdlYiIsImRldmljZV9pZCI6IjJkYmQwZDJiLWRjMTYtNGIwOS1iYTA1LWUwYjQzNzc5NDhkOSIsImx0eXBlIjoiIiwiaWF0IjoxNzcyMTU5NDMyfQ.F_CwnDc1Bpen9o7uJNTP1lCqwcHMbY48rZOftlRYLC0'
    }
    try:
        res = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        # Regex ini dibuat general agar bisa menangkap semua channel MNC
        match = re.search(r'(https://[a-zA-Z0-9\-\.]+\.rctiplus\.id/[a-zA-Z0-9\-]+\.m3u8\?auth_key=[a-zA-Z0-9\-]+)', res.text)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error saat mengambil dari {url}: {e}")
    return None

def update_all_channels():
    print("Memulai proses penarikan token...")
    
    # 1. Ambil token masing-masing
    rcti_url = ambil_token('https://m.rctiplus.com/tv/rcti')
    gtv_url = ambil_token('https://m.rctiplus.com/tv/gtv')
    # Kalau mau tambah MNCTV, cukup tambahkan baris ini:
    # mnctv_url = ambil_token('https://m.rctiplus.com/tv/mnctv')
    
    # 2. Siapkan wadah untuk teks M3U
    m3u_content = ""
    
    # 3. Cetak format RCTI jika token didapat
    if rcti_url:
        print(f"Berhasil mendapat token RCTI!")
        m3u_content += f"""#EXTINF:-1 tvg-id="RCTI" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/RCTI_logo.svg/1200px-RCTI_logo.svg.png" group-title="MNC Group", RCTI
#EXTVLCOPT:http-referrer=https://m.rctiplus.com/
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36
{rcti_url}\n
"""

    # 4. Cetak format GTV jika token didapat
    if gtv_url:
        print(f"Berhasil mendapat token GTV!")
        m3u_content += f"""#EXTINF:-1 tvg-id="GTV" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/GTV_logo_%282006%29.svg/1200px-GTV_logo_%282006%29.svg.png" group-title="MNC Group", GTV
#EXTVLCOPT:http-referrer=https://m.rctiplus.com/
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36
{gtv_url}\n
"""

    # 5. Tulis ulang ke dalam file streams/id.m3u
    # Pastikan foldernya ada
    os.makedirs('streams', exist_ok=True)
    
    with open('streams/id.m3u', 'w', encoding='utf-8') as file:
        file.write(m3u_content.strip())
        
    print("Selesai! File id.m3u berhasil ditulis ulang dengan token terbaru.")

if __name__ == "__main__":
    update_all_channels()
