# Import built-in/installed modules
import io
import unicodedata
import customtkinter as ctk
import hashlib
# import logging
from PIL import Image
from datetime import datetime
from rapidfuzz.fuzz import ratio

# Import own-made modules
from core import paths
from core.event_bus import event_bus   # add at top
from core.inventory_backend import retrieve_display_data, delete_data
from ui.notifs import CustomMessageBox
from .new_item import CreateItem
from .edit_item import EditItem

# Constants
ICON_SIZE = (16, 16)


class InventoryAdmin(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#FFFFFF")

        # logging.basicConfig(level=logging.INFO)
        # self.log = logging.getLogger(__name__)

        # CONSTANTS
        self.LOW_STOCK_MULTIPLIER = 2

        # OTHER VARIABLES
        self.toplevel_window = None
        self.product_frames = []          # list of tuples: (product_data_list, frame)
        self.products = {}                # dict by product_id -> product_data_list
        self.frame_cache = {}             # dict by product_id -> frame
        self.image_cache = {}
        self.data_cache = None
        self.toast_label = None
        self.last_added_product_id = None
        self.no_result_label = None
        self.delete_msgbox = None
        self.scrolling = False            # << unified scrolling flag
        self._after_jobs = []  # keep track of after IDs
        # self._click_bind_id = None

        self.column_configs = [
            {"text": "Photo", "width": 50, "padx": (22, 30)},
            {"text": "Code", "width": 60, "padx": (0, 15), "textlength": 100},
            {"text": "Name", "width": 115, "padx": (0, 15), "textlength": 100},
            {"text": "Category", "width": 95, "padx": (0, 15), "textlength": 100},
            {"text": "Price", "width": 85, "padx": (0, 15), "textlength": 55},
            {"text": "Type", "width": 60, "padx": (0, 15), "textlength": 50},
            {"text": "Brand", "width": 80, "padx": (0, 15), "textlength": 50},
            {"text": "Unit", "width": 50, "padx": (0, 10), "textlength": 50},
            {"text": "Stock", "width": 60, "padx": (0, 5), "textlength": 100},
            {"text": "Min", "width": 60, "padx": (0, 5), "textlength": 100},
            {"text": "Stock Status", "width": 120, "padx": (0, 10)},
            {"text": "Actions", "width": 125, "padx": (0, 15), "textlength": 100},
        ]

        self.empty_image = self.load_image(paths.IMAGE_EMPTY, (200, 200))

        self.fallback_image = ctk.CTkImage(
            light_image=Image.open(paths.IMAGE_PLACEHOLDER).resize((50, 50)),
            size=(50, 50)
        )

        self.icon_in_stock = ctk.CTkImage(Image.open(paths.EMOJI_IN_STOCK), size=ICON_SIZE)
        self.icon_low_stock = ctk.CTkImage(Image.open(paths.EMOJI_LOW_STOCK), size=ICON_SIZE)
        self.icon_out_stock = ctk.CTkImage(Image.open(paths.EMOJI_OUT_STOCK), size=ICON_SIZE)

        self.title_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.title_frame.pack(fill='x')

        self.status_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.status_frame.pack(fill='x', pady=(0, 12))

        self.search_frame = ctk.CTkFrame(self, fg_color="#e8e8e8", corner_radius=5)
        self.search_frame.pack(fill='x', padx=(16, 19), pady=(10, 8))

        self.content_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0)
        self.content_frame.pack(fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="#298753", corner_radius=10)
        self.header_frame.pack(fill="x", padx=(16, 20))

        self.scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="#FFFFFF", height=276, width=1143)
        self.scrollable_frame.pack(padx=(5, 5), pady=(0, 5), expand=True, fill="both")

        # (MouseBindings)
        # bind to the scrollable frame's parent canvas mouse wheel, but set the local scrolling flag
        canvas = self.scrollable_frame._parent_canvas  # fallback if needed
        canvas.bind("<MouseWheel>", self.on_mouse_scroll)

        # Keyboard Shortcuts (KeyboardBindings) - fixed syntax
        # self.create_keyboard_shortcut(self.winfo_toplevel(), "<Control-r>", lambda event: self.refresh_inventory(force_refresh=True))
        # self.create_keyboard_shortcut(self.winfo_toplevel(), "<Control-t>", lambda event: self.scroll_to_top())
        # self.create_keyboard_shortcut(self.winfo_toplevel(), "<Control-b>", lambda event: self.scroll_to_bottom())
        # self.create_keyboard_shortcut(self.winfo_toplevel(), "<Control-s>", lambda event: self.search_pane_focus())
        # self.create_keyboard_shortcut(self.winfo_toplevel(), "<Control-BackSpace>", lambda event: self.search_pane.delete(0, "end"))
        # self.create_keyboard_shortcut(self.winfo_toplevel(), "<Escape>", lambda event: self.unfocus_search())

        self.setup_title()

        self._click_bind_id = None
        self.bind_shortcuts()
        self.setup_searchbar()

        self.scroll_controls()
        self.setup_headers()

        # ✅ Initialize counters
        self.overall_item_count = 0
        self.low_stock_counter = 0
        self.out_stock_counter = 0

        self.setup_status_bar()
        self.refresh_inventory()

        # Optional debug
        print("\n[DEBUG] InventoryAdmin UI initialized successfully.\n")

        self.shortcut_bar = ctk.CTkLabel(
            self, 
            text="⎇ Shortcuts: Ctrl+R Refresh | Ctrl+S Search | Esc Cancel Search | Ctrl+? View All Shortcuts", 
            font=("Poppins", 13), 
            text_color="gray20",
            anchor="center"
        )
        self.shortcut_bar.pack(side="bottom", pady=(5, 5))

    def after_safe(self, delay, callback):
        """Like .after(), but remembers the job so it can be cancelled on destroy."""
        job_id = self.after(delay, callback)
        self._after_jobs.append(job_id)
        return job_id

    def cleanup(self):
        """Cancel all scheduled after() jobs before window closes."""
        for job in getattr(self, "_after_jobs", []):
            try:
                self.after_cancel(job)
            except Exception:
                pass
        self._after_jobs.clear()

        # Unbind global click if bound
        if self._click_bind_id:
            self.winfo_toplevel().unbind("<Button-1>", self._click_bind_id)
            self._click_bind_id = None

        master = self.winfo_toplevel()
        for seq in ("<Control-r>", "<Control-t>", "<Control-b>", "<Control-s>", "<Control-BackSpace>", "<Escape>", "<Control-n>", "<Control-question>", "<Control-slash>"):
            master.unbind(seq)

    def setup_title(self):
        today = datetime.today().strftime("As of %B %d, %Y").upper()

        _3MI_icon = ctk.CTkLabel(
            self.title_frame,
            text="",
            bg_color="transparent",
            image=ctk.CTkImage(light_image=Image.open(paths.IMAGE_APP), size=(250, 100)),
        )
        _3MI_icon.pack(side='left', anchor='n', padx=(35, 0), pady=(15, 0))

        inv_label = ctk.CTkLabel(
            self.title_frame,
            text=today,
            # text_color="#298753",
            text_color="#000000",
            font=('Poppins', 14, "bold"),
            bg_color="transparent",
            anchor="n",
        )
        inv_label.pack(side='right', anchor='s', padx=(0, 25), pady=(0, 5))

    def prepare_for_display(self):
        # hide counters
        self.total_item_count.grid_remove()
        self.low_stock_count.grid_remove()
        self.out_of_stock_count.grid_remove()

    def show_counters(self):
        # show them again after the page is ready
        self.total_item_count.grid()
        self.low_stock_count.grid()
        self.out_of_stock_count.grid()

    def setup_status_bar(self):
        ctk.CTkLabel(self.status_frame, text='View Inventory', font=('Poppins', 27, 'bold'), fg_color="transparent", text_color="#298753", anchor="s").grid(row=0, column=0, padx=(20, 65), ipady=15)

        total_item_status_frame = ctk.CTkFrame(self.status_frame, fg_color="#298753", width=250, height=70)
        total_item_status_frame.grid(row=0, column=1, padx=15)
        total_item_status_frame.grid_propagate(False)

        total_item_icon = ctk.CTkLabel(
            total_item_status_frame,
            text='',
            image=ctk.CTkImage(light_image=Image.open(paths.ICON_TOTAL), size=(38, 38)),
        )
        total_item_icon.grid(row=0, column=0, rowspan=2, pady=(0, 12), padx=(18, 0))

        total_item_label = ctk.CTkLabel(
            total_item_status_frame,
            text='Total Items',
            text_color="#FFFFFF",
            font=("Poppins", 17, "bold"),
            fg_color="#298753",
        )
        total_item_label.grid(row=0, column=1, padx=(10, 0), pady=(6, 0))

        self.total_item_count = ctk.CTkLabel(
            total_item_status_frame,
            text=self.overall_item_count,
            text_color="#ffffff",
            font=("Poppins", 23, "bold"),
            fg_color="#298753",
        )
        self.total_item_count.grid(row=1, column=1, padx=(11, 0), sticky="w")

        low_stock_alerts_frame = ctk.CTkFrame(self.status_frame, fg_color="#298753", width=300, height=70)
        low_stock_alerts_frame.grid(row=0, column=2, padx=10)
        low_stock_alerts_frame.grid_propagate(False)

        low_stock_alerts_icon = ctk.CTkLabel(
            low_stock_alerts_frame,
            text='',
            image=ctk.CTkImage(light_image=Image.open(paths.ICON_STOCK_ALERTS), size=(41, 41))
        )
        low_stock_alerts_icon.grid(row=0, column=0, rowspan=2, pady=(0, 18), padx=(15, 0))

        low_stock_alerts_label = ctk.CTkLabel(
            low_stock_alerts_frame,
            text=' Low In Stock',
            text_color="#FFFFFF",
            font=("Poppins", 17, "bold"),
        )
        low_stock_alerts_label.grid(row=0, column=1, padx=(10, 0), pady=(7, 0), sticky="w")

        self.low_stock_alerts_label_frame = ctk.CTkFrame(low_stock_alerts_frame, fg_color="transparent", width=20, height=15, corner_radius=0)
        self.low_stock_alerts_label_frame.grid(row=1, column=1, padx=(15, 0), pady=(0, 5), sticky="w")

        self.low_stock_count = ctk.CTkLabel(self.low_stock_alerts_label_frame, text=self.low_stock_counter, text_color="#ffffff", font=("Poppins", 23, "bold"), fg_color="#298753")
        self.low_stock_count.grid(row=0, column=0, pady=(0, 5))

        out_of_stock_frame = ctk.CTkFrame(self.status_frame, fg_color="#298753", width=250, height=70)
        out_of_stock_frame.grid(row=0, column=3, padx=15)
        out_of_stock_frame.grid_propagate(False)

        out_of_stock_icon = ctk.CTkLabel(
            out_of_stock_frame,
            text='',
            image=ctk.CTkImage(light_image=Image.open(paths.ICON_OUT_STOCK), size=(42, 42)),
        )
        out_of_stock_icon.grid(row=0, column=0, rowspan=2, pady=(0, 9), padx=(18, 0))

        out_of_stock_label = ctk.CTkLabel(
            out_of_stock_frame,
            text='Out Of Stock',
            text_color="#FFFFFF",
            font=("Poppins", 17, "bold"),
            fg_color="#298753",
        )
        out_of_stock_label.grid(row=0, column=1, padx=(13, 0), pady=(6, 0))

        self.out_of_stock_count = ctk.CTkLabel(
            out_of_stock_frame,
            text=f"{self.out_stock_counter}",
            text_color="#ffffff",
            font=("Poppins", 23, "bold"),
            fg_color="#298753",
            anchor="n"
        )
        self.out_of_stock_count.grid(row=1, column=1, padx=(16, 0), sticky="w")

    def open_shortcut_help(self):
        """Popup window showing all shortcuts for this page."""
        help_win = ctk.CTkToplevel(self)
        help_win.title("Keyboard Shortcuts")
        help_win.iconbitmap(paths.ICON_APP)
        help_win.geometry("460x430+190+222")
        help_win.resizable(False, False)
        help_win.grab_set()

        ctk.CTkLabel(
            help_win, 
            text="Keyboard Shortcuts", 
            font=("Poppins", 18, "bold"), 
            text_color="#298753"
        ).pack(pady=(15, 10))

        shortcut_frame = ctk.CTkFrame(help_win, fg_color="white")
        shortcut_frame.pack(fill="both", expand=True)

        # Common shortcuts
        shortcuts = [
            ("Ctrl+R", "Refresh page"),
            ("Ctrl+S", "Focus search bar"),
            ("Ctrl+Backspace", "Clear search bar"),
            ("Ctrl+T", "Scroll to top"),
            ("Ctrl+B", "Scroll to bottom"),
            ("Escape", "Unfocus search bar"),
        ]

        # Add page-specific ones
        shortcuts += [
            ("Ctrl+N", "Add new product"),
            ("Ctrl+E", "Edit selected product"),
            ("Delete", "Delete selected product"),
            ("Ctrl+U", "Update stock of selected product"),
        ]

        # Nicely format
        # for combo, desc in shortcuts:
        for i, (combo, desc) in enumerate(shortcuts):
            ctk.CTkLabel(shortcut_frame, text=combo, font=("Poppins", 14, "bold"), anchor="w").grid(row=i, column=0, sticky="w", padx=25, pady=4)
            ctk.CTkLabel(shortcut_frame, text=desc, font=("Poppins", 15, "italic"), anchor="w").grid(row=i, column=1, sticky="w", padx=15, pady=4)

            # ctk.CTkLabel(
            #     help_win, 
            #     text=f"{combo:<15} {desc}", 
            #     font=("Poppins", 14), 
            #     anchor="w", 
            #     justify="left"
            # ).pack(anchor="w", padx=25, pady=4)

    def create_keyboard_shortcut(self, master, shortcut, fn):
        master.bind(shortcut, fn)

    def search_pane_focus(self, event=None):
        self.search_pane.focus()
        self.search_pane.configure(border_color="#298753")

    def count_stock_status(self):
        low_stock_count = 0
        out_of_stock_count = 0

        for product_data, _ in self.product_frames:
            stock_status = product_data[11]  # Status is at index 11

            if stock_status == "Low Stock":
                low_stock_count += 1
            elif stock_status == "Out of Stock":
                out_of_stock_count += 1

        return low_stock_count, out_of_stock_count

    def on_mouse_scroll(self, event):
        ''' Scroll only if scrollable frame has overflow content '''
        # Use local scrolling flag consistently
        self.scrolling = True
        self.after_safe(300, lambda: setattr(self, "scrolling", False))

        canvas = self.scrollable_frame._parent_canvas
        scroll_region = canvas.bbox("all")
        if scroll_region is None:
            return

        content_height = scroll_region[3] - scroll_region[1]
        canvas_height = canvas.winfo_height()

        if content_height > canvas_height:
            scroll_speed = 9
            canvas.yview_scroll(-1 * (event.delta // 120) * scroll_speed, "units")

    def setup_headers(self):
        ''' This function setups the headers for the inventory product table. '''
        for col_index, col in enumerate(self.column_configs):
            if col_index == 10:
                header_label = ctk.CTkLabel(
                self.header_frame,
                text=col["text"],
                font=("Arial", 14, "bold"),
                text_color="#ffffff",
                width=col["width"],
                anchor="center",
                wraplength=60,
                )
                header_label.grid(row=0, column=col_index, padx=col["padx"], pady=8)
                continue

            header_label = ctk.CTkLabel(
                self.header_frame,
                text=col["text"],
                font=("Arial", 14, "bold"),
                text_color="#ffffff",
                width=col["width"],
                anchor="center",
                wraplength=90,
            )
            header_label.grid(row=0, column=col_index, padx=col["padx"], pady=8)
            self.header_frame.grid_columnconfigure(col_index, minsize=col["width"])

    def delayed_filter(self, *args):
        if hasattr(self, "_search_after_id"):
            self.after_cancel(self._search_after_id)
        self._search_after_id = self.after_safe(250, self.filter_and_sort_products)

    def unfocus_search(self, event=None):
        if self.search_pane and self.search_pane.winfo_exists():
            if event:
                if self.search_pane.winfo_rootx() <= event.x_root <= self.search_pane.winfo_rootx() + self.search_pane.winfo_width() and \
                self.search_pane.winfo_rooty() <= event.y_root <= self.search_pane.winfo_rooty() + self.search_pane.winfo_height():
                    self.search_pane.configure(border_color='#298753')
                    return

            # Unfocus the search entry 
            self.search_pane.focus_set()
            self.focus_force()
            self.search_pane.configure(border_color='#979da2')

    def setup_searchbar(self):
        ''' This setups the searchbar for the fast retrieval of a specific item on the table. '''

        self.search_pane = ctk.CTkEntry(
            self.search_frame,
            fg_color='#ffffff',
            placeholder_text='Search code, name, category, type, or brand',
            placeholder_text_color='gray',
            width=350,
            height=30,
            font=('Poppins', 14),
            text_color="black")
        self.search_pane.pack(pady=10, padx=10, anchor="w", side="left")
        self.search_pane.bind('<KeyRelease>', self.delayed_filter)

        self.bind_global_click()
        # self._click_bind_id = self.winfo_toplevel().bind("<Button-1>", self.unfocus_search, add="+")

        self.sort_by_var = ctk.StringVar(value="Sort by")
        sort_by_values = ["Name", "Category", "Price", "Type", "Unit", "Current stock"]
        sort_by_menu = ctk.CTkOptionMenu(
            master=self.search_frame,
            values=sort_by_values,
            variable=self.sort_by_var,
            height=33,
            width=145,
            font=('Poppins', 14),
            text_color="black",
            button_color="#298753",
            button_hover_color="#4BAC76",
            fg_color="white",
            dropdown_fg_color="#298753",
            dropdown_text_color="#ffffff",
            dropdown_font=('Poppins', 13),
            dropdown_hover_color="#4BAC76",
            command=lambda _: self.filter_and_sort_products()
        )
        sort_by_menu.pack(pady=10, padx=(0, 10), side="left")

        self.status_var = ctk.StringVar(value="Status")
        status_values = ["In Stock", "Low Stock", "Out of Stock"]
        status_sort_menu = ctk.CTkOptionMenu(
            master=self.search_frame,
            values=status_values,
            variable=self.status_var,
            height=33,
            width=135,
            font=('Poppins', 14),
            text_color="black",
            button_color="#298753",
            button_hover_color="#4BAC76",
            fg_color="white",
            dropdown_fg_color="#298753",
            dropdown_text_color="#ffffff",
            dropdown_font=('Poppins', 13),
            dropdown_hover_color="#4BAC76",
            command=lambda _: self.filter_and_sort_products()
        )
        status_sort_menu.pack(pady=10, padx=(0, 10), side="left")

        self.new_item_btn = ctk.CTkButton(
            self.search_frame,
            width=120,
            fg_color="#298753",
            hover_color="#4BAC76",
            text_color="#ffffff",
            text="New Item",
            font=("Poppins", 14, "bold"),
            cursor="hand2",
            image=ctk.CTkImage(light_image=Image.open(paths.ICON_ADD_PLUS), size=(18, 18)),
            compound="left",
            border_spacing=4,
            anchor="center",
            command=self.open_create_item
        )
        self.new_item_btn.pack(pady=10, padx=(0, 10), side="right")

        self.sort_order_var = ctk.StringVar(value="ASCEND ↑")
        self.sort_order_btn = ctk.CTkButton(
            self.search_frame,
            width=90,
            height=33,
            textvariable=self.sort_order_var,
            font=('Poppins', 14),
            fg_color="gray",
            text_color="#ffffff",
            corner_radius=6,
            command=self.toggle_sort_order,
            state="disabled",
        )
        self.sort_order_btn.pack(pady=10, padx=(0, 10), side="left")

        self.reset_searchbar_button = ctk.CTkButton(
            self.search_frame,
            text="Reset",
            width=55,
            height=33,
            font=('Poppins', 14),
            fg_color="gray",
            text_color="#ffffff",
            corner_radius=6,
            command=self.reset_button_on_searchbar,
            state="disabled",
        )
        self.reset_searchbar_button.pack(pady=10, padx=(0, 10), side="left")

    def bind_global_click(self):
        """Bind outside click to unfocus search entry."""
        if self._click_bind_id:
            self.winfo_toplevel().unbind("<Button-1>", self._click_bind_id)
        self._click_bind_id = self.winfo_toplevel().bind("<Button-1>", self.unfocus_search, add="+")

    def on_show(self):
        """Called when page is navigated to → rebind events and refresh inventory."""
        self.bind_global_click()
        self.bind_shortcuts()
        self.refresh_inventory(force_refresh=True, messages="✅ Refreshed", durations=1500)

    def bind_shortcuts(self):
        master = self.winfo_toplevel()
        self.create_keyboard_shortcut(master, "<Control-r>", lambda event: self.refresh_inventory(force_refresh=True))
        self.create_keyboard_shortcut(master, "<Control-t>", lambda event: self.scroll_to_top())
        self.create_keyboard_shortcut(master, "<Control-b>", lambda event: self.scroll_to_bottom())
        self.create_keyboard_shortcut(master, "<Control-s>", lambda event: self.search_pane_focus())
        self.create_keyboard_shortcut(master, "<Control-BackSpace>", lambda event: self.search_pane.delete(0, "end"))
        self.create_keyboard_shortcut(master, "<Escape>", lambda event: self.unfocus_search())
        self.create_keyboard_shortcut(master, "<Control-n>", lambda event: self.open_create_item())
        self.create_keyboard_shortcut(master, "<Control-question>", lambda e: self.open_shortcut_help())
        self.create_keyboard_shortcut(master, "<Control-slash>", lambda e: self.open_shortcut_help())  

    def reset_button_on_searchbar(self):
        self.search_pane.delete(0, ctk.END)
        self.sort_by_var.set("Sort by")
        self.status_var.set("Status")
        self.sort_order_var.set("ASCEND ↑")
        self.filter_and_sort_products()

    def normalize(self, text):
        """Removes accents, lowercases, and trims whitespace."""
        text = unicodedata.normalize('NFKD', text)
        return ''.join(c for c in text if not unicodedata.combining(c)).strip().lower()

    def is_fuzzy_match(self, query, target):
        """Avoid fuzzy match on short strings unless very close."""
        if len(query) < 4:
            return False  # Prevent false positives on short strings
        similarity = ratio(query, target)
        if len(query) < 6:
            return similarity >= 85  # Require high match for medium strings
        return similarity >= 70  # More relaxed threshold for longer queries

    def clear_no_result_ui(self):
        self._safe_destroy(self.no_result_label)
        self._safe_destroy(getattr(self, "caption_label", None))
        self.no_result_label = None
        self.caption_label = None

    def activate_reset_button(self):
        self.reset_searchbar_button.configure(fg_color="#E63946", hover_color="#C92A3F", state="normal")

    def filter_and_sort_products(self):
        query = self.normalize(self.search_pane.get())
        sort_by = self.sort_by_var.get()
        status = self.status_var.get()
        order = self.sort_order_var.get() == "DESCEND ↓"

        # Prevent heavy filtering while scrolling
        if getattr(self, "scrolling", False):
            return

        # Sorting, Status, Descend, Ascend, Reset Switching
        if sort_by != "Sort by":
            self.sort_order_btn.configure(fg_color="#298753", hover_color="#4BAC76", state="normal")
            self.activate_reset_button()
        elif status != "Status":
            self.activate_reset_button()
        elif query != "":
            self.activate_reset_button()
        else:
            self.sort_order_btn.configure(state="disabled", fg_color="gray")
            self.reset_searchbar_button.configure(state="disabled", fg_color="gray")

        # Clear "no result" display if it exists
        self.clear_no_result_ui()

        sort_index = {
            "Name": 3,
            "Category": 4,
            "Price": 5,
            "Type": 6,
            "Unit": 8,
            "Current stock": 9,
        }.get(sort_by, None)

        # product_frames is [(product_data, frame), ...]
        filtered = [(p[0], p) for p, _ in self.product_frames]  # (product_id, product_data)

        if query:
            self.scroll_to_top()
            # ABLE TO SEARCH: code, name, category, type, brand
            searchable_fields = [2, 3, 4, 6, 7]
            filtered = []

            for pid, p in [(p[0], p) for p, _ in self.product_frames]:
                for i in searchable_fields:
                    field_value = self.normalize(str(p[i]))

                    # Strong matches
                    if query == field_value:
                        filtered.append((pid, p))
                        break
                    elif field_value.startswith(query):
                        filtered.append((pid, p))
                        break
                    elif query in field_value:
                        filtered.append((pid, p))
                        break
                    elif self.is_fuzzy_match(query, field_value):
                        filtered.append((pid, p))
                        break

            if filtered:
                self.show_toast(f"{len(filtered)} matching item(s) found", duration=1500, fgcolor="#298753")

            # Handle no results
            if not filtered:
                for _, frame in self.product_frames:
                    frame.pack_forget()

                self.no_result_label = ctk.CTkLabel(self.scrollable_frame, text="", image=self.empty_image)

                self.caption_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="No matching item(s) found.",
                    font=("Poppins", 15)
                )
                self.no_result_label.pack(pady=(45, 20))
                self.caption_label.pack(pady=10)
                return

        # Continue with filter by status and sorting...
        if status != "Status":
            self.scroll_to_top()
            filtered = [(pid, p) for pid, p in filtered if p[11] == status]

        if sort_index is not None:
            self.scroll_to_top()

            def sort_key(item):
                value = item[1][sort_index]
                if isinstance(value, str):
                    value = value.replace(",", "")
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return value.lower() if isinstance(value, str) else value

            # filtered.sort(key=sort_key, reverse=order)
            filtered.sort(key=lambda item: self._parse_value(item[1][sort_index]), reverse=order)


        # Hide all product frames
        self.clear_product_frames()

        # Show only filtered ones
        for pid, product in filtered:
            frame = self.frame_cache.get(str(pid))
            if frame:
                frame.pack(fill="x", padx=(5, 0), pady=5)
            else:
                print(f"Warning: Frame for product ID {pid} not found in cache.")

    def clear_product_frames(self):
        for _, frame in self.product_frames:
            try:
                frame.pack_forget()
            except Exception:
                pass

    def toggle_sort_order(self):
        current = self.sort_order_var.get()
        new_value = "DESCEND ↓" if current == "ASCEND ↑" else "ASCEND ↑"
        self.sort_order_var.set(new_value)
        self.filter_and_sort_products()

    def _safe_destroy(self, widget):
        """Destroy a CTk widget if it still exists."""
        if widget and widget.winfo_exists():
            widget.destroy()

    def show_toast(self, message, duration=2000, fgcolor="#444", relxx=0.5, relyy=0.9):
        self._safe_destroy(self.toast_label)
        self.toast_label = ctk.CTkLabel(self, text=message, fg_color=fgcolor, bg_color="#e0e0e0", font=("Roboto", 14), text_color="white", corner_radius=5, padx=10
        )
        self.toast_label.place(relx=relxx, rely=relyy, anchor="s", y=-5)
        self.after_safe(duration, lambda: self._safe_destroy(self.toast_label))

    def diff_inventory(self, old, new):
        old_dict = {p[0]: p for p in old}
        new_dict = {p[0]: p for p in new}

        added = [p for pid, p in new_dict.items() if pid not in old_dict]

        removed = [pid for pid in old_dict if pid not in new_dict]

        updated = [p for pid, p in new_dict.items() if pid in old_dict and p != old_dict[pid]]

        return added, removed, updated

    def convert_blob_to_image(self, blob_data, product_id):
        try:
            if not blob_data:
                raise ValueError("No image data provided.")

            blob_hash = self.get_blob_hash(blob_data)
            cache_key = f"{product_id}_{blob_hash}"

            if cache_key in self.image_cache:
                return self.image_cache[cache_key]

            image = Image.open(io.BytesIO(blob_data)).convert("RGBA")
            bg = Image.new("RGBA", image.size, (255, 255, 255, 0))
            diff = Image.alpha_composite(bg, image)
            bbox = diff.getbbox()
            if bbox:
                image = image.crop(bbox)
            image = image.resize((50, 50), Image.LANCZOS)

            final_img = ctk.CTkImage(light_image=image, dark_image=image, size=(50, 50))
            self.image_cache[cache_key] = final_img
            return final_img

        except Exception as e:
            print(f"[ERROR] Failed to convert image blob: {e}")

            # Handle fallback and ensure it's cached
            fallback_key = f"{product_id}_fallback"
            if fallback_key in self.image_cache:
                return self.image_cache[fallback_key]

            self.image_cache[fallback_key] = self.fallback_image
            return self.fallback_image

    def refresh_inventory(self, force_refresh=False, messages="✅ Refreshed", durations=1500, fgcolors="#298753", relyys=0.688):
        """
        Refresh inventory from backend. If force_refresh=True, always fetch fresh data.
        """
        final_data = {}

        if self.data_cache is None or force_refresh:
            db_data = retrieve_display_data()
            # update cache only when we've actually fetched
            self.data_cache = db_data
        else:
            db_data = self.data_cache

        for stock in db_data:
            stock = list(stock)
            product_id = str(stock[0])

            try:
                image_blob = stock[1]
                stock[1] = self.convert_blob_to_image(image_blob, product_id)
            except Exception:
                pass

            # normalize numeric fields if they come as strings
            stock[-2] = int(stock[-2]) if isinstance(stock[-2], str) and stock[-2].isdigit() else stock[-2]
            stock[-1] = int(stock[-1]) if isinstance(stock[-1], str) and stock[-1].isdigit() else stock[-1]
            q, t = stock[-2], stock[-1]
            low_stock = t * self.LOW_STOCK_MULTIPLIER

            stock_status = (
                "Out of Stock" if q <= t
                else "Low Stock" if q <= low_stock
                else "In Stock"
            )
            stock.append(stock_status)

            try:
                final_data[product_id] = stock
                self.overall_item_count = len(final_data)
                self.total_item_count.configure(text=str(self.overall_item_count))
            except Exception:
                pass

        # self.log.info(" Total products loaded: %s", len(final_data))

        old_data = list(self.products.values())
        new_data = list(final_data.values())

        added, removed, updated = self.diff_inventory(old_data, new_data)

        # Remove deleted frames
        self._remove_deleted(removed)

        # Update changed items
        self._updated_products(updated)

        # Add new items
        self._add_products(added)

        # Rebuild product_frames list
        self.product_frames = [(p, self.frame_cache[str(p[0])]) for p in self.products.values() if str(p[0]) in self.frame_cache]

        # Recalculate stock counters
        self.low_stock_counter, self.out_stock_counter = self.count_stock_status()
        self.low_stock_count.configure(text=self.low_stock_counter)
        self.out_of_stock_count.configure(text=self.out_stock_counter)

        if self.last_added_product_id:
            print(f"Highlighting product: {self.last_added_product_id}")
            self.highlight_and_scroll_to(str(self.last_added_product_id))
            self.last_added_product_id = None

        self.filter_and_sort_products()
        self.show_toast(message=messages, duration=durations, fgcolor=fgcolors, relyy=relyys)

    def _remove_deleted(self, removed_ids):
        for pid in removed_ids:
            pid = str(pid)
            if pid in self.frame_cache:
                try:
                    self.frame_cache[pid].destroy()
                except Exception:
                    pass
                del self.frame_cache[pid]
            self.products.pop(pid, None)

    def _updated_products(self, updated):
        for product in updated:
            pid = str(product[0])
            self.products[pid] = product

            if pid in self.frame_cache:
                self._safe_destroy(self.frame_cache[pid])
                del self.frame_cache[pid]

            frame = self.create_product_frame(product)
            self.frame_cache[pid] = frame

    def _add_products(self, added):
        for product in added:
            pid = str(product[0])
            self.products[pid] = product
            frame = self.create_product_frame(product)
            self.frame_cache[pid] = frame

    def create_product_frame(self, product):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color="#e0e0e0")

        for col_index, (value, col) in enumerate(zip(product[1:], self.column_configs)):
            if col_index == 0:
                image = product[1]
                if not isinstance(image, ctk.CTkImage):
                    print(f"[WARN] Invalid image at index 0: {image}")
                    continue
                label = ctk.CTkLabel(
                    frame,
                    text="",
                    image=image,
                    width=col["width"],
                    anchor="center",
                )
            elif col_index == 10:
                stock_status = value
                stock_icon = (
                    self.icon_out_stock if stock_status == "Out of Stock"
                    else self.icon_low_stock if stock_status == "Low Stock"
                    else self.icon_in_stock
                )
                label = ctk.CTkLabel(
                    frame,
                    text=stock_status,
                    image=stock_icon,
                    compound="left",
                    text_color="black",
                    font=('Segoe UI Emoji', 14),
                    width=col["width"],
                    anchor="center",
                    padx=5,
                )
            elif col_index == 5:
                label = ctk.CTkLabel(
                    frame,
                    text=value,
                    text_color="black",
                    font=('Segoe UI Emoji', 14),
                    width=col["width"],
                    anchor="center",
                    wraplength=col["textlength"],
                )
            else:
                label = ctk.CTkLabel(
                    frame,
                    text=value,
                    text_color="black",
                    font=('Segoe UI Emoji', 14),
                    width=col["width"],
                    anchor="center",
                    wraplength=col.get("textlength", 100)
                )
            label.grid(row=0, column=col_index, padx=col["padx"], pady=15)

        button_frame = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=0, height=45, width=128)
        button_frame.grid(row=0, column=11)
        button_frame.grid_propagate(False)

        ctk.CTkButton(
            button_frame,
            text="EDIT",
            font=("Poppins", 13, "bold"),
            text_color="#FFFFFF",
            width=50,
            height=25,
            cursor="hand2",
            command=lambda i=product[0]: self.edit_window(str(i)),
        ).grid(row=0, column=0, sticky="nsew", pady=(8, 0), padx=(6, 7))

        ctk.CTkButton(
            button_frame,
            text="DELETE",
            font=("Poppins", 13, "bold"),
            text_color="#FFFFFF",
            width=40,
            height=25,
            cursor="hand2",
            fg_color="#E63946",
            hover_color="#C92A3F",
            command=lambda i=product[0]: self.ask_delete(str(i)),
        ).grid(row=0, column=1, sticky="nsew", pady=(8, 0))

        frame.pack()
        self.update_idletasks()
        return frame

    def highlight_and_scroll_to(self, product_id):
        frame = self.frame_cache.get(product_id)
        if not frame:
            # self.log.warning("Frame not found for product ID %s", product_id)
            print("Frame not found for product ID {}".format(product_id))
            return

        def scroll_to_frame():
            self.update_idletasks()
            frame_y = frame.winfo_y()
            scroll_region_height = max(1, self.scrollable_frame.winfo_height())
            self.scrollable_frame._parent_canvas.yview_moveto(frame_y / scroll_region_height)

        # Delay scrolling to ensure layout is updated
        self.after_safe(50, scroll_to_frame)

        def pulse(count=0):
            if count >= 8:
                frame.configure(border_width=0)
                return
            color = "#3B8ED0" if count % 2 == 0 else frame.cget("fg_color")
            frame.configure(border_width=2, border_color=color)
            self.after_safe(260, lambda: pulse(count + 1))

        pulse()

    def scroll_controls(self):
        button_frame = ctk.CTkFrame(self.search_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=(0, 10))

        to_top_btn = ctk.CTkButton(button_frame, text="↑ Top", width=60, command=self.scroll_to_top)
        to_bottom_btn = ctk.CTkButton(button_frame, text="↓ Bottom", width=80, command=self.scroll_to_bottom)

        to_top_btn.pack(side="left", padx=(5, 3))
        to_bottom_btn.pack(side="left", padx=(3, 5))

    def scroll_to_top(self):
        self.after_idle(lambda: self.scrollable_frame._parent_canvas.yview_moveto(0))

    def scroll_to_bottom(self):
        self.after_idle(lambda: self.scrollable_frame._parent_canvas.yview_moveto(1))

    def ask_delete(self, item_id):
        if self.delete_msgbox and self.delete_msgbox.winfo_exists():
            self.delete_msgbox.focus_force()
            return

        def confirm_delete():
            # self.log.debug(f"Deleting item_id: {item_id}")
            print(f"Deleting item_id: {item_id}")
            delete_data(item_id)
            self._safe_destroy(self.delete_msgbox)
            self.refresh_inventory(force_refresh=True, messages="✅ Deleted", durations=2100, fgcolors="#E63946")
            event_bus.publish("inventory_changed")   # 🔔 notify others
            event_bus.subscribe("inventory_changed", self.mark_stale_and_refresh)

        self.delete_msgbox = CustomMessageBox(
            self,
            title="Delete Item",
            message="Are you sure you want to delete the item?",
            on_confirm=confirm_delete,
            toplvl_posx=550,
            toplvl_posy=435
        )

    def open_create_item(self):
        """
        Open the CreateItem dialog. When a new item is added, immediately refresh inventory
        and highlight the newly added item.
        """
        def after_add(product_id):
            # store last added id and force refresh so UI is updated immediately
            self.last_added_product_id = product_id
            # clear cache so refresh gets fresh data
            self.invalidate_cache(messages="✅ Item added", durations=1600)
            event_bus.publish("inventory_changed")   # 🔔 notify others
            event_bus.subscribe("inventory_changed", self.mark_stale_and_refresh)

        CreateItem(self, on_add_callback=after_add)

    def edit_window(self, product_id):
        EditItem(self, item_id=product_id)

    def invalidate_cache(self, **kwargs):
        self.data_cache = None
        self.refresh_inventory(force_refresh=True, **kwargs)

    def _parse_value(self, value):
        if isinstance(value, str):
            val = value.replace(",", "")
            return float(val) if val.replace(".", "").isdigit() else val.lower()
        return value

    def load_image(self, path, size):
        """Load and resize a PNG image using PIL and return a CTkImage."""
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ctk.CTkImage(light_image=image, dark_image=image, size=size)

    def get_blob_hash(self, blob):
        return hashlib.md5(blob).hexdigest() if blob else None
    
    def mark_stale_and_refresh(self, on_complete=None):
        # hide counters immediately
        self.prepare_for_display()

        def do_refresh():
            self.refresh_inventory(force_refresh=True)
            self.show_counters()

        # Schedule refresh after a short delay (so UI paints first)
        self.after_safe(200, do_refresh)
        if on_complete:
            self.after(10, on_complete) 

