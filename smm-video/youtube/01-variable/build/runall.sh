#!/bin/bash
# рендер в 4 потока
export NODE_PATH=/opt/node-tools/node_modules
END=$(python3 -c "import json;print(json.load(open('gaps.json'))['end'])")
Q=$(python3 -c "print(round($END/4,1))")
for k in 0 1 2 3; do
  A=$(python3 -c "print(round($k*$Q,4))"); B=$(python3 -c "print($END if $k==3 else round(($k+1)*$Q,4))")
  node render.js $A $B /tmp/yt1f 30 > /tmp/yt1f_$k.log 2>&1 &
done
wait; echo done
