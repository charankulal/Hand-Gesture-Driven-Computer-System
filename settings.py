import asyncio
import threading
import time
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
import frames as f
from screeninfo import get_monitors
import pywinstyles
from PIL import Image, ImageTk, ImageDraw, ImageOps
from config import set_theme_change_flag, get_theme_change_flag, get_theme, set_root

# THEME = "aero"
# THEME_VAR = tk.IntVar(value=0)
root = None


def settings():
    global root
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("dark-blue")
    primary_window = get_monitors()[0]

    # Root Window
    root = ctk.CTk()
    # task = asyncio.create_task(change_theme(root))
    set_root(root)

    # Top left window Icon
    ico = Image.open("./Icons/lists.ico")
    # App_Icon = ctk.CTkImage(light_image=ico,
    #                         dark_image=ico)

    # Root window Attributes/Properties
    root.iconbitmap("./Icons/lists.ico")
    root.config(background='#1a1a1a')
    root.title("GCS")
    root.minsize(int(primary_window.width / 2), int(primary_window.height / 2))
    root.geometry(f"{primary_window.height // 2}x{primary_window.width // 2}")
    root.after(0, lambda: root.state('zoomed'))
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    pywinstyles.apply_style(root, style="optimised")
    pywinstyles.change_border_color(root, color="#101010")

    # Tabs
    menu_buttons_frame = ctk.CTkFrame(root)
    # menu_buttons_frame.pack(fill="y",expand=True, side="left")
    menu_buttons_frame.grid(row=0, column=0, sticky="nsew")
    menu_buttons_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)
    pywinstyles.apply_style(menu_buttons_frame, style="optimised")

    content_frame = ctk.CTkFrame(root)
    # content_frame.configure(fg_color="#FF0FF0")
    # pywinstyles.set_opacity(menu_buttons_frame,value=0.4)
    content_frame.grid(row=0, column=1, sticky="nsew")
    content_frame.rowconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=1)

    # ID, key pairs for frame
    frame_id = {
        0: "Gen",
        1: "Auth",
        2: "Abo",
        3: "Help",
        4: "Contact"
    }

    frame_names = ("General", "Authentication", "About", "Help", "Contact")

    # All frames with content
    frames = {}
    frames["Gen"] = f.gen_frame(root)
    frames["Auth"] = f.auth_frame(content_frame)
    frames["Abo"] = f.about_frame(content_frame)
    frames["Help"] = f.help_frame(content_frame)
    frames["Contact"] = f.others_frame(content_frame)

    # ("Gen", "Auth", "Ges","Help","Others")

    # To show particular frame

    def display_frame(id):
        for i in frames.keys():
            frames[i].grid_forget()

        frames[id].grid(row=0, column=1, sticky="nsew")

    for i in range(5):
        btn = ctk.CTkButton(menu_buttons_frame,
                            text=frame_names[i],
                            command=lambda id=frame_id[i]: display_frame(id=id),
                            font=('Ariel', 30))
        pywinstyles.set_opacity(btn.winfo_id(), value=1, color="#000000")
        btn.grid(row=i, column=0, pady=5, sticky="nsew")
    frames["Gen"].grid(row=0, column=1, sticky="nsew")
    frames["Gen"].lift()

    root.mainloop()


def change_theme():
    global root

    while True:
        if root is None:
            continue
        else:
            # print("Applied theme, ",get_theme())
            pywinstyles.apply_style(root, get_theme())
            # if get_theme() == set_theme():
            #     set_theme_change_flag(0)

            time.sleep(1)


theme_thread = threading.Thread(target=change_theme).start()
settings()
