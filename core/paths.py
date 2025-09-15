# paths.py
import os, sys

def resource_path(*parts):
    """
    Build an absolute path to a resource file.
    Works in both development and when packaged with PyInstaller.

    Example:
        ICON_APP = resource_path("icons", "wcsp_logo.ico")
    """
    if hasattr(sys, "_MEIPASS"):
        # running inside a PyInstaller bundle
        base_dir = sys._MEIPASS
    else:
        # running in normal Python
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(base_dir, *parts))


# Use-cases
# ".." means a resoure file is found outside subfolder
# "../.." means a resource file is found outside main folder
# omitting either ".." or "../.." means a resource file is found inside the current folder

# --- ICONS ---
ICON_APP      = resource_path("..", "icons", "wcsp_logo.ico")
ICON_HOME = resource_path("..", "icons", "navigation", "home.png")
ICON_INVENTORY = resource_path("..", "icons", "navigation", "inventory.png")
ICON_REQUESTS = resource_path("..", "icons", "navigation", "requests.png")
ICON_PURCHASES = resource_path("..", "icons", "navigation", "purchases.png")
ICON_SUPPLIERS = resource_path("..", "icons", "navigation", "suppliers.png")
ICON_REPORTS = resource_path("..", "icons", "navigation", "reports.png")
ICON_USERMANAGEMENT = resource_path("..", "icons", "navigation", "user_management.png")
ICON_SETTINGS = resource_path("..", "icons", "navigation", "settings.png")
ICON_HELP = resource_path("..", "icons", "navigation", "help.png")
ICON_PROFILE24 = resource_path("..", "icons", "navigation", "profile-24.png")
ICON_INVENTORY_MAIN_LOGO = resource_path("..", "icons", "navigation", "inventory_main_logo.png")
ICON_BACK = resource_path("..", "icons", "navigation", "back.png")
ICON_TOTAL = resource_path("..", "icons", "total.png")
ICON_STOCK_ALERTS = resource_path("..", "icons", "stock_alerts.png")
ICON_OUT_STOCK = resource_path("..", "icons", "out_of_stock.png")
ICON_ADD_PLUS = resource_path("..", "icons", "plus_add_icon.png")

# --- EMOJIS ---
EMOJI_IN_STOCK = resource_path("..", "icons", "in_stock_emoji.png")
EMOJI_LOW_STOCK = resource_path("..", "icons", "low_stock_emoji.png")
EMOJI_OUT_STOCK = resource_path("..", "icons", "out_of_stock_emoji.png")

# --- IMAGES ---
IMAGE_APP = resource_path("..", "icons", "wcsp_icon.png")
IMAGE_LOGIN_BG = resource_path("..", "icons", "login", "WCSP-IMS-BG.png")
IMAGE_EMPTY = resource_path("..", "icons", "empty_2.png")
IMAGE_PLACEHOLDER = resource_path("..", "icons", "placeholder_image_original.png")
IMAGE_PROFILE_COVER = resource_path("..", "icons", "account", "profile_cover_photo.png")

# --- DATABASES ---
DB_MAIN = resource_path("backend.db")

# --- OTHER ASSETS ---
# LOGO_MAIN     = resource_path("assets", "company_logo.png")
# THEME_FILE    = resource_path("themes", "light_theme.json")
