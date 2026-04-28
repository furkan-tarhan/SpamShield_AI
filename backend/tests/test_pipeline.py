from datetime import datetime
from unittest.mock import Mock

from backend.src.domain.models import AnalysisResult, EmailMessage
from backend.src.services.email_pipeline import EmailPipeline


def test_pipeline_moves_high_risk_email_to_spam():
    imap_client = Mock()
    ai_client = Mock()
    database = Mock()

    test_email = EmailMessage(
        message_id="m-1",
        sender="spam@example.com",
        subject="Win now",
        body="You won a prize",
        received_at=datetime.utcnow(),
    )

    imap_client.fetch_unread_messages.return_value = [test_email]
    imap_client.move_to_spam.return_value = True
    ai_client.analyze_email.return_value = AnalysisResult(
        risk_score=90,
        label="spam",
        reason="Prize scam pattern",
        model_name="test-model",
    )

    pipeline = EmailPipeline(imap_client, ai_client, database, risk_threshold=40)
    stats = pipeline.run(limit=5)

    assert stats.processed == 1
    assert stats.moved_to_spam == 1
    imap_client.move_to_spam.assert_called_once_with("m-1")
