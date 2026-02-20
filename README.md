# 🎬 YT Downloader CLI

A Dockerized YouTube video and playlist downloader built with yt-dlp.

## Features
- Download video or playlist
- Resolution selection
- Audio-only mode
- Metadata tagging
- Docker support

## Run Locally
python yt_tool.py

## Run With Docker
docker build -t yt-downloader .
docker run -it -v "$PWD":/app yt-downloader