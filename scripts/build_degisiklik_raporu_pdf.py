"""
SpamShield AI - yapilan degisikliklerin PDF raporunu uretir.
Calistir: python scripts/build_degisiklik_raporu_pdf.py
Cikti: docs/SpamShield_Degisiklik_Raporu.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs"
OUT_PDF = OUT_DIR / "SpamShield_Degisiklik_Raporu.pdf"

SECTIONS: list[tuple[str, list[str]]] = [
    (
        "Genel bakis",
        [
            "Bu rapor, PDF yol haritasina (4 haftalik backend plani) uyum ve teknik "
            "borclarin giderilmesi icin yapilan calismalari ozetler.",
            "Tarih: Mayis 2026 (proje guncellemesi).",
        ],
    ),
    (
        "1. Veritabani katmani (backend/src/storage/database.py)",
        [
            "SQLite semasi ile INSERT uyumu: body_preview kolonu, message_id tekilligi.",
            "Hatali _get_connection kullanimi kaldirildi; tum baglantilar _connect ile.",
            "save_email: mukerrer message_id kontrolu, alici tarih datetime/str destegi.",
            "save_analysis: ayni message_id icin once DELETE sonra INSERT (tek guncel analiz).",
            "Etiket normalizasyonu: spam / safe ve SQL tarafinda LOWER() ile filtre.",
            "get_emails_by_label, get_filtered_analysis, get_all_summaries sinif icine alindi; "
            "syntax hatalari ve disari tasinmis fonksiyonlar duzeltildi.",
            "get_dashboard_stats: toplam e-posta, spam sayisi, ortalama risk (tek akis, "
            "gereksiz tekrar sorgularinin azaltilmasi).",
            "idx_analysis_message_id indeksi eklendi.",
        ],
    ),
    (
        "2. E-posta pipeline (backend/src/services/email_pipeline.py)",
        [
            "EmailPipeline artik imap_client + ai_client + database + risk_threshold ile calisir; "
            "main.py ve pytest ile imza uyumu saglandi.",
            "Yerel SpamDetector yerine harici AI istemcisi (OpenAI uyumlu HTTP) kullanilir.",
            "EmailProcessor.clean_data (Pandas + HTML temizligi) analiz oncesi govde icin kullanilir.",
            "Nihai etiket: risk_score >= risk_threshold (varsayilan 40, .env: RISK_THRESHOLD) ise spam, "
            "aksi halde safe.",
            "Yuksek riskte imap_client.move_to_spam cagrisi korunur.",
        ],
    ),
    (
        "3. AI entegrasyonu (backend/src/integrations/ai_client.py)",
        [
            "Guvenlik odakli kullanici ve sistem promptlari guncellendi.",
            "MockAiClient sinifi bu dosyaya tasindi; API anahtari yokken sezgisel mock analiz.",
            "Mevcut retry, JSON parse ve hata sonrasi fallback davranisi korunur.",
        ],
    ),
    (
        "4. Backend CLI (backend/src/main.py)",
        [
            "MockAiClient importu ai_client modulunden yapilir (tekrarlayan sinif kaldirildi).",
            "Pipeline olusturma akisi onceki haliyle uyumludur.",
        ],
    ),
    (
        "5. masaustu arayuzu (CustomTkinter)",
        [
            "main.py (kök): Settings, Database, kosullu EmailPipeline (.env: EMAIL_ADDRESS, EMAIL_PASSWORD).",
            "DashboardFrame: canli istatistik (veritabani), TARAMAYI BASLAT arka planda pipeline.run.",
            "EmailListFrame: get_filtered_analysis('safe'), Yenile, Postayi cek (thread).",
            "SpamListFrame: get_filtered_analysis('spam'), Yenile; ornek veriler kaldirildi.",
            "dashboard_view.py: bozuk sinif yapisi ve [cite] kalintilari temizlendi; kartlar value_label ile guncellenir.",
        ],
    ),
    (
        "6. Testler",
        [
            "backend/tests/test_e2e.py: Mock IMAP + Mock AI + gercek SQLite ile uctan uca akis.",
            "backend/tests/test_ai_model.py: importta egitim calistiran script kaldirildi; "
            "tmp_path ile pytest uyumlu SpamDetector testi.",
            "backend/tests/test_pipeline.py: datetime.utcnow yerine timezone-aware UTC.",
            "backend/tests/test_processor.py: mevcut EmailProcessor testi korunur.",
        ],
    ),
    (
        "7. Proje yapisi ve bagimliliklar",
        [
            "data/ klasoru eklendi (.gitkeep) - PDF'teki veri klasoru beklentisi.",
            "requirements.txt: pytest, pandas, scikit-learn, joblib, customtkinter, pillow vb. eklendi.",
        ],
    ),
    (
        "PDF yol haritasi ile kalan maddeler (kod disi / istege bagli)",
        [
            "GitHub ana dal korumalari: depo ayarlarinda manuel yapilir.",
            "python -m venv: gelistirici makinesinde olusturulur, repoya konmaz.",
            "Gemini ozel SDK: su an OpenAI uyumlu URL/model ile Mistral vb. kullanilabilir; "
            "ayri SDK istenirse sonradan eklenebilir.",
        ],
    ),
]


def _find_unicode_font() -> str | None:
    candidates = [
        Path(r"C:\Windows\Fonts\arial.ttf"),
        Path(r"C:\Windows\Fonts\calibri.ttf"),
        Path(r"C:\Windows\Fonts\segoeui.ttf"),
    ]
    for p in candidates:
        if p.is_file():
            return str(p)
    return None


def build_pdf(path: Path) -> None:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    font_path = _find_unicode_font()
    font_name = "ReportFont"
    if font_path:
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        base_font = font_name
    else:
        base_font = "Helvetica"

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName=base_font,
        fontSize=18,
        spaceAfter=16,
        textColor=colors.HexColor("#1a5276"),
    )
    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontName=base_font,
        fontSize=13,
        spaceBefore=14,
        spaceAfter=8,
        textColor=colors.HexColor("#2874a6"),
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName=base_font,
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    story: list = []

    story.append(Paragraph("SpamShield AI", title_style))
    story.append(
        Paragraph(
            "Yapilan Degisiklikler Raporu (PDF yol haritasi uyumu)",
            ParagraphStyle(
                "Sub",
                parent=body_style,
                fontSize=12,
                textColor=colors.grey,
                spaceAfter=20,
            ),
        )
    )

    for heading, bullets in SECTIONS:
        story.append(Paragraph(_escape(heading), h2_style))
        for line in bullets:
            story.append(Paragraph(_bullet(_escape(line)), body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 20))
    story.append(
        Paragraph(
            _escape(
                "Bu PDF, scripts/build_degisiklik_raporu_pdf.py ile otomatik uretilmistir. "
                "Guncellemek icin ayni scriptteki SECTIONS listesini duzenleyip scripti tekrar calistirin."
            ),
            ParagraphStyle("Foot", parent=body_style, fontSize=9, textColor=colors.grey),
        )
    )

    doc.build(story)


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _bullet(text: str) -> str:
    return f"&bull; {text}"


def main() -> int:
    try:
        build_pdf(OUT_PDF)
    except Exception as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 1
    print(f"Olusturuldu: {OUT_PDF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
