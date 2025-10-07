# import customtkinter as ctk
# from core.aircon_backend import insert_model, cursor

# class ACManagerApp(ctk.CTkFrame):
#     def __init__(self, master=None, refresh_callback=None):
#         super().__init__(master)
#         self.refresh_callback = refresh_callback

#         # Entry fields
#         self.model_entry = ctk.CTkEntry(self, placeholder_text="Model Name")
#         self.model_entry.pack(pady=5)

#         self.hp_entry = ctk.CTkEntry(self, placeholder_text="HP Rating")
#         self.hp_entry.pack(pady=5)

#         self.series_entry = ctk.CTkEntry(self, placeholder_text="Series Name")
#         self.series_entry.pack(pady=5)

#         self.brand_entry = ctk.CTkEntry(self, placeholder_text="Brand")
#         self.brand_entry.pack(pady=5)

#         self.tech_entry = ctk.CTkEntry(self, placeholder_text="Technology (INVERTER/NON_INVERTER)")
#         self.tech_entry.pack(pady=5)

#         self.type_entry = ctk.CTkEntry(self, placeholder_text="AC Type (WINDOW/WALL_MOUNTED/...)")
#         self.type_entry.pack(pady=5)

#         # Buttons
#         ctk.CTkButton(self, text="Add Model", command=self.add_model).pack(pady=5)
#         ctk.CTkButton(self, text="View All Models", command=self.view_models).pack(pady=5)

#         # Output box
#         self.output_box = ctk.CTkTextbox(self, width=700, height=250)
#         self.output_box.pack(pady=10)

#     def add_model(self):
#         model = self.model_entry.get()
#         hp = float(self.hp_entry.get())
#         series = self.series_entry.get()
#         brand = self.brand_entry.get()
#         tech = self.tech_entry.get()
#         ac_type = self.type_entry.get()

#         insert_model(ac_type, tech, brand, series, model, hp)
#         self.output_box.insert("end", f"✅ Added: {model}\n")

#         # Trigger refresh in parent form
#         if self.refresh_callback:
#             self.refresh_callback()

#     def view_models(self):
#         self.output_box.delete("1.0", "end")
#         cursor.execute("""
#             SELECT m.model_name, m.hp, s.series_name, b.brand_name, t.tech_name, a.type_name
#             FROM models m
#             JOIN series s ON m.series_id = s.id
#             JOIN brands b ON s.brand_id = b.id
#             JOIN technology t ON m.tech_id = t.id
#             JOIN ac_types a ON m.type_id = a.id
#         """)
#         for row in cursor.fetchall():
#             self.output_box.insert("end", f"{row}\n")


# if __name__ == "__main__":
#     app = ACManagerApp()
#     app.mainloop()

















import customtkinter as ctk
from tkinter import messagebox
from core.aircon_backend import (
    cursor, insert_model, get_ac_types, get_technologies, get_brands, get_series, get_models, add_ac_type, add_technology, add_brand, add_series, delete_ac_type, delete_technology, delete_brand, delete_series, delete_model
)

# ==============================
# Constants
# ==============================
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
FONT_BOLD = ("Poppins", 15, "bold")


