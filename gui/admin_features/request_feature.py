import customtkinter as ctk
from datetime import datetime
from PIL import Image

from ui.notifs import CustomMessageBox
from .material_request_form import MaterialReqForm
from .new_ac_details import ACManagerApp

from core import paths
from core.ims_data import ACSpecs, field_employees, aircon_hps
from core.aircon_backend import get_technologies, get_brands, get_ac_types, get_series, get_models, get_hp

from gui.admin_features.new_ac_details import DatabaseManagerWindow

# Constants
INFO_FRAMES_COLOR = "#38B06E"
ENTRY_FOCUS_COLOR = "#007334"
BUTTON_FG_COLOR = "#FFFFFF"
BUTTON_BORDER_COLOR = "gray"
COLOR_GRAY = "#e8e8e8"
COLOR_GREEN = "#298753"
COLOR_GREEN_HOVER = "#207347"
COLOR_RED = "#E63946"
COLOR_RED_HOVER = "#D72533"
FRAMES_FG_COLOR = "#C0F0C0"
FONT_NORMAL = ("Poppins", 15)

DEFAULT_TYPE = "-- AC Type --"
DEFAULT_COMPRESSOR = "-- Type --"
DEFAULT_BRAND = "-- Brand --"
DEFAULT_HP = "- HP -"
DEFAULT_SERIES = "-- Series --"
DEFAULT_MODEL = "-- Model --"

DEFAULT_COMPRESSORS = ["INVERTER", "NON_INVERTER"]
DEFAULT_HP_VALUES = ["0.5", "1.0", "1.5", "2.0", "2.5", "3.0", "MORE"]


