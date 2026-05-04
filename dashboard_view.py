import threading
import customtkinter


class DashboardCard(customtkinter.CTkFrame):
    def __init__(
        self,
        master,
        title,
        value,
        subtext=None,
        progress=None,
        icon_color=None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.configure(fg_color="#1e1e1e", border_width=1, border_color="#333333")

        self.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(
            self,
            text=title,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color="#888888",
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        self.value_label = customtkinter.CTkLabel(
            self,
            text=value,
            font=customtkinter.CTkFont(size=28, weight="bold"),
            text_color="white",
        )
        self.value_label.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="w")

        if progress is not None:
            self.progress_bar = customtkinter.CTkProgressBar(
                self,
                progress_color="#1f6aa5",
                width=200,
            )
            self.progress_bar.set(progress)
            self.progress_bar.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="ew")

        elif subtext:
            self.subtext_label = customtkinter.CTkLabel(
                self,
                text=subtext,
                font=customtkinter.CTkFont(size=11),
                text_color=icon_color if icon_color else "#888888",
            )
            self.subtext_label.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")


class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, database=None, pipeline=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.database = database
        self.pipeline = pipeline

        self.grid_columnconfigure((0, 1, 2), weight=1, pad=20)
        self.grid_rowconfigure(0, weight=0)

        self.scanned_card = DashboardCard(
            self,
            title="TOTAL SCANNED",
            value="0",
            progress=0.0,
        )
        self.scanned_card.grid(row=0, column=0, sticky="nsew", padx=10)

        self.threats_card = DashboardCard(
            self,
            title="THREATS (SPAM)",
            value="0",
            subtext="Veritabanından",
            icon_color="#e74c3c",
        )
        self.threats_card.grid(row=0, column=1, sticky="nsew", padx=10)

        self.confidence_card = DashboardCard(
            self,
            title="ORTALAMA RİSK",
            value="—",
            subtext="Analiz edilen postalar",
        )
        self.confidence_card.grid(row=0, column=2, sticky="nsew", padx=10)

        self.scan_button = customtkinter.CTkButton(
            self,
            text="TARAMAYI BAŞLAT",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870",
            height=40,
            command=self.start_scan_event,
        )
        self.scan_button.grid(row=1, column=0, columnspan=3, pady=(30, 0), padx=40, sticky="ew")

        self._refresh_from_db()

    def _refresh_from_db(self) -> None:
        if not self.database:
            return
        stats = self.database.get_dashboard_stats()
        total = int(stats.get("total_emails", 0))
        spam_n = int(stats.get("spam_count", 0))
        avg_risk = stats.get("avg_risk")

        self.scanned_card.value_label.configure(text=f"{total:,}".replace(",", "."))
        if hasattr(self.scanned_card, "progress_bar"):
            self.scanned_card.progress_bar.set(min(1.0, total / 100.0) if total else 0.0)

        self.threats_card.value_label.configure(text=str(spam_n))

        if avg_risk is None:
            self.confidence_card.value_label.configure(text="—")
        else:
            self.confidence_card.value_label.configure(text=f"{int(round(avg_risk))}%")

    def start_scan_event(self) -> None:
        if self.pipeline is None:
            print("Pipeline yok: .env içinde EMAIL_ADDRESS / EMAIL_PASSWORD gerekli.")
            return

        self.scan_button.configure(state="disabled", text="Taranıyor...")

        def work() -> None:
            try:
                self.pipeline.run(limit=10)
            finally:
                self.after(0, self._scan_finished)

        threading.Thread(target=work, daemon=True).start()

    def _scan_finished(self) -> None:
        self.scan_button.configure(state="normal", text="TARAMAYI BAŞLAT")
        self._refresh_from_db()
