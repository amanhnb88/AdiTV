import requests
import re
import os

def update_gtv_m3u():
    print("Mencari token GTV terbaru...")
    
    # 1. Mengatur URL, Headers, dan Cookies berdasarkan cURL kamu
    url = 'https://m.rctiplus.com/tv/gtv'
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'referer': 'https://m.rctiplus.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36'
    }
    
    cookies = {
        'device_uuid': '2dbd0d2b-dc16-4b09-ba05-e0b4377948d9',
        'visitor_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aWQiOjAsInRva2VuIjoiMjM0OTM2NGE5ZTgzMjQ1NyIsInBsIjoibXdlYiIsImRldmljZV9pZCI6IjJkYmQwZDJiLWRjMTYtNGIwOS1iYTA1LWUwYjQzNzc5NDhkOSIsImx0eXBlIjoiIiwiaWF0IjoxNzcyMTU5NDMyfQ.F_CwnDc1Bpen9o7uJNTP1lCqwcHMbY48rZOftlRYLC0'
    }
    
    try:
        # Request ke halaman web GTV
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        
        # 2. Mencari teks link m3u8 untuk GTV
        # Pola regex ini akan menangkap URL m3u8 yang mengandung 'gtv' dan 'auth_key'
        match = re.search(r'(https://[a-zA-Z0-9\-\.]+\.rctiplus\.id/gtv[a-zA-Z0-9\-]*\.m3u8\?auth_key=[a-zA-Z0-9\-]+)', response.text)
        
        if match:
            new_gtv_url = match.group(1)
            print(f"Token baru GTV ditemukan: {new_gtv_url}")
            
            # 3. Membaca file id.m3u
            m3u_path = 'streams/id.m3u'
            if not os.path.exists(m3u_path):
                print(f"File {m3u_path} tidak ditemukan!")
                return
                
            with open(m3u_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 4. Mengganti link GTV lama dengan yang baru menggunakan Regex
            updated_content = re.sub(
                r'https://[a-zA-Z0-9\-\.]+\.rctiplus\.id/gtv[a-zA-Z0-9\-]*\.m3u8\?auth_key=[a-zA-Z0-9\-]+', 
                new_gtv_url, 
                content
            )
            
            # 5. Menyimpan perubahan ke id.m3u
            with open(m3u_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
                
            print("Berhasil memperbarui tautan GTV di file id.m3u!")
            
        else:
            print("Gagal menemukan link m3u8 GTV. Periksa apakah cookie masih valid atau struktur web berubah.")
            
    except Exception as e:
        print(f"Terjadi error: {e}")

if __name__ == "__main__":
    update_gtv_m3u()
