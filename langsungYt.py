import urllib.request
import json
import os

# Nama file output M3U sesuai permintaan Anda
OUTPUT_M3U = "langsungYtb.m3u"

# Daftar Channel YouTube via Handle
CHANNEL_HANDLES = [
    "@ArRaudhahTVOfficial",
    "@SNTVOfficialTelecast"
]

def generate_playlist():
    m3u_content = '#EXTM3U\n'
    
    for handle in CHANNEL_HANDLES:
        print(f"Mengecek channel: {handle}")
        clean_name = handle.replace("@", "")
        try:
            # Mengambil halaman channel publik untuk mendeteksi apakah sedang live
            url = f"https://www.youtube.com/{handle}/live"
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8')
                
                # Cek apakah string 'isLive' atau indikator live lainnya ada di source code halaman
                if '"isLive":true' in html or 'hlstrm' in html or 'broadcast_id' in html:
                    m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Live",🟢 [LIVE] {clean_name}\n'
                    m3u_content += f'https://www.youtube.com/{handle}/live\n'
                    print(f"-> Status: LIVE terdeteksi untuk {handle}")
                else:
                    m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Offline",🔴 [OFFLINE] {clean_name}\n'
                    m3u_content += f'https://www.youtube.com/{handle}/live\n'
                    print(f"-> Status: OFFLINE")
        except Exception as e:
            print(f"Error pada {handle}: {e}")
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Offline",🔴 [OFFLINE] {clean_name}\n'
            m3u_content += f'https://www.youtube.com/{handle}/live\n'

    with open(OUTPUT_M3U, "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"File {OUTPUT_M3U} berhasil diperbarui!")

if __name__ == "__main__":
    generate_playlist()
