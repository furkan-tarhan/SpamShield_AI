from dataclasses import dataclass
from typing import List

from backend.src.domain.models import EmailMessage
from backend.src.integrations.ai_client import AiClient
from backend.src.integrations.imap_client import ImapClient
from backend.src.storage.database import Database


@dataclass
class PipelineStats:
    processed: int = 0
    moved_to_spam: int = 0


class EmailPipeline:
    def __init__(
        self,
        imap_client: ImapClient,
        ai_client: AiClient,
        database: Database,
        risk_threshold: int,
    ) -> None:
        self.imap_client = imap_client
        self.ai_client = ai_client
        self.database = database
        self.risk_threshold = risk_threshold

    def run(self, limit: int = 20) -> PipelineStats:
        stats = PipelineStats()
        emails: List[EmailMessage] = self.imap_client.fetch_unread_messages(limit=limit)

        for email_message in emails:
            self.database.save_email(email_message)
            analysis = self.ai_client.analyze_email(email_message)
            self.database.save_analysis(email_message.message_id, analysis)

            if analysis.risk_score >= self.risk_threshold:
                moved = self.imap_client.move_to_spam(email_message.message_id)
                if moved:
                    stats.moved_to_spam += 1

            stats.processed += 1

        return stats