class RequestItems(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="WHITE")

        # Important variables
        self.date_entry = None
        self.delete_msgbox = None
        self.ac_specs = ACSpecs()
        self.ac_hp_list = aircon_hps

        # Main container for all pages
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.pack(fill="both", expand=True)

        # Store all pages here
        self.pages = {}

        # Create both pages once
        self.create_pages()

        # Show Categories page first
        self.show_page("categories")

    def create_collapsible_section(self, parent, row, title, frame_height=150):
        """Creates a header + collapsible frame container."""
        container = {}

        # Start collapsed
        container["is_expanded"] = False
        container["title"] = title

        # Header Button
        container["button"] = ctk.CTkButton(
            parent,
            text=f" {title} ▼",  # ▼ means collapsed initially
            font=("Poppins", 18),
            fg_color="#EAEAEA",
            text_color="black",
            hover_color="#C7C7C7",
            corner_radius=8,
            anchor="w",
            command=lambda: self.toggle_section(container)
        )
        container["button"].grid(row=row, column=0, pady=(20, 5), sticky="ew")

        # Content Frame (but not gridded yet)
        container["frame"] = ctk.CTkFrame(parent, fg_color=INFO_FRAMES_COLOR, height=frame_height)
        container["frame"].pack_propagate(False)

        return container
    
    def center_on_widget(self, widget):
        """Scroll the scroll_area so the widget is vertically centered."""
        try:
            canvas = self.scroll_area._parent_canvas
            widget.update_idletasks()

            # Get widget position relative to canvas
            widget_y = widget.winfo_rooty() - canvas.winfo_rooty()
            widget_height = widget.winfo_height()

            # Get visible region
            visible_height = canvas.winfo_height()

            # Target scroll so widget center is in middle
            target_y = widget_y + widget_height / 2 - visible_height / 2

            # Normalize (0.0–1.0 range for yview_moveto)
            scroll_fraction = target_y / (canvas.winfo_height())
            scroll_fraction = max(0, min(1, scroll_fraction))

            canvas.yview_moveto(scroll_fraction)
        except Exception as e:
            print("center_on_widget error:", e)

    def toggle_section(self, container):
        """Expand/Collapse a section and center it in the scroll area."""
        if container["is_expanded"]:
            # Collapse
            container["frame"].grid_forget()
            container["button"].configure(text=f"{container['title']} ▼")
            container["is_expanded"] = False
        else:
            # Expand
            container["frame"].grid(
                row=container["button"].grid_info()["row"] + 1,
                column=0,
                sticky="ew",
                padx=45,
                pady=(0, 10)
            )
            container["button"].configure(text=f"{container['title']} ▲")
            container["is_expanded"] = True

            # After expansion, center it in scroll
            self.after(100, lambda: self.center_on_widget(container["frame"]))

    def create_pages(self):
        # --- CATEGORIES PAGE ---
        self.categories_page = ctk.CTkFrame(self.container, fg_color="#FFFFFF", corner_radius=15, width=900, height=480)
        self.pages["categories"] = self.categories_page
        self.setup_categories(self.categories_page)

        self.installation_page = ctk.CTkFrame(self.container, fg_color="white")
        self.pages["installation"] = self.installation_page
        self.setup_installation_items(self.installation_page)
        self.after_idle(lambda: self.scroll_area._parent_canvas.yview_moveto(.2))

        # Place both pages in the same location
        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_page(self, page_name):
        """Bring the requested page to the front instantly."""
        self.pages[page_name].lift()

    def create_entry(self, parent, width=200, height=30, text_font=("Poppins", 14), **kwargs):
        return ctk.CTkEntry(parent, width=width, height=height, fg_color=COLOR_GRAY, font=text_font, border_color=INFO_FRAMES_COLOR, **kwargs)

    def create_category_btn(self, parent, text, text_color="black", font=("Poppins", 20), width=305, height=220, fg_color="#69E569", border_color=COLOR_GREEN, border_width=1, hover_color="#298753", **kwargs):
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

        ctk.CTkLabel(parent, text="What's today's activity?", font=("Poppins Bold", 23)).grid(row=0, column=0, columnspan=2, pady=(50, 15))

        install_btn = self.create_category_btn(
            parent,
            text="INSTALLATION",
            command=lambda: self.show_page("installation")
        )
        install_btn.grid(row=1, column=0, sticky="se", padx=(0, 35), pady=(0, 20))

        cleaning_btn = self.create_category_btn(
            parent,
            text="CLEANING",
        )
        cleaning_btn.grid(row=1, column=1, sticky="sw", padx=(35, 0), pady=(0, 20))

        repair_btn = self.create_category_btn(
            parent,
            text="REPAIR",
        )
        repair_btn.grid(row=2, column=0, sticky="ne", padx=(0, 35), pady=(20, 20))

        dismantle_btn = self.create_category_btn(
            parent,
            text="DISMANTLE",
        )
        dismantle_btn.grid(row=2, column=1, sticky="nw", padx=(35, 0), pady=(20, 20))

        for btn in [install_btn, cleaning_btn, repair_btn, dismantle_btn]:
            btn.bind("<Enter>", lambda e, b=btn: b.configure(fg_color="#298753", text_color="white", font=("Poppins", 20, "bold")))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(fg_color="#69E569", text_color="black", font=("Poppins", 20)))

    def build_basic_info(self, parent):
        # Move all your Basic Info widgets here (date, team, etc.)
        # Example:
        self.basic_details_inner_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.basic_details_inner_frame.pack(fill="y", padx=(103, 0), pady=5, anchor="w")
        
        # DATE
        def get_current_date():
            today = datetime.today().strftime("%B %d, %Y")
            self.date_entry.delete(0, "end")
            self.date_entry.insert(0, today)
            self.get_date_btn.configure(state="disabled", fg_color=COLOR_GRAY)
            
        ctk.CTkLabel(self.basic_details_inner_frame, text="Date:", text_color="white", font=("Poppins", 16, "bold")).grid(row=0, column=0, padx=(1, 0), pady=(20, 0), sticky="w")
        self.date_entry = self.create_entry(self.basic_details_inner_frame)
        self.date_entry.grid(row=0, column=1, padx=(4, 0), pady=(20, 0), sticky="w")

        self.get_date_btn = ctk.CTkButton(
            self.basic_details_inner_frame, text="get date", font=("Poppins", 14),
            text_color="white", fg_color=COLOR_GREEN_HOVER,
            hover_color=COLOR_GREEN, width=80, command=get_current_date
        )
        self.get_date_btn.grid(row=0, column=2, padx=(10, 0), pady=(21, 0), sticky="w")

        # TEAM MEMBERS
        ctk.CTkLabel(self.basic_details_inner_frame, text="Team:", text_color="white", font=("Poppins", 16, "bold")).grid(
            row=1, column=0, padx=(1, 0), pady=(10, 0), sticky="e"
        )
        team_mem_frames = ctk.CTkFrame(self.basic_details_inner_frame, fg_color="#e8e8e8", width=300, height=100)
        team_mem_frames.grid(row=1, column=1, pady=(10, 1), padx=(15, 0), columnspan=4, sticky="w")
        team_mem_frames.grid_propagate(False)

        checkbox_vars = {}
        columns_per_row = 2

        def show_selected():
            selected = [name for name, var in checkbox_vars.items() if var.get()]
            print("Selected:", selected)

        def toggle_all():
            state = switch.get() 
            for name, var in checkbox_vars.items():
                var.set(1) if state == "on" else var.set(0)

        for i, name in enumerate(field_employees):
            row = i // columns_per_row
            col = i % columns_per_row
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(team_mem_frames, text=name, variable=var, checkbox_width=20, checkbox_height=20, font=("Poppins", 15), hover=False)
            cb.grid(row=row, column=col, padx=(18, 0), pady=3, sticky="w")
            checkbox_vars[name] = var

        # select_all_var = ctk.BooleanVar()
        last_index = len(field_employees)
        row = last_index // columns_per_row
        col = last_index % columns_per_row

        self.switch_var = ctk.StringVar(value="off")
        switch = ctk.CTkSwitch(team_mem_frames, text="Whole Team", font=("Poppins", 15), command=toggle_all, variable=self.switch_var, onvalue="on", offvalue="off")
        switch.grid(row=row, column=col, columnspan=columns_per_row, padx=(18, 0), pady=3, sticky="w")

    def build_customer_info(self, parent):
        self.customer_details_inner_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.customer_details_inner_frame.pack(fill="x", padx=(100, 5), pady=5)
        
        # Customer Name
        ctk.CTkLabel(self.customer_details_inner_frame, text="Customer Name:", text_color="white", font=("Poppins", 16, "bold")).grid(row=2, column=0, padx=(4, 0), pady=(15, 10), sticky="w")

        self.customer_name = self.create_entry(self.customer_details_inner_frame, width=300)
        self.customer_name.grid(row=2, column=1, padx=(15, 0), pady=(15, 10), sticky="w")

        # Customer Address
        ctk.CTkLabel(self.customer_details_inner_frame, text="Address:", text_color="white", font=("Poppins", 16, "bold")).grid(
            row=3, column=0, padx=(4, 0), pady=(5, 10), sticky="w"
        )
        self.customer_address = self.create_entry(self.customer_details_inner_frame, width=300)
        self.customer_address.grid(
            row=3, column=1, padx=(15, 0), pady=(5, 10), sticky="w", columnspan=2
        )

        # Customer Contact Number
        ctk.CTkLabel(self.customer_details_inner_frame, text="Contact No:", text_color="white", font=("Poppins", 16, "bold")).grid(
            row=4, column=0, padx=(4, 0), pady=(5, 20), sticky="w"
        )
        self.customer_contact_number = self.create_entry(self.customer_details_inner_frame, width=250)
        self.customer_contact_number.grid(
            row=4, column=1, padx=(15, 0), pady=(5, 20), sticky="w", columnspan=2
        )

    def build_aircon_details(self, parent):
        ac_details_inner_frame = ctk.CTkFrame(parent, fg_color="transparent", border_width=0)
        ac_details_inner_frame.pack(fill="y", padx=(103, 0), pady=5, anchor="w")

        def force_uppercase(*args):
            current = self.other_brand_var.get()
            self.other_brand_var.set(current.upper())

        def hide_entry(entry_widget, border_color=INFO_FRAMES_COLOR):
            """ Clear and hide entry """
            entry_widget.delete(0, "end")
            entry_widget.grid_forget()

        def disable_optionmenu(opt_menu):
            """ Clear and lock option menu """
            opt_menu.configure(state="disabled")
            opt_menu.set("")

        def disable_input_widgets(brand="", series="", model="", hp="", other_brand="", other_hp=""):
            if other_brand:
                self.other_brand_entry.delete(0, "end")
            if other_hp:
                self.other_hp_entry.delete(0, "end")

            if brand and series and model and hp:
                self.ac_brand_menu.configure(state="disabled")
                self.ac_series.configure(state="disabled")
                self.ac_models.configure(state="disabled")
                self.ac_hps.configure(state="disabled")
                self.chosen_brand.set(value="")
                self.chosen_series.set(value="")
                self.chosen_model.set(value="")
                self.chosen_hp.set(value="")
            elif series and not model and not hp:
                self.ac_series.configure(state="disabled") 
                self.chosen_series.set(value="")
            elif not series and model and not hp:
                self.ac_models.configure(state="disabled")
                self.chosen_model.set(value="")
            elif not series and not model and hp:
                self.ac_hps.configure(state="disabled")
                self.chosen_hp.set(value="")
            elif series and model and not hp:
                self.ac_series.configure(state="disabled")
                self.ac_models.configure(state="disabled")
                self.chosen_series.set(value="")
                self.chosen_model.set(value="")
            elif not series and model and hp:
                self.ac_models.configure(state="disabled")
                self.ac_hps.configure(state="disabled")
                self.chosen_model.set(value="")
                self.chosen_hp.set(value="")
            elif series and model and hp:
                self.ac_series.configure(state="disabled")
                self.ac_models.configure(state="disabled")
                self.ac_hps.configure(state="disabled")
                self.chosen_series.set(value="")
                self.chosen_model.set(value="")
                self.chosen_hp.set(value="")

            hide_entry(self.other_brand_entry)

        def check_ac_type(value):
            techs = get_technologies(value)
            print(f"compressors: {techs}")
            self.ac_comps.configure(state="normal", values=techs)
            # self.chosen_compressor.set(techs[0] if techs else "")
            self.chosen_compressor.set(DEFAULT_COMPRESSOR)

            disable_input_widgets(brand="-", series="-", model="-", hp="-")

        def check_compressor(value):
            if value:
                brands = get_brands(self.chosen_ac_type.get(), value)
                print(f"brands: {brands}")
                self.ac_brand_menu.configure(state="normal", values=brands)
                # self.chosen_brand.set(brands[0] if brands else "")
                self.chosen_brand.set(DEFAULT_BRAND)

            disable_input_widgets(series="-", model="-", hp="-")

        def check_brand(value):
            if value == "OTHER":
                self.other_brand_entry.grid(row=3, column=1, padx=(230, 0), pady=(30, 10), sticky="w")
                self.other_brand_entry.configure(state="normal", border_color=ENTRY_FOCUS_COLOR)
                self.other_brand_entry.focus()

                self.ac_series.configure(state="disabled")
                self.ac_models.configure(state="disabled")
                self.ac_hps.configure(state="disabled")
                self.chosen_series.set(value="")
                self.chosen_model.set(value="")
                self.chosen_hp.set(value="")
                return

            series = get_series(value, self.chosen_compressor.get(), self.chosen_ac_type.get())
            print(f"series: {series}")

            if series:
                self.ac_series.configure(state="normal", values=series)
                # self.chosen_series.set(series[0])
                self.chosen_series.set(DEFAULT_SERIES)

                disable_input_widgets(model="-", hp="-")
            else:
                # No series → go directly to HP (for window / floor types)
                self.ac_series.configure(state="disabled", values=[])
                self.ac_models.configure(state="disabled", values=[])

        def check_other_brand_for_series(event):
            val = self.other_brand_entry.get().strip().upper()
            tech = self.chosen_compressor.get()
            brands = get_brands(self.chosen_ac_type.get(), tech)
            print("check other brand tech:", tech)
            print("check other brand brands:", brands[:-1])

            # Case 1: Entry is empty → keep HP disabled
            if val == "":
                self.ac_hps.configure(state="disabled")
                self.chosen_hp.set(value="")
                hide_entry(self.other_hp_entry)
                return   # stop further checks
            
            # Case 2: Brand already exists in predefined brands
            if val in brands:
                self.other_brand_entry.configure(border_color=COLOR_RED)
                self.ac_hps.configure(state="disabled")
                self.chosen_hp.set(value="")

                Toast(self.ac_frame_container["frame"], f"⚠ {val} already exists in menu.", x=865, y=325, duration=2300, bg_color=COLOR_RED, font=("Poppins", 16, "bold"), wrap=400)

            else:
                # Case 3: Custom brand → allow HP selection
                self.other_brand_entry.configure(border_color=ENTRY_FOCUS_COLOR)
                self.ac_series.configure(state="disabled", values=[])
                self.ac_models.configure(state="disabled", values=[])
                self.ac_hps.configure(state="normal", values=["0.5", "1.0", "1.5", "2.0", "2.5", "3.0", "more"])
                self.chosen_hp.set(DEFAULT_HP)

        def check_series(series):
            models = get_models(series, self.chosen_brand.get())
            if models:
                self.ac_models.configure(state="normal", values=models)
                # self.chosen_model.set(models[0])
                self.chosen_model.set(DEFAULT_MODEL)
            else:
                self.ac_models.configure(state="disabled", values=[])

        def check_model_for_hp(model):
            hp = get_hp(model)
            if hp:
                self.ac_hps.configure(state="normal", values=[str(hp)])
                self.chosen_hp.set(str(hp))
            else:
                self.ac_hps.configure(state="disabled", values=[])

        def check_hp(hp):
            brand = self.chosen_brand.get().upper()
            series = self.chosen_series.get().upper()

            if brand == "OTHER":
                if hp == "more":
                    self.other_hp_entry.grid(row=0, column=2, padx=(15, 0), pady=10, sticky="w")
                    self.other_hp_entry.configure(state="normal", border_color=ENTRY_FOCUS_COLOR)
                    self.other_hp_entry.focus()
                else:
                    models = self.ac_specs._aircon_hp_list["NONE"]["_NONE"]

                    for k, v in models.items():
                        if hp == str(v):
                            self.ac_models.set(k)
                    hide_entry(self.other_hp_entry)

            else:
                series = self.chosen_series.get().upper()
                models = self.ac_specs._aircon_hp_list[brand][series]

                if hp == "more":
                    # print(True)
                    # if brand != "MIDEA":
                    #     self.other_hp_entry.configure(state="normal", border_color=COLOR_GREEN)
                    #     self.other_hp_entry.focus()
                    # else:
                    self.other_hp_entry.grid(row=0, column=2, padx=(15, 0), pady=10, sticky="w")
                    self.other_hp_entry.configure(state="normal", border_color=ENTRY_FOCUS_COLOR)
                    self.other_hp_entry.focus()
                    disable_optionmenu(self.ac_models)

                else:
                    print("hp: {}".format(hp))
                    self.ac_models.configure(state="normal")
                    for k, v in models.items():
                        if hp == str(v):
                            self.ac_models.set(k)
                    hide_entry(self.other_hp_entry)

        # NEW AIRCON DETAILS
        ctk.CTkButton(
            ac_details_inner_frame, 
            text="New Aircon Details", 
            text_color="white", 
            font=("Poppins", 15), 
            fg_color="#457B9D", 
            hover_color="#1D3557", 
            width=150, 
            image=ctk.CTkImage(light_image=Image.open(paths.ICON_ADD_PLUS)),
            command=self.open_new_aircon_window
        ).grid(row=0, column=0, padx=(1, 0), pady=(20, 10), sticky="w")

        ctk.CTkButton(
            ac_details_inner_frame,
            text="🛠 Manage Database",
            fg_color="#298753",
            hover_color="#207347",
            text_color="white",
            font=FONT_NORMAL,
            command=self.open_database_manager
        ).grid(row=0, column=1, padx=(10, 0), pady=(20, 10), sticky="w")

        # AC TYPE (INSTALLATION FORM)
        ctk.CTkLabel(ac_details_inner_frame, text="Type:", font=("Poppins", 16, "bold"), text_color="white").grid(row=1, column=0, padx=(1, 0), pady=10, sticky="w")
        self.chosen_ac_type = ctk.StringVar(value=DEFAULT_TYPE)
        self.ac_types = ctk.CTkOptionMenu(
            master=ac_details_inner_frame,
            values=get_ac_types(),
            height=33,
            width=250,
            font=FONT_NORMAL,
            text_color="black",
            button_color=COLOR_GREEN,
            button_hover_color=COLOR_GREEN_HOVER,
            fg_color=COLOR_GRAY,
            dropdown_fg_color=COLOR_GRAY,
            dropdown_text_color="black",
            dropdown_font=FONT_NORMAL,
            dropdown_hover_color="#2CC985",
            command=check_ac_type,
            anchor="center",
            variable=self.chosen_ac_type,
        )
        self.ac_types.grid(row=1, column=1, padx=(10, 0), pady=(20, 10), sticky="w")
            
        # AC COMPRESSOR TECHNOLOGY
        ctk.CTkLabel(ac_details_inner_frame, text="Compressor:", font=("Poppins", 16, "bold"), text_color="white").grid(row=2, column=0, padx=(1, 0), pady=10, sticky="w")
        self.chosen_compressor = ctk.StringVar()
        self.ac_comps = ctk.CTkOptionMenu(
            master=ac_details_inner_frame,
            values=get_technologies(),
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
            command=check_compressor,
            anchor="center",
            variable=self.chosen_compressor,
            state="disabled"
        )
        self.ac_comps.grid(row=2, column=1, padx=(10, 0), pady=10, sticky="w")

        # AC BRAND
        ctk.CTkLabel(ac_details_inner_frame, text="Brand:", font=("Poppins", 16, "bold"), text_color="white").grid(row=3, column=0, padx=(1, 0), pady=(30, 10), sticky="w")
        self.chosen_brand = ctk.StringVar()
        self.ac_brand_menu = ctk.CTkOptionMenu(
            master=ac_details_inner_frame,
            values=get_brands(),
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
            variable=self.chosen_brand,
            state="disabled"
        )
        self.ac_brand_menu.grid(row=3, column=1, padx=(10, 0), pady=(30, 10), sticky="w")

        self.other_brand_var = ctk.StringVar()
        self.other_brand_var.trace_add("write", force_uppercase)

        self.other_brand_entry = self.create_entry(ac_details_inner_frame, width=140, textvariable=self.other_brand_var)
        self.other_brand_entry.bind("<KeyRelease>", lambda e: check_other_brand_for_series(e))

        # AC SERIES
        ctk.CTkLabel(ac_details_inner_frame, text="Series:", font=("Poppins", 16, "bold"), text_color="white").grid(row=4, column=0, padx=(1, 0), pady=10, sticky="w")
        self.chosen_series = ctk.StringVar()
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
        self.ac_series.grid(row=4, column=1, padx=(10, 0), pady=10, sticky="w")

        # AC MODEL
        ctk.CTkLabel(ac_details_inner_frame, text="Model:", font=("Poppins", 16, "bold"), text_color="white").grid(row=5, column=0, padx=(1, 0), pady=10, sticky="w")

        self.chosen_model = ctk.StringVar()
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
        self.ac_models.grid(row=5, column=1, padx=(10, 0), pady=10, sticky="w")

        self.ac_stat_frame = ctk.CTkFrame(ac_details_inner_frame, fg_color="transparent", width=320, height=100, border_width=0)
        self.ac_stat_frame.grid(row=6, column=0, padx=(1, 0), pady=10, sticky="w", columnspan=3)
        self.ac_stat_frame.grid_propagate(False)

        # AC HORSE POWER
        ctk.CTkLabel(self.ac_stat_frame, text="Horse Power:", font=("Poppins", 16, "bold"), text_color="white").grid(row=0, column=0, padx=(1, 0), pady=10, sticky="w", columnspan=2)

        self.chosen_hp = ctk.StringVar()
        self.ac_hps = ctk.CTkOptionMenu(
            self.ac_stat_frame, 
            values=self.ac_hp_list, 
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
        self.ac_hps.grid(row=0, column=1, padx=(85, 0), pady=10, sticky="w")

        self.other_hp_entry = self.create_entry(self.ac_stat_frame, width=60, state="disabled")

        ctk.CTkLabel(self.ac_stat_frame, text="QTY:", font=("Poppins", 16, "bold"), text_color="white").grid(row=1, column=0, padx=(1, 0), pady=10, sticky="w")
        self.qty_entry = CTkSpinbox(self.ac_stat_frame, min_val=0, max_val=15, step=1, fg_color=INFO_FRAMES_COLOR)
        self.qty_entry.grid(row=1, column=1, padx=(10, 45), pady=10, sticky="w")

        ctk.CTkButton(ac_details_inner_frame, text="Reset", text_color="white", font=("Poppins", 15), fg_color="#E63946", hover_color="#C92A3F", width=60, command=lambda w=ac_details_inner_frame: self.clear_widget_inputs(w)).grid(row=7, column=0, padx=(1, 0), pady=(5, 10), sticky="w")

    # def refresh_aircon_optionmenus(self):
    #     # Refresh Type
    #     self.ac_types.configure(values=get_ac_types())

    #     # Refresh Compressor Tech based on selected type (optional)
    #     selected_type = self.chosen_ac_type.get()
    #     if selected_type:
    #         self.ac_comps.configure(values=get_technologies(selected_type))
    #     else:
    #         self.ac_comps.configure(values=get_technologies())

    #     # Refresh Brand based on current Type + Tech (if applicable)
    #     selected_tech = self.chosen_compressor.get()
    #     if selected_type and selected_tech:
    #         self.ac_brand_menu.configure(values=get_brands(selected_type, selected_tech))
    #     else:
    #         self.ac_brand_menu.configure(values=get_brands())

    #     # Reset series and models dropdowns
    #     self.ac_series.configure(values=[])
    #     self.ac_models.configure(values=[])
    #     self.ac_hps.configure(values=self.ac_hp_list)

    #     # Clear chosen values to avoid inconsistencies
    #     self.chosen_series.set("")
    #     self.chosen_model.set("")
    #     self.chosen_hp.set("")

    def refresh_aircon_optionmenus(self):
        """Refresh all AC-related option menus while preserving current selections."""
        # 1️⃣ Store current selections
        current_type = self.chosen_ac_type.get()
        current_comp = self.chosen_compressor.get()
        current_brand = self.chosen_brand.get()
        current_series = self.chosen_series.get()
        current_model = self.chosen_model.get()
        current_hp = self.chosen_hp.get()

        # 2️⃣ Refresh AC Types
        new_types = get_ac_types()
        self.ac_types.configure(values=new_types)
        if current_type in new_types:
            self.ac_types.set(current_type)
        else:
            self.ac_types.set(DEFAULT_TYPE)

        # 3️⃣ Refresh Compressor Technologies (if AC type is selected)
        if current_type:
            new_techs = get_technologies(current_type)

            # ✅ Use fallback compressors if no technology is linked yet
            if not new_techs:
                new_techs = DEFAULT_COMPRESSORS

            self.ac_comps.configure(values=new_techs, state="normal")
            if current_comp in new_techs:
                self.ac_comps.set(current_comp)
            elif new_techs:
                self.ac_comps.set(new_techs[0])
        else:
            self.ac_comps.configure(values=[], state="disabled")
            self.ac_comps.set(DEFAULT_COMPRESSOR)

        # if current_type:
        #     new_techs = get_technologies(current_type)
        #     # ✅ if no techs, fallback to default two
        #     if not new_techs:
        #         print("No new techs")
        #         new_techs = ["INVERTER", "NON_INVERTER"]

        # else:
        #     self.ac_comps.configure(values=[], state="disabled")
        #     self.ac_comps.set(DEFAULT_COMPRESSOR)

        # 4️⃣ Refresh Brands (if AC type + compressor are selected)
        if current_type and current_comp:
            new_brands = get_brands(current_type, current_comp)
            self.ac_brand_menu.configure(values=new_brands, state="normal")
            if current_brand in new_brands:
                self.ac_brand_menu.set(current_brand)
            else:
                self.ac_brand_menu.set("")
        else:
            self.ac_brand_menu.configure(values=[], state="disabled")
            self.ac_brand_menu.set("")

        # 5️⃣ Refresh Series (if brand selected and not "OTHER")
        if current_brand and current_brand != "OTHER":
            new_series = get_series(current_brand, current_comp, current_type)
            self.ac_series.configure(values=new_series, state="normal" if new_series else "disabled")
            if current_series in new_series:
                self.ac_series.set(current_series)
            elif new_series:
                self.ac_series.set(new_series[0])
            else:
                self.ac_series.set("")
        else:
            self.ac_series.configure(values=[], state="disabled")
            self.ac_series.set("")

        # 6️⃣ Refresh Models (if series selected)
        if current_series and current_brand and current_brand != "OTHER":
            new_models = get_models(current_series, current_brand)
            self.ac_models.configure(values=new_models, state="normal" if new_models else "disabled")
            if current_model in new_models:
                self.ac_models.set(current_model)
            elif new_models:
                self.ac_models.set(new_models[0])
            else:
                self.ac_models.set("")
        else:
            self.ac_models.configure(values=[], state="disabled")
            self.ac_models.set("")

        # 7️⃣ Refresh HP
        if current_model and current_brand and current_series:
            hp_value = get_hp(current_model)
            if hp_value:
                self.ac_hps.configure(values=[str(hp_value)], state="normal")
                self.ac_hps.set(str(hp_value))
            else:
                self.ac_hps.configure(values=DEFAULT_HP_VALUES, state="normal")
                self.ac_hps.set(DEFAULT_HP_VALUES[0])
        else:
            # ✅ Always fall back to default HP list if no model selected yet
            self.ac_hps.configure(values=DEFAULT_HP_VALUES, state="normal")
            if current_hp in DEFAULT_HP_VALUES:
                self.ac_hps.set(current_hp)
            else:
                self.ac_hps.set(DEFAULT_HP_VALUES[0])

        # if current_model and current_brand and current_series:
        #     hp_value = get_hp(current_model)
        #     if hp_value:
        #         self.ac_hps.configure(values=[str(hp_value)], state="normal")
        #         self.ac_hps.set(str(hp_value))
        #     else:
        #         self.ac_hps.configure(values=[], state="disabled")
        #         self.ac_hps.set("")
        # else:
        #     self.ac_hps.configure(values=self.ac_hp_list, state="disabled")
        #     if current_hp in self.ac_hp_list:
        #         self.ac_hps.set(current_hp)
        #     else:
        #         self.ac_hps.set("")

    def build_request_items(self, parent):
        self.request_btn = ctk.CTkButton(
            parent,
            text="Open Request Form",
            font=("Poppins", 15.5),
            text_color="#299C5C",
            height=30,
            width=250,
            fg_color="#FFFFFF",
            hover_color="#F0F0F0",
            command=self.open_request_form
        )
        self.request_btn.pack(pady=(15, 10), padx=(0, 25))

    # def open_database_manager(self):
    #     manager = DatabaseManagerWindow(self.ac_frame_container["frame"])
    #     manager.protocol("WM_DELETE_WINDOW", lambda: (manager.destroy(), self.refresh_aircon_optionmenus()))

    def open_database_manager(self):
        DatabaseManagerWindow(self, refresh_callback=self.refresh_aircon_optionmenus)

    def open_new_aircon_window(self):
        new_window = ctk.CTkToplevel(self)
        new_window.title("New Aircon Details")
        new_window.geometry("800x600+350+35")
        # new_window.overrideredirect(True)
        new_window.grab_set()

        # Pass callback to ACManagerApp
        app = ACManagerApp(master=new_window, refresh_callback=self.refresh_aircon_options)
        app.pack(fill="both", expand=True)

    def refresh_aircon_options(self):
        # Re-fetch updated brand, series, models, hp from DB
        # (assuming you already have helper functions or can query directly)
        global aircon_brands, aircon_types, aircon_compressors  

        aircon_brands = get_brands()       # should return updated list from DB
        aircon_types = get_ac_types()
        aircon_compressors = get_technologies()

        # Update dropdowns with latest values
        self.ac_brand_menu.configure(values=aircon_brands)
        self.ac_types.configure(values=aircon_types)
        self.ac_comps.configure(values=aircon_compressors)

        # Reset selected values to defaults
        # self.chosen_brand.set(DEFAULT_BRAND)
        # self.chosen_ac_type.set(DEFAULT_TYPE)
        # self.chosen_compressor.set(DEFAULT_COMPRESSOR)

    def enable_entry_bindings(self):
        entry_fields = [self.date_entry, self.customer_name, self.customer_address, self.customer_contact_number, self.other_brand_entry, self.ac_series, self.other_hp_entry]
        for field in entry_fields:
            field.bind("<FocusIn>", lambda e, w=field: w.configure(border_color=ENTRY_FOCUS_COLOR))
            field.bind("<FocusOut>", lambda e, w=field: w.configure(border_color=INFO_FRAMES_COLOR))

    def enable_container_focus_removal_event(self):
        parent_frames = [self.installation_page, self.mainframe, self.basic_details_inner_frame, self.ac_stat_frame, self.customer_details_inner_frame, self.basic_frame_container["frame"], self.customer_frame_container["frame"], self.ac_frame_container["frame"], self.request_frame_container["frame"]]
        for frame in parent_frames:
            frame.bind("<Button-1>", self.clear_focus)

    def setup_installation_items(self, parent):
        # --- Top Bar ---
        top_bar = ctk.CTkFrame(parent, fg_color="#DEDEDE", height=50, corner_radius=0)
        top_bar.pack(fill="x", side="top")

        self.back_btn_icon = ctk.CTkImage(light_image=Image.open(paths.ICON_BACK), size=(18, 18))
        btn = ctk.CTkButton(
            top_bar,
            text="",
            width=55,
            height=30,
            fg_color="transparent",
            hover_color="#2CC985",
            image=self.back_btn_icon,
            command=self.confirm_back_to_menu
        )
        btn.pack(padx=25, pady=12, anchor="sw")

        # --- Scrollable Area ---
        self.scroll_area = ctk.CTkScrollableFrame(
            parent,
            fg_color="white",
            scrollbar_fg_color="white",
            scrollbar_button_color="#cccccc",
            scrollbar_button_hover_color="#aaaaaa"
        )
        self.scroll_area.pack(fill="both", expand=True)

        self.mainframe = ctk.CTkFrame(self.scroll_area, fg_color="white", border_width=0)
        self.mainframe.pack(fill="both", expand=True, padx=(30, 30), pady=(0, 20))

        self.mainframe.columnconfigure(0, weight=1)

        # -------- INSTALLATION HEADER --------
        ctk.CTkLabel(
            self.mainframe,
            text="INSTALLATION",
            font=("Roboto", 21, "bold"),
            corner_radius=30,
            fg_color="#48E19F",
            width=200,
            height=40
        ).grid(row=0, column=0, padx=(0, 25), pady=20, sticky="ns")

        # === BASIC INFO ===
        self.basic_frame_container = self.create_collapsible_section(
            parent=self.mainframe,
            row=1,
            title="Basic Info",
            frame_height=180
        )
        self.build_basic_info(self.basic_frame_container["frame"])

        # === CUSTOMER INFO ===
        self.customer_frame_container = self.create_collapsible_section(
            parent=self.mainframe,
            row=3,
            title="Customer Info",
            frame_height=170
        )
        self.build_customer_info(self.customer_frame_container["frame"])

        # === AIRCON DETAILS ===
        self.ac_frame_container = self.create_collapsible_section(
            parent=self.mainframe,
            row=5,
            title="Aircon Details",
            frame_height=550
        )
        self.build_aircon_details(self.ac_frame_container["frame"])

        # === REQUEST ITEMS ===
        self.request_frame_container = self.create_collapsible_section(
            parent=self.mainframe,
            row=7,
            title="Request Items",
            frame_height=65
        )
        self.build_request_items(self.request_frame_container["frame"])

        self.enable_entry_bindings()
        self.enable_container_focus_removal_event()

    def clear_focus(self, event):
        self.focus()

    def collapse_all_section(self):
        for container in [self.basic_frame_container, self.customer_frame_container, self.ac_frame_container, self.request_frame_container]:
            container["is_expanded"] = True
            self.toggle_section(container)

    def open_request_form(self):
        MaterialReqForm(self, fg_color="#F0F0F0")
    
    def clear_installation_form(self):
        """Reset all inputs on the installation page to default."""
        # Clear entries
        for widget in self.pages["installation"].winfo_children():
            self.clear_widget_inputs(widget)
        
        self.collapse_all_section()
            
    def back_to_menu(self):
        if self.delete_msgbox and self.delete_msgbox.winfo_exists():
            self.delete_msgbox.destroy()
        self.clear_installation_form()
        self.show_page("categories")
        self.get_date_btn.configure(state="normal", fg_color=COLOR_GREEN)
        self.other_brand_entry.configure(state="normal", border_color=INFO_FRAMES_COLOR)
        self.other_brand_entry.delete(0, "end")
        self.other_brand_entry.configure(state="disabled")
        self.focus()
        self.scroll_area.update_idletasks()
        self.scroll_area._parent_canvas.yview_moveto(0)  # reset scroll

    def clear_widget_inputs(self, widget):
        """Recursively clear entries, option menus, and checkboxes."""
        for child in widget.winfo_children():

            if child == self.qty_entry:
                self.qty_entry.value.set(0)
                continue

            elif isinstance(child, ctk.CTkEntry):
                child.delete(0, "end")
                if child in [self.other_brand_entry, self.other_hp_entry]:
                    self.other_brand_entry.delete(0, "end")
                    self.other_hp_entry.delete(0, "end")
                    self.other_brand_entry.grid_forget()
                    self.other_hp_entry.grid_forget()
                # else:
                #     self.other_brand_entry.delete(0, "end")
                #     self.other_hp_entry.delete(0
                # , "end")
                #     self.other_brand_entry.grid_forget()
                #     self.other_hp_entry.grid_forget()

            elif isinstance(child, ctk.CTkOptionMenu):
                if child == self.ac_types:
                    # AC Type should always reset to placeholder
                    child.set(DEFAULT_TYPE)
                    child.configure(state="normal")
                elif child == self.ac_comps:
                    child.set("")  # clear text
                    child.configure(state="disabled")
                elif child == self.ac_brand_menu:
                    child.set("")
                    child.configure(state="disabled")
                elif child == self.ac_series:
                    child.set("")
                    child.configure(state="disabled")
                elif child == self.ac_models:
                    child.set("")
                    child.configure(state="disabled")
                elif child == self.ac_hps:
                    child.set("")
                    child.configure(state="disabled")

            elif isinstance(child, ctk.CTkCheckBox):
                child.deselect()

            elif isinstance(child, ctk.CTkSwitch):
                self.switch_var.set("off")

            # Recursively clear inside nested frames
            self.clear_widget_inputs(child)

    def has_changes(self):
        """Return True if any input differs from defaults."""
        today_str = datetime.today().strftime("%B %d, %Y")

        # Entries
        if self.date_entry.get().strip() not in ["", today_str]:
            print("Change detected: date")
            return True
        if self.customer_name.get().strip():
            print("Change detected: customer_name")
            return True
        if self.customer_address.get().strip():
            print("Change detected: customer_address")
            return True
        if self.customer_contact_number.get().strip():
            print("Change detected: customer_contact_number")
            return True
        if self.other_brand_entry.get().strip():
            print("Change detected: other_brand_entry")
            return True
        if self.other_hp_entry.get().strip():
            print("Change detected: other_hp_entry")
            return True

        # Dropdowns
        # if self.chosen_ac_type.get() != self.optionmenu_defaults["type"]:
        #     print("Change detected: ac_type")
        #     return True
        # if self.chosen_compressor.get() != self.optionmenu_defaults["compressor"]:
        #     print("Change detected: compressor")
        #     return True
        # if self.chosen_brand.get() != self.optionmenu_defaults["brand"]:
        #     print("Change detected: brand")
        #     return True
        if self.chosen_compressor.get() not in ["", DEFAULT_COMPRESSOR]:
            return True
        if self.chosen_brand.get() not in ["", DEFAULT_BRAND]:
            return True
        if self.chosen_series.get() not in ["", DEFAULT_SERIES]:
            return True
        if self.chosen_model.get() not in ["", DEFAULT_MODEL]:
            return True
        if self.chosen_hp.get() not in ["", DEFAULT_HP]:
            return True

        # Only check series/model if AC Type is Split Type
        # if self.chosen_ac_type.get() == "SPLIT TYPE":
        #     if self.chosen_series.get() != self.optionmenu_defaults["series"]:
        #         print("Change detected: series")
        #         return True
        #     if self.chosen_model.get() != self.optionmenu_defaults["models"]:
        #         print("Change detected: model")
        #         return True

        # if self.chosen_hp.get() != self.optionmenu_defaults["hp"]:
        #     print("Change detected: hp")
        #     return True

        # Spinbox
        if self.qty_entry.value.get() != 0:
            print("Change detected: qty_entry")
            return True

        # Checkboxes
        for child in self.pages["installation"].winfo_children():
            if self.check_any_checkbox(child):
                print("Change detected: checkbox")
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



class Toast(ctk.CTkToplevel):
    def __init__(self, parent, message, *, x=600, y=325, duration=1800, bg_color="#218838", fg_color="#ffffff", font=("Poppins", 15, "bold"), width=225, height=50, wrap=280):
        super().__init__(parent)
        self.resizable(False, False)
        self.overrideredirect(True)   # no titlebar
        self.lift()   # stay on top
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.0)

        self.x = x
        self.y = y

        # message label
        self.label = ctk.CTkLabel(
            self,
            text=message,
            text_color=fg_color,
            fg_color=bg_color,
            font=font,
            padx=15,
            pady=8,
            width=width,
            height=height,
            bg_color=bg_color,
            wraplength=wrap
        )
        self.label.pack()

        # position at bottom-right of parent
        self.update_idletasks()
        tw = self.winfo_reqwidth()
        th = self.winfo_reqheight()

        self.geometry(f"{tw}x{th}+{self.x}+{self.y}")

        # fade in
        self.attributes("-alpha", 0.0)
        self._fade(step=0.05, target=1.0, delay=10)

        # schedule fade-out
        self.after(duration, lambda: self._fade(step=-0.05, target=0.0, delay=10, on_done=self.destroy))

    def _fade(self, step, target, delay, on_done=None):
        alpha = self.attributes("-alpha") + step
        alpha = max(0.0, min(1.0, alpha))
        self.attributes("-alpha", alpha)
        if (step > 0 and alpha < target) or (step < 0 and alpha > target):
            self.after(delay, lambda: self._fade(step, target, delay, on_done))
        elif on_done:
            on_done()


