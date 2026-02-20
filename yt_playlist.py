import yt_dlp

def get_user_input():
    url = input("\nEnter YouTube Video or Playlist URL: ").strip()

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

    return url, resolution, audio_only


def download_video(url, resolution, audio_only):
    if audio_only:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                {"key": "FFmpegMetadata"},
                {"key": "EmbedThumbnail"},
            ],
            "writethumbnail": True,
            "outtmpl": "%(playlist_title|Single_Video)s/%(title)s.%(ext)s",
        }
    else:
        if resolution:
            format_string = f"bestvideo[height<={resolution}]+bestaudio/best"
        else:
            format_string = "bestvideo+bestaudio/best"

        ydl_opts = {
            "format": format_string,
            "merge_output_format": "mp4",
            "postprocessors": [
                {"key": "FFmpegMetadata"},
                {"key": "EmbedThumbnail"},
            ],
            "writethumbnail": True,
            "outtmpl": "%(playlist_title|Single_Video)s/%(playlist_index)s - %(title)s.%(ext)s",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    print("🎬 YouTube Downloader CLI Tool")

    url, resolution, audio_only = get_user_input()
    download_video(url, resolution, audio_only)

    print("\n✅ Download Complete!")