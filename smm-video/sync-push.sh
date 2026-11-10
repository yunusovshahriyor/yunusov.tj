#!/usr/bin/env bash
# Пас аз ҳар commit: push ба шохаи кории худ ва ба шохаи асосии репозиторий (claude/clever-cori-8bobpv).
# Агар шохаи асосӣ пеш рафта бошад — аввал бо merge якҷоя мекунад. Дар ҳолати муноқиша merge-ро бекор мекунад ва огоҳ мекунад.
MAIN=claude/clever-cori-8bobpv
cd "$(git rev-parse --show-toplevel)" || exit 0
B=$(git rev-parse --abbrev-ref HEAD)
[ "$B" = "HEAD" ] && exit 0
git push -q -u origin "$B" 2>&1 | tail -1
git fetch -q origin "$MAIN" 2>/dev/null || exit 0
if ! git merge-base --is-ancestor "origin/$MAIN" HEAD; then
  if ! git merge -q --no-edit "origin/$MAIN" >/dev/null 2>&1; then
    git merge --abort 2>/dev/null
    echo "sync-push: муноқиша бо $MAIN — merge дастӣ лозим аст (push ба $MAIN иҷро нашуд)"
    exit 0
  fi
  git push -q origin "$B" 2>&1 | tail -1
fi
git push -q origin "HEAD:$MAIN" 2>&1 | tail -1
echo "sync-push: $B → $B ва $MAIN (ok)"
