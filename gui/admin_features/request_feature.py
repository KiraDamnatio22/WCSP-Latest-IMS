import customtkinter as ctk
from datetime import datetime
from PIL import Image

from core import paths
from ui.notifs import CustomMessageBox
from .material_request_form import MaterialReqForm
from core.ims_data import ACSpecs, field_employees, aircon_brands, aircon_hps

# Constants
BUTTON_FG_COLOR = "#FFFFFF"
BUTTON_BORDER_COLOR = "gray"
COLOR_GRAY = "#e8e8e8"
COLOR_GREEN = "#4BAC76"
COLOR_GREEN_HOVER = "#298753"
FRAMES_FG_COLOR = "#C0F0C0"
FONT_NORMAL = ("Poppins", 14)
DEFAULT_BRAND = "-- Brand --"
DEFAULT_HP = "- HP -"
DEFAULT_SERIES = "-- Series --"
DEFAULT_MODEL = "-- Model --"


class RequestItems(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="WHITE")

        # Important variables
        self.date_entry = None
        self.delete_msgbox = None
        self.optionmenu_defaults = {
            "brand": DEFAULT_BRAND,
            "hp": DEFAULT_HP,
            "series": DEFAULT_SERIES,
            "models": DEFAULT_MODEL,
        }
        self.ac_specs = ACSpecs()

        # Main container for all pages
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.pack(fill="both", expand=True)

        # Store all pages here
        self.pages = {}

        # Create both pages once
        self.create_pages()

        # Show Categories page first
        self.show_page("categories")

    def create_pages(self):
        # --- CATEGORIES PAGE ---
        self.categories_page = ctk.CTkFrame(self.container, fg_color="#FFFFFF", corner_radius=15, width=900, height=480)
        self.pages["categories"] = self.categories_page
        self.setup_categories(self.categories_page)

        self.installation_page = ctk.CTkFrame(self.container, fg_color="white")
        self.pages["installation"] = self.installation_page
        self.setup_installation_items(self.installation_page)
        # self.after_idle(lambda: self.scroll_area._parent_canvas.yview_moveto(1))

        # Place both pages in the same location
        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_page(self, page_name):
        """Bring the requested page to the front instantly."""
        self.pages[page_name].lift()

    def create_entry(self, parent, width=200, height=30, **kwargs):
        return ctk.CTkEntry(
            parent, width=width, height=height, fg_color=COLOR_GRAY, font=("Poppins", 14), **kwargs
        )

    def create_category_btn(self, parent, text, text_color="black", font=("Poppins", 20), width=285, height=200, fg_color="#69E569", border_color=COLOR_GREEN, border_width=1, hover_color="#298753", **kwargs):
        return ctk.CTkButton(
            master=parent,
            text=text,
            text_color=text_color,
            font=font,
            width=width,
            height=height,
            fg_color=fg_color,
            border_color=border_color,
            border_width=border_width,
            hover_color=hover_color,
            corner_radius=10,
            **kwargs,
        )

    # ------------------- PAGE SETUPS ------------------- #
    def setup_categories(self, parent):
        parent.columnconfigure((0, 1), weight=1)
        parent.rowconfigure((0, 2), weight=1)

        ctk.CTkLabel(parent, text="What's today's activity?", font=("Poppins Bold", 20)).grid(row=0, column=0, columnspan=2, pady=(20, 0))

        install_btn = self.create_category_btn(
            parent,
            text="INSTALLATION",
            command=lambda: self.show_page("installation")
        )
        install_btn.grid(row=1, column=0, sticky="se", padx=(0, 35), pady=(0, 15))

        cleaning_btn = self.create_category_btn(
            parent,
            text="CLEANING",
        )
        cleaning_btn.grid(row=1, column=1, sticky="sw", padx=(35, 0), pady=(0, 15))

        repair_btn = self.create_category_btn(
            parent,
            text="REPAIR",
        )
        repair_btn.grid(row=2, column=0, sticky="ne", padx=(0, 35), pady=(15, 20))

        dismantle_btn = self.create_category_btn(
            parent,
            text="DISMANTLE",
        )
        dismantle_btn.grid(row=2, column=1, sticky="nw", padx=(35, 0), pady=(15, 20))

        for btn in [install_btn, cleaning_btn, repair_btn, dismantle_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.configure(fg_color="#298753", text_color="white", font=("Poppins", 20, "bold")))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(fg_color="#69E569", text_color="black", font=("Poppins", 20)))
        
    def setup_installation_items(self, parent):
        # --- Create a fixed top frame for the back button ---
        top_bar = ctk.CTkFrame(parent, fg_color="#D4F0D4", height=50, corner_radius=0)
        top_bar.pack(fill="x", side="top")

        self.back_btn_icon = ctk.CTkImage(light_image=Image.open(paths.ICON_BACK), size=(18, 18))
        btn = ctk.CTkButton(
            top_bar,
            text="",
            width=55,
            height=30,
            fg_color="transparent",
            bg_color="#D4F0D4",
            hover_color="#2CC985",
            image=self.back_btn_icon,
            command=self.confirm_back_to_menu
        )
        btn.pack(padx=25, pady=12, anchor="sw")

        # --- Create a scrollable content area ---
        self.scroll_area = ctk.CTkScrollableFrame(
            parent,
            fg_color="white",
            scrollbar_fg_color="white",
            scrollbar_button_color="#cccccc",
            scrollbar_button_hover_color="#aaaaaa"
        )
        self.scroll_area.pack(fill="both", expand=True)

        # Now place the rest of the content inside `scroll_area`
        self.mainframe = ctk.CTkFrame(self.scroll_area, fg_color="#ffffff", border_width=0, border_color=COLOR_GREEN)
        self.mainframe.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.mainframe.columnconfigure((0), weight=0)
        self.mainframe.rowconfigure((0, 1, 2, 3, 4), weight=0)

        ctk.CTkLabel(self.mainframe, text="INSTALLATION", font=("Roboto", 21, "bold"), corner_radius=30, fg_color="#2CC985", width=200, height=40).grid(
            row=0, column=0, padx=(35, 0), pady=(20, 0), sticky="nw"
        )

        # BASIC DETAILS FRAME
        ctk.CTkLabel(self.mainframe, text="Basic Details", font=("Roboto", 21, "bold")).grid(
            row=1, column=0, padx=65, pady=(30, 5), sticky="nw"
        )
        basic_details_frame = ctk.CTkFrame(self.mainframe, fg_color=FRAMES_FG_COLOR, border_width=0, border_color="gray", width=820, height=180)
        basic_details_frame.grid(row=2, column=0, sticky="nw", padx=(45, 0))
        basic_details_frame.pack_propagate(False)

        basic_details_inner_frame = ctk.CTkFrame(basic_details_frame, width=800, border_width=0, fg_color="transparent")
        basic_details_inner_frame.pack(fill="y", padx=(103, 0), pady=5, anchor="w")

        # DATE
        ctk.CTkLabel(basic_details_inner_frame, text="Date:", font=("Poppins", 16)).grid(row=0, column=0, padx=(1, 0), pady=(20, 0), sticky="e")
        self.date_entry = self.create_entry(basic_details_inner_frame)
        self.date_entry.grid(row=0, column=1, padx=(1, 0), pady=(20, 0), sticky="w")

        def get_current_date():
            today = datetime.today().strftime("%B %d, %Y")
            self.date_entry.delete(0, "end")
            self.date_entry.insert(0, today)
            self.get_date_btn.configure(state="disabled", fg_color=COLOR_GRAY)

        self.get_date_btn = ctk.CTkButton(
            basic_details_inner_frame, text="get date", font=("Poppins", 14),
            text_color="white", fg_color=COLOR_GREEN,
            hover_color=COLOR_GREEN_HOVER, width=80, command=get_current_date
        )
        self.get_date_btn.grid(row=0, column=2, pady=(20, 0), sticky="w")

        # TEAM MEMBERS
        ctk.CTkLabel(basic_details_inner_frame, text="Team:", font=("Poppins", 16)).grid(
            row=1, column=0, padx=(1, 0), pady=(10, 0), sticky="e"
        )
        team_mem_frames = ctk.CTkFrame(basic_details_inner_frame, fg_color="#e8e8e8", width=300, height=100)
        team_mem_frames.grid(row=1, column=1, pady=(10, 1), padx=1, columnspan=4, sticky="w")
        team_mem_frames.grid_propagate(False)

        checkbox_vars = {}
        columns_per_row = 2

        def show_selected():
            selected = [name for name, var in checkbox_vars.items() if var.get()]
            print("Selected:", selected)

        def toggle_all():
            state = switch.get() 
            for name, var in checkbox_vars.items():
                print(var)
                var.set(1) if state == "on" else var.set(0)

        for i, name in enumerate(field_employees):
            row = i // columns_per_row
            col = i % columns_per_row
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(team_mem_frames, text=name, variable=var, checkbox_width=20, checkbox_height=20, font=("Poppins", 14), hover=False)
            cb.grid(row=row, column=col, padx=(18, 0), pady=3, sticky="w")
            checkbox_vars[name] = var

        # select_all_var = ctk.BooleanVar()
        last_index = len(field_employees)
        row = last_index // columns_per_row
        col = last_index % columns_per_row

        self.switch_var = ctk.StringVar(value="off")
        switch = ctk.CTkSwitch(team_mem_frames, text="Whole Team", font=("Poppins", 14), command=toggle_all, variable=self.switch_var, onvalue="on", offvalue="off")
        switch.grid(row=row, column=col, columnspan=columns_per_row, padx=(18, 0), pady=3, sticky="w")


        # CUSTOMER DETAILS FRAME
        ctk.CTkLabel(self.mainframe, text="Customer Details", font=("Roboto", 21, "bold")).grid(
            row=3, column=0, padx=65, pady=(30, 5), sticky="nw"
        )
        customer_details_frame = ctk.CTkFrame(self.mainframe, fg_color=FRAMES_FG_COLOR, border_width=0, border_color="gray", width=820, height=170)
        customer_details_frame.grid(row=4, column=0, sticky="nw", padx=(45, 0))
        customer_details_frame.grid_propagate(False)

        # Customer Name
        ctk.CTkLabel(customer_details_frame, text="Customer Name:", font=("Poppins", 16)).grid(
            row=2, column=0, padx=(20, 0), pady=(20, 10), sticky="e"
        )
        self.customer_name = self.create_entry(customer_details_frame, width=300)
        self.customer_name.grid(row=2, column=1, padx=(10, 0), pady=(20, 10), sticky="w")

        # Customer Address
        ctk.CTkLabel(customer_details_frame, text="Address:", font=("Poppins", 16)).grid(
            row=3, column=0, padx=(20, 0), pady=(5, 10), sticky="e"
        )
        self.customer_address = self.create_entry(customer_details_frame, width=300)
        self.customer_address.grid(
            row=3, column=1, padx=(10, 30), pady=(5, 10), sticky="w", columnspan=2
        )

        # Customer Contact Number
        ctk.CTkLabel(customer_details_frame, text="Contact No:", font=("Poppins", 16)).grid(
            row=4, column=0, padx=(20, 0), pady=(5, 20), sticky="e"
        )
        self.customer_contact_number = self.create_entry(customer_details_frame, width=250)
        self.customer_contact_number.grid(
            row=4, column=1, padx=10, pady=(5, 20), sticky="w", columnspan=2
        )

        # AC DETAILS FRAME
        ctk.CTkLabel(self.mainframe, text="Aircon Details", font=("Roboto", 21, "bold")).grid(row=5, column=0, padx=65, pady=(30, 5), sticky="nw")

        ac_details_frame = ctk.CTkFrame(self.mainframe, fg_color=FRAMES_FG_COLOR, border_width=0, border_color="gray", width=820, height=350)
        ac_details_frame.grid(row=6, column=0, sticky="nw", padx=(45, 0))
        ac_details_frame.pack_propagate(False)

        ac_details_inner_frame = ctk.CTkFrame(ac_details_frame, width=800, border_width=0, fg_color="transparent")
        ac_details_inner_frame.pack(fill="y", padx=(103, 0), pady=5, anchor="w")

        def disable_series_and_brand_menu():
            self.ac_series.set(self.optionmenu_defaults["series"])
            self.ac_series.configure(values=[])
            self.ac_models.set(self.optionmenu_defaults["models"])
            self.ac_models.configure(values=[])

        def check_brand(value):
            """Enable entry only if 'Other' is selected, else reset and lock it."""
            if value == "Other":
                print("Other model")
                disable_series_and_brand_menu()
                self.other_brand_entry.configure(state="normal", border_color=COLOR_GREEN)
                self.other_brand_entry.focus()
            else:
                self.ac_series.configure(state="normal")
                self.chosen_series.set(self.optionmenu_defaults["series"])
                if value == "Midea":
                    self.ac_series.configure(values=self.ac_specs._midea_series)
                    self.ac_models.configure(values=self.ac_specs._midea_models[0]["Celest"])
                else:
                    self.ac_series.set(self.optionmenu_defaults["series"])
                    self.ac_series.configure(values=[])
                    self.ac_models.configure(values=[])

                # Clear and lock entry
                self.other_brand_entry.configure(state="normal", border_color="#979DA2")
                self.other_brand_entry.delete(0, "end")
                self.other_brand_entry.configure(state="readonly")
            
        def check_other_brand_for_series(event):
            value = self.other_brand_entry.get().strip()
            print("Clicked", value)
            if value == "Midea":
                self.ac_series.configure(values=self.ac_specs._midea_series)
                self.ac_models.configure(values=self.ac_specs._midea_models[0]["Celest"])
            else:
                self.ac_series.configure(values=[])
                self.ac_models.configure(values=[])

        def check_series(series):
            if series:
                self.ac_models.configure(state="normal")
                self.chosen_model.set(self.optionmenu_defaults["models"])
                self.ac_hp_menu.configure(state="normal")
                self.ac_hp_menu.set(self.optionmenu_defaults["hp"])

        def check_model_for_hp(model):
            brand = self.chosen_brand.get()
            series = self.chosen_series.get()
            _model = model
            hp = self.ac_specs._aircon_hp_list[brand][series][_model]
            self.chosen_hp.set(hp)

        def check_hp(hp):
            brand = self.chosen_brand.get()
            series = self.chosen_series.get()
            models = self.ac_specs._aircon_hp_list[brand][series]

            if hp == "more":
                self.other_hp_entry.configure(state="normal", border_color=COLOR_GREEN)
                self.other_hp_entry.focus()
                self.ac_models.set(self.optionmenu_defaults["models"])
            else:
                for k, v in models.items():
                    if hp == str(v):
                        self.ac_models.set(k)

                # Clear and lock entry
                self.other_hp_entry.configure(state="normal", border_color="#979DA2")
                self.other_hp_entry.delete(0, "end")
                self.other_hp_entry.configure(state="readonly")

        # AC BRAND
        ctk.CTkLabel(ac_details_inner_frame, text="Brand:", font=("Poppins", 16)).grid(row=0, column=0, padx=(1, 0), pady=(20, 10), sticky="w")
        self.chosen_brand = ctk.StringVar(value=self.optionmenu_defaults["brand"])
        self.ac_brand_menu = ctk.CTkOptionMenu(
            master=ac_details_inner_frame,
            values=aircon_brands,
            height=33,
            width=200,
            font=FONT_NORMAL,
            text_color="black",
            button_color=COLOR_GREEN,
            button_hover_color=COLOR_GREEN_HOVER,
            fg_color=COLOR_GRAY,
            dropdown_fg_color=COLOR_GRAY,
            dropdown_text_color="black",
            dropdown_font=FONT_NORMAL,
            dropdown_hover_color="#2CC985",
            command=check_brand,
            anchor="center",
            variable=self.chosen_brand
        )
        self.ac_brand_menu.grid(row=0, column=1, padx=(1, 0), pady=(20, 10), sticky="w")

        self.other_brand_entry = self.create_entry(ac_details_inner_frame, width=200, state="readonly")
        self.other_brand_entry.grid(row=0, column=2, padx=(1, 0), pady=(20, 10), sticky="w", columnspan=2)
        self.other_brand_entry.bind("<KeyRelease>", lambda e: check_other_brand_for_series(e))

        # AC SERIES
        ctk.CTkLabel(ac_details_inner_frame, text="Series:", font=("Poppins", 16)).grid(
            row=1, column=0, padx=(1, 0), pady=10, sticky="w"
        )
        self.chosen_series = ctk.StringVar(value="")
        self.ac_series = ctk.CTkOptionMenu(
            ac_details_inner_frame,
            values=[],
            height=33,
            width=200,
            font=FONT_NORMAL,
            text_color="black",
            button_color=COLOR_GREEN,
            button_hover_color=COLOR_GREEN_HOVER,
            fg_color=COLOR_GRAY,
            dropdown_fg_color=COLOR_GRAY,
            dropdown_text_color="black",
            dropdown_font=FONT_NORMAL,
            dropdown_hover_color="#2CC985",
            anchor="center",
            variable=self.chosen_series,
            command=check_series,
            state="disabled",
        )
        self.ac_series.grid(row=1, column=1, padx=(1, 0), pady=10, sticky="w")

        # AC MODEL
        ctk.CTkLabel(ac_details_inner_frame, text="Model:", font=("Poppins", 16)).grid(
            row=2, column=0, padx=(1, 0), pady=10, sticky="w"
        )
        self.chosen_model = ctk.StringVar(value="")
        self.ac_models = ctk.CTkOptionMenu(
            master=ac_details_inner_frame,
            values=[],
            height=33,
            width=200,
            font=FONT_NORMAL,
            text_color="black",
            button_color=COLOR_GREEN,
            button_hover_color=COLOR_GREEN_HOVER,
            fg_color=COLOR_GRAY,
            dropdown_fg_color=COLOR_GRAY,
            dropdown_text_color="black",
            dropdown_font=FONT_NORMAL,
            dropdown_hover_color="#2CC985",
            anchor="center",
            command=check_model_for_hp,
            variable=self.chosen_model,
            state="disabled",
        )
        self.ac_models.grid(row=2, column=1, padx=(1, 0), pady=10, sticky="w")

        ac_stat_frame = ctk.CTkFrame(ac_details_inner_frame, fg_color="transparent", width=320, height=100, border_width=0)
        ac_stat_frame.grid(row=3, column=0, padx=(1, 0), pady=10, sticky="w", columnspan=3)
        ac_stat_frame.grid_propagate(False)

        ctk.CTkLabel(ac_stat_frame, text="Horse Power:", font=("Poppins", 16)).grid(row=0, column=0, padx=(1, 0), pady=10, sticky="w", columnspan=2)

        self.chosen_hp = ctk.StringVar(value="")
        self.ac_hp_menu = ctk.CTkOptionMenu(
            ac_stat_frame, 
            values=aircon_hps, 
            height=33, 
            width=92, 
            font=FONT_NORMAL,
            text_color="black",
            button_color=COLOR_GREEN,
            button_hover_color=COLOR_GREEN_HOVER,
            fg_color=COLOR_GRAY,
            dropdown_fg_color=COLOR_GRAY,
            dropdown_text_color="black",
            dropdown_font=FONT_NORMAL,
            dropdown_hover_color="#2CC985", 
            anchor="center", 
            command=check_hp,
            state="disabled",
            variable=self.chosen_hp,
        )
        self.ac_hp_menu.grid(row=0, column=1, padx=(75, 0), pady=10, sticky="w")

        self.other_hp_entry = self.create_entry(ac_stat_frame, width=60, state="readonly")
        self.other_hp_entry.grid(row=0, column=2, pady=10, sticky="w")

        ctk.CTkLabel(ac_stat_frame, text="QTY:", font=("Poppins", 16)).grid(row=1, column=0, padx=(1, 0), pady=10, sticky="w")
        self.qty_entry = CTkSpinbox(ac_stat_frame, min_val=0, max_val=15, step=1, fg_color="#D4F0D4")
        self.qty_entry.grid(row=1, column=1, padx=(10, 45), pady=10, sticky="w")

        ctk.CTkButton(ac_details_inner_frame, text="Reset", text_color="white", font=("Poppins", 15), fg_color="#E63946", hover_color="#C92A3F", width=60).grid(row=4, column=0, padx=(1, 0), pady=(5, 10), sticky="w")

        # Request Form
        ctk.CTkLabel(self.mainframe, text="Request Items", font=("Roboto", 21, "bold")).grid(row=7, column=0, padx=65, pady=(30, 5), sticky="nw")

        request_frame = ctk.CTkFrame(self.mainframe, fg_color=FRAMES_FG_COLOR, border_width=0, border_color="gray", width=820, height=70)
        request_frame.grid(row=8, column=0, sticky="nw", padx=(45, 0), pady=(0, 20))
        request_frame.grid_propagate(False)

        self.request_btn = ctk.CTkButton(request_frame, text="Open Request Form", font=("Poppins", 15), text_color="white", height=30, width=250, fg_color=COLOR_GREEN_HOVER, hover_color=COLOR_GREEN, command=self.open_request_form)
        self.request_btn.grid(row=0, column=0, padx=(285, 0), pady=20, sticky="w")

        # ENTRY & FRAME BINDINGS
        entry_fields = [self.date_entry, self.customer_name, self.customer_address, self.customer_contact_number, self.other_brand_entry, self.ac_series]
        for field in entry_fields:
            field.bind("<FocusIn>", lambda e, w=field: w.configure(border_color='#298753'))
            field.bind("<FocusOut>", lambda e, w=field: w.configure(border_color='#979da2'))

        parent_frames = [self.installation_page, self.mainframe, basic_details_frame, customer_details_frame, ac_details_frame]
        for frame in parent_frames:
            frame.bind("<Button-1>", self.clear_focus)

    def clear_focus(self, event):
        self.focus()

    def open_request_form(self):
        MaterialReqForm(self, fg_color="#F0F0F0")
    
    def clear_installation_form(self):
        """Reset all inputs on the installation page to default."""
        # Clear entries
        for widget in self.pages["installation"].winfo_children():
            self.clear_widget_inputs(widget)

    def clear_widget_inputs(self, widget):
        """Recursively clear entries, option menus, and checkboxes."""
        for child in widget.winfo_children():

            if child == self.qty_entry:
                self.qty_entry.value.set(0)
                continue

            if isinstance(child, ctk.CTkEntry):
                if child.cget("state") != "normal":
                    child.configure(state="normal")
                child.delete(0, "end")

            elif isinstance(child, ctk.CTkOptionMenu):
                if child == self.ac_brand_menu:
                    child.set(self.optionmenu_defaults["brand"])
                elif child == self.ac_series:
                    child.configure(state="disabled")
                    child.set("")
                elif child == self.ac_models:
                    child.configure(state="disabled")
                    child.set("")
                elif child == self.ac_hp_menu:
                    child.configure(state="disabled")
                    child.set("")

            elif isinstance(child, ctk.CTkCheckBox):
                child.deselect()

            elif isinstance(child, ctk.CTkSwitch):
                self.switch_var.set("off")

            # Recursively clear inside nested frames
            self.clear_widget_inputs(child)
            
    def back_to_menu(self):
        if self.delete_msgbox and self.delete_msgbox.winfo_exists():
            self.delete_msgbox.destroy()
        self.clear_installation_form()
        self.show_page("categories")
        self.get_date_btn.configure(state="normal", fg_color=COLOR_GREEN)
        self.other_brand_entry.configure(state="normal", border_color="#979DA2")
        self.other_brand_entry.delete(0, "end")
        self.other_brand_entry.configure(state="readonly")
        self.focus()

    def has_changes(self):
        """Return True if any input differs from defaults."""
        # Check entries
        if self.date_entry.get().strip():
            return True
        if self.customer_name.get().strip():
            return True
        if self.customer_address.get().strip():
            return True
        if self.other_brand_entry.get().strip():
            return True

        # Check dropdowns
        if self.chosen_brand.get() != self.optionmenu_defaults["brand"]:
            return True
        if self.chosen_series.get() != self.optionmenu_defaults["series"]:
            return True
        if self.ac_hp_menu.get() != self.optionmenu_defaults["hp"]:
            return True

        # Check spinbox
        if self.qty_entry.value.get() != 0:
            return True

        # Check checkboxes
        for child in self.pages["installation"].winfo_children():
            if self.check_any_checkbox(child):
                return True

        return False


    def check_any_checkbox(self, widget):
        """Recursively check if any checkbox is ticked."""
        for child in widget.winfo_children():
            if isinstance(child, ctk.CTkCheckBox) and child.get() == 1:
                return True
            if self.check_any_checkbox(child):
                return True
        return False
    
    # Otherwise show confirmation
    def confirm_back_to_menu(self):
        if not self.has_changes():
            # No changes → just go back 
            self.back_to_menu()
            return

        # If there's already a msgbox open, focus it
        if self.delete_msgbox and self.delete_msgbox.winfo_exists():
            self.delete_msgbox.focus_force()
            return


        self.delete_msgbox = CustomMessageBox(
            self,
            title="Confirm",
            message="All changes will be discarded. Do you want to go back?",
            on_confirm=self.back_to_menu,
            msg1="No",
            msg2="Yes, Discard",
            # title_fg="#209F3C",
            title_fg="#0C955A",
            msg2_fgcolor="#E63946",
            msg2_hovercolor="#C92A3F",
            message_pady=(20, 22),
            btn_pady=(0, 15),
            toplvl_height=190,
            toplvl_posx=510,
            toplvl_posy=300,
            msg_font=("Poppins", 15),
        )




class CTkSpinbox(ctk.CTkFrame):
    def __init__(self, master=None, min_val=0, max_val=100, step=1, **kwargs):
        super().__init__(master, **kwargs)
        
        self.value = ctk.IntVar(value=min_val)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step

        # Decrease button
        self.decrease_btn = ctk.CTkButton(self, text="-", height=30, width=30, command=self.decrease, fg_color=COLOR_GREEN_HOVER, hover_color=COLOR_GREEN)
        self.decrease_btn.grid(row=0, column=0, padx=(0, 5))

        # Entry
        self.entry = ctk.CTkEntry(self, textvariable=self.value, height=30, width=60, justify="center", font=("Poppins", 14))
        self.entry.grid(row=0, column=1)

        # Increase button
        self.increase_btn = ctk.CTkButton(self, text="+", height=30, width=30, command=self.increase, fg_color=COLOR_GREEN_HOVER, hover_color=COLOR_GREEN)
        self.increase_btn.grid(row=0, column=2, padx=(5, 0))

    def increase(self):
        if self.value.get() + self.step <= self.max_val:
            self.value.set(self.value.get() + self.step)

    def decrease(self):
        if self.value.get() - self.step >= self.min_val:
            self.value.set(self.value.get() - self.step)
