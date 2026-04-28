import customtkinter

class LoginFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)

        # 1. Title Label
        self.title_label = customtkinter.CTkLabel(
            self,
            text="SpamShield AI Login",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 2. Email Address Entry
        self.email_label = customtkinter.CTkLabel(self, text="Email Address:", font=customtkinter.CTkFont(size=12))
        self.email_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.email_entry = customtkinter.CTkEntry(
            self,
            placeholder_text="example@mail.com",
            width=300
        )
        self.email_entry.grid(row=2, column=0, padx=20, pady=10)

        # 3. App Password Entry
        self.password_label = customtkinter.CTkLabel(self, text="App Password:", font=customtkinter.CTkFont(size=12))
        self.password_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        self.password_entry = customtkinter.CTkEntry(
            self,
            show="*",
            width=300
        )
        self.password_entry.grid(row=4, column=0, padx=20, pady=10)

        # 4. IMAP Server OptionMenu
        self.imap_label = customtkinter.CTkLabel(self, text="IMAP Server:", font=customtkinter.CTkFont(size=12))
        self.imap_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")

        self.imap_menu = customtkinter.CTkOptionMenu(
            self,
            values=["Gmail", "Outlook", "Yahoo"],
            width=300
        )
        self.imap_menu.grid(row=6, column=0, padx=20, pady=10)
        self.imap_menu.set("Gmail") # Default value

        # 5. Connect Button
        self.connect_button = customtkinter.CTkButton(
            self,
            text="Connect",
            hover_color="#1f6aa5",
            command=self.connect_event,
            width=300
        )
        self.connect_button.grid(row=7, column=0, padx=20, pady=(20, 20))

    def connect_event(self):
        # BACKEND INTEGRATION POINT:
        # Add connection logic here using self.email_entry.get(),
        # self.password_entry.get(), and self.imap_menu.get()
        print(f"Connecting to {self.imap_menu.get()} for {self.email_entry.get()}...")

# --- Example Usage ---
# if __name__ == "__main__":
#     app = customtkinter.CTk()
#     app.geometry("400x500")
#     app.grid_columnconfigure(0, weight=1)
#     app.grid_rowconfigure(0, weight=1)
#
#     login_frame = LoginFrame(master=app)
#     login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
#
#     app.mainloop()
