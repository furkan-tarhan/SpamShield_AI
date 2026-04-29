# -*- coding: utf-8 -*-
import pytest
from unittest.mock import Mock
from datetime import datetime

from backend.src.domain.models import EmailMessage
from backend.src.services.email_pipeline import EmailPipeline

def test_pipeline_domino_effect_crash():
    """
    KRITIK BUG KONTROLU: Eger 1. mail veritabanina kaydedilemezse, 
    diger mailler islenmeden sistem cokuyor mu?
    """
    imap_client = Mock()
    ai_client = Mock()
    database = Mock()

    emails = [
        EmailMessage(f"m-{i}", "test@test.com", "Subj", "Body", datetime.utcnow()) 
        for i in range(3)
    ]
    imap_client.fetch_unread_messages.return_value = emails
    
    # Veritabani SADECE ilk mailde hata versin
    database.save_email.side_effect = Exception("Veritabani kilitli!")

    pipeline = EmailPipeline(imap_client, ai_client, database, risk_threshold=40)
    
    with pytest.raises(Exception) as exc_info:
        pipeline.run()
    
    assert "Veritabani kilitli!" in str(exc_info.value)
    
    # Sistem coktugu icin AI analizi HIC cagrilmamis olmali
    ai_client.analyze_email.assert_not_called()