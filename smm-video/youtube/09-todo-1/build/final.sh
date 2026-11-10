#!/bin/bash
# кадрҳо + овоз бо пауза + эффектҳо + мусиқӣ -> ../youtube-lesson-9.mp4 (1920x1080, 30 fps)
set -e
ffmpeg -loglevel error -y -framerate 30 -i "C:/Users/User/AppData/Local/Temp/claude/D--Android-projects-yunusov-tj/a999f0f8-176d-48f8-8614-1c707736d265/scratchpad/yt9f/f%05d.jpg" -i voice_g.wav -i fx.wav -i music.wav  -filter_complex "[3:a]volume=0.55[m0];[m0][1:a]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400[md];[1:a]volume=1.0[v];[2:a]volume=0.9[fx];[v][fx][md]amix=inputs=3:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"  -map 0:v -map "[a]" -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest ../youtube-lesson-9.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 ../youtube-lesson-9.mp4
