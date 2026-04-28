import customtkinter

class EmailItemFrame(customtkinter.CTkFrame):
    def __init__(self, master, sender, subject, risk_level, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)

        # 1. Sender Label
        self.sender_label = customtkinter.CTkLabel(
            self,
            text=sender,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            width=150,
            anchor="w"
        )
        self.sender_label.grid(row=0, column=0, padx=15, pady=10)

        # 2. Subject Label
        self.subject_label = customtkinter.CTkLabel(
            self,
            text=subject,
            font=customtkinter.CTkFont(size=13),
            anchor="w"
        )
        self.subject_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # 3. Risk Level Indicator
        risk_color = "red" if risk_level > 40 else "green"
        self.risk_badge = customtkinter.CTkLabel(
            self,
            text=f"Risk: {risk_level}%",
            fg_color=risk_color,
            text_color="white",
            corner_radius=6,
            font=customtkinter.CTkFont(size=11, weight="bold"),
            width=80
        )
        self.risk_badge.grid(row=0, column=2, padx=15, pady=10)

class EmailListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Header / Refresh Area
        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 20))
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(
            self.header_frame,
            text="Inbox",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.refresh_button = customtkinter.CTkButton(
            self.header_frame,
            text="Refresh",
            command=self.refresh_emails,
            width=100
        )
        self.refresh_button.grid(row=0, column=1, sticky="e")

        # Initial dummy data
        self.email_data = [
            ("Security Team", "Suspicious login attempt detected", 85),
            ("Marketing Pro", "Exclusive deal just for you!", 25),
            ("Cloud Service", "Your monthly invoice is ready", 10),
            ("Unknown Sender", "Urgent: Action required on your account", 65),
            ("Support", "Ticket #4421 has been resolved", 5)
        ]

        self.email_rows = []
        self.render_emails()

    def render_emails(self):
        # Clear existing rows
        for row in self.email_rows:
            row.destroy()
        self.email_rows = []

        # BACKEND INTEGRATION: Loop through fetched email objects
        for i, (sender, subject, risk) in enumerate(self.email_data):
            row = EmailItemFrame(self, sender=sender, subject=subject, risk_level=risk)
            row.grid(row=i+1, column=0, sticky="ew", padx=5, pady=2)
            self.email_rows.append(row)

    def refresh_emails(self):
        # BACKEND INTEGRATION POINT:
        # 1. Trigger IMAP fetch
        # 2. Update self.email_data
        # 3. Call self.render_emails()
        print("Simulating IMAP fetch and refreshing list...")
        self.render_emails()

# --- Example Usage ---
# if __name__ == "__main__":
#     app = customtkinter.CTk()
#     app.geometry("800x600")
#     app.grid_columnconfigure(0, weight=1)
#     app.grid_rowconfigure(0, weight=1)
#
#     list_frame = EmailListFrame(master=app, width=700, height=500)
#     list_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
#
#     app.mainloop()
