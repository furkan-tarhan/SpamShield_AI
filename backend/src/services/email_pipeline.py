from dataclasses import dataclass, replace
from typing import List

from backend.src.domain.models import AnalysisResult, EmailMessage
from backend.src.integrations.ai_client import AiClient
from backend.src.integrations.imap_client import ImapClient
from backend.src.storage.database import Database
from backend.src.utils.processor import EmailProcessor


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
        risk_threshold: int = 40,
    ) -> None:
        self.imap_client = imap_client
        self.ai_client = ai_client
        self.database = database
        self.risk_threshold = risk_threshold

    def _final_label(self, risk_score: int) -> str:
        return "spam" if risk_score >= self.risk_threshold else "safe"

    def run(self, limit: int = 20) -> PipelineStats:
        stats = PipelineStats()
        emails: List[EmailMessage] = self.imap_client.fetch_unread_messages(limit=limit)
        print(f"[{len(emails)}] adet yeni e-posta işleme alınıyor...")

        df = EmailProcessor.clean_data(emails)
        body_by_id: dict[str, str] = {}
        if df is not None and not df.empty:
            body_by_id = dict(zip(df["message_id"], df["body"]))

        for email_message in emails:
            clean_body = body_by_id.get(email_message.message_id, email_message.body)
            to_analyze = replace(email_message, body=clean_body)

            self.database.save_email(email_message)

            raw = self.ai_client.analyze_email(to_analyze)
            final = self._final_label(raw.risk_score)
            analysis = AnalysisResult(
                risk_score=raw.risk_score,
                label=final,
                reason=raw.reason,
                model_name=raw.model_name,
            )
            self.database.save_analysis(email_message.message_id, analysis)

            if analysis.risk_score >= self.risk_threshold:
                moved = self.imap_client.move_to_spam(email_message.message_id)
                if moved:
                    stats.moved_to_spam += 1

            stats.processed += 1
            print(f"İşlendi: {email_message.subject[:30]}... -> {analysis.label}")

        return stats
