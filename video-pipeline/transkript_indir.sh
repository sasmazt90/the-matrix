#!/usr/bin/env bash
# Slayt 42 — YouTube Video Analizi: transkript ve kare örneklemesi

# 1. Transkripti indir
yt-dlp --write-auto-sub --skip-download \
       --sub-format vtt --sub-lang tr \
       "https://youtube.com/watch?v=VIDEO_ID"
# İndiriliyor: video_title.tr.vtt
# ✓ Transkript kaydedildi

# 2. Kare örneklemesi (her 30 saniyede bir kare)
ffmpeg -i video.mp4 -vf fps=1/30 frames/frame_%04d.jpg
# ✓ 48 kare çıkarıldı (24 dakika × 2)
