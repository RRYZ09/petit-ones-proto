import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


class SQLiteMemory:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.schema_path = Path(__file__).with_name("schema.sql")

    def setup(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(self.schema_path.read_text(encoding="utf-8"))

    def add(self, one_id: str, kind: str, content: str, source: str = "system"):
        self.setup()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO memories (one_id, created_at, kind, content, source)
                VALUES (?, ?, ?, ?, ?)
                """,
                (one_id, now_iso(), kind, content, source),
            )

    def recent(self, limit: int = 10):
        self.setup()
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                """
                SELECT created_at, kind, content, source
                FROM memories
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [
            {
                "created_at": row[0],
                "kind": row[1],
                "content": row[2],
                "source": row[3],
            }
            for row in rows
        ]
