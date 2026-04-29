# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch, Mock
from datetime import datetime
import json

from backend.src.domain.models import EmailMessage
from backend.src.integrations.ai_client import OpenAiCompatibleClient

@pytest.fixture
def dummy_email():
    return EmailMessage(
        message_id="test-1",
        sender="hacker@test.com",
        subject="Urgent",
        body="Bu bir test mailidir.",
        received_at=datetime.utcnow()
    )

def test_ai_extract_json_with_markdown_blocks():
    """
    BUG KONTROLU: AI modeli bazen sadece JSON donmez, basa ve sona markdown koyar.
    Regex bunu yakalayabiliyor mu?
    """
    client = OpenAiCompatibleClient("dummy_key", "http://dummy", "dummy-model")
    
    ai_response = """
    Iste analiz sonucunuz:
    ```json
    {"risk_score": 85, "label": "spam", "reason": "Phishing link detected"}
    ```
    Lutfen dikkatli olun.
    """
    
    extracted = client._extract_json(ai_response)
    
    assert extracted["risk_score"] == 85
    assert extracted["label"] == "spam"

@patch("backend.src.integrations.ai_client.requests.post")
def test_ai_client_fallback_on_timeout(mock_post, dummy_email):
    """
    BUG KONTROLU: API zaman asimina ugradiginda cokuyor mu yoksa Fallback (Yedek) mi devreye giriyor?
    """
    import requests
    mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")
    
    client = OpenAiCompatibleClient("dummy_key", "http://dummy", "dummy-model", max_retries=1, retry_delay_seconds=0)
    
    result = client.analyze_email(dummy_email)
    
    assert result.risk_score == 50
    assert result.label == "safe"
    assert "fallback" in result.model_name