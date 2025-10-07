# Import built-in modules
import customtkinter as ctk

# Import own-made modules
from core import paths
from core.tools import resize_image
from core.users_backend import retrieve_user_data_by_name
from ui.notifs import Toast
from ui.register import RegisterPage


class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login):
        super().__init__(master)
        # self.configure()
        self.on_login = on_login
        self.selected_role = None

        # --- main frame with border color ---
        self.mainframe = ctk.CTkFrame(self, fg_color='white')
        self.mainframe.pack(fill="both", expand=True, padx=0, pady=0)

        # tell grid how to distribute space
        # self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)

        # --- left frame with background image ---
        self.left_frame = ctk.CTkFrame(self.mainframe, corner_radius=0)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        bg_image = resize_image(paths.IMAGE_LOGIN_BG, (400, 570))
        image_label = ctk.CTkLabel(self.left_frame, text="", image=bg_image)
        image_label.pack(fill="both", expand=True)

        # --- right frame with login widgets ---
        self.right_frame = ctk.CTkFrame(self.mainframe, corner_radius=0, fg_color="white")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        title_header_frame = ctk.CTkFrame(self.right_frame, corner_radius=0, fg_color="transparent")
        title_header_frame.pack()

        entry_frame = ctk.CTkFrame(self.right_frame, corner_radius=0, fg_color="transparent")
        entry_frame.pack()

        registry_restore_frame = ctk.CTkFrame(self.right_frame, corner_radius=0, fg_color="transparent", height=200)
        registry_restore_frame.pack(fill="x")
        registry_restore_frame.pack_propagate()

        ctk.CTkLabel(title_header_frame, text="Welcome Back!", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(65, 8))
        ctk.CTkLabel(title_header_frame, text="Sign in to your account", font=ctk.CTkFont(size=14)).pack(pady=(0, 30))

        self.username_entry = ctk.CTkEntry(entry_frame, placeholder_text="Username", width=400, height=40, font=('Arial', 14), border_width=1, corner_radius=5)
        self.username_entry.pack(padx=40, pady=(0, 15))
        self.username_entry.bind("<Return>", lambda e: self.authenticate_login())

        self.password_entry = ctk.CTkEntry(entry_frame, placeholder_text="Password", show="●", width=400, height=40, font=('Arial', 14), border_width=1, corner_radius=5)
        self.password_entry.pack(padx=40, pady=(0, 5))
        self.password_entry.bind("<Return>", lambda e: self.authenticate_login())
        
        def show_hide_password():
            if self.show_password_btn.get():
                self.password_entry.configure(show="")
            else:
                self.password_entry.configure(show="●")

        self.show_password_btn = ctk.CTkSwitch(entry_frame, text="show password", font=("Poppins", 14), command=show_hide_password)
        self.show_password_btn.pack(padx=40, pady=(0, 20))

        self.role_var = ctk.StringVar(value="Select role")
        dropdown = ctk.CTkOptionMenu(
            master=entry_frame,
            values=["Admin", "Owner/Manager", "Technician"],
            height=30,
            width=105,
            font=('Segoe UI', 13, 'bold'),
            anchor='center',
            # fg_color="#298753",
            fg_color="#F0F0F0",
            # button_color="#298753",
            button_color="#F0F0F0",
            button_hover_color="#4BAC76",
            dropdown_fg_color="white",
            dropdown_text_color="black",
            dropdown_hover_color="#298753",
            dropdown_font=('Segoe UI', 13),
            command=self.selection_change,
            state="disabled",
            variable=self.role_var
        )
        # dropdown.set("Select role")
        dropdown.pack(pady=(0, 20))

        # Login Button
        ctk.CTkButton(entry_frame, text="Login", fg_color="#7211FB", hover_color="#4B00B5", width=120, font=('Roboto', 14), command=self.authenticate_login).pack(padx=40)

        # Register & Reset Password 
        register_frame = ctk.CTkFrame(registry_restore_frame, corner_radius=0, fg_color="transparent")
        register_frame.pack(pady=(25, 5))

        reset_frame = ctk.CTkFrame(registry_restore_frame, corner_radius=0, fg_color="transparent")
        reset_frame.pack(pady=(0, 15))
        
        # Register
        ctk.CTkLabel(register_frame, text="Don't have an account?", text_color='gray', font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=1, pady=1)
        signup_label = ctk.CTkLabel(register_frame, text=" Sign up", text_color="#582CF8", font=ctk.CTkFont(size=14, weight="bold"), cursor="hand2")
        signup_label.grid(row=0, column=1, padx=(0, 1), pady=1)
        signup_label.bind("<Button-1>", lambda event: self.open_registration_page(event))

        # Reset Password
        ctk.CTkLabel(reset_frame, text="Can't sign in?", text_color='gray', font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, padx=1, pady=1)
        signup_label = ctk.CTkLabel(reset_frame, text=" Click here", text_color="#582CF8", font=ctk.CTkFont(size=14, weight="bold"), cursor="hand2")
        signup_label.grid(row=0, column=1, padx=(0, 1), pady=1)

        # self.enable_frames_layout([title_header_frame, entry_frame, registry_rest2ore_frame, register_frame])

        # --- widget bindings ---
        entries = [self.username_entry, self.password_entry]
        for entry in entries:
            entry.bind("<FocusIn>", lambda e, w=entry: w.configure(border_color="black"))
            entry.bind("<FocusOut>", lambda e, w=entry: w.configure(border_color="#979DA2"))

        rf_widgets = [w for w in self.right_frame.winfo_children()] + [self.right_frame]
        for widget in rf_widgets:
            widget.bind("<Button-1>", self.remove_focus_on_entry)

        self.enable_entries_autodelete()

    def enable_frames_layout(self, frames):
        for frame in frames:
            frame.configure(border_width=1)

    def enable_entries_autodelete(self):
        self.username_entry.bind("<Control-BackSpace>", lambda event: self.username_entry.delete(0, "end"))
        self.password_entry.bind("<Control-BackSpace>", lambda event: self.password_entry.delete(0, "end"))
    
    def remove_focus_on_entry(self, event):
        self.focus()

    def selection_change(self, role):
        self.selected_role = role.lower()

    def authenticate_login(self):
        user = self.username_entry.get()
        pasw = self.password_entry.get()

        if user != "":
            try:
                account_from_db = retrieve_user_data_by_name(user)
                # user_from_db = account_from_db[2]
                pasw_from_db = account_from_db[5]

                if pasw == "":
                    Toast(self,"Enter password", x=790, y=580, bg_color="#E63946")
                
                elif pasw != "":
                    if pasw != pasw_from_db:
                        Toast(self, "Password doesn't match", x=790, y=580, bg_color="#E63946")
                    elif pasw == pasw_from_db:
                            self.username_entry.delete(0, "end")
                            self.password_entry.delete(0, "end")
                            self.focus()
                            Toast(self, 'Login Success!', x=790, y=580, on_close=self.on_login)

            except Exception as e:
                Toast(self, "Username not found", x=790, y=580, bg_color="#E63946")

        elif user == "":
            Toast(self, "Enter username", x=790, y=580, bg_color="#E63946")

        elif pasw == "":
            Toast(self, "Enter password", x=790, y=580, bg_color="#E63946")

    def open_registration_page(self, event):
        RegisterPage(self)
