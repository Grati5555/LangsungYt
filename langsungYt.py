import subprocess
import os

CHANNELS_FILE = "channels.txt"
OUTPUT_M3U = "langsungYtb.m3u"

def get_stream_url(youtube_url):
    try:
        command = [
            "yt-dlp",
            "--get-url",
            "--no-warnings",
            youtube_url
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            urls = result.stdout.strip().split('\n')
            for url in urls:
                if "m3u8" in url or "manifest" in url or "videoplayback" in url:
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
        
        channel_name = channel_url.split("/")[-1].replace("@", "")
        if stream_url:
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Live",🟢 [LIVE] {channel_name}\n'
            m3u_content += f'{stream_url}\n'
            print(f"-> Status: LIVE")
        else:
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Offline",🔴 [OFFLINE] {channel_name}\n'
            m3u_content += f'https://raw.githubusercontent.com/Grati555/LangsungYt/main/offline.mp4\n'
            print(f"-> Status: OFFLINE")

    with open(OUTPUT_M3U, "w") as f:
        f.write(m3u_content)
    print("Playlist langsungYtb.m3u berhasil diperbarui!")

if __name__ == "__main__":
    generate_m3u()