class CTkSpinbox(ctk.CTkFrame):
    def __init__(self, master=None, min_val=0, max_val=100, step=1, **kwargs):
        super().__init__(master, **kwargs)
        
        self.value = ctk.IntVar(value=min_val)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step

        # Decrease button
        self.decrease_btn = ctk.CTkButton(self, text="-", text_color="#FFFFFF", font=("Poppins", 14, "bold"), height=32, width=30, command=self.decrease, fg_color="#1A7B45", hover_color=COLOR_GREEN)
        self.decrease_btn.grid(row=0, column=0, padx=(0, 5))

        # Entry
        self.entry = ctk.CTkEntry(self, font=("Poppins", 14), textvariable=self.value, height=26, width=45, justify="center", border_color=INFO_FRAMES_COLOR)
        self.entry.grid(row=0, column=1)

        # Increase button
        self.increase_btn = ctk.CTkButton(self, text="+", text_color="#FFFFFF", font=("Poppins", 14, "bold"), height=32, width=30, command=self.increase, fg_color="#1A7B45", hover_color=COLOR_GREEN)
        self.increase_btn.grid(row=0, column=2, padx=(5, 0))

    def increase(self):
        if self.value.get() + self.step <= self.max_val:
            self.value.set(self.value.get() + self.step)

    def decrease(self):
        if self.value.get() - self.step >= self.min_val:
            self.value.set(self.value.get() - self.step)











