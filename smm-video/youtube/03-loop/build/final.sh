#!/bin/bash
# кадры (/tmp/yt3f) + голос с паузой + эффекты + музыка -> ../youtube-lesson-3.mp4 (1920x1080, 30 fps)
# музыка ~ -21 дБ в паузах, под голосом автоматически тише (sidechain)
set -e
ffmpeg -loglevel error -y -framerate 30 -i /tmp/yt3f/f%05d.jpg -i voice_g.wav -i fx.wav -i music.wav \
 -filter_complex "[3:a]volume=0.55[m0];[m0][1:a]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[md];[1:a]volume=1.0[v];[2:a]volume=0.9[fx];[v][fx][md]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]" \
 -map 0:v -map "[a]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest ../youtube-lesson-3.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 ../youtube-lesson-3.mp4
