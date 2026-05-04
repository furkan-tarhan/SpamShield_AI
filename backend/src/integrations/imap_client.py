from datetime import datetime, timezone
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import imaplib
from typing import List, Optional, Protocol

from backend.src.domain.models import EmailMessage


class ImapClient(Protocol):
    def fetch_unread_messages(self, limit: int = 20) -> List[EmailMessage]:
        ...

    def move_to_spam(self, message_id: str) -> bool:
        ...


class GmailImapClient:
    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    # backend/src/integrations/imap_client.py

    def fetch_unread_messages(self, limit: int = 10) -> List[EmailMessage]:
        messages: List[EmailMessage] = []
        # Bağlantıyı kuruyoruz
        with self._connect() as mail:
            mail.select("INBOX")
            # 2. Hafta Görevi: Okunmamış (UNSEEN) mailleri arıyoruz
            status, data = mail.search(None, "UNSEEN")
            
            if status != "OK" or not data or not data[0]:
                return messages
            
            # Mail ID'lerini alıyoruz
            mail_ids = data[0].split()
            
            # Son 'limit' kadar maili ters sırayla (en yeni en başta) alalım
            for mail_id in reversed(mail_ids[-limit:]):
                status, raw_message = mail.fetch(mail_id, "(RFC822)")
                if status != "OK":
                    continue
                
                # Burada maili parse (ayrıştırma) edeceğiz
                # 2. Hafta Görevi: HTML'den düz metne dönüştürme burada başlayacak
                payload = raw_message[0][1]
                parsed = email.message_from_bytes(payload)
                
                # Modellerimize uygun şekilde listeye ekliyoruz
                # (Furkan'ın hazırladığı yardımcı fonksiyonları kullanmaya devam ediyoruz)
                messages.append(
                    EmailMessage(
                        message_id=parsed.get("Message-ID", "").strip(),
                        sender=self._decode_mime_header(parsed.get("From", "Unknown")),
                        subject=self._decode_mime_header(parsed.get("Subject", "(no subject)")),
                        body=self._extract_text_body(parsed), # İşte HTML temizleme burada yapılıyor!
                        received_at=self._parse_email_date(parsed.get("Date")),
                    )
                )
        return messages

    def move_to_spam(self, message_id: str) -> bool:
        with self._connect() as mail:
            mail.select("INBOX")
            status, ids_data = mail.search(None, f'HEADER Message-ID "{message_id}"')
            if status != "OK" or not ids_data or not ids_data[0]:
                return False

            for mail_id in ids_data[0].split():
                # Gmail'de \Spam etiketi ile hedef klasore tasiyoruz.
                copied, _ = mail.copy(mail_id, "[Gmail]/Spam")
                if copied != "OK":
                    return False
                mail.store(mail_id, "+FLAGS", "\\Deleted")

            mail.expunge()
            return True

    def test_connection(self) -> bool:
        with self._connect():
            return True

    def _connect(self) -> imaplib.IMAP4_SSL:
        mail = imaplib.IMAP4_SSL(self.host, self.port)
        mail.login(self.username, self.password)
        return mail

    @staticmethod
    def _decode_mime_header(value: str) -> str:
        decoded_parts = decode_header(value)
        chunks: List[str] = []
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                chunks.append(part.decode(encoding or "utf-8", errors="replace"))
            else:
                chunks.append(part)
        return "".join(chunks).strip()

    @staticmethod
    def _extract_text_body(parsed_message: email.message.Message) -> str:
        if parsed_message.is_multipart():
            for part in parsed_message.walk():
                content_type = part.get_content_type()
                disposition = str(part.get("Content-Disposition", ""))
                if content_type == "text/plain" and "attachment" not in disposition.lower():
                    payload = part.get_payload(decode=True)
                    if payload is None:
                        continue
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace").strip()
            return ""

        payload = parsed_message.get_payload(decode=True)
        if payload is None:
            return ""
        charset = parsed_message.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="replace").strip()

    @staticmethod
    def _parse_email_date(date_header: Optional[str]) -> datetime:
        if not date_header:
            return datetime.now(timezone.utc)
        try:
            parsed_date = parsedate_to_datetime(date_header)
            if parsed_date.tzinfo is None:
                return parsed_date.replace(tzinfo=timezone.utc)
            return parsed_date
        except (TypeError, ValueError):
            return datetime.now(timezone.utc)
