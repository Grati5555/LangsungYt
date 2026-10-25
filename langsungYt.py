import subprocess
import os

CHANNELS_FILE = "channels.txt"
OUTPUT_M3U = "langsungYtb.m3u"

def get_stream_url(youtube_url):
    try:
        # Menggunakan yt-dlp untuk langsung ekstrak URL stream m3u8/manifest
        command = [
            "yt-dlp",
            "-g",
            "--no-warnings",
            youtube_url
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=25)
        if result.returncode == 0:
            urls = result.stdout.strip().split('\n')
            for url in urls:
                if url.startswith("http"):
                    return url.strip()
        return None
    except Exception as e:
        print(f"Error fetching {youtube_url}: {e}")
        return None

def generate_m3u():
    if not os.path.exists(CHANNELS_FILE):
        print(f"File {CHANNELS_FILE} tidak ditemukan.")
        return

    with open(CHANNELS_FILE, "r") as f:
        channels = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    m3u_content = '#EXTM3U\n'
    
    for channel_url in channels:
        print(f"Memeriksa: {channel_url}")
        stream_url = get_stream_url(channel_url)
        
        # Ambil nama channel yang bersih untuk judul
        clean_name = channel_url.split("@")[-1].replace("/live", "").replace("/", "")
        
        if stream_url:
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Live",🟢 [LIVE] {clean_name}\n'
            m3u_content += f'{stream_url}\n'
            print(f"-> Status: LIVE Ditemukan!")
        else:
            # Jika offline, arahkan ke link channel aslinya atau placeholder khusus
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Offline",🔴 [OFFLINE] {clean_name}\n'
            m3u_content += f'{channel_url}\n'
            print(f"-> Status: OFFLINE")

    with open(OUTPUT_M3U, "w") as f:
        f.write(m3u_content)
    print("Playlist langsungYtb.m3u berhasil diperbarui!")

if __name__ == "__main__":
    generate_m3u()