# def check_ac_type(value):
        #     print("ac tpye:", value)
        #     if value == "SPLIT TYPE":
        #         self.ac_hp_list = [hp for hp in self.ac_hp_list if hp not in ["0.5", "0.6", "0.8"]]
            
        #     elif value == "WINDOW TYPE":
        #         self.ac_hp_list = [hp for hp in self.ac_hp_list if hp != "3.0"]
       
        #     else:
        #         pass

        #     # Enable compressor technology menu
        #     self.ac_comps.configure(state="normal")
        #     self.chosen_compressor.set(value=self.optionmenu_defaults["compressor"])

        #     # Enable brand menu
        #     self.ac_brand_menu.configure(state="normal")
        #     self.chosen_brand.set(value=self.optionmenu_defaults["brand"])

        #     # Disable series and models menu
        #     self.ac_series.configure(state="disabled")
        #     self.chosen_series.set("")
        #     self.ac_models.configure(state="disabled")
        #     self.chosen_model.set("")

        #     # self.series_frame.grid()   # show
        #     # self.model_frame.grid()    # show 
        #     # self.series_frame.grid_forget()  # hide
        #     # self.model_frame.grid_forget()   # hide





# # --- SERIES CONTAINER ---
        # self.series_frame = ctk.CTkFrame(ac_details_inner_frame, fg_color="transparent")
        # self.series_frame.grid(row=3, column=0, columnspan=2, sticky="w")

        # ctk.CTkLabel(self.series_frame, text="Series:", font=("Poppins", 16, "bold"), text_color="white").grid(row=0, column=0, padx=(1, 0), pady=10, sticky="w")
        # self.chosen_series = ctk.StringVar(value=self.optionmenu_defaults["series"])
        # self.ac_series = ctk.CTkOptionMenu(
        #     self.series_frame,
        #     values=[],
        #     height=33,
        #     width=200,
        #     font=FONT_NORMAL,
        #     text_color="black",
        #     button_color=COLOR_GREEN,
        #     button_hover_color=COLOR_GREEN_HOVER,
        #     fg_color=COLOR_GRAY,
        #     dropdown_fg_color=COLOR_GRAY,
        #     dropdown_text_color="black",
        #     dropdown_font=FONT_NORMAL,
        #     dropdown_hover_color="#2CC985",
        #     anchor="center",
        #     variable=self.chosen_series,
        #     command=check_series,
        #     state="disabled",
        # )
        # self.ac_series.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="w")

        # # --- MODEL CONTAINER ---
        # self.model_frame = ctk.CTkFrame(ac_details_inner_frame, fg_color="transparent")
        # self.model_frame.grid(row=4, column=0, columnspan=2, sticky="w")

        # ctk.CTkLabel(self.model_frame, text="Model:", font=("Poppins", 16, "bold"), text_color="white").grid(row=0, column=0, padx=(1, 0), pady=10, sticky="w")

        # self.chosen_model = ctk.StringVar(value=self.optionmenu_defaults["models"])
        # self.ac_models = ctk.CTkOptionMenu(
        #     self.model_frame,
        #     values=[],
        #     height=33,
        #     width=200,
        #     font=FONT_NORMAL,
        #     text_color="black",
        #     button_color=COLOR_GREEN,
        #     button_hover_color=COLOR_GREEN_HOVER,
        #     fg_color=COLOR_GRAY,
        #     dropdown_fg_color=COLOR_GRAY,
        #     dropdown_text_color="black",
        #     dropdown_font=FONT_NORMAL,
        #     dropdown_hover_color="#2CC985",
        #     anchor="center",
        #     command=check_model_for_hp,
        #     variable=self.chosen_model,
        #     state="disabled",
        # )
        # self.ac_models.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="w")