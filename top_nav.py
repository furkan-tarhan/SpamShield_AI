import customtkinter

class TopNavBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=60, fg_color="#000000", corner_radius=0, **kwargs)

        # Configure grid layout: 3 columns (Logo, Search, Actions)
        self.grid_columnconfigure(0, weight=1) # Logo area
        self.grid_columnconfigure(1, weight=2) # Search bar area
        self.grid_columnconfigure(2, weight=1) # Icons area
        self.grid_propagate(False) # Force the 60px height

        # 1. Logo / Brand (Left)
        self.logo_label = customtkinter.CTkLabel(
            self,
            text="SPAMSHIELD_AI",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        self.logo_label.grid(row=0, column=0, padx=20, sticky="w")

        # 2. Search Bar (Center)
        self.search_frame = customtkinter.CTkFrame(
            self,
            fg_color="#2a2a2a",
            height=36,
            corner_radius=8
        )
        self.search_frame.grid(row=0, column=1, pady=12, sticky="ew")
        self.search_frame.grid_columnconfigure(1, weight=1)

        # Magnifying Glass Placeholder (using text for simplicity)
        self.search_icon = customtkinter.CTkLabel(self.search_frame, text="🔍", text_color="#888888")
        self.search_icon.grid(row=0, column=0, padx=(10, 5))

        self.search_entry = customtkinter.CTkEntry(
            self.search_frame,
            placeholder_text="Search system...",
            border_width=0,
            fg_color="transparent",
            height=30
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        # 3. Action Icons (Right)
        self.actions_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=0, column=2, padx=20, sticky="e")

        self.notif_button = customtkinter.CTkButton(
            self.actions_frame, text="🔔", width=30, fg_color="transparent", hover_color="#2a2a2a"
        )
        self.notif_button.grid(row=0, column=0, padx=5)

        self.settings_button = customtkinter.CTkButton(
            self.actions_frame, text="⚙️", width=30, fg_color="transparent", hover_color="#2a2a2a"
        )
        self.settings_button.grid(row=0, column=1, padx=5)

        # Circular Profile Placeholder
        self.profile_btn = customtkinter.CTkButton(
            self.actions_frame,
            text="EE",
            width=36,
            height=36,
            corner_radius=18,
            fg_color="#1f6aa5",
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        self.profile_btn.grid(row=0, column=2, padx=(10, 0))

# --- Example Usage ---
# if __name__ == "__main__":
#     app = customtkinter.CTk()
#     app.geometry("1000x200")
#     app.configure(fg_color="#1a1a1a")
#
#     nav_bar = TopNavBar(master=app)
#     nav_bar.pack(fill="x")
#
#     app.mainloop()
