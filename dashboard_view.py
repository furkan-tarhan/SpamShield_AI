import customtkinter

class DashboardCard(customtkinter.CTkFrame):
    def __init__(self, master, title, value, subtext=None, progress=None, icon_color=None, **kwargs):
        super().__init__(master, **kwargs)

        # Glassmorphism aesthetic: semi-transparent dark background with border
        self.configure(fg_color="#1e1e1e", border_width=1, border_color="#333333")

        self.grid_columnconfigure(0, weight=1)

        # 1. Title
        self.title_label = customtkinter.CTkLabel(
            self,
            text=title,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color="#888888",
            anchor="w"
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        # 2. Main Value
        self.value_label = customtkinter.CTkLabel(
            self,
            text=value,
            font=customtkinter.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        self.value_label.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="w")

        # 3. Dynamic Elements (Progress Bar, Subtext, or Icon)
        if progress is not None:
            self.progress_bar = customtkinter.CTkProgressBar(
                self,
                progress_color="#1f6aa5",
                width=200
            )
            self.progress_bar.set(progress)
            self.progress_bar.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="ew")

        elif subtext:
            # For "Threats Blocked" or "AI Confidence"
            self.subtext_label = customtkinter.CTkLabel(
                self,
                text=subtext,
                font=customtkinter.CTkFont(size=11),
                text_color=icon_color if icon_color else "#888888"
            )
            self.subtext_label.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

class DashboardFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure((0, 1, 2), weight=1, pad=20)

        # Card 1: TOTAL SCANNED
        self.scanned_card = DashboardCard(
            self,
            title="TOTAL SCANNED",
            value="1,284",
            progress=0.7
        )
        self.scanned_card.grid(row=0, column=0, sticky="nsew", padx=10)

        # Card 2: THREATS BLOCKED
        self.threats_card = DashboardCard(
            self,
            title="THREATS BLOCKED",
            value="42",
            subtext="▲ +12% vs yesterday",
            icon_color="#e74c3c" # Alert Red
        )
        self.threats_card.grid(row=0, column=1, sticky="nsew", padx=10)

        # Card 3: AI CONFIDENCE
        self.confidence_card = DashboardCard(
            self,
            title="AI CONFIDENCE",
            value="99.8%",
            subtext="Model v4.2-Stable"
        )
        self.confidence_card.grid(row=0, column=2, sticky="nsew", padx=10)

# --- Example Usage ---
# if __name__ == "__main__":
#     app = customtkinter.CTk()
#     app.geometry("1000x300")
#     app.configure(fg_color="#121212")
#
#     dashboard = DashboardFrame(master=app)
#     dashboard.pack(fill="x", padx=20, pady=50)
#
#     app.mainloop()
