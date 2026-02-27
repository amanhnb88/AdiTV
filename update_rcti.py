import requests
import re
import os

def update_m3u_file():
    print("Mencari token RCTI terbaru...")
    
    # 1. Mengambil halaman web RCTI+ untuk mencari token
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36',
        'Referer': 'https://m.rctiplus.com/'
    }
    
    try:
        # Request ke halaman web RCTI
        response = requests.get('https://m.rctiplus.com/tv/rcti', headers=headers, timeout=10)
        
        # Mencari teks link m3u8 dengan regex (memanfaatkan API/JSON yang tersembunyi di HTML)
        match = re.search(r'(https://1s1\.rctiplus\.id/rcti-sdi\.m3u8\?auth_key=[a-zA-Z0-9\-]+)', response.text)
        
        if match:
            new_rcti_url = match.group(1)
            print(f"Token baru ditemukan: {new_rcti_url}")
            
            # 2. Membaca file id.m3u yang lama
            m3u_path = 'streams/id.m3u'
            if not os.path.exists(m3u_path):
                print(f"File {m3u_path} tidak ditemukan!")
                return
                
            with open(m3u_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 3. Mengganti link RCTI lama dengan yang baru menggunakan Regex
            # Mencari URL RCTI lama yang berawalan https://1s1.rctiplus.id...
            updated_content = re.sub(
                r'https://1s1\.rctiplus\.id/rcti-sdi\.m3u8\?auth_key=[a-zA-Z0-9\-]+', 
                new_rcti_url, 
                content
            )
            
            # 4. Menyimpan perubahan ke id.m3u
            with open(m3u_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
                
            print("Berhasil memperbarui file id.m3u!")
            
        else:
            print("Gagal menemukan link m3u8. Struktur web mungkin berubah.")
            
    except Exception as e:
        print(f"Terjadi error: {e}")

if __name__ == "__main__":
    update_m3u_file()
