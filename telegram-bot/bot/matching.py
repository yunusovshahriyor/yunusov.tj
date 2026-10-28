"""Ёфтани калимаи рамзӣ дар матни шарҳ."""

from __future__ import annotations

import re
import time

from .config import Keyword


def normalize(text: str) -> str:
    return " ".join(text.lower().replace("ё", "е").split())


def _pattern(word: str) -> re.Pattern[str]:
    # Калима бояд алоҳида бошад: «гайд» дар «гайдҳо» ҳисоб намешавад,
    # вале «Гайд!», «гайд 🔥» ва «мехоҳам гайд» ҳисоб мешаванд.
    return re.compile(rf"(?<!\w){re.escape(normalize(word))}(?!\w)")


class KeywordMatcher:
    def __init__(self, keywords: tuple[Keyword, ...]) -> None:
        self._items = [
            (keyword, [_pattern(w) for w in keyword.words]) for keyword in keywords
        ]

    def match(self, text: str | None) -> Keyword | None:
        if not text:
            return None
        normalized = normalize(text)
        for keyword, patterns in self._items:
            if any(p.search(normalized) for p in patterns):
                return keyword
        return None


class Cooldown:
    """Як корбар бо як калима дар шарҳҳо на зудтар аз як бор дар `seconds` ҷавоб мегирад."""

    def __init__(self, seconds: int) -> None:
        self._seconds = seconds
        self._last: dict[tuple[int, str], float] = {}

    def allow(self, user_id: int, keyword_id: str, now: float | None = None) -> bool:
        now = time.monotonic() if now is None else now
        key = (user_id, keyword_id)
        last = self._last.get(key)
        if last is not None and now - last < self._seconds:
            return False
        self._last[key] = now
        if len(self._last) > 10_000:
            self._last = {k: v for k, v in self._last.items() if now - v < self._seconds}
        return True
