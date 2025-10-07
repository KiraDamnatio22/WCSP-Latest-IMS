# # Import built-in modules
# import customtkinter as ctk
# import tkinter as tk
# from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageFilter

# # Import own-made modules
# from core.tools import CustomizeProfile
# from core import paths

# class AccountAdmin(ctk.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)
#         self.configure(fg_color="#FFFFFF")

#         self.customizer = CustomizeProfile()

#         self.mainframe = ctk.CTkFrame(self, fg_color="white")
#         self.mainframe.pack(fill="both", expand=True)

#         ctk.CTkButton(
#             self,
#             text="Logout",
#             font=("Poppins", 14),
#             fg_color="#E63946", 
#             hover_color="#C92A3F",
#             text_color="#FFFFFF",
#             cursor="hand2",
#             command=self.exit_main
#         ).pack(pady=10)
        
#         self.setup_frames()

#     def setup_frames(self):
#         # PF
#         self.profile_frame = ctk.CTkFrame(self.mainframe, fg_color="white")
#         self.profile_frame.pack(fill="x", pady=(15, 0))

#         # PF1: Cover Photo Frame
#         self.cover_photo_frame = ctk.CTkFrame(
#             self.profile_frame,
#             fg_color="white",
#             height=290,
#             width=1000,
#             border_width=0,
#             border_color="black"
#         )
#         self.cover_photo_frame.pack()
#         self.cover_photo_frame.pack_propagate(False)

#         # Canvas for layering (background + circular profile)
#         self.canvas = tk.Canvas(self.cover_photo_frame, width=990, height=280, highlightthickness=0)
#         self.canvas.pack(pady=(5, 0))

#         # Load and draw cover photo
#         cover_img = Image.open(paths.IMAGE_PROFILE_COVER).resize((990, 180))
#         self.cover_tk = ImageTk.PhotoImage(cover_img)
#         self.canvas.create_image(0, 0, image=self.cover_tk, anchor="nw")

#         # Create circular profile photo
#         circular_img = self.make_circle(paths.IMAGE_EMPTY, size=(150, 150), border_width=1, border_color="black")
#         self.profile_tk = ImageTk.PhotoImage(circular_img)

#         # Place circular profile on top of cover
#         self.canvas.create_image(495, 240, image=self.profile_tk, anchor="s")  # center bottom

#         # PF2: Profile details (below the photo)
#         self.profile_photo_frame = ctk.CTkFrame(self.profile_frame, fg_color="lightgray")
#         self.profile_photo_frame.pack(fill="x")

#         # PF3: Account Name Frame
#         # self.account_name_frame = ctk.CTkFrame(self.profile_frame, fg_color="red")
#         # self.account_name_frame.pack(fill="x")

#     def make_circle(self, image_path, size=(150, 150), border_width=4, border_color="lightgray"):
#         """Make a smooth circular image with anti-aliasing and crisp border (fixed final size)."""
#         img = Image.open(image_path).convert("RGBA")
#         img = img.resize(size, Image.LANCZOS)

#         # --- Create smooth circular mask ---
#         scale = 8  # higher = smoother edges
#         big_size = (size[0] * scale, size[1] * scale)
#         mask = Image.new("L", big_size, 0)
#         draw = ImageDraw.Draw(mask)

#         # Shrink radius for inward border
#         offset = border_width * scale
#         draw.ellipse((offset, offset, big_size[0] - offset, big_size[1] - offset), fill=255)

#         # Smooth edges by blurring before downscaling
#         mask = mask.filter(ImageFilter.GaussianBlur(scale / 2))
#         mask = mask.resize(size, Image.LANCZOS)

#         # Apply circular mask to image
#         circular_img = ImageOps.fit(img, size, centering=(0.5, 0.5))
#         circular_img.putalpha(mask)

#         # --- Create border mask ---
#         border_mask = Image.new("L", big_size, 0)
#         border_draw = ImageDraw.Draw(border_mask)
#         border_draw.ellipse((0, 0, big_size[0], big_size[1]), fill=255)
#         border_draw.ellipse((offset, offset, big_size[0] - offset, big_size[1] - offset), fill=0)

#         # Smooth border edges
#         border_mask = border_mask.filter(ImageFilter.GaussianBlur(scale / 2))
#         border_mask = border_mask.resize(size, Image.LANCZOS)

#         # Create border layer
#         border_layer = Image.new("RGBA", size, border_color)
#         border_layer.putalpha(border_mask)

#         # Composite border behind circular image
#         final_img = Image.alpha_composite(border_layer, circular_img)

#         return final_img

#     def exit_main(self):
#         for child in self.winfo_toplevel().winfo_children():
#             if hasattr(child, "cleanup"):
#                 child.cleanup()
#         self.winfo_toplevel().main_page.logout()



