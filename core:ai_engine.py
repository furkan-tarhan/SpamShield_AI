import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# API anahtarını sistemden oku
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class SpamAnalizMotoru:
    def __init__(self):
        # En hızlı ve verimli model
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analiz_et(self, email_baslik, email_icerik):
        # AI'ya verilecek talimat (Prompt)
        prompt = f"""
        Sen bir siber güvenlik uzmanısın. Şu e-postayı analiz et:
        Başlık: {email_baslik}
        İçerik: {email_icerik}
        
        Sadece JSON formatında şu bilgileri dön:
        - risk_skoru (0-100)
        - kategori (Spam/Güvenli)
        - sebep (Neden bu karar verildi?)
        """
        
        try:
            response = self.model.generate_content(prompt)
            # AI'dan gelen cevabı temizleyip sözlüğe çeviriyoruz
            temiz_cevap = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(temiz_cevap)
        except Exception as e:
            return {"risk_skoru": 0, "kategori": "Hata", "sebep": str(e)}