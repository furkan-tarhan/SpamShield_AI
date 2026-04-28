import sqlite3
from pathlib import Path

from backend.src.domain.models import AnalysisResult, EmailMessage


class Database:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True) if "/" in self.db_path or "\\" in self.db_path else None
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE NOT NULL,
                    sender TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    body_preview TEXT NOT NULL,
                    received_at TEXT NOT NULL
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT NOT NULL,
                    risk_score INTEGER NOT NULL,
                    label TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    model_name TEXT NOT NULL,
                    analyzed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(message_id) REFERENCES emails(message_id)
                );
                """
            )
            conn.commit()

    def save_email(self, email_message: EmailMessage) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO emails
                (message_id, sender, subject, body_preview, received_at)
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    email_message.message_id,
                    email_message.sender,
                    email_message.subject,
                    email_message.body[:250],
                    email_message.received_at.isoformat(),
                ),
            )
            conn.commit()

    def save_analysis(self, message_id: str, result: AnalysisResult) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO analysis
                (message_id, risk_score, label, reason, model_name)
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    message_id,
                    result.risk_score,
                    result.label,
                    result.reason,
                    result.model_name,
                ),
            )
            conn.commit()
