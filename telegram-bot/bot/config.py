"""Танзимоти бот аз тағйирёбандаҳои муҳит ва файли keywords.json."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Payload-и deep-link (t.me/bot?start=...) танҳо A-Z, a-z, 0-9, _ ва - -ро қабул мекунад.
_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


@dataclass(frozen=True)
class Keyword:
    id: str
    words: tuple[str, ...]
    url: str
    message: str
    button: str


@dataclass(frozen=True)
class Config:
    token: str
    channel: str
    discussion_chat_id: int | None
    require_subscription: bool
    admin_ids: frozenset[int]
    db_path: Path
    comment_cooldown: int
    keywords: tuple[Keyword, ...] = field(default_factory=tuple)

    def keyword_by_id(self, keyword_id: str) -> Keyword | None:
        return next((k for k in self.keywords if k.id == keyword_id), None)


def _bool(value: str | None, default: bool) -> bool:
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on", "ha", "ҳа"}


def parse_keywords(raw: str) -> tuple[Keyword, ...]:
    data = json.loads(raw)
    if not isinstance(data, list) or not data:
        raise ValueError("keywords бояд рӯйхати ғайриихолӣ бошад")

    keywords: list[Keyword] = []
    seen: set[str] = set()
    for item in data:
        keyword_id = str(item["id"]).strip()
        if not _ID_RE.match(keyword_id):
            raise ValueError(
                f"id «{keyword_id}» нодуруст аст: танҳо ҳарфҳои лотинӣ, рақам, _ ва -"
            )
        if keyword_id in seen:
            raise ValueError(f"id «{keyword_id}» такрор шудааст")
        seen.add(keyword_id)

        words = tuple(w.strip() for w in item["words"] if str(w).strip())
        if not words:
            raise ValueError(f"барои «{keyword_id}» калимаи рамзӣ нест")

        keywords.append(
            Keyword(
                id=keyword_id,
                words=words,
                url=str(item["url"]).strip(),
                message=item.get(
                    "message", "Ана маводи ваъдашуда 👇\n{url}"
                ),
                button=item.get("button", "📥 Кушодан"),
            )
        )
    return tuple(keywords)


def load_config() -> Config:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    channel = os.environ.get("TELEGRAM_CHANNEL", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN дода нашудааст")
    if not channel:
        raise RuntimeError("TELEGRAM_CHANNEL дода нашудааст (масалан @my_channel)")

    raw_keywords = os.environ.get("KEYWORDS_JSON")
    if not raw_keywords:
        path = Path(os.environ.get("KEYWORDS_FILE", ROOT / "keywords.json"))
        raw_keywords = path.read_text(encoding="utf-8")

    discussion = os.environ.get("DISCUSSION_CHAT_ID", "").strip()
    admins = os.environ.get("ADMIN_IDS", "")

    return Config(
        token=token,
        channel=channel,
        discussion_chat_id=int(discussion) if discussion else None,
        require_subscription=_bool(os.environ.get("REQUIRE_SUBSCRIPTION"), True),
        admin_ids=frozenset(int(x) for x in admins.replace(" ", "").split(",") if x),
        db_path=Path(os.environ.get("DB_PATH", ROOT / "data" / "bot.db")),
        comment_cooldown=int(os.environ.get("COMMENT_COOLDOWN", "600")),
        keywords=parse_keywords(raw_keywords),
    )
