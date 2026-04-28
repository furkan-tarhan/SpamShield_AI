import customtkinter as ctk

class EmailDetailWindow(ctk.CTkToplevel):
    def __init__(self, master, sender, subject, content, risk_score, ai_analysis, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Email Analysis Detail")
        self.geometry("600x700")
        self.configure(fg_color="#0a0a0a") # Görseldeki gibi derin siyah

        # Pencereyi her zaman üstte tut
        self.attributes("-topmost", True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # İçerik alanı genişlesin

        # --- HEADER ---
        self.header_label = ctk.CTkLabel(self, text="DETAILED ANALYSIS", font=ctk.CTkFont(size=14, weight="bold", slant="italic"), text_color="#888888")
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # --- SUBJECT & SENDER ---
        self.info_frame = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=10)
        self.info_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.subj_label = ctk.CTkLabel(self.info_frame, text=subject, font=ctk.CTkFont(size=18, weight="bold"), wraplength=540, justify="left")
        self.subj_label.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        self.sender_label = ctk.CTkLabel(self.info_frame, text=f"From: {sender}", font=ctk.CTkFont(size=13), text_color="#aaaaaa")
        self.sender_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")

        # --- RISK SCORE BADGE ---
        risk_color = "#ff4444" if risk_score > 40 else "#00c851"
        self.risk_box = ctk.CTkFrame(self, fg_color=risk_color, corner_radius=5)
        self.risk_box.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.risk_label = ctk.CTkLabel(self.risk_box, text=f"AI RISK SCORE: {risk_score}%", text_color="white", font=ctk.CTkFont(size=12, weight="bold"))
        self.risk_label.pack(padx=10, pady=5)

        # --- CONTENT & AI REASONING (Scrollable) ---
        self.content_area = ctk.CTkScrollableFrame(self, fg_color="#111111", corner_radius=10)
        self.content_area.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")

        # Original Mail Content
        self.mail_content_title = ctk.CTkLabel(self.content_area, text="ORIGINAL CONTENT:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#1f6aa5")
        self.mail_content_title.pack(padx=10, pady=(10, 5), anchor="w")

        self.mail_body = ctk.CTkLabel(self.content_area, text=content, wraplength=500, justify="left", font=ctk.CTkFont(size=13))
        self.mail_body.pack(padx=10, pady=(0, 20), anchor="w")

        # AI Analysis/Reasoning
        self.ai_title = ctk.CTkLabel(self.content_area, text="AI ANALYSIS REPORT:", font=ctk.CTkFont(size=11, weight="bold"), text_color="#e74c3c")
        self.ai_title.pack(padx=10, pady=(10, 5), anchor="w")

        self.ai_text = ctk.CTkLabel(self.content_area, text=ai_analysis, wraplength=500, justify="left", font=ctk.CTkFont(size=13, slant="italic"))
        self.ai_text.pack(padx=10, pady=(0, 20), anchor="w")

        # --- ACTIONS ---
        self.close_button = ctk.CTkButton(self, text="CLOSE", command=self.destroy, fg_color="#333333", hover_color="#444444")
        self.close_button.grid(row=4, column=0, padx=20, pady=20)