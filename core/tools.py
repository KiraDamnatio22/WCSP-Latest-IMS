import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps

def resize_image(img_path, img_size):
    image = Image.open(img_path)
    resized = image.resize(img_size, Image.LANCZOS)
    output_img = ctk.CTkImage(light_image=resized, dark_image=resized, size=(img_size))
    return output_img

class CustomizeProfile():
    def __init__(self):
        pass 

    def make_circle(self, image_path, size=(150, 150)):
        # Open image
        img = Image.open(image_path).convert("RGBA")
        img = img.resize(size, Image.LANCZOS)

        # Create circular mask with higher resolution (anti-aliasing)
        scale = 4  # scaling factor for smooth edges
        big_size = (size[0] * scale, size[1] * scale)
        mask = Image.new("L", big_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + big_size, fill=255)

        # Downscale mask to target size with smooth edges
        mask = mask.resize(size, Image.LANCZOS)

        # Apply mask to image
        circular_img = ImageOps.fit(img, size, centering=(0.5, 0.5))
        circular_img.putalpha(mask)

        return circular_img
    