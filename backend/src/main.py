import argparse

from backend.src.config import Settings
from backend.src.domain.models import AnalysisResult, EmailMessage
from backend.src.integrations.ai_client import OpenAiCompatibleClient
from backend.src.integrations.imap_client import GmailImapClient
from backend.src.services.email_pipeline import EmailPipeline
from backend.src.storage.database import Database


class MockAiClient:
    def analyze_email(self, email_message: EmailMessage) -> AnalysisResult:
        return AnalysisResult(
            risk_score=85,
            label="spam",
            reason="Suspicious urgent language and link pattern.",
            model_name="mock-model",
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--auth-only",
        action="store_true",
        help="Sadece IMAP girisini test eder, pipeline calistirmaz.",
    )
    args = parser.parse_args()

    settings = Settings()
    print(
        "Auth debug -> "
        f"host={settings.imap_host}, "
        f"port={settings.imap_port}, "
        f"email_set={bool(settings.email_address)}, "
        f"password_len={len(settings.email_password.strip()) if settings.email_password else 0}"
    )

    if not settings.email_address or not settings.email_password:
        raise ValueError(
            "EMAIL_ADDRESS ve EMAIL_PASSWORD bos. Lutfen .env dosyasini doldur."
        )

    database = Database(settings.sqlite_path)
    imap_client = GmailImapClient(
        host=settings.imap_host,
        port=settings.imap_port,
        username=settings.email_address,
        password=settings.email_password,
    )

    if args.auth_only:
        imap_client.test_connection()
        print("IMAP login basarili.")
        return

    ai_client = (
        OpenAiCompatibleClient(
            api_key=settings.ai_api_key,
            base_url=settings.ai_base_url,
            model=settings.ai_model,
        )
        if settings.ai_api_key
        else MockAiClient()
    )
    if not settings.ai_api_key:
        print("AI_API_KEY bulunamadi, MockAiClient kullaniliyor.")

    pipeline = EmailPipeline(
        imap_client=imap_client,
        ai_client=ai_client,
        database=database,
        risk_threshold=settings.risk_threshold,
    )
    stats = pipeline.run(limit=10)
    print(f"Processed: {stats.processed} | Moved to spam: {stats.moved_to_spam}")


if __name__ == "__main__":
    main()
