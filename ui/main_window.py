# Import built-in modules
import customtkinter as ctk
from PIL import Image

# Import own-made modules
from core import paths
from core.permissions import admin_access_list

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class IMSApp(ctk.CTkFrame):
    def __init__(self, master, on_logout):
        super().__init__(master)
        self.on_logout = on_logout

        self.nav_items = {}
        self.active_page = None

        # Load icons
        self.icons = {
            "Home": ctk.CTkImage(light_image=Image.open(paths.ICON_HOME), size=(20, 20)),
            "Inventory": ctk.CTkImage(light_image=Image.open(paths.ICON_INVENTORY), size=(20, 20)),
            "Requests": ctk.CTkImage(light_image=Image.open(paths.ICON_REQUESTS), size=(20, 20)),
            "Purchases": ctk.CTkImage(light_image=Image.open(paths.ICON_PURCHASES), size=(20, 20)),
            "Suppliers": ctk.CTkImage(light_image=Image.open(paths.ICON_SUPPLIERS), size=(20, 20)),
            "Reports": ctk.CTkImage(light_image=Image.open(paths.ICON_REPORTS), size=(20, 20)),
            "Manage User": ctk.CTkImage(light_image=Image.open(paths.ICON_USERMANAGEMENT), size=(20, 20)),
            "Settings": ctk.CTkImage(light_image=Image.open(paths.ICON_SETTINGS), size=(20, 20)),
            "Help": ctk.CTkImage(light_image=Image.open(paths.ICON_HELP), size=(20, 20)),
            "Account": ctk.CTkImage(light_image=Image.open(paths.ICON_PROFILE24), size=(20, 20)),
        }

        self.logo_image = ctk.CTkImage(light_image=Image.open(paths.ICON_INVENTORY_MAIN_LOGO), size=(30, 30))

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=170, corner_radius=0, fg_color='#298753')
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Top Logo and Title
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.pack(pady=20, anchor="w")

        self.logo_label = ctk.CTkLabel(
            self.logo_frame,
            width=30,
            text_color="#ffffff",
            text=" Inventory",
            font=("Poppins", 23, "bold"),
            image=self.logo_image,
            compound="left",
        )
        self.logo_label.pack(
            side="left",
            padx=(6, 0),
            pady=(30, 30)
        )

        # Main Content
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color='#ffffff')
        self.main_content.pack(side="right", expand=True, fill="both")

        self.main_content.grid_rowconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(0, weight=1)

        # Page containers and setup registry
        self.pages = {}
        self.page_setup_registry = {}
        self.page_instances = {}

        self.create_pages()

        # Navigation items
        for label in self.icons.keys():
            if label == "Account":
                break

            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                image=self.icons[label],
                anchor="w",
                width=200,
                height=40,
                font=("Poppins", 13, "bold"),
                fg_color="transparent",
                text_color="#ffffff",
                # hover_color="#ffffff",
                hover=False,
                command=lambda l=label: self.select_nav(l))
            btn.pack(padx=5, pady=2, fill="x")
            self.nav_items[label] = btn

        acc_btn = ctk.CTkButton(
            self.sidebar,
            text="Account",
            image=self.icons["Account"],
            anchor="w",
            width=200,
            height=40,
            font=("Poppins", 13, "bold"),
            fg_color="transparent",
            text_color="#ffffff",
            hover_color="#ffffff",
            command=lambda l="Account": self.select_nav(l),
            hover=False
        )
        acc_btn.pack(padx=5, pady=(0, 15), fill="x", side='bottom')
        self.nav_items["Account"] = acc_btn

        # Default selection
        self.select_nav("Requests")

    def logout(self):
        # Always reset view back to Home before logging out
        if self.active_page:
            self.pages[self.active_page].lower()
        self.active_page = None
        self.select_nav("Account")

        if self.on_logout:
            self.on_logout()

    def create_pages(self):
        for label in self.icons:
            frame = ctk.CTkFrame(self.main_content, fg_color='#FFFFFF')
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            frame.lower()  # Hide initially
            self.pages[label] = frame

        self.page_setup_registry = {
            "Home": self.setup_home_page,
            "Inventory": self.setup_inventory_page,
            "Requests": self.setup_requests_page,
            "Purchases": self.setup_purchases_page,
            "Suppliers": self.setup_suppliers_page,
            "Reports": self.setup_reports_page,
            "Manage User": self.setup_user_management_page,
            "Settings": self.setup_settings_page,
            "Help": self.setup_help_page,
            "Account": self.setup_account_page,
        }

    def show_overlay(self, frame, text="Loading..."):
        overlay = ctk.CTkFrame(frame, fg_color="white")
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        label = ctk.CTkLabel(overlay, text=text, font=("Poppins", 18))
        label.pack(expand=True)
        return overlay

    def hide_overlay(self, overlay):
        if overlay:
            overlay.destroy()

    def select_nav(self, selected_label):
        if self.active_page == selected_label:
            return  # already selected

        # Highlight selected button
        for label, btn in self.nav_items.items():
            if label == selected_label:
                btn.configure(fg_color="#ffffff", text_color='#298753')
            else:
                btn.configure(fg_color='transparent', text_color='#ffffff')

        # Cleanup previous page if needed
        if self.active_page and self.active_page in self.page_instances:
            prev_instance = self.page_instances.get(self.active_page)
            if prev_instance and hasattr(prev_instance, "cleanup"):
                try:
                    prev_instance.cleanup()
                except Exception:
                    pass

        # Hide the previous page
        if self.active_page:
            self.pages[self.active_page].lower()

        frame = self.pages[selected_label]
        overlay = self.show_overlay(frame, text="Loading...")

        # Lift the (blank) frame immediately
        frame.lift()
        self.active_page = selected_label

        instance = self.page_instances.get(selected_label)
        if instance and hasattr(instance, "on_show"):
            instance.on_show()

        def do_setup_and_refresh():
            # Setup only once
            if selected_label not in self.page_instances:
                setup_func = self.page_setup_registry.get(selected_label)
                if setup_func:
                    setup_func()

            # Refresh every time
            instance = self.page_instances.get(selected_label)
            if instance:
                if hasattr(instance, "mark_stale_and_refresh"):
                    # Pass a callback to hide overlay *after refresh finishes*
                    instance.mark_stale_and_refresh(on_complete=lambda: self.hide_overlay(overlay))
                    return
                elif hasattr(instance, "refresh_inventory"):
                    instance.refresh_inventory(force_refresh=True)
            
            # Default: hide overlay immediately if nothing async happens
            self.hide_overlay(overlay)

        # Small delay so overlay is drawn before refresh kicks in
        self.after(50, do_setup_and_refresh)

    # PAGE SETUP METHODS
    def setup_home_page(self):
        if "Home" not in self.page_instances:
            frame = self.pages["Home"]
            label = ctk.CTkLabel(frame, text="Home Page", font=("Arial", 24))
            label.pack(pady=50)
            self.page_instances["Home"] = label

    def setup_inventory_page(self):
        if "Inventory" not in self.page_instances:
            frame = self.pages["Inventory"]
            widget = admin_access_list["Inventory"](frame)
            widget.pack(fill="both", expand=True)
            self.page_instances["Inventory"] = widget

    def setup_requests_page(self):
        if "Requests" not in self.page_instances:
            frame = self.pages["Requests"]
            widget = admin_access_list["Requests"](frame)
            widget.pack(fill="both", expand=True)
            self.page_instances["Requests"] = widget

    def setup_purchases_page(self):
        if "Purchases" not in self.page_instances:
            frame = self.pages["Purchases"]
            label = ctk.CTkLabel(frame, text="Purchase Orders", font=("Arial", 24))
            label.pack(pady=50)
            self.page_instances["Purchases"] = label

    def setup_suppliers_page(self):
        if "Suppliers" not in self.page_instances:
            frame = self.pages["Suppliers"]
            label = ctk.CTkLabel(frame, text="Item Suppliers", font=("Arial", 24))
            label.pack(pady=50)
            self.page_instances["Suppliers"] = label

    def setup_reports_page(self):
        if "Reports" not in self.page_instances:
            frame = self.pages["Reports"]
            label = ctk.CTkLabel(frame, text="View Reports", font=("Arial", 24))
            label.pack(pady=50)
            self.page_instances["Reports"] = label

    def setup_user_management_page(self):
        if "Manage User" not in self.page_instances:
            frame = self.pages["Manage User"]
            widget = admin_access_list["Manage User"](frame)
            widget.pack(fill="both", expand=True)
            self.page_instances["Manage User"] = widget

    def setup_settings_page(self):
        if "Settings" not in self.page_instances:
            frame = self.pages["Settings"]
            label = ctk.CTkLabel(frame, text="Settings", font=("Arial", 24))
            label.pack(pady=50)
            self.page_instances["Settings"] = label

    def setup_help_page(self):
        if "Help" not in self.page_instances:
            frame = self.pages["Help"]
            label = ctk.CTkLabel(frame, text="User Help", font=("Arial", 24))
            label.pack(pady=50)
            self.page_instances["Help"] = label

    def setup_account_page(self):
        if "Account" not in self.page_instances:
            frame = self.pages["Account"]
            widget = admin_access_list["Account"](frame)
            widget.pack(fill="both", expand=True)
            self.page_instances["Account"] = widget

    def view_existing_pages(self):
        print(f'\n SELF.PAGES\n\n {self.pages}')
        print(f'\n PAGE.INSTANCES\n\n {self.page_instances}')
