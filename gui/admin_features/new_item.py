import os
from PIL import Image
from tkinter import filedialog
import customtkinter as ctk

from core.inventory_backend import insert_to_database
from ui.notifs import Toast

from core import paths


# Constants
FONT_MAIN = ("Poppins", 20)
FONT_NORMAL = ("Poppins", 14)
FONT_BOLD = ("Poppins", 14, "bold")
FONT_INPUT = ("Poppins", 13)

COLOR_GREEN = "#298753"
COLOR_GREEN_HOVER = "#4BAC76"
COLOR_GRAY = "#e8e8e8"
COLOR_ERROR = "#E63946"

DEFAULT_UNIT = "Select unit"
DEFAULT_CATEGORY = "Select category"

IMAGE_PREVIEW_SIZE = (60, 60)
IMAGE_BLOB_SIZE = (100, 100)

LAST_DIR = os.getcwd()


class CreateItem(ctk.CTkToplevel):
    def __init__(self, master, on_add_callback=None):
        super().__init__(master)

        self.master = master
        self.on_add_callback = on_add_callback
        self.actual_item_photo = None

        self.title("Add New Item")
        self.geometry("1000x600+205+111")
        self.resizable(False, False)
        self.configure(fg_color="#ffffff")
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.overrideredirect(True)
        self.grab_set()

        border_frame = ctk.CTkFrame(self, fg_color=COLOR_GREEN, corner_radius=5)
        border_frame.pack(expand=True, fill="both")

        self.mainframe = ctk.CTkFrame(border_frame, fg_color="#ffffff", corner_radius=0)
        self.mainframe.pack(fill="both", expand=True, padx=1.5, pady=10)

        self.entry_frame = ctk.CTkFrame(self.mainframe, fg_color="#ffffff", corner_radius=0)
        self.entry_frame.pack(fill="both", expand=True, padx=70, pady=(20, 0))

        self.setup_header()
        self.setup_frames()
        self.setup_all_fields()
    
    def setup_header(self):
        # NEW ITEM HEADER
        ctk.CTkLabel(
            self.entry_frame, text="New Item", font=('Poppins', 30, 'bold'), text_color=COLOR_GREEN,
        ).grid(row=0, column=0, sticky="w", pady=(12, 0))

        ctk.CTkLabel(
            self.entry_frame, text="", bg_color="transparent", image=ctk.CTkImage(light_image=Image.open(paths.IMAGE_APP), size=(170, 60))
        ).grid(row=0, column=0, sticky="e", pady=(10, 0))

    def setup_frames(self):
        self.frame_one_main = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0, width=856, height=79)
        self.frame_one_main.grid(row=1, column=0, sticky="w")
        self.frame_one_main.grid_propagate(False)

        self.frame_one = ctk.CTkFrame(self.frame_one_main, fg_color="#ffffff", corner_radius=0, width=435, height=60)
        self.frame_one.grid(row=0, column=0, sticky="nsew")
        self.frame_one.grid_propagate(False)

        self.frame_one_half = ctk.CTkFrame(self.frame_one_main, fg_color="#ffffff", corner_radius=0, width=300, height=65)
        self.frame_one_half.grid(row=0, column=1)
        self.frame_one_half.grid_propagate(False)
        self.frame_one_half.grid_rowconfigure((0, 1), weight=1)

        self.frame_two = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0, height=345, width=700)
        self.frame_two.grid(row=2, column=0, sticky="w")
        self.frame_two.grid_propagate(False)

        self.frame_three = ctk.CTkFrame(self.entry_frame, fg_color="#ffffff", corner_radius=0)
        self.frame_three.grid(row=3, column=0, sticky="nsew")

        # self.show_frame_layouts() 

    def show_frame_layouts(self):
        self.frame_one_main.configure(fg_color="gray") 
        self.frame_one.configure(fg_color="purple")
        self.frame_one_half.configure(fg_color="red")
        self.frame_two.configure(fg_color="gray")
        self.frame_three.configure(fg_color="yellow")

    def create_entry(self, parent, width=250, height=30, **kwargs):
        return ctk.CTkEntry(
            parent, width=width, height=height, fg_color=COLOR_GRAY, font=FONT_INPUT, **kwargs
        )

    def setup_all_fields(self):
        # ITEM PHOTO
        ctk.CTkLabel(self.frame_one, text="Item Photo", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=0, column=0)
        ctk.CTkButton(
            self.frame_one, text="Upload Photo", font=FONT_NORMAL, fg_color=COLOR_GREEN, text_color="#ffffff", hover_color=COLOR_GREEN_HOVER, width=100, command=self.upload_item_image
        ).grid(row=0, column=1, padx=(10, 0))

        # ITEM PHOTO PREVIEW
        self.item_photo_preview = ctk.CTkLabel(self.frame_one, text="", height=70)
        self.item_photo_preview.grid(row=0, column=2, padx=(20, 100))

        # ITEM NAME
        ctk.CTkLabel(self.frame_two, text="Item Name", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=0, column=0, sticky="w", padx=(0, 185))
        self.item_name_entry = self.create_entry(self.frame_two)
        self.item_name_entry.grid(row=1, column=0, padx=(0, 185), sticky="w")

        # ITEM PRICE
        ctk.CTkLabel(self.frame_one_half, text="Price", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=0, column=0, sticky="w")
        self.price_entry = self.create_entry(self.frame_one_half, width=122)
        self.price_entry.grid(row=1, column=0)

        # ITEM TYPE
        ctk.CTkLabel(self.frame_two, text="Type", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=2, column=0, sticky="w")
        self.type_entry = self.create_entry(self.frame_two)
        self.type_entry.grid(row=3, column=0, sticky="w")

        # ITEM BRAND
        ctk.CTkLabel(self.frame_two, text="Brand", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=4, column=0, sticky="w", pady=(10, 0))
        self.brand_entry = self.create_entry(self.frame_two)
        self.brand_entry.grid(row=5, column=0, sticky="w")

        # ITEM UNIT
        ctk.CTkLabel(self.frame_two, text="Unit", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=0, column=1, sticky="w")

        self.unit_entry = ctk.CTkOptionMenu(
            master=self.frame_two,
            values=["box", "pc/s", "roll", "ft", "in", "ft", "m", "cm", "mm", "kg", "g"],
            height=33,
            width=160,
            font=FONT_NORMAL,
            text_color="black",
            button_color=COLOR_GREEN,
            button_hover_color=COLOR_GREEN_HOVER,
            fg_color=COLOR_GRAY,
            dropdown_fg_color=COLOR_GRAY,
            dropdown_text_color="black",
            dropdown_font=FONT_NORMAL,
            dropdown_hover_color=COLOR_GREEN,
            command=lambda e: self.clear_focus(e)
        )
        self.unit_entry.set(DEFAULT_UNIT)
        self.unit_entry.grid(row=1, column=1, sticky="w")
        
        # ITEM SUPPLIER
        # self.supplier_entry = ctk.CTkEntry(self.entry_frame)
        ctk.CTkLabel(self.frame_two, text="Supplier", font=FONT_MAIN, text_color=COLOR_GREEN, bg_color="transparent").grid(row=6, column=0, sticky="w", pady=(10, 0))
        self.supplier_entry = self.create_entry(self.frame_two)
        self.supplier_entry.grid(row=7, column=0, sticky="w")

        # ITEM QUANTITY "Current Stock"
        ctk.CTkLabel(self.frame_two, text="Quantity", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=2, column=1, sticky="w", pady=(10, 0))
        self.current_stock_entry = self.create_entry(self.frame_two, width=60)
        self.current_stock_entry.grid(row=3, column=1, sticky="w")
        
        # ITEM THRESHOLD
        ctk.CTkLabel(self.frame_two, text="Set Threshold", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=4, column=1, sticky="w", pady=(10, 0))
        self.threshold_entry = self.create_entry(self.frame_two, width=50)
        self.threshold_entry.grid(row=5, column=1, sticky="w")

        # ITEM CATEGORY
        ctk.CTkLabel(self.frame_two, text="Category", font=FONT_MAIN, text_color=COLOR_GREEN).grid(row=6, column=1, sticky="w", pady=(10, 0))

        self.category_entry = ctk.CTkOptionMenu(
            master=self.frame_two,
            values=["Equipment", "Tools", "Consumables"],
            height=33,
            width=160,
            font=FONT_NORMAL,
            text_color="black",
            button_color=COLOR_GREEN,
            button_hover_color=COLOR_GREEN_HOVER,
            fg_color=COLOR_GRAY,
            dropdown_fg_color=COLOR_GRAY,
            dropdown_text_color="black",
            dropdown_font=FONT_NORMAL,
            dropdown_hover_color=COLOR_GREEN,
            command=lambda e: self.clear_focus(e)
        )
        self.category_entry.set(DEFAULT_CATEGORY)
        self.category_entry.grid(row=7, column=1, sticky="w")

        self.entry_fields = [
            self.item_name_entry,
            self.type_entry,
            self.brand_entry,
            self.price_entry,
            self.current_stock_entry,
            self.threshold_entry,
            self.supplier_entry,
        ]

        for widget in self.entry_fields:
            widget.bind("<FocusIn>", lambda e, w=widget: w.configure(border_color='#298753'))
            widget.bind("<FocusOut>", lambda e, w=widget: w.configure(border_color='#979da2'))
        
        self.option_menus = [
            self.unit_entry,
            self.category_entry,
        ]
        
        self.new_item_details = [
            self.item_name_entry,
            self.type_entry,
            self.brand_entry,
            self.price_entry,
            self.current_stock_entry,
            self.threshold_entry,
            self.unit_entry,
            self.category_entry,
            self.supplier_entry,
        ]

        # BACK BUTTON
        ctk.CTkButton(
            self.frame_three,
            text="Back",
            font=FONT_BOLD,
            text_color=COLOR_GREEN,
            width=200,
            fg_color="#ffffff",
            border_color=COLOR_GREEN,
            border_width=2.5,
            hover_color=COLOR_GRAY,
            command=self.close_window
        ).pack(side="left", anchor="s", padx=(0, 50), pady=(10, 0))

        # ADD BUTTON
        ctk.CTkButton(
            self.frame_three,
            text="Add",
            font=FONT_BOLD,
            text_color="#ffffff",
            width=200,
            height=35,
            fg_color=COLOR_GREEN,
            hover_color=COLOR_GREEN_HOVER,
            command=lambda: self.add_item_to_database(self.new_item_details)
        ).pack(side="left", anchor="s", pady=(10, 0))

        other_widgets = [
            self.mainframe,
            self.entry_frame,
            self.frame_one,
            self.frame_two,
            self.frame_one_main,
            self.frame_one_half,
        ]

        for menu in other_widgets:
            menu.bind("<Button-1>", self.clear_focus)

    def clear_focus(self, event):
        self.focus()

    def show_widget_fg_color(self):
        self.mainframe.configure(fg_color="yellow")
        self.entry_frame.configure(fg_color="blue")
        self.frame_one_main.configure(fg_color="lightblue")
        self.frame_one.configure(fg_color="lightgreen")
        self.frame_one_half.configure(fg_color="red")
        self.frame_two.configure(fg_color="lightyellow")
        self.frame_three.configure(fg_color="brown")

    def upload_item_image(self):
        global LAST_DIR
        self.update_idletasks()

        file_path = filedialog.askopenfilename(
            parent=self,
            initialdir=LAST_DIR, 
            filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")]
        )

        if file_path:
            LAST_DIR = os.path.dirname(file_path)
            image = Image.open(file_path)
            image.thumbnail(IMAGE_BLOB_SIZE)
            # image = image.resize(IMAGE_BLOB_SIZE)
            self.actual_item_photo = self.convert_image_to_blob(file_path)

            ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=IMAGE_PREVIEW_SIZE)
            self.item_photo_preview.configure(image=ctk_image)
            self.item_photo_preview.image = ctk_image
        
        # Bring the window back to front
        self.lift()
        self.attributes('-topmost', True)
        self.after(10, lambda: self.attributes('-topmost', False))

    def convert_image_to_blob(self, image_path):
        with open(image_path, 'rb') as file:
            return file.read()

    def validate_inputs(self):
        for entry in self.entry_fields:
            if not entry.get().strip():
                return False, "Some fields are empty"          
        try:
            float(self.price_entry.get())
        except ValueError:
            return False, "Enter a valid price"

        try:
            int(self.current_stock_entry.get())
        except ValueError:
            return False, "Enter a valid quantity"
        
        try:
            int(self.threshold_entry.get())
        except ValueError:
            return False, "Enter a valid threshold"
        
        if self.option_menus[0].get() == DEFAULT_UNIT:
            return False, "Select a UNIT"
        if self.option_menus[1].get() == DEFAULT_CATEGORY:
            return False, "Select a CATEGORY"
        if self.actual_item_photo == None:
            return False, "Upload an IMAGE"

        return True, ""

    def add_item_to_database(self, details):
        validation_result, message = self.validate_inputs()
        
        if not validation_result:
            Toast(self, message, duration=2500, x=590, y=130, bg_color=COLOR_ERROR, font=("Poppins", 16, "bold"))
            return
        try:
            item_id, code = insert_to_database(
                self.actual_item_photo,
                details[0].get(),  # name
                details[1].get(),  # type
                details[2].get(),  # brand
                details[3].get(),  # price
                details[4].get(),  # quantity
                details[5].get(),  # threshold
                details[6].get(),  # unit
                details[7].get(),  # category
                details[8].get(),  # supplier
            )

        except Exception as e:
            Toast(self, f"Database error: {e}", duration=3000, x=590, y=130, bg_color=COLOR_ERROR, font=("Poppins", 16, "bold"))
            return
        
        if self.on_add_callback:
            self.on_add_callback(item_id)
        self.close_add_window_and_refresh()
        
    def close_add_window_and_refresh(self):
        self.master.refresh_inventory(force_refresh=True, messages="✅ Added", durations=2100)
        self.grab_release()
        self.after(100, self.destroy())

    def close_window(self):
        self.grab_release()
        self.destroy()
