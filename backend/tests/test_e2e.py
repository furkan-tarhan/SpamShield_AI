"""Mail çekme -> AI analiz -> DB kaydı (mock IMAP + mock AI)."""

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock

import pytest

from backend.src.domain.models import AnalysisResult, EmailMessage
from backend.src.services.email_pipeline import EmailPipeline
from backend.src.storage.database import Database


@pytest.fixture
def tmp_db(tmp_path: Path) -> Database:
    return Database(str(tmp_path / "e2e.db"))


def test_e2e_fetch_analyze_persist(tmp_db: Database) -> None:
    imap_client = Mock()
    ai_client = Mock()

    msg = EmailMessage(
        message_id="e2e-msg-1",
        sender="phish@evil.test",
        subject="Verify your account",
        body="Urgent: click here to verify your bank login.",
        received_at=datetime(2026, 5, 1, 12, 0, tzinfo=timezone.utc),
    )
    imap_client.fetch_unread_messages.return_value = [msg]
    imap_client.move_to_spam.return_value = True
    ai_client.analyze_email.return_value = AnalysisResult(
        risk_score=85,
        label="spam",
        reason="Credential phishing pattern.",
        model_name="test-model",
    )

    pipeline = EmailPipeline(imap_client, ai_client, tmp_db, risk_threshold=40)
    stats = pipeline.run(limit=5)

    assert stats.processed == 1
    assert stats.moved_to_spam == 1

    rows = tmp_db.get_filtered_analysis("spam")
    assert len(rows) >= 1
    assert rows[0][0] == "phish@evil.test"
    assert rows[0][2] == 85

    with tmp_db._connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM emails WHERE message_id = ?", (msg.message_id,))
        assert cur.fetchone()[0] == 1
