import customtkinter as ctk
from inbox_view import EmailItemFrame # Mevcut satır yapısını kullanıyoruz

class SpamListFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Liste alanının uzamasını sağlar

        # --- 1. BAŞLIK ---
        self.title_label = ctk.CTkLabel(self, text="Spam & Threat Detection",
                                        font=ctk.CTkFont(size=22, weight="bold"), text_color="#e74c3c")
        self.title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # --- 2. AKSİYON BARI (Inline Tasarım) ---
        # Ayrı bir sınıf yerine doğrudan burada oluşturuyoruz
        self.action_bar = ctk.CTkFrame(self, height=45, fg_color="#111111", corner_radius=8)
        self.action_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.action_bar.grid_columnconfigure(2, weight=1) # Boşluk için
        self.action_bar.grid_propagate(False)

        # Silme Butonu
        self.delete_btn = ctk.CTkButton(self.action_bar, text="Delete All Spam", width=120, height=28,
                                        fg_color="#3d1414", hover_color="#5a1a1a", text_color="#ff4444",
                                        font=ctk.CTkFont(size=12, weight="bold"))
        self.delete_btn.grid(row=0, column=0, padx=15, pady=8)

        # Güvenli İşaretleme
        self.safe_btn = ctk.CTkButton(self.action_bar, text="Mark All Safe", width=120, height=28,
                                      fg_color="transparent", border_width=1, border_color="#333333",
                                      hover_color="#242424", text_color="#888888")
        self.safe_btn.grid(row=0, column=1, padx=5, pady=8)

        # --- 3. KAYDIRILABİLİR LİSTE ---
        self.list_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.list_container.grid_columnconfigure(0, weight=1)

        # Örnek Veriler
        self.spam_data = [
            ("Netflix Support", "Suspicious login attempt from Ohio, US", 88),
            ("Crypto-Bot", "You have 1.24 BTC waiting for withdrawal", 95),
            ("Unknown Sender", "Urgent: Verify your account details immediately", 72)
        ]

        self.render_spam()

    def render_spam(self):
        for i, (sender, subject, risk) in enumerate(self.spam_data):
            row = EmailItemFrame(self.list_container, sender=sender, subject=subject, risk_level=risk)
            row.grid(row=i, column=0, sticky="ew", padx=5, pady=2)