class ACManagerApp(ctk.CTkFrame):
    def __init__(self, master=None, refresh_callback=None):
        super().__init__(master, fg_color=FRAMES_FG_COLOR)
        self.refresh_callback = refresh_callback

        # widget references
        self.entries = {}
        self.extra_hp_entry = None
        self.extra_ac_type_entry = None
        self.entry_frames = {}
        self.entry_buttons = {}

        self.ac_type_container = None
        self.hp_container = None
        self.ac_type_menu = None
        self.hp_menu = None

        # container for fields
        self.fields_frame = ctk.CTkFrame(self, fg_color="lightblue")
        self.fields_frame.pack(pady=10, fill="x")

        # Field definitions
        self.available_fields = [
            ("AC Type", "ac_type"),
            ("Compressor", "tech"),
            ("Brand", "brand"),
            ("Series Name", "series"),
            ("Model Name", "model"),
            ("HP Rating", "hp"),
        ]

        # Option menu values (added MORE to ac_type)
        self.ac_type_options = [
            "WINDOW",
            "WALL_MOUNTED",
            "FLOOR_MOUNTED_CEILING_CASSETTE",
            "MORE",
        ]
        self.tech_options = ["INVERTER", "NON_INVERTER"]
        self.hp_options = ["0.5", "0.6", "0.7", "1.0", "1.5", "2.0", "2.5", "3.0", "MORE"]

        # Default shown fields
        self.default_shown = {"ac_type", "tech", "hp"}

        self._build_fields_section()

        # Action buttons
        ctk.CTkButton(
            self,
            text="Save Model",
            command=self.save_model,
            fg_color=COLOR_GREEN,
            hover_color=COLOR_GREEN_HOVER,
            text_color=BUTTON_FG_COLOR,
            font=FONT_NORMAL
        ).pack(pady=5)

        ctk.CTkButton(
            self,
            text="View All Models",
            command=self.view_models,
            fg_color=COLOR_GREEN,
            hover_color=COLOR_GREEN_HOVER,
            text_color=BUTTON_FG_COLOR,
            font=FONT_NORMAL
        ).pack(pady=5)

        # Close button (red)
        ctk.CTkButton(
            self,
            text="Close",
            command=self.master.destroy,   # or self.quit, depending on context
            fg_color=COLOR_RED,
            hover_color=COLOR_RED_HOVER,
            text_color=BUTTON_FG_COLOR,
            font=FONT_NORMAL
        ).pack(pady=5)

        # Output box
        self.output_box = ctk.CTkTextbox(self, width=700, height=250, font=FONT_NORMAL)
        self.output_box.pack(pady=10)

    def _build_fields_section(self):
        """Build labels, toggle buttons, and placeholder frames with aligned layout."""
        for label_text, key in self.available_fields:
            # Row container (neutral background)
            row_frame = ctk.CTkFrame(self.fields_frame, fg_color=FRAMES_FG_COLOR)
            row_frame.pack(fill="x", pady=(4, 10), padx=5)
            row_frame.columnconfigure(2, weight=1)  # allow entry area to expand

            # Label with green background (fixed width)
            label_frame = ctk.CTkFrame(row_frame, width=250, height=40, fg_color=INFO_FRAMES_COLOR)
            label_frame.grid(row=0, column=0, sticky="nsew")
            label_frame.pack_propagate(False)
            ctk.CTkLabel(
                label_frame,
                text=label_text,
                font=FONT_BOLD,
                text_color="white",
                anchor="w",
                padx=10
            ).pack(fill="both", expand=True)

            # Button or spacer
            if key not in self.default_shown:
                add_button = ctk.CTkButton(
                    row_frame,
                    text="+",
                    width=40,
                    height=40,
                    font=FONT_NORMAL,
                    fg_color=COLOR_GREEN,
                    hover_color=COLOR_GREEN_HOVER,
                    text_color=BUTTON_FG_COLOR,
                    command=lambda k=key: self._toggle_entry(k)
                )
                add_button.grid(row=0, column=1, padx=5)
                self.entry_buttons[key] = add_button
            else:
                # Invisible spacer to align layout
                spacer = ctk.CTkLabel(row_frame, text="", width=40, fg_color=FRAMES_FG_COLOR)
                spacer.grid(row=0, column=1, padx=5)

            # Entry frame (white background, fills remaining space)
            entry_frame = ctk.CTkFrame(row_frame, fg_color=FRAMES_FG_COLOR, height=70)
            entry_frame.grid(row=0, column=2, sticky="nsew")
            # entry_frame.pack_propagate(False)
            self.entry_frames[key] = entry_frame

            # Auto-show defaults
            if key in self.default_shown:
                widget = self._create_input_widget(key)
                widget.pack(fill="both", expand=True, padx=5, pady=4)
                self.entries[key] = widget

    def _toggle_entry(self, key):
        """Toggle optional fields (brand, series, model)."""
        if key not in self.entries:
            widget = self._create_input_widget(key)
            widget.pack(fill="x", padx=5, pady=2, expand=True)
            self.entries[key] = widget
            self.entry_buttons[key].configure(text="–")
        else:
            self.entries[key].destroy()
            del self.entries[key]
            self.entry_buttons[key].configure(text="+")
            if key == "hp" and self.extra_hp_entry:
                self.extra_hp_entry.destroy()
                self.extra_hp_entry = None
            if key == "ac_type" and self.extra_ac_type_entry:
                self.extra_ac_type_entry.destroy()
                self.extra_ac_type_entry = None

    def _create_input_widget(self, key):
        """Return appropriate input widget."""
        if key == "ac_type":
            self.ac_type_container = ctk.CTkFrame(self.entry_frames[key], fg_color=FRAMES_FG_COLOR)
            self.ac_type_container.pack(fill="both", expand=True)

            self.ac_type_menu = ctk.CTkOptionMenu(
                self.ac_type_container,
                values=self.ac_type_options,
                font=FONT_NORMAL,
                command=self._on_ac_type_select,
            )
            self.ac_type_menu.pack(fill="x", padx=5, pady=2)

            return self.ac_type_menu  # ✅ store the menu as the widget, not the container

        elif key == "hp":
            self.hp_container = ctk.CTkFrame(self.entry_frames[key], fg_color=FRAMES_FG_COLOR)
            self.hp_container.pack(fill="both", expand=True)

            self.hp_menu = ctk.CTkOptionMenu(
                self.hp_container,
                values=self.hp_options,
                font=FONT_NORMAL,
                command=self._on_hp_select
            )
            self.hp_menu.pack(fill="x", padx=5, pady=2)

            return self.hp_menu

        elif key == "tech":
            return ctk.CTkOptionMenu(
                self.entry_frames[key],
                values=self.tech_options,
                font=FONT_NORMAL
            )
        else:
            return ctk.CTkEntry(self.entry_frames[key], font=FONT_NORMAL)

    def _on_ac_type_select(self, value):
        """Show extra entry for custom AC Type."""
        if value == "MORE":
            if not self.extra_ac_type_entry:
                self.extra_ac_type_entry = ctk.CTkEntry(
                    self.ac_type_container,
                    placeholder_text="Enter custom AC Type",
                    font=FONT_NORMAL
                )
                self.extra_ac_type_entry.pack(fill="x", padx=5, pady=2)
                self.extra_ac_type_entry.focus()
        else:
            if self.extra_ac_type_entry:
                self.extra_ac_type_entry.delete(0, "end")
                self.extra_ac_type_entry.destroy()
                self.extra_ac_type_entry = None

    def _on_hp_select(self, value):
        """Show extra entry for custom HP."""
        if value == "MORE":
            if not self.extra_hp_entry:
                self.extra_hp_entry = ctk.CTkEntry(
                    self.hp_container,
                    placeholder_text="Enter custom HP",
                    font=FONT_NORMAL
                )
                self.extra_hp_entry.pack(fill="x", padx=5, pady=2)
                self.extra_hp_entry.focus()
        else:
            if self.extra_hp_entry:
                self.extra_hp_entry.delete(0, "end")
                self.extra_hp_entry.destroy()
                self.extra_hp_entry = None

    # def _on_hp_select(self, value):
    #     """Show extra entry for custom HP."""
    #     container = self.entries["hp"]
    #     if value == "MORE":
    #         if not self.extra_hp_entry:
    #             self.extra_hp_entry = ctk.CTkEntry(
    #                 container,
    #                 placeholder_text="Enter custom HP",
    #                 font=FONT_NORMAL
    #             )
    #             self.extra_hp_entry.pack(fill="x", padx=5, pady=2)
    #             self.extra_hp_entry.focus()
    #     else:
    #         if self.extra_hp_entry:
    #             self.extra_hp_entry.delete(0, "end")
    #             self.extra_hp_entry.destroy()
    #             self.extra_hp_entry = None

    def save_model(self):
        """Collect values, validate, and insert into DB safely."""
        data = {}
        for key, widget in self.entries.items():
            if isinstance(widget, ctk.CTkOptionMenu):
                val = widget.get()
                if key == "hp" and val == "MORE" and self.extra_hp_entry:
                    val = self.extra_hp_entry.get().strip()
                elif key == "ac_type" and val == "MORE" and self.extra_ac_type_entry:
                    val = self.extra_ac_type_entry.get().strip()
                data[key] = val.strip() if val else None
            else:
                val = widget.get().strip()
                data[key] = val if val else None

        # Validate required fields
        required_fields = ["ac_type", "tech", "model", "hp"]
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            self.output_box.insert("end", f"⚠️ Missing required fields: {', '.join(missing)}\n")
            return

        # Convert HP to float if possible
        try:
            data["hp"] = float(data["hp"]) if data["hp"] else None
        except ValueError:
            self.output_box.insert("end", f"❌ Invalid HP value: {data['hp']}\n")
            return

        # Safe defaults for optional fields
        ac_type = data.get("ac_type")
        tech = data.get("tech")
        brand = data.get("brand") or None
        series = data.get("series") or None
        model = data.get("model") or None
        hp = data.get("hp")

        try:
            insert_model(ac_type, tech, brand, series, model, hp)
            self.output_box.insert("end", f"✅ Added: {data}\n")
            if self.refresh_callback:
                self.refresh_callback()
        except Exception as e:
            self.output_box.insert("end", f"❌ Error saving model: {e}\n")

    def view_models(self):
        """Display all models."""
        self.output_box.delete("1.0", "end")
        cursor.execute("""
            SELECT m.model_name, m.hp, s.series_name, b.brand_name, t.tech_name, a.type_name
            FROM models m
            JOIN series s ON m.series_id = s.id
            JOIN brands b ON s.brand_id = b.id
            JOIN technology t ON m.tech_id = t.id
            JOIN ac_types a ON m.type_id = a.id
        """)
        for row in cursor.fetchall():
            self.output_box.insert("end", f"{row}\n")



