import subprocess
import os

CHANNELS_FILE = "channels.txt"
OUTPUT_M3U = "langsungYtb.m3u"

def get_stream_url(youtube_url):
    try:
        # Menggunakan argumen --print untuk menarik langsung URL video live aktif dari halaman channel/streams
        command = [
            "yt-dlp",
            "--print",
            "url",
            "--playlist-items",
            "1",
            "--no-warnings",
            youtube_url
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            for line in output_lines:
                if line.startswith("http"):
                    # Ambil link video tersebut lalu ekstrak link m3u8 langsungnya
                    video_url = line.strip()
                    cmd_stream = [
                        "yt-dlp",
                        "-g",
                        "--no-warnings",
                        video_url
                    ]
                    res_stream = subprocess.run(cmd_stream, capture_output=True, text=True, timeout=20)
                    if res_stream.returncode == 0:
                        streams = res_stream.stdout.strip().split('\n')
                        for s in streams:
                            if s.startswith("http"):
                                return s.strip()
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
        
        # Membersihkan nama channel untuk judul di aplikasi IPTV
        clean_name = channel_url.split("@")[-1].replace("/streams", "").replace("/live", "").replace("/", "")
        
        if stream_url:
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Live",🟢 [LIVE] {clean_name}\n'
            m3u_content += f'{stream_url}\n'
            print(f"-> Status: LIVE Ditemukan!")
        else:
            m3u_content += f'#EXTINF:-1 tvg-id="" tvg-logo="" group-title="YouTube Offline",🔴 [OFFLINE] {clean_name}\n'
            m3u_content += f'{channel_url.replace("/streams", "/live")}\n'
            print(f"-> Status: OFFLINE")

    with open(OUTPUT_M3U, "w") as f:
        f.write(m3u_content)
    print("Playlist langsungYtb.m3u berhasil diperbarui!")

if __name__ == "__main__":
    generate_m3u()
