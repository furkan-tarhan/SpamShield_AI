import customtkinter as ctk

from inbox_view import EmailItemFrame


class SpamListFrame(ctk.CTkFrame):
    def __init__(self, master, database=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.database = database

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Spam & Threat Detection",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#e74c3c",
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.action_bar = ctk.CTkFrame(self, height=45, fg_color="#111111", corner_radius=8)
        self.action_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.action_bar.grid_columnconfigure(2, weight=1)
        self.action_bar.grid_propagate(False)

        self.delete_btn = ctk.CTkButton(
            self.action_bar,
            text="Delete All Spam",
            width=120,
            height=28,
            fg_color="#3d1414",
            hover_color="#5a1a1a",
            text_color="#ff4444",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.delete_btn.grid(row=0, column=0, padx=15, pady=8)

        self.safe_btn = ctk.CTkButton(
            self.action_bar,
            text="Mark All Safe",
            width=120,
            height=28,
            fg_color="transparent",
            border_width=1,
            border_color="#333333",
            hover_color="#242424",
            text_color="#888888",
        )
        self.safe_btn.grid(row=0, column=1, padx=5, pady=8)

        self.refresh_btn = ctk.CTkButton(
            self.action_bar,
            text="Yenile",
            width=90,
            height=28,
            command=self.render_spam,
        )
        self.refresh_btn.grid(row=0, column=2, padx=8, pady=8, sticky="e")

        self.list_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_container.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.list_container.grid_columnconfigure(0, weight=1)

        self.render_spam()

    def _spam_tuples(self) -> list:
        if not self.database:
            return []
        rows = self.database.get_filtered_analysis("spam")
        return [(sender, subject, int(risk)) for sender, subject, risk, _ in rows]

    def render_spam(self) -> None:
        for w in self.list_container.winfo_children():
            w.destroy()
        self.spam_rows.clear()

        rows = self._spam_tuples()
        for i, (sender, subject, risk) in enumerate(rows):
            row = EmailItemFrame(self.list_container, sender=sender, subject=subject, risk_level=risk)
            row.grid(row=i, column=0, sticky="ew", padx=5, pady=2)

        if not rows:
            ctk.CTkLabel(
                self.list_container,
                text="Spam kaydı yok.",
                text_color="#888888",
            ).grid(row=0, column=0, padx=10, pady=20, sticky="w")
