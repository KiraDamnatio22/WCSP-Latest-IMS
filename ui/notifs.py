import customtkinter as ctk

class ToolTip:
    def __init__(self, widget, text="", fg_color="black", text_color="white", idle_delay=1500):
        self.widget = widget
        self.text = text
        self.fg_color = fg_color
        self.text_color = text_color
        self.tip_window = None
        self.idle_delay = idle_delay  # hide after idle (ms)
        self._after_id = None

    def show_tip(self, text=None, fg_color=None, text_color=None, auto_hide=True):
        if text is not None:
            self.text = text
        if fg_color:
            self.fg_color = fg_color
        if text_color:
            self.text_color = text_color

        if not self.text:
            self.hide_tip()
            return

        # If switching from persistent to auto_hide, reset window
        if self.tip_window and auto_hide:
            self.hide_tip()

        if self.tip_window:
            # update existing tooltip
            for child in self.tip_window.winfo_children():
                if isinstance(child, ctk.CTkLabel):
                    child.configure(
                        text=self.text,
                        fg_color=self.fg_color,
                        text_color=self.text_color
                    )
        else:
            # create new tooltip window
            x = self.widget.winfo_rootx()
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

            self.tip_window = tw = ctk.CTkToplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.geometry(f"+{x}+{y}")

            label = ctk.CTkLabel(
                tw,
                text=self.text,
                fg_color=self.fg_color,
                text_color=self.text_color,
                corner_radius=6,
                padx=8,
                pady=4,
                font=("Poppins", 12)
            )
            label.pack()

        # 🔑 Start auto-hide only once (don’t reset every keystroke)
        if auto_hide and self.idle_delay > 0 and not self._after_id:
            self._after_id = self.widget.after(self.idle_delay, self.hide_tip)


    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

class CustomMessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message, on_confirm, msg1="Cancel", msg2="Yes, Delete", title_fg="#218838", msg1_fgcolor="#979da2", msg1_hovercolor="#7a7f85", msg2_fgcolor="#E63946", msg2_hovercolor="#C92A3F", message_pady=20, btn_pady=10, toplvl_width=400, toplvl_height=200, toplvl_posx=890, toplvl_posy=465, msg_font=("Poppins", 14)):
        super().__init__(parent)
        self.title(title)
        self.geometry(f"{toplvl_width}x{toplvl_height}+{toplvl_posx}+{toplvl_posy}")
        self.resizable(False, False)
        self.configure(fg_color="#F0F0F0")
        self.grab_set()
        self.overrideredirect(True)

        # Title label
        title_label = ctk.CTkLabel(
            self, 
            text=title, 
            font=("Poppins", 18, "bold"),
            text_color="white", 
            fg_color=title_fg, 
            corner_radius=5, 
            pady=10,
            bg_color=title_fg
        )
        title_label.pack(fill="x")

        # Message label
        message_label = ctk.CTkLabel(
            self, text=message, font=msg_font,
            text_color="black", wraplength=350, pady=0
        )
        message_label.pack(pady=message_pady)

        # Buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="#F0F0F0")
        button_frame.pack(pady=btn_pady)

        ctk.CTkButton(
            button_frame, text=msg1,
            fg_color=msg1_fgcolor, hover_color=msg1_hovercolor,
            font=("Poppins", 13, "bold"),
            text_color="white",
            bg_color="#F0F0F0",
            command=self.destroy
        ).grid(row=0, column=0, padx=8)

        ctk.CTkButton(
            button_frame, text=msg2,
            fg_color=msg2_fgcolor, hover_color=msg2_hovercolor,
            font=("Poppins", 13, "bold"),
            text_color="white",
            bg_color="#F0F0F0",
            command=on_confirm
        ).grid(row=0, column=1, padx=8)


class Toast(ctk.CTkToplevel):
    def __init__(self, parent, message, *, x=600, y=325, duration=1800,
                 bg_color="#218838", fg_color="#ffffff",
                 font=("Poppins", 14, "bold"), width=225, height=50,
                 on_close=None):   # <-- new arg
        super().__init__(parent)
        self.overrideredirect(True)
        self.lift()
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.0)

        self.x = x
        self.y = y
        self.on_close = on_close   # store callback

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

        self.update_idletasks()
        tw = self.winfo_reqwidth()
        th = self.winfo_reqheight()
        self.geometry(f"{tw}x{th}+{self.x}+{self.y}")

        # fade in
        self._fade(step=0.05, target=1.0, delay=10)

        # schedule fade-out
        self.after(duration, lambda: self._fade(
            step=-0.05,
            target=0.0,
            delay=10,
            on_done=self._finish
        ))

    def _fade(self, step, target, delay, on_done=None):
        alpha = self.attributes("-alpha") + step
        alpha = max(0.0, min(1.0, alpha))
        self.attributes("-alpha", alpha)
        if (step > 0 and alpha < target) or (step < 0 and alpha > target):
            self.after(delay, lambda: self._fade(step, target, delay, on_done))
        elif on_done:
            on_done()

    def _finish(self):
        self.destroy()
        if self.on_close:
            self.on_close()



