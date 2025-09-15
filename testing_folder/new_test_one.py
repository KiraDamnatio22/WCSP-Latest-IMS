import io
import sys, os
import customtkinter as ctk

from PIL import Image
from tkinter import filedialog
from pop_ups.notifs import CustomMessageBox
from test_backend_from_test import (
    connect_db,
    insert_to_database,
    retrieve_data,
    update_data,
    delete_data
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class Inventory(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Inventory Table Mock Up")
        self.geometry("1170x410+120+65")
        # self.iconbitmap("testing folder/icons/WCSP-IMS.ico")
        self.iconbitmap(self.resource_path("icons/WCSP-IMS.ico"))
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")

        self.conn, self.curr = connect_db()
        # self.products = 
        self.delete_msgbox = None
        self.actual_item_photo = None
        # self.table_frame = None
        self.add_binding_id = None
        self.edit_binding_id = None

        self.search_frame = ctk.CTkFrame(self, corner_radius=5, fg_color="#E8E8E8")
        self.search_frame.pack(fill="x", padx=(16, 19), pady=5)

        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#FFFFFF")
        self.content_frame.pack(fill="both", expand=True)

        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="#298753", corner_radius=10)
        self.header_frame.pack(fill="x", padx=(16, 20))

        self.scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="#FFFFFF")
        self.scrollable_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.scrollable_frame._parent_canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)

        add_details = ctk.CTkButton(
        self, 
        text="Add Item",
        font=("Poppins", 13, "bold"),
        text_color="white",
        corner_radius=0, 
        cursor="hand2",
        command=self.add_window
        )
        add_details.pack(fill="x")

        self.setup_searchbar()
        self.setup_headers()
        self.set_products()
        self.setup_table()

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):  # PyInstaller sets this in a frozen app
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def setup_searchbar(self):
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_and_sort_products())

        search_pane = ctk.CTkEntry(self.search_frame, fg_color='#ffffff', placeholder_text=' Search item', width=350, height=30, font=('Poppins', 14), border_color="#298753", textvariable=self.search_var, text_color="black")
        search_pane.pack(pady=10, padx=(17, 10), anchor="w", side="left")

        self.sort_by_var = ctk.StringVar(value="Sort by")

        sort_by_values = ["Name", "Category", "Price", "Type", "Unit", "Current stock"]
        status_values = ["In Stock", "Low Stock", "Out of Stock"]
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
        # sort_by_menu.set("Sort by")
        sort_by_menu.pack(pady=10, padx=(0, 10), side="left")

        self.status_var = ctk.StringVar(value="Status")
        status_sort_menu = ctk.CTkOptionMenu(
            master=self.search_frame,
            values=status_values,
            variable=self.status_var,
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
        # status_sort_menu.set("Status")
        status_sort_menu.pack(pady=10, padx=(0, 10), side="left")

    def ask_delete(self, item_id):
        if self.delete_msgbox and self.delete_msgbox.winfo_exists():
            self.delete_msgbox.focus_force()
            return

        def confirm_delete():
            delete_data(self, item_id)
            if self.delete_msgbox and self.delete_msgbox.winfo_exists():
                self.delete_msgbox.destroy()
            self.setup_table()

        self.delete_msgbox = CustomMessageBox(
            self,
            title="Delete Item",
            message="Are you sure you want to delete the item?",
            on_confirm=confirm_delete
        )

    def update_item_details(self, item_id, details, photo_data):
        if self.actual_item_photo == None:
            update_data(self, item_id, photo_data, [e.get() for e in details])
        elif self.actual_item_photo == photo_data:
            update_data(self, item_id, photo_data, [e.get() for e in details])
        else:
            update_data(self, item_id, self.actual_item_photo, [e.get() for e in details])

        self.upload_button.pack_forget()
        self.update_button.pack_forget()
        self.close_edit_window_and_refresh()

    def upload_item_details(self, details):
        if details[0].get() == "":
            print("You entered nothing!")
            return
        
        insert_to_database(self, self.actual_item_photo, details[0].get(), details[1].get(), details[2].get(), details[3].get(), details[4].get(), details[5].get(), details[6].get(), details[7].get())
 
        for ent in details:
            ent.delete(0, "end")
        
        self.upload_button.pack_forget()
        self.add_button.pack_forget()
        self.close_add_window_and_refresh()

    def convert_image_to_blob(self, image_path):
            with open(image_path, 'rb') as file:
                profile_blob = file.read()
            return profile_blob

    def convert_blob_to_image(self, blob_data):
        image = Image.open(io.BytesIO(blob_data))
        image = image.resize((50, 50))
        return ctk.CTkImage(light_image=image, dark_image=image, size=(50, 50))

    def upload_item_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")])
        # print(file_path)
        if file_path:
            image = Image.open(file_path)
            image = image.resize((100, 100))
            self.actual_item_photo = self.convert_image_to_blob(file_path)
            self.item_photo_preview.configure(text="Uploaded.")

    def unfocus_entries(self, event, entries, root_window):
        if not root_window.winfo_exists():
            return

        clicked_inside_any = False

        for entry in entries:
            if entry.winfo_exists():
                if entry.winfo_rootx() <= event.x_root <= entry.winfo_rootx() + entry.winfo_width() and \
                entry.winfo_rooty() <= event.y_root <= entry.winfo_rooty() + entry.winfo_height():
                    entry.configure(border_color='#298753')
                    clicked_inside_any = True
                else:
                    entry.configure(border_color='#979da2')

        if not clicked_inside_any:
            if root_window.winfo_exists():
                root_window.focus_force()

    def close_add_window_and_refresh(self):
        if self.add_root.winfo_exists():
            if hasattr(self, 'add_click_binding_id'):
                self.add_root.unbind("<Button-1>", self.add_click_binding_id)
            self.add_root.destroy()
        self.setup_table()

    def close_edit_window_and_refresh(self):
        if self.edit_root.winfo_exists():
            if hasattr(self, 'edit_click_binding_id'):
                self.edit_root.unbind("<Button-1>", self.edit_click_binding_id)
            self.edit_root.destroy()
        self.setup_table()

    def add_window(self):
        print("ADDING ITEM TO INVENTORY...")

        self.add_root = ctk.CTkToplevel()
        self.add_root.title("ADD ITEM")
        self.add_root.geometry("800x670+270+10")
        self.add_root.configure(fg_color="#ffffff")
        self.add_root.resizable(False, False)
        self.add_root.grab_set()

        mainframe = ctk.CTkFrame(self.add_root, fg_color="transparent", corner_radius=0)
        mainframe.pack(fill="both", expand=True)

        entries = []

        ctk.CTkLabel(mainframe, text="Photo", font=("Poppins", 14, "bold"), text_color="#298753").pack(padx=10, pady=(10, 5))
        self.upload_button = ctk.CTkButton(
            mainframe, 
            text="Upload",
            font=("Poppins", 14),
            fg_color="#298753",
            text_color="#ffffff",
            hover_color="#4BAC76",
            border_color="#ffffff",
            width=100,
            cursor="hand2",
            command=self.upload_item_image
        )
        self.upload_button.pack(pady=(0, 0))
        self.item_photo_preview = ctk.CTkLabel(mainframe, text="", font=("Poppins", 14, "bold"), text_color="#E63946")
        self.item_photo_preview.pack(padx=10)

        labels = ["Name", "Category", "Price", "Type", "Brand", "Unit", "Quantity", "Threshold"]
        for label_text in labels:
            ctk.CTkLabel(mainframe, text=label_text, font=("Poppins", 14, "bold"), text_color="#298753").pack(padx=10, pady=(0 if label_text == "Name" else 5))
            entry = ctk.CTkEntry(mainframe, width=(200 if label_text == "Name" else 150))
            entry.pack(padx=10)
            entries.append(entry)

        self.add_details = entries  # store in instance variable

        self.add_click_binding_id = self.add_root.bind(
            "<Button-1>", lambda e: self.unfocus_entries(e, self.add_details, self.add_root)
        )

        self.add_button = ctk.CTkButton(
            self.add_root,
            text="Add Item",
            font=("Poppins", 13, "bold"),
            text_color="white",
            corner_radius=10,
            cursor="hand2",
            command=lambda: self.upload_item_details(self.add_details)
        )
        self.add_button.pack(padx=10, pady=(0, 10))

    def edit_window(self, item_id):
        print("EDITING ITEM FROM INVENTORY...")

        self.edit_root = ctk.CTkToplevel()
        self.edit_root.title("EDIT ITEM")
        self.edit_root.geometry("800x670+270+10")
        self.edit_root.configure(fg_color="#ffffff")
        self.edit_root.resizable(False, False)
        self.edit_root.grab_set()

        data = self.curr.execute("SELECT photo, name, category, price, _type, brand, unit, quantity FROM items WHERE id = ?", (item_id,)).fetchone()
        # print(data)

        mainframe = ctk.CTkFrame(self.edit_root, fg_color="transparent", corner_radius=0)
        mainframe.pack(fill="both", expand=True)

        ctk.CTkLabel(mainframe, text="Photo", font=("Poppins", 14, "bold"), text_color="#298753").pack(padx=10, pady=(10, 5))
        self.upload_button = ctk.CTkButton(
            mainframe, 
            text="Upload",
            font=("Poppins", 14),
            fg_color="#298753",
            text_color="#ffffff",
            hover_color="#4BAC76",
            border_color="#ffffff",
            width=100,
            cursor="hand2",
            command=self.upload_item_image
        )
        self.upload_button.pack(pady=(0, 0))
        self.item_photo_preview = ctk.CTkLabel(mainframe, text="", font=("Poppins", 14, "bold"), text_color="#E63946")
        self.item_photo_preview.pack(padx=10)

        labels = ["Name", "Category", "Price", "Type", "Brand", "Unit", "Quantity"]
        entries = []
        for i, label_text in enumerate(labels):
            ctk.CTkLabel(mainframe, text=label_text, font=("Poppins", 14, "bold"), text_color="#298753").pack(padx=10, pady=(0 if label_text == "Name" else 5))
            entry = ctk.CTkEntry(mainframe, width=(200 if i == 0 else 100))
            entry.insert(0, data[i+1])
            entry.pack(padx=10)
            entries.append(entry)

        self.edit_details = entries  # store in instance variable

        self.edit_click_binding_id = self.edit_root.bind(
            "<Button-1>", lambda e: self.unfocus_entries(e, self.edit_details, self.edit_root)
        )

        self.update_button = ctk.CTkButton(
            self.edit_root, 
            text="Update", 
            font=("Poppins", 13, "bold"),
            text_color="white",
            corner_radius=10,
            cursor="hand2",
            command=lambda: self.update_item_details(item_id, self.edit_details, data[0])
        )
        self.update_button.pack(padx=10, pady=(0, 10))

    def setup_headers(self):
        headers = ["Photo", "Code", "Name", "Category", "Price", "Type", "Brand", "Unit", "Current stock", "Threshold", "Stock Status"]
        for col, header in enumerate(headers):
            if  header == "Name":
                header_label = ctk.CTkLabel(
                self.header_frame,
                text=header,
                font=("Poppins", 14, "bold"),
                fg_color="#2E995E",
                bg_color="#2E995E",
                text_color="white",
                corner_radius=0,
                wraplength=80,
                padx=75,
                )
                header_label.grid(row=0, column=col, sticky="nsew")
                continue

            header_label = ctk.CTkLabel(
                self.header_frame,
                text=header,
                font=("Poppins", 14, "bold"),
                fg_color="#2E995E",
                bg_color="#2E995E",
                text_color="white",
                corner_radius=0,
                wraplength=80,
                padx=40,
            )
            header_label.grid(row=0, column=col, sticky="nsew")

            button_label = ctk.CTkLabel(
                self.header_frame,
                text="Actions",
                font=("Poppins", 14, "bold"),
                fg_color="#2E995E",
                bg_color="#2E995E",
                text_color="white",
                corner_radius=0,
                padx=40,
                pady=15,
            )
            button_label.grid(row=0, column=11, sticky="nsew")
        
        # Adjust column weights for responsiveness
        for col in range(len(headers)):
            self.header_frame.grid_columnconfigure(col, weight=1)

    def filter_and_sort_products(self):
        search_query = self.search_var.get().lower()
        sort_by = self.sort_by_var.get()
        status_filter = self.status_var.get()

        sort_index = {
            "Name": 2,
            "Category": 3,
            "Price": 4,
            "Type": 5,
            "Unit": 6,
            "Current stock": 7,
        }.get(sort_by, None)

        # Clear current view (hide frames)
        for product, frame in self.product_frames:
            frame.pack_forget()

        # Filter and sort products
        filtered = []
        for product, frame in self.product_frames:
            if search_query and search_query not in product[2].lower():
                continue
            if status_filter != "Status" and product[10] != status_filter:
                continue
            filtered.append((product, frame))

        if sort_index is not None:
            filtered.sort(key=lambda x: x[0][sort_index])

        # Show filtered, sorted frames
        for product, frame in filtered:
            # print(product, frame)
            frame.pack(fill="x", padx=5, pady=5)

    def create_product_frame(self, product):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)

        for col_index, (value, col) in enumerate(zip(product, self.column_configs)):
            label = ctk.CTkLabel(
                    frame,
                    text=value,
                    text_color="black",
                    font=('Roboto', 14),
                    width=col["width"],
                    anchor="center",
                    wraplength=90,
                    fg_color="lightblue",
            )
            frame.configure(fg_color="#c4c3c3" if col_index % 2 == 0 else "#e0e0e0", )
            label.grid(row=0, column=col_index, padx=col["padx"], pady=15)
        frame.pack(fill="x", padx=5, pady=5)
        return frame
    
    def set_products(self, ):
        ''' This function builds the entire table for the inventory products. '''   
        self.product_frames = []
        pass

        # for product in self.products:
        #     frame = self.create_product_frame(product)
        #     self.product_frames.append((product, frame))

    def setup_table(self):
        print("VIEWING INVENTORY...")

        # Clear old table content by destroying everything inside table_container
        # for widget in self.table_container.winfo_children():
        #     widget.destroy()

        # Create a fresh new table frame
        # self.table_frame = ctk.CTkScrollableFrame(
        #     self.table_container, corner_radius=0, fg_color="#FFFFFF")
        # self.table_frame.pack(fill="both", expand=True)

        # Add table headers
        db_data = retrieve_data()
        final_data = []

        for stock in db_data:
            stock = list(stock)
            for x in stock:
                print(x, type(x)) 
            q = stock[-2]
            t = stock[-1]
            low_stock = t * 2
            stock[1] = self.convert_blob_to_image(stock[1])

            if q <= t:
                stock.append("Out of stock")
                final_data.append(stock)
            elif q <= low_stock:
                stock.append("Low stock")
                final_data.append(stock)
            elif q > low_stock:
                stock.append("In stock")
                final_data.append(stock)

        # print(final_data)

        for row_index, row_data in enumerate(final_data, start=1):
            # print(final_data)
            # print("\n"*2)
            print(row_data)
            for col_index, cell_data in enumerate(row_data[1:]):
                if col_index == 10:
                    button_frame = ctk.CTkFrame(
                    self.scrollable_frame,
                    fg_color="#e0e0e0" if row_index % 2 == 0 else "#c4c3c3",
                    corner_radius=0,
                )
                    button_frame.grid(row=row_index, column=11, pady=(2, 0), sticky="nsew")

                    ctk.CTkButton(
                        button_frame, 
                        text="EDIT",
                        font=("Poppins", 13, "bold"),
                        text_color="#FFFFFF",
                        width=40,
                        cursor="hand2",
                        command=lambda i=row_data[0]: self.edit_window(i),
                        ).grid(row=0, column=0, sticky="nsew", pady=(15, 0), padx=(13, 6))
                    
                    ctk.CTkButton(
                        button_frame, 
                        text="DELETE",
                        font=("Poppins", 13, "bold"),
                        text_color="#FFFFFF",
                        width=40,
                        cursor="hand2",
                        fg_color="#E63946",
                        hover_color="#C92A3F",
                        command=lambda i=row_data[0]: self.ask_delete(i),
                        ).grid(row=0, column=1, sticky="nsew", pady=(15, 0))

                if col_index == 0:
                    cell_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text="",
                    image=cell_data,
                    fg_color="#e0e0e0" if row_index % 2 == 0 else "#c4c3c3",
                    corner_radius=0,
                    bg_color="#e0e0e0" if row_index % 2 == 0 else "#c4c3c3",
                    anchor="center"
                    )
                    cell_label.grid(row=row_index, column=col_index, pady=(2, 0), sticky="nsew", padx=(5, 0))
                    continue

                cell_label = ctk.CTkLabel(
                    self.scrollable_frame,
                    text=str(cell_data),
                    font=("Poppins", 12),
                    fg_color="#e0e0e0" if row_index % 2 == 0 else "#c4c3c3",
                    text_color="black",
                    corner_radius=0,
                    bg_color="#e0e0e0" if row_index % 2 == 0 else "#c4c3c3",
                    wraplength=105,
                )
                cell_label.grid(row=row_index, column=col_index, pady=(2, 0), sticky="nsew", ipady=15)

    def on_mouse_scroll(self, event):
        ''' This function is intended to change the speed of the mouse scroll on the scrollable frame. '''
    
        scroll_speed = 6  # The higher the faster
        
        if event.num == 4:  # For Linux
            self.scrollable_frame._parent_canvas.yview_scroll(-scroll_speed, "units")
        elif event.num == 5:  # For Linux
            self.scrollable_frame._parent_canvas.yview_scroll(scroll_speed, "units")
        else:  # For Windows & macOS
            self.scrollable_frame._parent_canvas.yview_scroll(-1 * (event.delta // 120) * scroll_speed, "units")

# Run the application
app = Inventory()
app.mainloop()

