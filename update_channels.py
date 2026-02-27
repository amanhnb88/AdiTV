import requests
import re
import os

def update_all_channels():
    print("Memulai proses pembaruan token saluran MNC Group...")
    
    # 1. Pastikan file m3u tersedia
    m3u_path = 'streams/id.m3u'
    if not os.path.exists(m3u_path):
        print(f"File {m3u_path} tidak ditemukan! Pastikan path-nya benar.")
        return

    # Baca seluruh isi file m3u ke dalam memori
    with open(m3u_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 2. Persiapkan Headers dan Cookies yang seragam
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

    # ==========================================
    # 3. PROSES UPDATE RCTI
    # ==========================================
    try:
        print("Mencari token RCTI...")
        res_rcti = requests.get('https://m.rctiplus.com/tv/rcti', headers=headers, cookies=cookies, timeout=10)
        match_rcti = re.search(r'(https://[a-zA-Z0-9\-\.]+\.rctiplus\.id/rcti[a-zA-Z0-9\-]*\.m3u8\?auth_key=[a-zA-Z0-9\-]+)', res_rcti.text)
        
        if match_rcti:
            new_rcti_url = match_rcti.group(1)
            print(f" -> Sukses! Token RCTI: {new_rcti_url}")
            # Ganti link lama dengan yang baru di dalam variabel 'content'
            content = re.sub(r'https://[a-zA-Z0-9\-\.]+\.rctiplus\.id/rcti[a-zA-Z0-9\-]*\.m3u8\?auth_key=[a-zA-Z0-9\-]+', new_rcti_url, content)
        else:
            print(" -> Gagal menemukan token RCTI.")
    except Exception as e:
            print(f" -> Error saat mengambil RCTI: {e}")

    # ==========================================
    # 4. PROSES UPDATE GTV
    # ==========================================
    try:
        print("Mencari token GTV...")
        res_gtv = requests.get('https://m.rctiplus.com/tv/gtv', headers=headers, cookies=cookies, timeout=10)
        match_gtv = re.search(r'(https://[a-zA-Z0-9\-\.]+\.rctiplus\.id/gtv[a-zA-Z0-9\-]*\.m3u8\?auth_key=[a-zA-Z0-9\-]+)', res_gtv.text)
        
        if match_gtv:
            new_gtv_url = match_gtv.group(1)
            print(f" -> Sukses! Token GTV: {new_gtv_url}")
            # Ganti link lama dengan yang baru di dalam variabel 'content'
            content = re.sub(r'https://[a-zA-Z0-9\-\.]+\.rctiplus\.id/gtv[a-zA-Z0-9\-]*\.m3u8\?auth_key=[a-zA-Z0-9\-]+', new_gtv_url, content)
        else:
            print(" -> Gagal menemukan token GTV.")
    except Exception as e:
            print(f" -> Error saat mengambil GTV: {e}")

    # ==========================================
    # 5. SIMPAN SEMUA PERUBAHAN
    # ==========================================
    with open(m3u_path, 'w', encoding='utf-8') as file:
        file.write(content)
        
    print("Selesai! File id.m3u berhasil diperbarui dengan semua token terbaru.")

if __name__ == "__main__":
    update_all_channels()
