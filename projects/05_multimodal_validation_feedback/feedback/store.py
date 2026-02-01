from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, Iterable

DB_PATH = Path(__file__).parent / "feedback.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                score REAL
            )
            """
        )


def save_feedback(items: Iterable[Dict[str, str]]) -> None:
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            "INSERT INTO feedback (question, answer, score) VALUES (?, ?, ?)",
            [
                (item.get("question"), item.get("answer"), item.get("score", 0.0))
                for item in items
            ],
        )
