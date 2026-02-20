FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    pip install yt-dlp

WORKDIR /app

COPY yt_playlist.py .

ENTRYPOINT ["python", "yt_playlist.py"]