"""Нигоҳ доштани корбароне, ки маводро гирифтаанд (SQLite)."""

from __future__ import annotations

import sqlite3
from pathlib import Path


class Storage:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(path)
        self._db.execute(
            """
            CREATE TABLE IF NOT EXISTS deliveries (
                user_id     INTEGER NOT NULL,
                keyword_id  TEXT    NOT NULL,
                username    TEXT,
                first_name  TEXT,
                created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, keyword_id)
            )
            """
        )
        self._db.commit()

    def save_delivery(
        self, user_id: int, keyword_id: str, username: str | None, first_name: str | None
    ) -> None:
        self._db.execute(
            """
            INSERT INTO deliveries (user_id, keyword_id, username, first_name)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (user_id, keyword_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name
            """,
            (user_id, keyword_id, username, first_name),
        )
        self._db.commit()

    def stats(self) -> tuple[int, list[tuple[str, int]]]:
        users = self._db.execute(
            "SELECT COUNT(DISTINCT user_id) FROM deliveries"
        ).fetchone()[0]
        per_keyword = self._db.execute(
            "SELECT keyword_id, COUNT(*) FROM deliveries GROUP BY keyword_id ORDER BY 2 DESC"
        ).fetchall()
        return users, per_keyword
