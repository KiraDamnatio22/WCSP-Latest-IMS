import ctypes
import customtkinter as ctk

from ui.login import LoginPage
from ui.main_window import IMSApp
from core import paths

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wintercool IMS")
        self.iconbitmap(paths.ICON_APP)
        self.geometry("800x600+300+50")
        self.resizable(False, False)

        # initialize frames
        self.login_page = LoginPage(self, on_login=self.show_main)
        self.main_page = IMSApp(self, on_logout=self.show_login)

        # show login first
        # self.login_page.pack(fill="both", expand=True)
        self.main_page.pack(fill="both", expand=True)
        self.after(1, lambda: self.state("zoomed"))

    def show_main(self):
        # ensure window zoom
        self.after(1, lambda: self.state("zoomed"))
        # self.disable_close_button(self)
        self.login_page.pack_forget()
        self.main_page.pack(fill="both", expand=True)

    def show_login(self):
        self.after(1, lambda: self.state("normal"))
        self.enable_close_button(self)
        self.main_page.pack_forget()
        self.login_page.pack(fill="both", expand=True)

    def disable_close_button(self, window):
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        menu = ctypes.windll.user32.GetSystemMenu(hwnd, False)
        ctypes.windll.user32.EnableMenuItem(menu, 0xF060, 0x1)  # SC_CLOSE = 0xF060, MF_GRAYED = 0x1

    def enable_close_button(self, window):
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        menu = ctypes.windll.user32.GetSystemMenu(hwnd, False)
        ctypes.windll.user32.EnableMenuItem(menu, 0xF060, 0x0)  # MF_ENABLED = 0x0

