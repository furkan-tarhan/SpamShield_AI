from dataclasses import dataclass
from datetime import datetime


@dataclass
class EmailMessage:
    message_id: str
    sender: str
    subject: str
    body: str
    received_at: datetime


@dataclass
class AnalysisResult:
    risk_score: int
    label: str
    reason: str
    model_name: str
