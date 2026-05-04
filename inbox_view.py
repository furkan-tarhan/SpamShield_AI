import threading

import customtkinter


class EmailItemFrame(customtkinter.CTkFrame):
    def __init__(self, master, sender, subject, risk_level, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        self.sender_label = customtkinter.CTkLabel(
            self,
            text=sender,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            width=150,
            anchor="w",
        )
        self.sender_label.grid(row=0, column=0, padx=15, pady=10)

        self.subject_label = customtkinter.CTkLabel(
            self,
            text=subject,
            font=customtkinter.CTkFont(size=13),
            anchor="w",
        )
        self.subject_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        risk_color = "red" if risk_level > 40 else "green"
        self.risk_badge = customtkinter.CTkLabel(
            self,
            text=f"Risk: {risk_level}%",
            fg_color=risk_color,
            text_color="white",
            corner_radius=6,
            font=customtkinter.CTkFont(size=11, weight="bold"),
            width=80,
        )
        self.risk_badge.grid(row=0, column=2, padx=15, pady=10)


class EmailListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, database=None, pipeline=None, **kwargs):
        super().__init__(master, **kwargs)
        self.database = database
        self.pipeline = pipeline

        self.grid_columnconfigure(0, weight=1)

        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(
            self.header_frame,
            text="Inbox (Güvenli)",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.refresh_button = customtkinter.CTkButton(
            self.header_frame,
            text="Yenile",
            command=self.refresh_emails,
            width=100,
        )
        self.refresh_button.grid(row=0, column=1, sticky="e")

        self.sync_button = customtkinter.CTkButton(
            self.header_frame,
            text="Postayı çek",
            command=self.sync_from_imap,
            width=120,
        )
        self.sync_button.grid(row=0, column=2, padx=(8, 0), sticky="e")

        self.email_rows = []
        self.render_emails()

    def _load_safe_rows(self) -> list:
        if not self.database:
            return []
        rows = self.database.get_filtered_analysis("safe")
        return [(sender, subject, int(risk)) for sender, subject, risk, _ in rows]

    def render_emails(self) -> None:
        for row in self.email_rows:
            row.destroy()
        self.email_rows = []

        self.email_data = self._load_safe_rows()
        if not self.email_data:
            hint = customtkinter.CTkLabel(
                self,
                text="Henüz güvenli olarak işaretlenmiş kayıt yok. Postayı çek veya veritabanını doldur.",
                text_color="#888888",
            )
            hint.grid(row=1, column=0, padx=10, pady=20, sticky="w")
            self.email_rows.append(hint)
            return

        for i, (sender, subject, risk) in enumerate(self.email_data):
            row = EmailItemFrame(self, sender=sender, subject=subject, risk_level=risk)
            row.grid(row=i + 1, column=0, sticky="ew", padx=5, pady=2)
            self.email_rows.append(row)

    def refresh_emails(self) -> None:
        self.render_emails()

    def sync_from_imap(self) -> None:
        if self.pipeline is None:
            print("Pipeline yok: .env ile IMAP ayarlayın.")
            return

        self.sync_button.configure(state="disabled", text="Çekiliyor...")

        def work() -> None:
            try:
                self.pipeline.run(limit=15)
            finally:
                self.after(0, self._sync_finished)

        threading.Thread(target=work, daemon=True).start()

    def _sync_finished(self) -> None:
        self.sync_button.configure(state="normal", text="Postayı çek")
        self.render_emails()
