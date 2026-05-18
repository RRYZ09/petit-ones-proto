import sqlite3
from pathlib import Path


class LegacyMemory:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def recent(self, limit: int = 10) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT
                    id,
                    timestamp,
                    content,
                    emotion,
                    importance,
                    category,
                    tags,
                    episode_id
                FROM memories
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return self._rows_to_dicts(rows)

    def important(self, limit: int = 10) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT
                    id,
                    timestamp,
                    content,
                    emotion,
                    importance,
                    category,
                    tags,
                    episode_id
                FROM memories
                ORDER BY importance DESC, timestamp DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return self._rows_to_dicts(rows)

    def search(self, query: str, limit: int = 10) -> list[dict]:
        like = f"%{query}%"

        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT
                    id,
                    timestamp,
                    content,
                    emotion,
                    importance,
                    category,
                    tags,
                    episode_id
                FROM memories
                WHERE content LIKE ?
                   OR normalized_content LIKE ?
                   OR tags LIKE ?
                ORDER BY importance DESC, timestamp DESC
                LIMIT ?
                """,
                (like, like, like, limit),
            ).fetchall()

        return self._rows_to_dicts(rows)

    def episodes(self, limit: int = 10) -> list[dict]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT
                    id,
                    title,
                    summary,
                    timestamp,
                    importance
                FROM episodes
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "summary": row[2],
                "created_at": row[3],
                "importance": row[4],
            }
            for row in rows
        ]

    def _rows_to_dicts(self, rows: list[tuple]) -> list[dict]:
        return [
            {
                "id": row[0],
                "created_at": row[1],
                "content": row[2],
                "emotion": row[3],
                "importance": row[4],
                "category": row[5],
                "tags": row[6],
                "episode_id": row[7],
                "source": "legacy_memory",
                "kind": row[5] or "memory",
            }
            for row in rows
        ]
