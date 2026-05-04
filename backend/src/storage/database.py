import sqlite3
from datetime import datetime
from pathlib import Path

from backend.src.domain.models import AnalysisResult, EmailMessage


class Database:
    PREVIEW_MAX = 4000

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _ensure_parent_dir(self) -> None:
        parent = Path(self.db_path).parent
        if str(parent) not in (".", ""):
            parent.mkdir(parents=True, exist_ok=True)

    def _initialize(self) -> None:
        self._ensure_parent_dir()
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
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_analysis_message_id
                ON analysis(message_id);
                """
            )
            conn.commit()

    @staticmethod
    def _received_at_value(received_at) -> str:
        if isinstance(received_at, datetime):
            return received_at.isoformat()
        return str(received_at)

    def save_email(self, email_data: EmailMessage) -> bool:
        """E-postayı mükerrer kontrolü yaparak kaydeder."""
        preview = (email_data.body or "")[: self.PREVIEW_MAX]
        received = self._received_at_value(email_data.received_at)
        try:
            with self._connect() as conn:
                cur = conn.cursor()
                cur.execute(
                    "SELECT 1 FROM emails WHERE message_id = ?",
                    (email_data.message_id,),
                )
                if cur.fetchone():
                    return True
                cur.execute(
                    """
                    INSERT INTO emails (message_id, sender, subject, body_preview, received_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        email_data.message_id,
                        email_data.sender,
                        email_data.subject,
                        preview,
                        received,
                    ),
                )
                conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Veritabanı kayıt hatası: {e}")
            return False

    @staticmethod
    def _normalize_label(result: AnalysisResult) -> str:
        label = (result.label or "safe").strip().lower()
        if label not in ("spam", "safe"):
            return "spam" if result.risk_score >= 50 else "safe"
        return label

    def save_analysis(self, message_id: str, result: AnalysisResult) -> None:
        label = self._normalize_label(result)
        with self._connect() as conn:
            conn.execute("DELETE FROM analysis WHERE message_id = ?", (message_id,))
            conn.execute(
                """
                INSERT INTO analysis
                (message_id, risk_score, label, reason, model_name)
                VALUES (?, ?, ?, ?, ?);
                """,
                (
                    message_id,
                    result.risk_score,
                    label,
                    result.reason,
                    result.model_name,
                ),
            )
            conn.commit()

    def get_emails_by_label(self, label: str) -> list:
        key = label.strip().lower()
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT e.sender, e.subject, e.received_at, a.label, a.risk_score
                FROM emails e
                JOIN analysis a ON e.message_id = a.message_id
                WHERE LOWER(a.label) = ?
                ORDER BY e.received_at DESC
                """,
                (key,),
            )
            return cur.fetchall()

    def get_filtered_analysis(self, label: str) -> list:
        """UI filtreleri: gönderen, konu, risk, etiket."""
        key = label.strip().lower()
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT e.sender, e.subject, a.risk_score, a.label
                FROM emails e
                JOIN analysis a ON e.message_id = a.message_id
                WHERE LOWER(a.label) = ?
                ORDER BY e.received_at DESC
                """,
                (key,),
            )
            return cur.fetchall()

    def get_all_summaries(self) -> dict:
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT LOWER(a.label) AS lb, COUNT(*)
                FROM analysis a
                GROUP BY LOWER(a.label)
                """
            )
            return {str(row[0]): int(row[1]) for row in cur.fetchall()}

    def get_dashboard_stats(self) -> dict:
        """Tek sorgu ile özet; gereksiz tekrarları önler."""
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM emails")
            total_emails = int(cur.fetchone()[0])
            cur.execute(
                "SELECT COUNT(*) FROM analysis WHERE LOWER(label) = 'spam'"
            )
            spam_rows = int(cur.fetchone()[0])
            cur.execute("SELECT AVG(risk_score) FROM analysis")
            row = cur.fetchone()
            avg_risk = float(row[0]) if row and row[0] is not None else None
        return {
            "total_emails": total_emails,
            "spam_count": spam_rows,
            "avg_risk": avg_risk,
        }