# Import built-in modules
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageOps, ImageFilter

# Import own-made modules
from core.tools import CustomizeProfile
from core import paths


class AccountAdmin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#FFFFFF")

        self.customizer = CustomizeProfile()

        self.mainframe = ctk.CTkFrame(self, fg_color="white")
        self.mainframe.pack(fill="both", expand=True)

        self.setup_frames()

    def setup_frames(self):
        # PF
        self.profile_frame = ctk.CTkFrame(self.mainframe, fg_color="white")
        self.profile_frame.pack(fill="x", pady=(15, 0))

        # PF1: Cover Photo Frame
        self.cover_photo_frame = ctk.CTkFrame(
            self.profile_frame,
            fg_color="white",
            height=350,
            width=1000,
            border_width=1,
            border_color="black",
        )
        self.cover_photo_frame.pack()
        self.cover_photo_frame.pack_propagate(False)

        # Canvas for layering (background + circular profile)
        self.canvas = tk.Canvas(self.cover_photo_frame, width=990, height=340, highlightthickness=0)
        self.canvas.pack(pady=(5, 0))

        # Load and draw cover photo
        cover_img = Image.open(paths.IMAGE_PROFILE_COVER).resize((990, 180))
        self.cover_tk = ImageTk.PhotoImage(cover_img)
        self.canvas.create_image(0, 0, image=self.cover_tk, anchor="nw")

        # Create circular profile photo
        circular_img = self.make_circle(paths.IMAGE_EMPTY, size=(150, 150), border_width=1.5, border_color="black")
        self.profile_tk = ImageTk.PhotoImage(circular_img)

        # Place circular profile on top of cover
        self.profile_image_id = self.canvas.create_image(495, 240, image=self.profile_tk, anchor="s")

        # Bind events to make it clickable
        self.canvas.tag_bind(self.profile_image_id, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.profile_image_id, "<Leave>", lambda e: self.canvas.config(cursor=""))
        self.canvas.tag_bind(self.profile_image_id, "<Button-1>", self.show_profile_options)

        # Account name
        account_frame = ctk.CTkFrame(self.canvas, fg_color="transparent", border_width=0, corner_radius=10, width=200, height=100)

        self.canvas.create_window(496, 265, window=account_frame, anchor="center")

        btn = ctk.CTkLabel(account_frame, text="Rensyl Quiroben II", font=ctk.CTkFont(size=22, weight="bold"), anchor="n")
        btn.pack(padx=10, pady=10)

        # PF2: Profile details (below the photo)
        self.profile_photo_frame = ctk.CTkFrame(self.profile_frame, fg_color="white", border_color="black", border_width=1, width=1000)
        self.profile_photo_frame.pack(pady=(10, 0))
        self.profile_photo_frame.pack_propagate(False)

        ctk.CTkButton(
            self.profile_photo_frame,
            text="Logout",
            font=("Poppins", 14),
            fg_color="#E63946",
            hover_color="#C92A3F",
            text_color="#FFFFFF",
            cursor="hand2",
            command=self.exit_main,
        ).pack(pady=10, side="bottom")

    def make_circle(self, image_path, size=(150, 150), border_width=4, border_color="lightgray"):
        """Make a smooth circular image with anti-aliasing and crisp border (fixed final size)."""
        img = Image.open(image_path).convert("RGBA")
        img = img.resize(size, Image.LANCZOS)

        # --- Create smooth circular mask ---
        scale = 8  # higher = smoother edges
        big_size = (size[0] * scale, size[1] * scale)
        mask = Image.new("L", big_size, 0)
        draw = ImageDraw.Draw(mask)

        # Shrink radius for inward border
        offset = border_width * scale
        draw.ellipse((offset, offset, big_size[0] - offset, big_size[1] - offset), fill=255)

        # Smooth edges by blurring before downscaling
        mask = mask.filter(ImageFilter.GaussianBlur(scale / 2))
        mask = mask.resize(size, Image.LANCZOS)

        # Apply circular mask to image
        circular_img = ImageOps.fit(img, size, centering=(0.5, 0.5))
        circular_img.putalpha(mask)

        # --- Create border mask ---
        border_mask = Image.new("L", big_size, 0)
        border_draw = ImageDraw.Draw(border_mask)
        border_draw.ellipse((0, 0, big_size[0], big_size[1]), fill=255)
        border_draw.ellipse((offset, offset, big_size[0] - offset, big_size[1] - offset), fill=0)

        # Smooth border edges
        border_mask = border_mask.filter(ImageFilter.GaussianBlur(scale / 2))
        border_mask = border_mask.resize(size, Image.LANCZOS)

        # Create border layer
        border_layer = Image.new("RGBA", size, border_color)
        border_layer.putalpha(border_mask)

        # Composite border behind circular image
        final_img = Image.alpha_composite(border_layer, circular_img)

        return final_img
    
    def show_profile_options(self, event=None):
        """Show a popup with options: view or upload profile picture."""
        popup = tk.Toplevel(self)
        popup.title("")
        popup.geometry("250x120+630+210")
        popup.resizable(False, False)
        popup.configure(bg="white")
        popup.grab_set()  # make it modal

        # See profile picture button
        ctk.CTkButton(
            popup,
            text="See Profile Picture",
            command=lambda: [popup.destroy(), self.view_profile_picture()],
        ).pack(pady=(20, 15))

        # Upload new photo button
        ctk.CTkButton(
            popup,
            text="Upload New Photo",
            fg_color="#4CAF50",
            hover_color="#388E3C",
            text_color="white",
            command=lambda: [popup.destroy(), self.change_profile_picture()],
        ).pack(pady=(0, 5))

    def view_profile_picture(self):
        """Open a window to preview the current profile picture with zoom/fullscreen support."""
        preview = tk.Toplevel(self)
        preview.title("Profile Picture")
        preview.configure(bg="white")
        preview.overrideredirect(True)

        # Load current saved profile picture
        img = Image.open(paths.IMAGE_EMPTY)
        preview.normal_size = (300, 300)
        preview.img = img  # keep reference to original image

        # Create small preview
        img_resized = img.resize(preview.normal_size, Image.LANCZOS)
        preview.img_tk = ImageTk.PhotoImage(img_resized)

        # Label to hold the image
        label = tk.Label(preview, image=preview.img_tk, bg="white")
        label.image = preview.img_tk
        label.pack(padx=20, pady=(20, 5))

        # Buttons
        btn_frame = tk.Frame(preview, bg="white")
        btn_frame.pack(pady=10)

        def zoom_toggle():
            """Toggle between preview size and fullscreen."""
            if getattr(preview, "is_zoomed", False):
                # Back to normal size
                img_resized = img.resize(preview.normal_size, Image.LANCZOS)
                preview.img_tk = ImageTk.PhotoImage(img_resized)
                label.configure(image=preview.img_tk)
                label.image = preview.img_tk
                preview.geometry("350x380")
                preview.is_zoomed = False
            else:
                # Fullscreen fit to screen
                screen_w = preview.winfo_screenwidth()
                screen_h = preview.winfo_screenheight()
                img_resized = img.copy()
                img_resized.thumbnail((screen_w - 100, screen_h - 100), Image.LANCZOS)
                preview.img_tk = ImageTk.PhotoImage(img_resized)
                label.configure(image=preview.img_tk)
                label.image = preview.img_tk
                preview.geometry(f"{screen_w}x{screen_h}")
                preview.is_zoomed = True

        # Zoom button
        zoom_btn = ctk.CTkButton(
            btn_frame,
            text="Zoom / Fullscreen",
            command=zoom_toggle,
            fg_color="#2196F3",
            hover_color="#1976D2",
            text_color="white"
        )
        zoom_btn.pack(side="left", padx=5)

        # Close button
        close_btn = ctk.CTkButton(
            btn_frame,
            text="Close",
            command=preview.destroy,
            fg_color="#E63946",
            hover_color="#C92A3F",
            text_color="white"
        )
        close_btn.pack(side="left", padx=5)

        # Set initial geometry
        preview.geometry("350x380")

    # def change_profile_picture(self, event=None):
    #     """Open file dialog to choose a new profile picture, update canvas, and persist."""
    #     file_path = filedialog.askopenfilename(
    #         title="Select Profile Picture",
    #         filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")],
    #     )
    #     if not file_path:
    #         return  # user cancelled

    #     # Save new image to persistent location
    #     from shutil import copyfile
    #     copyfile(file_path, paths.IMAGE_EMPTY)  # overwrite the profile placeholder

    #     # Re-generate circular image
    #     new_img = self.make_circle(paths.IMAGE_EMPTY, size=(150, 150), border_width=3, border_color="black")
    #     self.profile_tk = ImageTk.PhotoImage(new_img)

    #     # Update canvas image
    #     self.canvas.itemconfig(self.profile_image_id, image=self.profile_tk)

    def change_profile_picture(self, event=None):
        """Open file dialog to choose a new profile picture and update canvas."""
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif")],
        )
        if not file_path:
            return  # user cancelled

        # Make new circular image
        new_img = self.make_circle(file_path, size=(150, 150), border_width=3, border_color="black")
        self.profile_tk = ImageTk.PhotoImage(new_img)  # must keep a reference

        # Update canvas image
        self.canvas.itemconfig(self.profile_image_id, image=self.profile_tk)

    def exit_main(self):
        for child in self.winfo_toplevel().winfo_children():
            if hasattr(child, "cleanup"):
                child.cleanup()
        self.winfo_toplevel().main_page.logout()
