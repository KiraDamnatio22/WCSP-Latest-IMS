# Import built-in/installed modules
import io
import unicodedata
import customtkinter as ctk
import hashlib
from PIL import Image
# from datetime import datetime
from rapidfuzz.fuzz import ratio

# Import own-made modules
from core import paths 
from core.event_bus import event_bus
from core.users_backend import retrieve_all_user_data, delete_user
from ui.notifs import CustomMessageBox


class UserManagement(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#FFFFFF")

        # OTHER VARIABLES
        self.user_frames = []   # list of (product_data, frame)
        self._users = {}
        self.frame_cache = {}
        self.image_cache = {}
        self.data_cache = None
        self.toast_label = None
        self.no_result_label = None
        self.delete_msgbox = None
        self.scrolling = False
        self._after_jobs = []  # keep track of after IDs
        # self._click_bind_id = None

        self.column_configs = [
            {"text": "Photo", "width": 70, "padx": (20, 10)},
            {"text": "Code", "width": 100, "padx": (10, 15), "textlength": 100},
            {"text": "Name", "width": 135, "padx": (0, 17), "textlength": 100},
            {"text": "Username", "width": 135, "padx": (0, 17), "textlength": 100},
            {"text": "Role", "width": 95, "padx": (0, 15), "textlength": 100},
            {"text": "Actions", "width": 125, "padx": (0, 15), "textlength": 100},
        ]

        self.data_widths = [
            [70, (10, 15)], # Photo
            [100, (7, 15)], # Code
            [135, (0, 15)], # Name
            [135, (0, 15)], # Username
            [95, (0, 14)], # Role
            [95, (0, 15)] # Actions
        ]

        self.empty_image = self.load_image(paths.IMAGE_EMPTY, (200, 200))

        self.fallback_image = ctk.CTkImage(
            light_image=Image.open(paths.IMAGE_PLACEHOLDER).resize((50, 50)),
            size=(50, 50)
        )

        self.status_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0, border_width=0)
        self.status_frame.pack(fill='x', pady=(66, 0))

        self.search_frame = ctk.CTkFrame(self, fg_color="#e8e8e8", corner_radius=5, border_width=0)
        self.search_frame.pack(fill='x', padx=(16, 19), pady=(0, 8))

        self.content_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0, border_width=0)
        self.content_frame.pack(fill='both', expand=True)

        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="#7211FB", corner_radius=10, border_width=0)
        self.header_frame.pack(padx=(16, 20)) 

        self.scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="#FFFFFF", height=276, width=1143, border_width=1)
        self.scrollable_frame.pack(padx=(5, 5), expand=True, fill="both")

        self.footer_frame = ctk.CTkFrame(self, border_width=0, fg_color="white", height=5)
        self.footer_frame.pack(padx=(5, 5), pady=(0, 60), fill="x")
        self.footer_frame.pack_propagate(False)

        # (MouseBindings)
        canvas = self.scrollable_frame._parent_canvas  # fallback if needed
        canvas.bind("<MouseWheel>", self.on_mouse_scroll)

        self._click_bind_id = None
        self.bind_shortcuts()
        self.setup_searchbar()
        
        self.scroll_controls()
        self.setup_headers()

        self.setup_status_bar()
        self.refresh_inventory()
        event_bus.subscribe("inventory_changed", self.on_inventory_changed)  # 🔔 subscribe

        # Optional debug
        print("\n[DEBUG] ManageUser UI initialized successfully.\n")

        ctk.CTkLabel(self.footer_frame, text="").pack(padx=5)

    def on_inventory_changed(self, *args, **kwargs):
        """Called whenever inventory changes elsewhere."""
        self.mark_stale_and_refresh()

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
        for seq in ("<Control-r>", "<Control-t>", "<Control-b>", "<Control-s>", "<Control-BackSpace>", "<Escape>"):
            master.unbind(seq)

    def setup_status_bar(self):
        ctk.CTkLabel(self.status_frame, text='Manage User', font=('Poppins', 27, 'bold'), fg_color="transparent", text_color="#298753", anchor="s").grid(row=0, column=0, padx=(20, 65), ipady=10, pady=1)

    def create_keyboard_shortcut(self, master, shortcut, fn):
        master.bind(shortcut, fn)

    def search_pane_focus(self, event=None):
        self.search_pane.focus()
        self.search_pane.configure(border_color="#298753")

    def on_mouse_scroll(self, event):
        ''' Scroll only if scrollable frame has overflow content '''
        # use local scrolling flag
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
        ''' This function setups the headers for the requests product table. '''
        for col_index, col in enumerate(self.column_configs):
            header_label = ctk.CTkLabel(
                self.header_frame,
                text=col["text"],
                font=("Arial", 14, "bold"),
                text_color="#ffffff",
                width=col["width"],
                anchor="center",
                wraplength=90,
                # fg_color="lightblue"
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
            placeholder_text='Search code, username, or role',
            placeholder_text_color='gray',
            width=350,
            height=30,
            font=('Poppins', 14),
            text_color="black")
        self.search_pane.pack(pady=10, padx=10, anchor="w", side="left")
        self.search_pane.bind('<KeyRelease>', self.delayed_filter)

        self.bind_global_click()

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

    def reset_button_on_searchbar(self):
        self.search_pane.delete(0, ctk.END)
        # self.sort_by_var.set("Sort by")
        # self.sort_order_var.set("ASCEND ↑")
        self.filter_and_sort_products()

    def normalize(self, text):
        """Removes accents, lowercases, and trims whitespace."""
        text = unicodedata.normalize('NFKD', text)
        return ''.join(c for c in text if not unicodedata.combining(c)).strip().lower()

    def is_fuzzy_match(self, query, target):
        """Avoid fuzzy match on short strings unless very close."""
        similarity = ratio(query, target)

        if len(query) <= 2:
            return similarity >= 95   # Only allow nearly exact matches for 1–2 chars
        elif len(query) <= 4:
            return similarity >= 85   # Tight matching for 3–4 chars
        elif len(query) <= 6:
            return similarity >= 80   # Medium strictness
        else:
            return similarity >= 70   # Relaxed threshold for long queries

    def clear_no_result_ui(self):
        self._safe_destroy(self.no_result_label)
        self._safe_destroy(getattr(self, "caption_label", None))
        self.no_result_label = None
        self.caption_label = None

    def activate_reset_button(self):
        self.reset_searchbar_button.configure(fg_color="#E63946", hover_color="#C92A3F", state="normal")

    def filter_and_sort_products(self):
        query = self.normalize(self.search_pane.get())

        # Prevent heavy filtering while scrolling
        if getattr(self, "scrolling", False):
            return

        # Clear "no result" display if it exists
        self.clear_no_result_ui()

        filtered = [(p[0], p) for p, _ in self.user_frames]  # (product_id, product_data)

        if query:
            self.scroll_to_top()
            searchable_fields = [2, 3, 4]
            # searchable_fields = [2]
            filtered = []

            for pid, p in [(p[0], p) for p, _ in self.user_frames]:
                matched = False

                # --- Code search (field index 2) ---
                code_val = self.normalize(str(p[2]))
                if query == code_val or code_val.startswith(query):
                    filtered.append((pid, p))
                    continue  # move to next product

                # --- Username search (field index 3) ---
                username_val = self.normalize(str(p[3]))
                if query == username_val or username_val.startswith(query):
                    filtered.append((pid, p))
                    continue

                # --- Role search (field index 4) ---
                role_val = self.normalize(str(p[4]))
                if query == role_val or role_val.startswith(query):
                    filtered.append((pid, p))
                    continue

            if filtered:
                self.show_toast(f"{len(filtered)} matching item(s) found", duration=1500, fgcolor="#298753")

            # Handle no results
            if not filtered:
                for _, frame in self.user_frames:
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

        # Hide all product frames
        self.clear_user_frames()

        # Show only filtered ones
        for pid, user in filtered:
            frame = self.frame_cache.get(str(pid))
            if frame:
                frame.pack(padx=(5, 0), pady=5)
            else:
                print(f"Warning: Frame for product ID {pid} not found in cache.")

    def clear_user_frames(self):
        for _, frame in self.user_frames:
            try:
                frame.pack_forget()
            except Exception:
                pass
    
    def _safe_destroy(self, widget):
        """Destroy a CTk widget if it still exists."""
        if widget and widget.winfo_exists():
            widget.destroy()

    def show_toast(self, message, duration=2000, fgcolor="#444", relxx=0.5, relyy=0.9):
        self._safe_destroy(self.toast_label)
        self.toast_label = ctk.CTkLabel(self, text=message, fg_color=fgcolor, font=("Roboto", 14), text_color="white", bg_color="#e0e0e0", corner_radius=5, padx=10)
        self.toast_label.place(relx=relxx, rely=relyy, anchor="s", y=-5)
        self.after_safe(duration, self.toast_label.destroy)

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

    def refresh_inventory(self, force_refresh=False, messages="✅ Refreshed", durations=1500, fgcolors="#298753", relyys=0.638):
        final_data = {}

        if self.data_cache is None or force_refresh:
            db_data = retrieve_all_user_data()
            self.data_cache = db_data
        else:
            db_data = self.data_cache

        for stock in db_data:
            stock = list(stock)
            user_id = str(stock[0])       # ID
            image_blob = stock[1]         # photo blob
            full_name = stock[3] + " " + stock[4]

            try:
                photo = self.convert_blob_to_image(image_blob, user_id)
            except Exception:
                photo = self.fallback_image

            # Rebuild row into UI-friendly format
            # [photo, id, code, username, role]
            final_data[user_id] = [stock[0], photo, stock[2], full_name, stock[5], stock[6]]

        old_data = list(self._users.values())
        new_data = list(final_data.values())

        # print("[OLD]", old_data)
        # print("[NEW]", new_data)

        added, removed, updated = self.diff_inventory(old_data, new_data)
        self._remove_deleted(removed)
        self._updated_users(updated)
        self._add_users(added)

        # note: key is now stock[1] = id
        self.user_frames = [
            (p, self.frame_cache[str(p[0])]) for p in self._users.values() if str(p[0]) in self.frame_cache
        ]

        self.filter_and_sort_products()
        self.show_toast(message=messages, duration=durations, fgcolor=fgcolors, relyy=relyys, relxx=0.49)

    def _remove_deleted(self, removed_ids):
        for pid in removed_ids:
            pid = str(pid)
            if pid in self.frame_cache:
                try:
                    self.frame_cache[pid].destroy()
                except Exception:
                    pass
                del self.frame_cache[pid]
            self._users.pop(pid, None)

    def _updated_users(self, updated):
        for user in updated:
            pid = str(user[0])
            self._users[pid] = user

            if pid in self.frame_cache:
                self._safe_destroy(self.frame_cache[pid])
                del self.frame_cache[pid]

            frame = self.create_user_frame(user)
            self.frame_cache[pid] = frame

    def _add_users(self, added):
        for user in added:
            pid = str(user[0])
            self._users[pid] = user
            frame = self.create_user_frame(user)
            self.frame_cache[pid] = frame

    def create_user_frame(self, user):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10, fg_color="#e0e0e0")

        # Column 0 → Photo
        ctk.CTkLabel(frame, text="", image=user[1], width=self.data_widths[0][0], anchor="center").grid(row=0, column=0, padx=self.data_widths[0][1], pady=15)

        # Column 1 → Code
        ctk.CTkLabel(frame, text=user[2], text_color="black", font=('Segoe UI Emoji', 14), width=self.data_widths[1][0], anchor="center").grid(row=0, column=1, padx=self.data_widths[1][1], pady=15)

        # Column 2 → Full Name
        ctk.CTkLabel(frame, text=user[3], text_color="black", font=('Segoe UI Emoji', 14), width=self.data_widths[2][0], anchor="center").grid(row=0, column=2, padx=self.data_widths[2][1], pady=15)

        # Column 2 → Username
        ctk.CTkLabel(frame, text=user[3], text_color="black", font=('Segoe UI Emoji', 14), width=self.data_widths[3][0], anchor="center").grid(row=0, column=3, padx=self.data_widths[3][1], pady=15)

        # Column 3 → Role
        ctk.CTkLabel(frame, text=user[4], text_color="black", font=('Segoe UI Emoji', 14), width=self.data_widths[4][0], anchor="center").grid(row=0, column=4, padx=self.data_widths[4][1], pady=15)

        # Column 4 → Actions
        button_frame = ctk.CTkFrame(frame, corner_radius=0, height=45, width=128, fg_color="transparent")
        button_frame.grid(row=0, column=5)
        button_frame.grid_propagate(False)

        ctk.CTkButton(
            button_frame,
            text="Remove",
            font=("Poppins", 13, "bold"),
            text_color="#FFFFFF",
            width=90,
            height=25,
            fg_color="#E63946",
            hover_color="#C92A3F",
            command=lambda id=user[0]: self.open_deletion_dialog(id)
        ).grid(row=0, column=0, sticky="nsew", pady=(8, 0), padx=(19, 7))

        frame.pack(pady=(0, 8))
        return frame

    def open_deletion_dialog(self, user_id):
        if self.delete_msgbox and self.delete_msgbox.winfo_exists():
            self.delete_msgbox.focus_force()
            return

        def confirm_delete():
            delete_user(user_id)
            self._safe_destroy(self.delete_msgbox)
            self.refresh_inventory(force_refresh=True, messages="✅ Deleted", durations=2100, fgcolors="#E63946")
            # event_bus.publish("inventory_changed")   # 🔔 notify others
            # event_bus.subscribe("inventory_changed", self.mark_stale_and_refresh)

        self.delete_msgbox = CustomMessageBox(
            self,
            title="Delete User",
            message="Are you sure to delete the user?",
            on_confirm=confirm_delete,
            toplvl_posx=550,
            toplvl_posy=380
        )

    def open_edit_stock_form(self, item_id):
        dialog = ctk.CTkInputDialog(text="Enter new stock quantity", font=("Poppins", 15), button_text_color="white")
        dialog.overrideredirect(True)
        dialog.geometry("+600+350")

        # --- close when clicking outside ---
        def close_dialog(event=None):
            try:
                dialog.unbind_all("<Button-1>")
                dialog.unbind("<Escape>")
                dialog.destroy()
            except Exception:
                pass

        def click_outside(event):
            try:
                x1, y1 = dialog.winfo_rootx(), dialog.winfo_rooty()
                x2, y2 = x1 + dialog.winfo_width(), y1 + dialog.winfo_height()

                # if click outside dialog → close
                if not (x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2):
                    close_dialog()
            except Exception:
                pass

        # catch clicks anywhere
        dialog.bind_all("<Button-1>", click_outside, add="+")
        # close on Escape
        dialog.bind("<Escape>", close_dialog)
        # clean up if user clicks the window’s "X"
        dialog.protocol("WM_DELETE_WINDOW", close_dialog)

        # now get_input() will return None if closed
        new_stock = dialog.get_input()

        # only update if input was valid
        if new_stock is not None and new_stock.isdigit():
            # update_item_stock(item_id, int(new_stock))
            self.refresh_inventory(force_refresh=True, messages="✅ Updated", durations=2100)

        # cleanup (safety net)
        try:
            dialog.unbind_all("<Button-1>")
            dialog.unbind("<Escape>")
        except Exception:
            pass

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
        self.after_idle(lambda: self.scrollable_frame._parent_canvas._parent_canvas.yview_moveto(1) if hasattr(self.scrollable_frame._parent_canvas, "_parent_canvas") else self.scrollable_frame._parent_canvas.yview_moveto(1))

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
        self.data_cache = None

        def do_refresh():
            self.refresh_inventory(force_refresh=True)

        # Schedule refresh after a short delay (so UI paints first)
        self.after_safe(200, do_refresh)
        if on_complete:
            self.after(10, on_complete) 