# class DatabaseManagerWindow(ctk.CTkToplevel):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.title("Manage Database")
#         self.geometry("600x600+450+83")
#         self.resizable(False, False)
#         self.grab_set()

#         self.configure(fg_color="#F5F5F5")

#         title_label = ctk.CTkLabel(
#             self,
#             text="🛠 Manage AC Database",
#             font=("Poppins", 20, "bold")
#         )
#         title_label.pack(pady=15)

#         # Section container
#         self.section_frame = ctk.CTkScrollableFrame(self, width=550, height=550)
#         self.section_frame.pack(pady=10, padx=10, fill="both", expand=True)

#         # Build management sections
#         self._build_section("AC Type", get_ac_types, add_ac_type, delete_ac_type)
#         self._build_section("Technology", get_technologies, add_technology, delete_technology)
#         self._build_section("Brand", get_brands, add_brand, delete_brand)
#         self._build_series_section()
#         self._build_model_section()
class DatabaseManagerWindow(ctk.CTkToplevel):
    def __init__(self, master=None, refresh_callback=None):
        super().__init__(master)
        self.title("Manage Database")
        self.geometry("600x600+450+83")
        self.resizable(False, False)
        self.grab_set()

        self.refresh_callback = refresh_callback  # ✅ store the callback
        self.selected_ac_type = ""

        self.configure(fg_color="#F5F5F5")

        title_label = ctk.CTkLabel(
            self,
            text="🛠 Manage AC Database",
            font=("Poppins", 20, "bold")
        )
        title_label.pack(pady=15)

        # Section container
        self.section_frame = ctk.CTkScrollableFrame(self, width=550, height=550)
        self.section_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Build management sections
        self.ac_type_data = self._build_section("AC Type", get_ac_types, add_ac_type, delete_ac_type)
        self.compressor_type_data = self._build_section("Technology", get_technologies, add_technology, delete_technology)
        self.ac_brand_data = self._build_section("Brand", get_brands, add_brand, delete_brand)
        self._build_series_section()
        self._build_model_section()

    def _build_section(self, label_text, getter_fn, add_fn, delete_fn):
        """Generic section for AC Type, Technology, Brand."""
        frame = ctk.CTkFrame(self.section_frame)
        frame.pack(fill="x", pady=10, padx=5)

        ctk.CTkLabel(frame, text=label_text, font=("Poppins", 16, "bold")).pack(anchor="w", padx=5, pady=3)

        # Dropdown for existing values
        values = getter_fn()
        dropdown = ctk.CTkOptionMenu(frame, values=values if values else [""])
        dropdown.pack(side="left", padx=5, pady=5)

        # Entry for new value
        entry = ctk.CTkEntry(frame, placeholder_text=f"New {label_text}")
        entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        # Add button
        ctk.CTkButton(
            frame,
            text="➕ Add",
            fg_color="#298753",
            hover_color="#207347",
            text_color="white",
            command=lambda: self._handle_add(entry.get(), add_fn, dropdown)
        ).pack(side="left", padx=3)

        # Delete button
        ctk.CTkButton(
            frame,
            text="🗑 Delete",
            fg_color="#E63946",
            hover_color="#D72533",
            text_color="white",
            command=lambda: self._handle_delete(dropdown.get(), delete_fn, dropdown, getter_fn)
        ).pack(side="left", padx=3)
        
        return entry

    def _build_series_section(self):
        """Series depends on Brand."""
        frame = ctk.CTkFrame(self.section_frame)
        frame.pack(fill="x", pady=10, padx=5)

        ctk.CTkLabel(frame, text="Series (by Brand)", font=("Poppins", 16, "bold")).pack(anchor="w", padx=5, pady=3)

        # Brand dropdown
        self.series_brand_dd = ctk.CTkOptionMenu(frame, values=get_brands())
        self.series_brand_dd.pack(side="left", padx=5, pady=5)

        # Series dropdown
        self.series_dd = ctk.CTkOptionMenu(frame, values=[""])
        self.series_dd.pack(side="left", padx=5, pady=5)

        # Refresh series when brand changes
        self.series_brand_dd.configure(command=self._refresh_series_dropdown)

        # Entry for new series
        entry = ctk.CTkEntry(frame, placeholder_text="New Series")
        entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)

        # Add Series
        ctk.CTkButton(
            frame,
            text="➕ Add",
            fg_color="#298753",
            hover_color="#207347",
            text_color="white",
            command=lambda: self._handle_add_series(entry.get())
        ).pack(side="left", padx=3)

        # Delete Series
        ctk.CTkButton(
            frame,
            text="🗑 Delete",
            fg_color="#E63946",
            hover_color="#D72533",
            text_color="white",
            command=self._handle_delete_series
        ).pack(side="left", padx=3)

    def _build_model_section(self):
        """Model depends on Series + Brand."""
        frame = ctk.CTkFrame(self.section_frame)
        frame.pack(fill="x", pady=10, padx=5)

        ctk.CTkLabel(frame, text="Model (by Series)", font=("Poppins", 16, "bold")).pack(anchor="w", padx=5, pady=3)

        # Brand dropdown
        self.model_brand_dd = ctk.CTkOptionMenu(frame, values=get_brands())
        self.model_brand_dd.pack(side="left", padx=5, pady=5)

        # Series dropdown
        self.model_series_dd = ctk.CTkOptionMenu(frame, values=[""])
        self.model_series_dd.pack(side="left", padx=5, pady=5)

        self.model_brand_dd.configure(command=self._refresh_model_series_dropdown)

        # Model dropdown
        self.model_dd = ctk.CTkOptionMenu(frame, values=[""])
        self.model_dd.pack(side="left", padx=5, pady=5)

        # Refresh models when series changes
        self.model_series_dd.configure(command=self._refresh_models_dropdown)

        # Delete button
        ctk.CTkButton(
            frame,
            text="🗑 Delete Model",
            fg_color="#E63946",
            hover_color="#D72533",
            text_color="white",
            command=self._handle_delete_model
        ).pack(side="left", padx=3)

    # =======================
    # INTERNAL HANDLERS
    # =======================

    def _handle_add(self, value, add_fn, dropdown):
        if not value.strip():
            messagebox.showwarning("Warning", "Please enter a value to add.")
            return
        try:
            msg = add_fn(value)
            messagebox.showinfo("Success", msg)
            dropdown.configure(values=[*dropdown.cget("values"), value.upper()])
            dropdown.set(value.upper())

            # ✅ Trigger refresh in parent window
            if self.refresh_callback:
                self.refresh_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _handle_delete(self, value, delete_fn, dropdown, getter_fn):
        if not value.strip():
            messagebox.showwarning("Warning", "Please select a value to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{value}'?"):
            return
        try:
            msg = delete_fn(value)
            messagebox.showinfo("Deleted", msg)
            dropdown.configure(values=getter_fn())

            # ✅ Trigger refresh in parent window
            if self.refresh_callback:
                self.refresh_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _handle_add_series(self, series_name):
        ac_type = self.ac_type_data.get()
        brand = self.series_brand_dd.get()
        if not brand or not series_name.strip():
            messagebox.showwarning("Warning", "Select a brand and enter series name.")
            return
        try:
            msg = add_series(series_name, brand, ac_type)
            messagebox.showinfo("Success", msg)
            self._refresh_series_dropdown(brand)

            if self.refresh_callback:
                self.refresh_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _handle_delete_series(self):
        brand = self.series_brand_dd.get()
        series = self.series_dd.get()
        if not brand or not series:
            messagebox.showwarning("Warning", "Select a brand and series to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Delete series '{series}' under '{brand}'?"):
            return
        try:
            msg = delete_series(series, brand)
            messagebox.showinfo("Deleted", msg)
            self._refresh_series_dropdown(brand)

            if self.refresh_callback:
                self.refresh_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _handle_delete_model(self):
        model = self.model_dd.get()
        if not model:
            messagebox.showwarning("Warning", "Select a model to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Delete model '{model}'?"):
            return
        try:
            msg = delete_model(model)
            messagebox.showinfo("Deleted", msg)
            self._refresh_models_dropdown(self.model_series_dd.get())

            if self.refresh_callback:
                self.refresh_callback()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =======================
    # DROPDOWN REFRESHERS
    # =======================

    def _refresh_series_dropdown(self, brand):
        self.series_dd.configure(values=get_series(brand))

    def _refresh_model_series_dropdown(self, brand):
        self.model_series_dd.configure(values=get_series(brand))
        self.model_dd.configure(values=[""])

    def _refresh_models_dropdown(self, series):
        brand = self.model_brand_dd.get()
        self.model_dd.configure(values=get_models(series, brand))
