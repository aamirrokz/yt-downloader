import yt_dlp

def main():
    print("🎬 YouTube Downloader CLI Tool")

    url = input("Enter YouTube Video or Playlist URL: ").strip()

    print("\nSelect Resolution:")
    print("1. 1080p")
    print("2. 720p")
    print("3. 480p")
    print("4. Best Available")

    res_choice = input("Enter choice (1-4): ").strip()

    resolution_map = {
        "1": "1080",
        "2": "720",
        "3": "480",
        "4": None
    }

    resolution = resolution_map.get(res_choice, None)

    audio_only_input = input("\nDownload audio only? (y/n): ").strip().lower()
    audio_only = audio_only_input == "y"

    if audio_only:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:
        format_string = (
            f"bestvideo[height<={resolution}]+bestaudio/best"
            if resolution else
            "bestvideo+bestaudio/best"
        )

        ydl_opts = {
            "format": format_string,
            "merge_output_format": "mp4",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])