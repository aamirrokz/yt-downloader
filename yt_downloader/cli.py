import yt_dlp
from yt_dlp.utils import DownloadError
from tqdm import tqdm
import re

progress_bar = None


def progress_hook(d):
    global progress_bar

    if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate")

        if total:
            if progress_bar is None:
                progress_bar = tqdm(total=total, unit="B", unit_scale=True)

            downloaded = d.get("downloaded_bytes", 0)
            progress_bar.n = downloaded
            progress_bar.refresh()

    elif d["status"] == "finished":
        if progress_bar:
            progress_bar.close()
            print("🔄 Merging & processing...")


def is_valid_youtube_url(url: str) -> bool:
    youtube_pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
    return re.match(youtube_pattern, url) is not None


def get_valid_url():
    while True:
        url = input("\nEnter YouTube Video or Playlist URL: ").strip()
        if not is_valid_youtube_url(url):
            print("❌ Invalid YouTube URL format. Try again.")
            continue
        return url


def main():
    print("🎬 YouTube Downloader CLI Tool")

    url = get_valid_url()

    print("\nSelect Resolution:")
    print("1. 1080p")
    print("2. 720p")
    print("3. 480p")
    print("4. Best Available")

    resolution_map = {
        "1": "1080",
        "2": "720",
        "3": "480",
        "4": None
    }

    res_choice = input("Enter choice (1-4): ").strip()
    resolution = resolution_map.get(res_choice, None)

    audio_only = input("\nDownload audio only? (y/n): ").strip().lower() == "y"

    if audio_only:
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "progress_hooks": [progress_hook],
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
            "progress_hooks": [progress_hook],
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download Complete!")

    except DownloadError:
        print("\n❌ Download failed.")


if __name__ == "__main__":
    main()
