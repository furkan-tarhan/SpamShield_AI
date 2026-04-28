# SpamShield AI Backend

Bu klasor, e-posta cekme, analiz etme ve sonuc kaydetme akisini yonetir.

## Klasor yapisi

- `src/config.py`: Ortam degiskenleri ve temel ayarlar
- `src/domain/models.py`: Veri siniflari
- `src/integrations/imap_client.py`: IMAP istemci arayuzu
- `src/integrations/ai_client.py`: AI istemci arayuzu
- `src/storage/database.py`: SQLite baglantisi ve tablo olusturma
- `src/services/email_pipeline.py`: Uctan uca email isleme akisi
- `src/main.py`: Calistirma giris noktasi
- `tests/`: Backend testleri

## Baslangic

1. Sanal ortam olustur
2. `pip install -r requirements.txt`
3. `.env.example` dosyasini `.env` olarak kopyala
4. `python -m backend.src.main`

## Faydalı komutlar

- `python -m backend.src.main --auth-only`: Sadece IMAP girisini test eder.
- AI istemcisi gecici hata alirsa otomatik retry dener; yine basarisiz olursa fallback analiz sonucu dondurur.
