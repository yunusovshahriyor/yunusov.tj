#!/bin/bash
# рендери кадрҳо дар 4 ҷараён -> $1 (папкаи кадрҳо)
OUT=$1; mkdir -p "$OUT"
END=$(python -c "import json;print(json.load(open('gaps.json'))['end'])")
for k in 0 1 2 3; do
  read A B <<< $(python -c "e=$END;k=$k;print(round(k*e/4,4), e if k==3 else round((k+1)*e/4,4))")
  node render.js $A $B "$OUT" 30 > render_$k.log 2>&1 &
done
wait; echo done
