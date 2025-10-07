import customtkinter as ctk

from core import paths
from core.users_backend import insert_new_user, retrieve_all_user_data, retrieve_user_data_by_name
from ui.notifs import Toast, ToolTip

class RegisterPage(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Register")
        self.protocol("WM_DELETE_WINDOW", self.return_to_login)
        self.geometry("500x600+460+50")
        self.resizable(False, False)
        self.grab_set()

        self.existing_usernames = {retrieve_user_data_by_name(row[5].lower())[:-1] for row in retrieve_all_user_data()}
        self.thumbnail_profile = self.convert_image_to_blob(paths.IMAGE_PLACEHOLDER)

        print(self.existing_usernames)

        # MAIN FRAME
        self.mainframe = ctk.CTkFrame(self, fg_color='white')
        self.mainframe.pack(fill="both", expand=True, padx=1, pady=1)

        self.title_header_frame = ctk.CTkFrame(self.mainframe, corner_radius=0, fg_color="transparent")
        self.title_header_frame.pack(fill="x", padx=2, pady=2)

        self.entry_frame = ctk.CTkFrame(self.mainframe, corner_radius=0, fg_color="transparent")
        self.entry_frame.pack(fill="x", padx=2, pady=2)

        self.submit_frame = ctk.CTkFrame(self.mainframe, corner_radius=0, fg_color="transparent")
        self.submit_frame.pack(fill="x", padx=2, pady=2)
        
        # self.enable_frames_layout([self.title_header_frame, self.entry_frame, self.submit_frame])
        # retrieve_all_user_data
        self.setup_all_fields()

    def convert_image_to_blob(self, image_path):
        with open(image_path, 'rb') as file:
            return file.read()

    def setup_all_fields(self):
        # TITLE AND HEADINGS
        ctk.CTkLabel(self.title_header_frame, text="Register", font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(35, 8))
        ctk.CTkLabel(self.title_header_frame, text="Create an account for WCSP IMS", font=ctk.CTkFont(size=14)).pack(pady=(0, 30))

        # ENTRY FIELDS
        self.first_name_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="First Name", width=400, height=40, font=('Arial', 14), border_width=1, corner_radius=5)
        self.first_name_entry.pack(padx=40, pady=(0, 15))

        self.last_name_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Last Name", width=400, height=40, font=('Arial', 14), border_width=1, corner_radius=5)
        self.last_name_entry.pack(padx=40, pady=(0, 15))

        self.username_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Username", width=400, height=40, font=('Arial', 14), border_width=1, corner_radius=5)
        self.username_entry.pack(padx=40, pady=(0, 15))

        # Tooltip (hidden by default)
        self.username_tooltip = ToolTip(self.username_entry, idle_delay=1500)

        # Bind key release → check username availability
        self.username_entry.bind("<KeyRelease>", self.check_username)

        self.password_entry = ctk.CTkEntry(self.entry_frame, width=400, height=40, font=('Arial', 14), border_width=1, border_color="white", corner_radius=5, state="disabled")
        self.password_entry.pack(padx=40, pady=(0, 20))
        self.password_entry.bind("<KeyRelease>", self.enable_select_role)

        def on_role_selection(value):
            self.focus()
            self.submit_button.configure(state="normal", fg_color="#4BAC76", hover_color="#298753")

        # ROLE
        self.role_var = ctk.StringVar(value="Which role?")
        self.role_selection = ctk.CTkOptionMenu(
            master=self.entry_frame,
            values=["User", "Admin", "Developer"],
            height=30,
            width=135,
            font=('Poppins', 13),
            anchor='center',
            text_color="white",
            fg_color="#F0F0F0",
            button_color="#F0F0F0",
            button_hover_color="#4B00B5",
            dropdown_fg_color="white",
            dropdown_text_color="#161616",
            dropdown_font=('Poppins', 13),
            state="disabled",
            variable=self.role_var,
            command=on_role_selection
        )
        self.role_selection.pack(pady=(10, 0))

        # SUBMIT
        self.submit_button = ctk.CTkButton(self.submit_frame, text="Register", text_color="white", fg_color="#F0F0F0", hover_color="#F0F0F0", width=150, font=('Poppins', 14, "bold"), command=self.register_credentials, state="disabled")
        self.submit_button.pack(padx=40, pady=(30, 0))

        self.enable_entry_bindings()
        self.enable_root_focus_binding()

    def check_username(self, event=None):
        username = self.username_entry.get().strip().lower()

        if not username:
            self.username_tooltip.hide_tip()
            return
        
        if username in self.existing_usernames:
            # ⚠️ Keep tooltip visible (auto_hide=False)
            self.username_tooltip.show_tip(
                "⚠️ This username already exists",
                fg_color="#E63946",  # red
                text_color="white",
                auto_hide=False
            )
            # self.password_entry.configure(placeholder_text="")
            self.password_entry.delete(0, "end")
            self.password_entry.configure(state="disabled", border_color="white")
        else:
            # self.username_tooltip.show_tip(
            #     "✔️ This username is available",
            #     fg_color="#298753",  # green
            #     text_color="white",
            #     auto_hide=True
            # )

            self.password_entry.configure(state="normal", border_color="#979DA2")
            self.after(1, lambda: self.password_entry.configure(placeholder_text="Password"))

    def remove_focus_on_entry(self, event):
        self.focus()

    def enable_root_focus_binding(self):
        rf_widgets = [w for w in self.mainframe.winfo_children()]
        for widget in rf_widgets:
            widget.bind("<Button-1>", self.remove_focus_on_entry)

    def enable_entry_bindings(self):
        for entry in [self.username_entry, self.password_entry]:
            entry.bind("<FocusIn>", lambda e, w=entry: w.configure(border_color="black"))
            entry.bind("<FocusOut>", lambda e, w=entry: w.configure(border_color="#979DA2"))

    def enable_frames_layout(self, frames):
        for frame in frames:
            frame.configure(border_width=1, border_color="black")
        
    def get_registration_data(self):
        fname = self.first_name_entry.get().capitalize()
        lname = self.last_name_entry.get().capitalize()
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        return fname, lname, username, password, role

    def register_credentials(self):
        firstname, lastname, username, password, role = self.get_registration_data()

        if username != "" and password != "":
            self.clear_fields()
            insert_new_user(firstname, lastname, username, password, role, self.thumbnail_profile)
            Toast(self, 'Registration successful', x=600, y=285, on_close=self.return_to_login)
    
    def enable_select_role(self, event=None):
        user = self.username_entry.get()
        pasw = self.password_entry.get()
        if user != "":
            if pasw != "":
                self.role_selection.configure(state="normal", fg_color="#7211FB", button_color="#7211FB")
            elif pasw == "":
                self.role_selection.configure(state="disabled", fg_color="#F0F0F0", button_color="#F0F0F0")
        else:
            return

    def clear_fields(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.focus()

    def return_to_login(self):
        self.clear_fields()
        self.grab_release()
        self.destroy()
        # self.master.destroy()

# ctk.set_appearance_mode("light")
# ctk.set_default_color_theme("blue")

# app = ctk.CTk()
# app.geometry("200x200")

# def open_register_page():
#     RegisterPage(app)

# ctk.CTkButton(app, text="Register", text_color="white", font=ctk.CTkFont(size=16, weight="bold"), command=open_register_page).pack(pady=50)

# app.mainloop()
