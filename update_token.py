import requests
import os

# Nama file playlist lu di dalam repositori
PLAYLIST_FILE = "BRFID07_Clean.m3u"

def get_new_token():
    # Logika untuk mengambil token baru. 
    # Contoh: request ke API atau scrape dari website tertentu.
    print("Mengambil token baru...")
    try:
        # Ganti URL ini dengan sumber token lu
        # response = requests.get("https://api.sumbertoken.com/get")
        # return response.json()['token']
        
        # Simulasi token baru
        return "TOKEN_BARU_DARI_SERVER_12345" 
    except Exception as e:
        print(f"Gagal mengambil token: {e}")
        return None

def update_playlist(new_token):
    if not os.path.exists(PLAYLIST_FILE):
        print("File playlist tidak ditemukan!")
        return

    print("Membaca playlist lama...")
    with open(PLAYLIST_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Logika untuk mencari token lama (regex atau replace) dan menggantinya.
    # Tergantung format token di URL-nya, misal: ?token=XYZ diganti jadi ?token=TOKEN_BARU
    print("Memperbarui token di dalam playlist...")
    updated_content = content.replace("TOKEN_LAMA_ATAU_PLACEHOLDER", new_token)

    # Simpan kembali ke file yang sama
    with open(PLAYLIST_FILE, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("Playlist berhasil diperbarui!")

if __name__ == "__main__":
    token = get_new_token()
    if token:
        update_playlist(token)
