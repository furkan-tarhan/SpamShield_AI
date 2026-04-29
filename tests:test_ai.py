import unittest
from unittest.mock import MagicMock, patch
from core.ai_engine import SpamAnalizMotoru

class TestAI(unittest.TestCase):
    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_spam_tespiti(self, mock_ai):
        # Sahte bir AI cevabı oluşturuyoruz (API'yi harcamadan test etmek için)
        mock_cevap = MagicMock()
        mock_cevap.text = '{"risk_skoru": 95, "kategori": "Spam", "sebep": "Sahte link"}'
        mock_ai.return_value = mock_cevap

        motor = SpamAnalizMotoru()
        sonuc = motor.analiz_et("Hediye Kazandınız!", "Tıkla: http://sahte-link.com")

        # Test kontrolü: Risk skoru 95 mi?
        self.assertEqual(sonuc['risk_skoru'], 95)

if __name__ == '__main__':
    unittest.main()