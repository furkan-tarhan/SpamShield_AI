import customtkinter
import tkinter
from PIL import Image

from spam_view import SpamListFrame
from top_nav import TopNavBar
from dashboard_view import DashboardFrame
from inbox_view import EmailListFrame
from login_view import LoginFrame

# Basic configuration
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. PENCERE AYARLARI ---
        self.title("SpamShield AI")
        self.geometry("1100x650") # Biraz daha uzun yaptık

        # --- 2. GRID YAPISI (PROJE MİMARİSİ) ---
        # 0. Sütun: Sidebar | 1. Sütun: Main Content
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # 0. Satır: Top Nav Bar | 1. Satır: Alt Panel (Sidebar + Main)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # --- 3. TOP NAV BAR ---
        self.nav_bar = TopNavBar(master=self)
        self.nav_bar.grid(row=0, column=0, columnspan=2, sticky="ew")

        # --- 4. SIDEBAR FRAME ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0, fg_color="#0d0d0d")
        self.sidebar_frame.grid(row=1, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) # Spacer

        # Logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="SPAMSHIELD", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        # Butonlar
        self.dashboard_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=45, text="Dashboard",
                                                        fg_color="transparent", anchor="w", command=self.dashboard_button_event)
        self.dashboard_button.grid(row=1, column=0, sticky="ew")

        self.inbox_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=45, text="Inbox",
                                                    fg_color="transparent", anchor="w", command=self.inbox_button_event)
        self.inbox_button.grid(row=2, column=0, sticky="ew")

        self.spam_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=45, text="Spam",
                                                   fg_color="transparent", anchor="w", command=self.spam_button_event)
        self.spam_button.grid(row=3, column=0, sticky="ew")

        self.settings_button = customtkinter.CTkButton(self.sidebar_frame, corner_radius=0, height=45, text="Settings",
                                                       fg_color="transparent", anchor="w", command=self.settings_button_event)
        self.settings_button.grid(row=4, column=0, sticky="ew")

        # --- 5. MAIN CONTENT FRAME ---
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="#121212")
        self.main_frame.grid(row=1, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Varsayılan Sayfa
        self.select_frame_by_name("dashboard")

    def select_frame_by_name(self, name):
        # Aktif butonu boya
        self.dashboard_button.configure(fg_color=("gray75", "#1f6aa5") if name == "dashboard" else "transparent")
        self.inbox_button.configure(fg_color=("gray75", "#1f6aa5") if name == "inbox" else "transparent")
        self.spam_button.configure(fg_color=("gray75", "#1f6aa5") if name == "spam" else "transparent")
        self.settings_button.configure(fg_color=("gray75", "#1f6aa5") if name == "settings" else "transparent")

        # Ekranı temizle
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if name == "dashboard":
            self.create_dashboard_view()
        elif name == "inbox":
            self.create_inbox_view()
        elif name == "spam":
            self.create_spam_view()
        elif name == "settings":
            self.create_settings_view()

    def create_dashboard_view(self):
        # DashboardFrame'i merkeze tam oturt
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.welcome_label = customtkinter.CTkLabel(self.main_frame, text="System Overview", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.welcome_label.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="w")

        self.stats_screen = DashboardFrame(master=self.main_frame)
        self.stats_screen.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

    def create_inbox_view(self):
        self.inbox_screen = EmailListFrame(master=self.main_frame, fg_color="transparent")
        self.inbox_screen.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def create_spam_view(self):
        # Karmaşık importlara gerek kalmadı, sadece SpamListFrame yeterli
        self.spam_screen = SpamListFrame(master=self.main_frame)
        self.spam_screen.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def create_settings_view(self):
        self.login_screen = LoginFrame(master=self.main_frame, fg_color="transparent")
        self.login_screen.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def dashboard_button_event(self): self.select_frame_by_name("dashboard")
    def inbox_button_event(self): self.select_frame_by_name("inbox")
    def spam_button_event(self): self.select_frame_by_name("spam")
    def settings_button_event(self): self.select_frame_by_name("settings")

if __name__ == "__main__":
    app = App()
    app.mainloop()