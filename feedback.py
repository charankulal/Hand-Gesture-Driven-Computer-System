import customtkinter as ctk
import tkinter as tk
import pyautogui as pag
import pywinstyles
from functools import partial
from notifypy import Notify
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
from threading import Timer
# import pythoncom
from PIL import Image

#
#
screensize = pag.size()
# # Set the appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
#
# # Create a CTk window
# app = ctk.CTk()
#
# # Set the window geometry
# app.geometry("400x240")
#
curr_toast = None
posX = screensize.width // 2 - 100
posY = screensize.height - 100
print(posX, posY)


# percent = tk.StringVar()
# Function to create and configure toast


def toast(master, size="small"):
    flyout = ctk.CTkToplevel(master)
    flyout.attributes("-topmost", True)
    flyout.overrideredirect(True)
    pywinstyles.apply_style(flyout, style="acrylic")
    # pywinstyles.change_border_color(flyout,color="#ffffff")
    if size == "small":
        flyout.geometry(f"200x50+{posX}+{posY}")
    elif size == "large":
        flyout.geometry(f"400x150+{posX - 100}+{posY - 100}")
    return flyout


large_msg = "This is a very long and not so important message but the user has to know what is going on. Therefore we are letting user know through this message."


def small_toast(obj):
    obj.geometry(f"200x50+{posX}+{posY}")


def large_toast(obj):
    obj.geometry(f"400x150+{posX - 100}+{posY - 100}")


# Toast function with message
def msg_toast(master, msg):
    global curr_toast, posX, posY
    if curr_toast:
        curr_toast.destroy()

    if len(msg) >= 60:
        flyout = toast(master, "large")
    else:
        flyout = toast(master, "small")
    curr_toast = flyout
    flyout.after(50, partial(fade, flyout))

    # Create a label in the new window
    label = ctk.CTkLabel(flyout, text=msg, fg_color="#FF0000", anchor="center", padx="10", pady="20", wraplength=180)
    label.pack()
    label.configure(font=("Arial", 16, "bold"))


#
# def progress_toast(master):
#     ico = Image.open("./Icons/mixer.ico")
#     App_Icon = ctk.CTkImage(light_image=ico,
#                         dark_image=ico)
#     global curr_toast,percent
#     if curr_toast:
#         curr_toast.destroy()
#
#     flyout = toast(master=master)
#     small_toast(flyout)
#     curr_toast = flyout
#     # Timer(0.1,update_volume_label).start()
#     flyout.after(100,update_volume_label)
#     flyout.after(150,partial(fade ,flyout))
#     label = ctk.CTkLabel(flyout, textvariable = percent, anchor="center", padx=10,pady=20, image=App_Icon, compound="left")
#     # label.bind(command=progressLevel)
#     label.pack()
#     label.configure(font=("Arial", 16, "bold"))


# Notification function
def notification(title="Hand Gesture Application", msg=""):
    notif = Notify()
    notif.title = title
    notif.message = msg
    notif.send()


#
# # Define a function to be called when the button is pressed
# def button_function_long():
#     msg_toast(app, large_msg)
#     # pag.press("volumeup")
#
# def button_function_short():
#     msg_toast(app, "A short message for users.")
#     # pag.press("volumedown")
#
#     # Create a slider and bind it to the volume and brightness control.

def fade(master):
    global curr_toast
    alpha = master.attributes('-alpha')
    # print(alpha)
    if alpha > 0.00001:
        master.attributes('-alpha', alpha - 0.01 * (1 / (1.5 * alpha)))
        master.after(50, partial(fade, master))
    else:
        master.destroy()
        curr_toast = None
# # Create a CTkButton and place it in the center of the window
# button = ctk.CTkButton(master=app, text="Flyout (long)", command=button_function_long)
# button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
#
# button = ctk.CTkButton(master=app, text="Flyout (short)", command=button_function_short)
# button.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)
#
# button = ctk.CTkButton(master=app, text="Notify", command=partial(notification,msg="Hey user, you have been notified !!"))
# button.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)
#
#
#
# # Start the main event loop
# app.after(100,update_volume_label)
# app.mainloop()
