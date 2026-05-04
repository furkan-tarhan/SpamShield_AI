import unittest
from unittest.mock import MagicMock
from backend.src.utils.processor import EmailProcessor

class TestEmailProcessor(unittest.TestCase):
    def test_clean_data_removes_html(self):
        """2. Hafta: Sahte veri ile temizleme testi."""
        mock_mail = MagicMock()
        mock_mail.message_id = "test-123"
        mock_mail.sender = "test@example.com"
        mock_mail.subject = "Konu"
        mock_mail.body = "<h1>Merhaba</h1><p>Bu bir testtir.</p>"
        mock_mail.received_at = "2026-05-04"

        # Veriyi işle
        df = EmailProcessor.clean_data([mock_mail])
        cikti_metni = df.iloc[0]['body']

        # KONTROLLER
        self.assertNotIn("<h1>", cikti_metni)
        # HTML etiketleri boşlukla değiştiği için arada İKİ boşluk olmalı
        self.assertIn("Merhaba Bu bir testtir.", cikti_metni)

if __name__ == '__main__':
    unittest.main()