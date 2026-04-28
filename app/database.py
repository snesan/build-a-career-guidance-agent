"""SQLite persistence for career guidance sessions."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "career_guidance.sqlite3"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                answers_json TEXT NOT NULL,
                recommendation_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def save_assessment(student_name: str, answers: dict, recommendation: dict) -> int:
    init_db()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO assessments (student_name, answers_json, recommendation_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                student_name.strip() or "Anonymous student",
                json.dumps(answers),
                json.dumps(recommendation),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        return int(cursor.lastrowid)


def recent_assessments(limit: int = 20) -> list[dict]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, student_name, recommendation_json, created_at
            FROM assessments
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [
        {
            "id": row["id"],
            "student_name": row["student_name"],
            "recommendation": json.loads(row["recommendation_json"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]
