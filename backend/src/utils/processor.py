import pandas as pd
import re

class EmailProcessor:
    @staticmethod
    def remove_html(text):
        """Metindeki HTML etiketlerini temizler."""
        if not text:
            return ""
        # 'clean' değişkenini burada tanımlıyoruz
        clean_reg = re.compile('<.*?>')
        return re.sub(clean_reg, ' ', text)

    @staticmethod
    def clean_data(emails_list):
        """E-postaları temizleyip DataFrame'e dönüştürür."""
        if not emails_list:
            return None
            
        df = pd.DataFrame([
            {
                'message_id': e.message_id,
                'sender': e.sender,
                'subject': e.subject,
                'body': e.body,
                'received_at': e.received_at
            } for e in emails_list
        ])
        
        # Temizleme işlemini çağırıyoruz
        df['body'] = df['body'].apply(EmailProcessor.remove_html)
        df['body'] = df['body'].str.replace(r'\s+', ' ', regex=True).str.strip()
        df['body'] = df['body'].str[:1000] 
        
        return df