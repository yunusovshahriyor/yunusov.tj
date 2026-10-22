#!/bin/sh
# Использование: ./add-voice.sh voice.mp3
# Накладывает озвучку на hook.mp4 и сохраняет hook-voiced.mp4 (~26 с).
# Озвучку лучше записывать по narration.txt, ориентируясь на метки времени.
set -e
ffmpeg -y -i hook.mp4 -i "$1" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest hook-voiced.mp4
