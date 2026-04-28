from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    imap_host: str = os.getenv("IMAP_HOST", "imap.gmail.com")
    imap_port: int = int(os.getenv("IMAP_PORT", "993"))
    email_address: str = os.getenv("EMAIL_ADDRESS", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    ai_base_url: str = os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
    ai_model: str = os.getenv("AI_MODEL", "gpt-4o-mini")
    risk_threshold: int = int(os.getenv("RISK_THRESHOLD", "40"))
    sqlite_path: str = os.getenv("SQLITE_PATH", "spamshield.db")
