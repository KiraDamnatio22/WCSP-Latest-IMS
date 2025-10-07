# Import built-in modules
import customtkinter as ctk
from PIL import Image

# Import own-made modules
from core import paths
from core.ims_data import indoor_items, sample_data


COLOR_GREEN = "#4BAC76"
COLOR_GREEN_HOVER = "#298753"
COLOR_RED = "#E63946"
COLOR_RED_HOVER = "#D72533"
COLOR_GRAY = "#E8E8E8"

BTN_COLOR_GREEN = "#2CC985"
BTN_COLOR_GREEN_HOVER = "#0C955A"


class HoverScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<Button-1>", self._bind_mousewheel)
        # self.bind("<Enter>", self._bind_mousewheel)
        # self.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, event=None):
        self._parent_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event=None):
        self._parent_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        scroll_speed = 15
        if event.num == 4 or event.delta > 0:
            self._parent_canvas.yview_scroll(-1 * scroll_speed, "units")
        elif event.num == 5 or event.delta < 0:
            self._parent_canvas.yview_scroll(1 * scroll_speed, "units")


class MaterialReqForm(ctk.CTkToplevel):
    def __init__(self, *args, fg_color = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.title("Request Form")
        self.geometry("1100x600+180+80")
        self.configure(fg_color="#FFFFFF")
        self.grab_set()

        # Global variables
        self.ac_entries = {}  # keep entries here
        self.mframe = None    # will hold scrollable frame later
        self.ac_data = []
        self.indoor_entries = {}
        self.outdoor_entries = {}
        self.sample_data = sample_data

        mainframe = HoverScrollableFrame(self, fg_color="#A6E4C2", corner_radius=10, border_width=0, border_color="gray")
        mainframe.pack(fill="both", expand=True, padx=10, pady=10) 
        mainframe.bind("<Button-1>", self.clear_focus)

        # IMPORTANT FRAMES
        # INDOOR ITEMS
        ctk.CTkLabel(mainframe, text="INDOOR", font=("Poppins", 20, "bold")).pack(padx=10, pady=(10, 0), anchor="w")
        self.indoor_frame = ctk.CTkFrame(mainframe, fg_color="#D4F0D4")
        self.indoor_frame.pack(fill="x", padx=10, pady=(0, 10))
        # self.indoor_frame.grid_propagate(False)
        self.indoor_frame.grid_columnconfigure(0, weight=0)
        self.indoor_frame.grid_columnconfigure(1, weight=1)
        self.indoor_frame.bind("<Button-1>", self.clear_focus)

        # OUTDOOR ITEMS
        ctk.CTkLabel(mainframe, text="OUTDOOR", font=("Poppins", 20, "bold")).pack(padx=10, pady=(10, 0), anchor="w")
        self.outdoor_frame = ctk.CTkFrame(mainframe, fg_color="#D4F0D4", width=1020, height=340)
        self.outdoor_frame.pack(padx=10, pady=(0, 10), anchor="w")
        self.outdoor_frame.grid_propagate(False)
        self.outdoor_frame.grid_columnconfigure(0, weight=0)
        self.outdoor_frame.grid_columnconfigure(1, weight=1)
        
        # SUPPLY ITEMS
        ctk.CTkLabel(mainframe, text="SUPPLY", font=("Poppins", 20, "bold")).pack(padx=10, pady=(10, 0), anchor="w")
        self.supply_frame = ctk.CTkFrame(mainframe, fg_color="#D4F0D4", width=1020, height=340)
        self.supply_frame.pack(padx=10, pady=(0, 10), anchor="w")
        self.supply_frame.grid_propagate(False)
        self.supply_frame.grid_columnconfigure(0, weight=0)
        self.supply_frame.grid_columnconfigure(1, weight=1)

        # DRAINAGE ITEMS
        ctk.CTkLabel(mainframe, text="DRAINAGE", font=("Poppins", 20, "bold")).pack(padx=10, pady=(10, 0), anchor="w")
        self.drainage_frame = ctk.CTkFrame(mainframe, fg_color="#D4F0D4", width=1020, height=340)
        self.drainage_frame.pack(padx=10, pady=(0, 10), anchor="w")
        self.drainage_frame.grid_propagate(False)
        self.drainage_frame.grid_columnconfigure(0, weight=0)
        self.drainage_frame.grid_columnconfigure(1, weight=1)

        # REQUEST BUTTON
        ctk.CTkButton(mainframe, text="REQUEST", text_color="#FFFFFF", font=("Poppins", 15, "bold"), fg_color="#2CC985", hover_color="#2DAF76").pack(padx=10, pady=10)

        self.setup_installation_checklist()

    def clear_focus(self, event):
        self.focus()

    def setup_installation_checklist(self):
        # Aircon Header
        ctk.CTkLabel(
            self.indoor_frame, text="Aircon:", fg_color="#2CC985",
            font=("Poppins", 15, "bold"), corner_radius=15,
            width=80, height=27
        ).grid(row=0, column=0, padx=(10, 0), pady=(15, 10), sticky="w")

        aircon_add = ctk.CTkButton(
            self.indoor_frame, 
            text="Add Details",
            fg_color=COLOR_GREEN_HOVER,
            hover_color=COLOR_GREEN,
            image=ctk.CTkImage(light_image=Image.open(paths.ICON_ADD_PLUS), size=(18, 18)),
            width=150, 
            height=30, 
            font=("Poppins", 15),
            command=self.open_aircon_add_form,
        )
        aircon_add.grid(row=0, column=1, padx=(10, 0), pady=(15, 10), sticky="w")

        # Frames
        copper_items_frame = self._create_items_frame(self.indoor_frame)
        copper_items_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 5), columnspan=2)

        insulation_items_frame = self._create_items_frame(self.indoor_frame)
        insulation_items_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 5), columnspan=2)

        indoor2_if = self._create_items_frame(self.indoor_frame)
        outdoor_items_frame = self._create_items_frame(self.outdoor_frame)
        supply_items_frame = self._create_items_frame(self.supply_frame)
        drainage_items_frame = self._create_items_frame(self.drainage_frame)

        # Special frames for qty handling

        # COPPER TUBE OUTER
        self.copper_qty_frames = ctk.CTkFrame(copper_items_frame, fg_color="transparent", border_width=0)
        self.copper_qty_frames.pack(fill="x", padx=10, pady=10)
        
        # COPPER TUBE INNER
        copper_tube_special_frame_inner = ctk.CTkFrame(self.copper_qty_frames, border_color="black", border_width=0, fg_color="transparent") # fg_color="lightblue"
        copper_tube_special_frame_inner.pack(fill="x", padx=5, pady=1)

        # INITIAL COPPER TUBE then add as follows
        self._create_special_item_instance(copper_tube_special_frame_inner, "Copper Tube")

        copper_add_button = ctk.CTkButton(
            self.indoor_frame, 
            text=f"Copper Tube", 
            font=("Poppins", 15), 
            image=ctk.CTkImage(light_image=Image.open(paths.ICON_ADD_PLUS)),
            command=lambda: self._create_special_item_instance(copper_tube_special_frame_inner, "Copper Tube")
        )
        copper_add_button.grid(row=1, column=0, padx=(20, 0), pady=10, sticky="w", columnspan=2)
        
        # RUBBER INSULATION OUTER
        self.insulation_qty_frames = ctk.CTkFrame(insulation_items_frame, fg_color="transparent", border_width=0)
        self.insulation_qty_frames.pack(fill="x", padx=10, pady=(0, 10))
        
        # RUBBER INSULATION INNER
        rubber_insulation_special_frame_inner = ctk.CTkFrame(self.insulation_qty_frames, border_color="black", border_width=0, fg_color="transparent") # fg_color="lightblue"
        rubber_insulation_special_frame_inner.pack(fill="x", padx=5, pady=1)

        # INITIAL COPPER TUBE then add as follows
        self._create_special_item_instance(rubber_insulation_special_frame_inner, "Rubber Insulation")

        insulation_add_button = ctk.CTkButton(
            self.indoor_frame, 
            text=f"Rubber Insulation", 
            font=("Poppins", 15), 
            image=ctk.CTkImage(light_image=Image.open(paths.ICON_ADD_PLUS)),
            command=lambda: self._create_special_item_instance(rubber_insulation_special_frame_inner, "Rubber Insulation")
        )
        insulation_add_button.grid(row=1, column=1, padx=(85, 0), pady=10, sticky="w")

        indoor = CustomItemSelector(self.indoor_frame, title="Indoor", border_width=0, fgc="transparent") # fg_color="lightblue"
        indoor.grid(row=4, column=0, padx=(20, 0), pady=(0, 10), sticky="w", columnspan=2)
        indoor.item_builder(self.sample_data)


    # ---------------- HELPER FUNCTIONS ---------------- #

    def gather_request_resources(self):
        pass
    
    def _create_special_item_instance(self, parent, item_name, curr_stock=10):
        frame = ctk.CTkFrame(parent, border_width=1, height=45)
        frame.pack(fill="x", pady=2, padx=1)
        frame.grid_propagate(False)

        frame.grid_columnconfigure(0, weight=0) # entry
        frame.grid_columnconfigure(1, weight=0, uniform="col") # name
        frame.grid_columnconfigure(2, weight=0, uniform="col") # size
        frame.grid_columnconfigure(3, weight=0) # stock l
        frame.grid_columnconfigure(4, weight=0) # stock c
        frame.grid_columnconfigure(5, weight=0, uniform="col") # rmv btn

        # ENTRY
        q = ctk.CTkEntry(frame, width=60, justify="center")
        q.grid(row=0, column=0, padx=(5, 0), pady=(8, 0), sticky="w")
        q.insert(0, 0)

        # ITEM NAME
        ctk.CTkLabel(frame, text=item_name, font=ctk.CTkFont(size=14, weight="bold"), width=120).grid(row=0, column=1, padx=(62, 5), pady=(8, 0), sticky="ew")
        
        size_var = ctk.StringVar(value="size")
        sizes = None

        if item_name == "Copper Tube":
            sizes = indoor_items[0]["sizes"]
        elif item_name == "Rubber Insulation":
            sizes = indoor_items[1]["sizes"]

        # SIZES
        ctk.CTkOptionMenu(frame, values=sizes, width=60, fg_color=COLOR_GREEN, button_color="#3B9162", button_hover_color="#347F56", variable=size_var, anchor="center").grid(row=0, column=2, padx=(10, 0), pady=(8, 0), sticky="ew")

        # STOCK LABEL
        ctk.CTkLabel(frame, text=f"Available stock:", font=ctk.CTkFont(size=14)).grid(row=0, column=3, padx=(20, 0), pady=(8, 0), sticky="e")

        # STOCK COUNT
        ctk.CTkLabel(frame, text=curr_stock, font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=4, padx=(10, 30), pady=(8, 0), sticky="w")

        # REMOVE BTN
        ctk.CTkButton(frame, text="-", text_color="black", font=("Poppins", 10, "bold"), width=50, height=20, command=lambda: frame.pack_forget()).grid(row=0, column=5, padx=(0, 10), pady=(8, 0), sticky="w")

    def _create_basic_frame(self, parent):
        """Reusable container for basic items."""
        pass

    def _create_items_frame(self, parent):
        """Reusable container frame for items."""
        frame = ctk.CTkFrame(parent, fg_color="transparent", border_width=0,border_color="black", corner_radius=10)
        return frame

    # def _create_qty_frame(self, parent, width):
    #     """Reusable sub-frame for quantity inputs."""
    #     return ctk.CTkFrame(parent, fg_color="white", height=36, width=width, border_color="black", border_width=0)

    # def _render_items(self, parent_frame, items, is_indoor):
    #     """Render all items inside a given frame."""
    #     for idx, item in enumerate(items):
    #         if item["name"] in ["Copper Tube", "Rubber Insulation", "Breaker", "Breaker Box"]:
    #             self._render_qty_item(parent_frame, item, idx, is_indoor)
    #         elif item["name"] == "Dust Bag":
    #             self._render_simple_entry_item(parent_frame, item, idx, pady=(5, 10))
    #         else:
    #             self._render_generic_item(parent_frame, item, idx)

    # def _render_qty_item(self, parent, item, idx, is_indoor):
    #     # if item["name"] == "Copper Tube":
    #     #     target_frame, pad, is_insulation = self.copper_qty_frames, 35, False
    #     # elif item["name"] == "Rubber Insulation":
    #     #     target_frame, pad, is_insulation = self.insulation_qty_frames, 15, True
    #     # else:
    #     target_frame, pad, is_insulation = parent, 15, False  # fallback (e.g., Breaker/Box)

    #     qty = ctk.CTkOptionMenu(
    #         parent, font=("Poppins", 15),
    #         values=[str(x) for x in range(0, 5)], width=50,
    #         command=lambda value, row=idx, col=2, sizes=item["sizes"], frame=target_frame, base_pad=pad, is_insulation=is_insulation:
    #             self.check_item_qty(value, row, col, sizes, frame, base_pad, is_insulation),
    #         fg_color=BTN_COLOR_GREEN_HOVER, button_color= BTN_COLOR_GREEN_HOVER, button_hover_color=BTN_COLOR_GREEN
    #     )
    #     qty.grid(row=idx, column=0, padx=(22, 0), pady=20 if item["name"] != "Breaker" else 5)
    #     qty.set("0")

    #     self._create_labels(parent, item, idx)

    # def _render_simple_entry_item(self, parent, item, idx, pady=(2, 2)):
    #     """For Dust Bag or items with only entry + labels."""
    #     qty_entry = ctk.CTkEntry(parent, fg_color=COLOR_GRAY, width=50, justify="center", font=("Poppins", 15))
    #     qty_entry.grid(row=idx, column=0, padx=(22, 0), pady=pady)
    #     self._create_labels(parent, item, idx)

    # def _render_generic_item(self, parent, item, idx):
    #     """For generic items (entry + maybe option menu)."""
    #     qty_entry = ctk.CTkEntry(parent, fg_color=COLOR_GRAY, width=50, justify="center", font=("Poppins", 15))
    #     qty_entry.grid(row=idx, column=0, padx=(22, 0), pady=2)

    #     if isinstance(item["unit"], list):
    #         ctk.CTkOptionMenu(parent, values=item["unit"], width=60, fg_color=BTN_COLOR_GREEN_HOVER, button_color= BTN_COLOR_GREEN_HOVER, button_hover_color=BTN_COLOR_GREEN).grid(row=idx, column=1, padx=(20, 0), pady=2)
    #     else:
    #         ctk.CTkLabel(parent, text=item["unit"], font=("Poppins", 15)).grid(row=idx, column=1, padx=(20, 0), pady=2)

    #     ctk.CTkLabel(parent, text=item["name"], font=("Poppins", 15, "bold")).grid(row=idx, column=2, padx=(40, 0), pady=2, sticky="w")
    #     self.indoor_entries[item["name"]] = qty_entry if parent == self.indoor_frame else None
    #     self.outdoor_entries[item["name"]] = qty_entry if parent == self.outdoor_frame else None

    # def _create_labels(self, parent, item, idx):
    #     """Helper to create consistent labels."""
    #     ctk.CTkLabel(parent, text=item["unit"], font=("Poppins", 15), fg_color="white").grid(row=idx, column=1, padx=(20, 0), pady=2)
    #     ctk.CTkLabel(parent, text=item["name"], font=("Poppins", 15, "bold"), fg_color="white").grid(row=idx, column=2, padx=(40, 10), pady=2, sticky="w")

    # def check_item_qty(self, value, row, start_col, sizes, target_frame, base_pad=15, is_insulation=False):
    #     """
    #     Dynamically create size + qty entry widgets inside target_frame.
    #     """
    #     target_frame.grid(row=row, column=3, sticky="w", padx=(15, 0), pady=(13, 15))
    #     target_frame.grid_propagate(False)

    #     # Clear old widgets
    #     for w in target_frame.winfo_children():
    #         w.grid_forget()

    #     if value == "0":
    #         return

    #     qty_num = int(value) * 2

    #     for i in range(1, qty_num + 1):
    #         if i % 2 != 0:  # size option
    #             size_opt = ctk.CTkOptionMenu(target_frame, values=sizes, width=60, fg_color=BTN_COLOR_GREEN_HOVER)
    #             size_opt.grid(row=0, column=i, padx=(5 if is_insulation else base_pad, 0), pady=2, sticky="w")
    #         else:  # qty entry
    #             qty_entry = ctk.CTkEntry(
    #                 target_frame, fg_color=COLOR_GRAY, width=50,
    #                 justify="center", font=("Poppins", 15)
    #             )
    #             qty_entry.grid(row=0, column=i, padx=(5, 0), pady=2)

    # def setup_headers(self, parent):
    #     items_headers = ctk.CTkFrame(parent, fg_color="transparent", border_width=1, corner_radius=10, width=500, height=30)
    #     items_headers.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky="w")
    #     items_headers.grid_propagate(False)

    #     headers_config = [
    #         {"name": "Qty", "width": 50, "padxx": (22, 0)},
    #         {"name": "UoM", "width": 50, "padxx": (25, 0)},
    #         {"name": "Particulars", "width": 150, "padxx": (25, 0)}
    #     ]
    #     for idx, header in enumerate(headers_config):
    #         label = ctk.CTkLabel(items_headers, text=header["name"], font=("Poppins", 15, "bold"), width=header["width"], fg_color="lightblue", anchor="center")
    #         label.grid(row=0, column=idx, padx=header["padxx"], pady=1)

    # def get_indoor_entries(self):
    #     for k, v in self.indoor_entries.items():
    #         print(v.get())

    # def check_ac_details(self):
    #     for idx, (ent, val) in enumerate(self.ac_entries.items()):
    #         if idx % 2 == 0:
    #             print(f"INDOOR SN: {val.get()}")
    #         else:
    #             print(f"OUTDOOR SN: {val.get()}\n")

    def open_aircon_add_form(self):
        add_form = ctk.CTkToplevel(self, fg_color="white")
        add_form.title("Add AC Details")
        add_form.geometry("600x315+415+200")
        add_form.configure(fg_color="black")
        add_form.overrideredirect(True)
        add_form.grab_set()

        ac_entries = []
        trace_ids = []
        has_existing_data = bool(self.ac_data)

        def update_save_button_text():
            if not add_form.winfo_exists():
                return  # form is gone

            try:
                if not ac_entries:
                    self.save_btn.configure(text="Exit")
                    return
            except Exception:
                return  # probably destroyed widgets

            for idx, (indoor, outdoor) in enumerate(ac_entries):
                if has_existing_data and idx < len(self.ac_data):
                    clear_btn.configure(state="normal", fg_color=COLOR_RED, hover_color=COLOR_RED_HOVER)
                    continue
                if indoor.get().strip() and outdoor.get().strip():
                    clear_btn.configure(state="normal", fg_color=COLOR_RED, hover_color=COLOR_RED_HOVER)
                    self.save_btn.configure(text="Save", fg_color=BTN_COLOR_GREEN, hover_color=BTN_COLOR_GREEN_HOVER)
                    return
            self.save_btn.configure(text="Exit")

        def add_more_entry(indoor_val="", outdoor_val=""):
            if ac_entries:
                last_indoor, last_outdoor = ac_entries[-1]
                if not last_indoor.get().strip() or not last_outdoor.get().strip():
                    Toast(add_form, "⚠ Please fill in both fields first.",
                        x=555, y=410, duration=2100, bg_color=COLOR_RED, font=("Poppins", 16, "bold"))
                    return

            serial_frame = ctk.CTkFrame(mframe, fg_color="lightgreen")
            serial_frame.pack(fill="x", padx=10, pady=8)

            indoorsn = ctk.StringVar(value=indoor_val)
            ctk.CTkLabel(serial_frame, text="Indoor SN:", font=("Poppins", 15)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
            ctk.CTkEntry(serial_frame, width=280, textvariable=indoorsn).grid(row=0, column=1, padx=5, pady=5)

            outdoorsn = ctk.StringVar(value=outdoor_val)
            ctk.CTkLabel(serial_frame, text="Outdoor SN:", font=("Poppins", 15)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
            ctk.CTkEntry(serial_frame, width=280, textvariable=outdoorsn).grid(row=1, column=1, padx=5, pady=5)

            ac_entries.append((indoorsn, outdoorsn))
            trace_ids.append((indoorsn, indoorsn.trace_add("write", lambda *_: update_save_button_text())))
            trace_ids.append((outdoorsn, outdoorsn.trace_add("write", lambda *_: update_save_button_text())))

            update_save_button_text()

        def clear_all_entries():
            # Move focus away from entry
            try:
                if clear_btn.winfo_exists():
                    clear_btn.focus_set()
            except Exception:
                pass

            # Remove traces
            for var, t_id in trace_ids:
                try:
                    var.trace_remove("write", t_id)
                except Exception:
                    pass
            trace_ids.clear()

            # Schedule destruction after Tk finishes current event cycle
            add_form.after(10, _really_clear_entries)

        def _really_clear_entries():
            for widget in mframe.winfo_children():
                widget.destroy()

            ac_entries.clear()
            self.ac_data.clear()
            clear_btn.configure(fg_color=COLOR_GRAY, state="disabled")
            update_save_button_text()

        def at_destroy():
            # 1. Remove variable traces so no callbacks try to use destroyed widgets
            for var, t_id in trace_ids:
                try:
                    var.trace_remove("write", t_id)
                except Exception:
                    pass
            trace_ids.clear()

            # 2. Cancel any scheduled .after calls
            try:
                if hasattr(add_form, "_after_id"):
                    add_form.after_cancel(add_form._after_id)
            except Exception:
                pass

            # 3. Save data if needed
            if self.save_btn.cget("text") == "Save":
                self.ac_data = [
                    (indoor.get(), outdoor.get())
                    for indoor, outdoor in ac_entries
                    if indoor.get().strip() and outdoor.get().strip()
                ]
                Toast(self.winfo_toplevel(), "Saved", x=600, y=360, duration=2100,
                    bg_color=BTN_COLOR_GREEN, font=("Poppins", 16, "bold"))


            # 4. Destroy only if still alive
            if add_form.winfo_exists():
                add_form.destroy()


        # --- UI LAYOUT ---
        outer = ctk.CTkFrame(add_form, fg_color="red")
        outer.pack(fill="both", expand=True, padx=1, pady=1)

        outer.grid_columnconfigure((0, 1), weight=0)
        ctk.CTkButton(outer, text="ADD Serial Numbers", command=add_more_entry).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        clear_btn = ctk.CTkButton(outer, text="CLEAR", command=clear_all_entries, fg_color=COLOR_GRAY, state="disabled")
        clear_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        mframe = HoverScrollableFrame(outer, fg_color="white", width=550)
        mframe.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.save_btn = ctk.CTkButton(outer, text="Exit", command=at_destroy, fg_color=COLOR_RED, hover_color=COLOR_RED_HOVER)
        self.save_btn.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Restore data if any
        for indoor_val, outdoor_val in self.ac_data:
            add_more_entry(indoor_val, outdoor_val)

        update_save_button_text()


class Toast(ctk.CTkToplevel):
    def __init__(self, parent, message, *, x=600, y=325, duration=1800, bg_color="#218838", fg_color="#ffffff", font=("Poppins", 15, "bold"), width=225, height=50):
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
            wraplength=280
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

class CustomItemSelector(ctk.CTkFrame):
    def __init__(self, master=None, fgc="transparent", title="", items_frame_width=500, items_frame_height=300, **kwargs):
        super().__init__(master, fg_color=fgc, **kwargs)
        self.items_frame_width = items_frame_width
        self.items_frame_height = items_frame_height
        self.item_vars = {}  # <-- store item: IntVar mappings here
        
        self.items_frame = ctk.CTkFrame(self, border_width=1, width=self.items_frame_width, height=self.items_frame_height)
        self.items_frame.pack(padx=7, pady=7)
        self.items_frame.pack_propagate(False)

    def enable_layouts(self):
        self.a.configure(bg_color="lightyellow")
        self.b.configure(fg_color="lightyellow")
        self.c.configure(bg_color="lightyellow")
        self.d.configure(bg_color="lightyellow")
        self.e.configure(bg_color="lightyellow")
        self.f.configure(fg_color="lightyellow")
        self.g.configure(fg_color="lightyellow")

    def item_builder(self, item_list):
        self.items_frame.grid_columnconfigure(0, weight=0, uniform="col")  # Entry
        self.items_frame.grid_columnconfigure(1, weight=0, uniform="col")  # Item name
        self.items_frame.grid_columnconfigure(2, weight=0)  # Size (if any)
        self.items_frame.grid_columnconfigure(3, weight=0)  # + button
        self.items_frame.grid_columnconfigure(4, weight=0)  # - button
        self.items_frame.grid_columnconfigure(5, weight=0, uniform="col")  # Stock label
        self.items_frame.grid_columnconfigure(6, weight=0, uniform="col")  # Stock count

        for row_index, (item_name, item_data) in enumerate(item_list.items()):
            stock_var = ctk.IntVar(value=0)
            size_var = ctk.StringVar(value=item_data["sizes"][0] if item_data["sizes"] else "")  

            # save both qty + size
            self.item_vars[item_name] = {"qty": stock_var, "size": size_var}

            def add_stock(var=stock_var):
                var.set(var.get() + 1)

            def remove_stock(var=stock_var):
                if var.get() > 0:
                    var.set(var.get() - 1)

            # column 0: entry (user qty)
            self.a = ctk.CTkEntry(self.items_frame, width=60, justify="center", textvariable=stock_var)
            self.a.grid(row=row_index, column=0, padx=5, pady=5, sticky="w")

            # column 1: item name
            self.b = ctk.CTkLabel(
                self.items_frame, text=item_name, text_color="black",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            self.b.grid(row=row_index, column=1, padx=(0, 5), pady=5, sticky="ew")

            # column 2: size dropdown (if available)
            self.c = ctk.CTkOptionMenu(
                    self.items_frame, values=item_data["sizes"], variable=size_var,
                    fg_color="#F0F0F0", text_color="black"
                )
            if item_data["sizes"]:
                self.c.grid(row=row_index, column=2, padx=5, pady=5, sticky="w")

            # column 3: + button
            self.d = ctk.CTkButton(
                self.items_frame, width=50, height=25, text="+",
                fg_color=COLOR_GREEN, hover_color=COLOR_GREEN_HOVER,
                command=add_stock
            )
            self.d.grid(row=row_index, column=3, padx=(35, 5), pady=5, sticky="w")

            # column 4: - button
            self.e = ctk.CTkButton(
                self.items_frame, width=50, height=25, text="-",
                fg_color=COLOR_RED, hover_color=COLOR_RED_HOVER,
                command=remove_stock
            )
            self.e.grid(row=row_index, column=4, padx=(5, 0), pady=5, sticky="w")

            # column 5: available stock label
            self.f = ctk.CTkLabel(
                self.items_frame, text=f"Available stock:",
                font=ctk.CTkFont(size=14),
            )
            self.f.grid(row=row_index, column=5, padx=(20, 10), pady=5, sticky="e")

            # column 6: available stock count
            self.g = ctk.CTkLabel(
                self.items_frame, text=item_data['stock'],
                font=ctk.CTkFont(size=14, weight="bold"),
            )
            self.g.grid(row=row_index, column=6, padx=(0, 5), pady=5, sticky="w")

            # self.enable_layouts()

    def get_all_values(self):
        results = {}
        for name, data in self.item_vars.items():
            results[name] = {
                "qty": data["qty"].get(),
                "size": data["size"].get()
            }
        return results
