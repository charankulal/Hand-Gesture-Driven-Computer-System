import os.path
import tkinter as tk
from config import set_theme, set_global_status
import pywinstyles
from functools import partial
import customtkinter as ctk
from PIL import Image
from config import get_auth_photo, set_auth_photo
from face_auth import capture_face

THEME = "aero"
# THEME_VAR = tk.IntVar(value=0)

desc = [
    "I'm a passionate software crafter and tech-enthusiast. My mission is to create elegant solutions that make the world a better place in one line of code at time.",
    "Competent person with strong computer,communication, and time management abilities.Motivated and meticulous person who wants to apply analytical and problem-solving abilities to achieve objectives.",
    "A dedicated Computer Science student with a strong foundation in software development, specializing in web technologies and mobile app development. With a keen interest in creating intuitive user interfaces and efficient backend systems, this individual has demonstrated proficiency in languages such as JavaScript, Python, and Java. ",
    "An innovative Computer Science student focused on artificial intelligence and machine learning, with a passion for leveraging technology to solve complex problems. This student has gained expertise in Python, TensorFlow, and Keras through hands-on projects involving natural language processing and predictive analytics.",
    "Mr. Prasad S R received B.E degree from VTU Belagavi in 2011 and M. Tech degree from JNTU Hyderabad in 2015. His areas of interest are Deep Learning, IoT and AI\nHe is an Assistant Professor in the Department of Computer Science and Engineering at SDM Institute of Technology."
]

text_color = "#F0F0FF"
dark_grey_color = "#1A1A1A"
darker_color = "#010101"
red_color = "#F00F00"
light_color = "#F5F0F2"
widget_background = "transparent"
widget_border = "#FEFEFE"
widget_border_opacity = 0.4
widget_padding = 20
widget_margin = 10

about_text = "This project is an innovative project aiming to revolutionize the way you interact with your computer. Imagine controlling your digital world with a simple wave, tap, or twist of your hand. This project harnesses the power of machine learning to develop a real-time hand gesture recognition system, eliminating the need for keyboards and mice.\n\nOur mission is to create a seamless and intuitive user experience. This project fosters increased productivity and accessibility, especially for users with physical limitations."


# Generates a general frame with GCS status control.
def gen_frame(master):
    global about_text
    frame = ctk.CTkScrollableFrame(master)
    configure_frames(frame)
    heading = configure_heading(frame, "General").grid(row=0, column=0, sticky="n",
                                                       columnspan=3)  # Creates a heading widget labeled "General" inside the frame
    switch_var = ctk.StringVar(value="on")  # StringVar to track switch state, starting with "on"
    activation_toggle = ctk.CTkSwitch(frame, text="GCS Status", variable=switch_var, onvalue="on", offvalue="off",
                                      font=("Ariel", 30), command=lambda s=switch_var:set_global_status(s.get())).grid(row=1, column=2, sticky="se")
    # frame.rowconfigure([0,1,2])
    frame.columnconfigure(0, weight=2)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=1)
    # general_info = ctk.CTkFrame(frame).grid(row=2,column=1, sticky="we")

    theme_frame = ctk.CTkFrame(frame)
    theme_frame.grid(row=2, column=0, sticky="ew", columnspan=3)

    info = ctk.CTkLabel(theme_frame, corner_radius=5, text_color="#FFFFFF", text="THEMES", wraplength=500, padx=20,
                        pady=20,
                        font=("Ariel", 32)).grid(row=0, column=0, sticky="ne")
    # info.grid(row=0,column=0, columnspan=3)
    theme = themes_gen(frame)
    theme.grid(row=3, column=0, sticky="nsew", columnspan=3)
    return frame


# Creates an authentication scrollable frame.
def auth_frame(master):
    frame = ctk.CTkScrollableFrame(master)
    configure_frames(frame)
    configure_heading(frame, "Authentication settings").grid(row=0, column=0, sticky="n", columnspan=3)
    frame.columnconfigure(0, weight=2)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=1)

    # Card
    comp = ctk.CTkFrame(frame)
    comp.grid(row=2, column=0, columnspan=3, sticky="new")
    # Photo
    pic = None
    if os.path.isfile("DP.jpg"):
        img = Image.open("DP.jpg")
        set_auth_photo(img)
        pic = ctk.CTkImage(get_auth_photo(),size=(500,500))
    else:
        pic = ctk.CTkLabel(comp, text="No Admin Registered")

    ctk.CTkLabel(comp,image=pic, text='').grid(row=0,column=0)
    # Change Button
    sub_comp = ctk.CTkLabel(comp, text='',padx=30)
    sub_comp.grid(row=0, column=1, sticky="nsw")
    ctk.CTkLabel(sub_comp,text="Admin",font=("Helvetica",30)).grid(row=0, column=0, sticky="ew", padx=30)
    btn = ctk.CTkButton(sub_comp, text="Change Admin", command=capture_face,font=("Helvetica",30))
    btn.grid(row=1, column=0, sticky="ew")
    # Name
    return frame


# Produces a frame for managing gesture controls.
def about_frame(master):
    global about_text
    frame = ctk.CTkScrollableFrame(master)
    configure_frames(frame)
    heading = configure_heading(frame, "About Us").grid(row=0, column=0, sticky="n", columnspan=3)
    frame.columnconfigure(0, weight=2)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=1)

    desc_frame = ctk.CTkFrame(frame)
    desc_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
    about_project_heading = ctk.CTkLabel(desc_frame, corner_radius=5, text_color="#FFFFFF", text="Why this project?",
                                         padx=20, pady=20,
                                         font=("Ariel", 32), fg_color="transparent").grid(row=0, column=0, sticky="new")
    ctk.CTkFrame(frame, border_color="#FFFFFF", height=2, fg_color="#FFFFFF").grid(row=3, column=0, columnspan=3,
                                                                                   sticky="ew")
    about_project = ctk.CTkTextbox(frame)
    about_project.grid(row=4, column=0, columnspan=3, sticky="sew")
    about_project.insert(0.0, about_text)
    about_project.configure(state="disabled", font=("Helvetica", 20), wrap="word", text_color="#FFFFFF", padx=20,
                            pady=20, fg_color="transparent", height=180)

    dev_title_frame = ctk.CTkFrame(frame)
    dev_title_frame.grid(row=5, column=0, columnspan=3, sticky="new")
    dev_title = ctk.CTkLabel(dev_title_frame, corner_radius=5, text_color="#FFFFFF", text="Contributing developers",
                             padx=20, pady=20,
                             font=("Ariel", 32), fg_color="transparent").grid(row=0, column=0, sticky="new")
    ctk.CTkFrame(frame, border_color="#FFFFFF", height=2, fg_color="#FFFFFF").grid(row=6, column=0, columnspan=3,
                                                                                   sticky="ew")

    charan_img = Image.open("./Icons/Charan.JPG")
    charan_dev = developer_card(frame, "Charan", charan_img, desc[0])

    charan_dev.grid(row=7, column=0, columnspan=3, sticky="ew")

    g_img = Image.open("./Icons/GhanashyamaKPMakkithaya.jpg")
    g_dev = developer_card(frame, "Ghanashyama K P Makkithaya", g_img, desc[1])

    g_dev.grid(row=8, column=0, columnspan=3, sticky="ew")

    k_img = Image.open("./Icons/Keerthana.jpg")
    k_dev = developer_card(frame, "Keerthana M S", k_img, desc[2])
    k_dev.grid(row=9, column=0, columnspan=3, sticky="ew")

    l_img = Image.open("./Icons/Larine.jpg")
    l_dev = developer_card(frame, "Larine Theresa Pereira", l_img, desc[3])
    l_dev.grid(row=10, column=0, columnspan=3, sticky="ew")

    guide_title_frame = ctk.CTkFrame(frame)
    guide_title_frame.grid(row=11, column=0, columnspan=3, sticky="new")
    ctk.CTkLabel(guide_title_frame, corner_radius=5, text_color="#FFFFFF", text="Project Guide",
                 padx=20, pady=20,
                 font=("Ariel", 32), fg_color="transparent").grid(row=0, column=0, sticky="new")
    ctk.CTkFrame(frame, border_color="#FFFFFF", height=2, fg_color="#FFFFFF").grid(row=12, column=0, columnspan=3,
                                                                                   sticky="ew")

    guide_img = Image.open("./Icons/Guide.jpg")
    guide_dev = developer_card(frame, "Prof. Prasad S R", guide_img, desc[4], sub="Asst. Professor, SDMIT, Ujire")
    guide_dev.grid(row=13, column=0, columnspan=3, sticky="ew")

    return frame


def help_frame(master):
    frame = ctk.CTkScrollableFrame(master)  ## Initializes a scrollable frame using the `ctk` library,
    configure_frames(frame)
    heading = configure_heading(frame, "Help").grid(row=0, column=0, sticky="n", columnspan=3)
    frame.columnconfigure(0, weight=2)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=1)

    dev_title_frame = ctk.CTkFrame(frame)
    dev_title_frame.grid(row=2, column=0, columnspan=3, sticky="new")
    dev_title = ctk.CTkLabel(dev_title_frame, corner_radius=5, text_color="#FFFFFF", text="Basic Controls",
                             padx=20, pady=20,
                             font=("Ariel", 32), fg_color="transparent").grid(row=0, column=0, sticky="new")
    ctk.CTkFrame(frame, border_color="#FFFFFF", height=2, fg_color="#FFFFFF").grid(row=3, column=0, columnspan=3,
                                                                                   sticky="ew")

    help_card(frame, name="Cursor control", control="Use of index and middle fingers",description= "Use index finger and middle finger and move to change the position of the cursor on the system.", hands="Any one of the hands", number=1).grid(row=4, column=0, columnspan=3, sticky="ew")
    help_card(frame, name="Left Click", control="Use of index and middle fingers",description= "Use index finger and middle finger and move to change the position of the cursor on the system.", hands="Any one of the hands", number=2).grid(row=5, column=0, columnspan=3, sticky="ew")
    help_card(frame, name="Right Click", control="Use of index, middle, and little fingers",description= "Use index finger and middle finger and move to change the position of the cursor on the system.", hands="Any one of the hands", number=3).grid(row=6, column=0, columnspan=3, sticky="ew")
    help_card(frame, name="Volume control", control="Use of index and thumb fingers",description= "Use index finger and middle finger and move to change the position of the cursor on the system.", hands="Right Hand only", number=4).grid(row=7, column=0, columnspan=3, sticky="ew")
    help_card(frame, name="Brightness control", control="Use of index and thumb fingers",description= "Use index finger and middle finger and move to change the position of the cursor on the system.", hands="Left hand only", number=5).grid(row=8, column=0, columnspan=3, sticky="ew")
    help_card(frame, name="Next Slide", control="Use of index, middle and ring fingers",description= "Use index finger and middle finger and move to change the position of the cursor on the system.", hands="Right hand only", number=6).grid(row=9, column=0, columnspan=3, sticky="ew")
    help_card(frame, name="Previous Slide", control="Use of index, middle and ring fingers",description= "Use index finger and middle finger and move to change the position of the cursor on the system.", hands="Left hand only", number=7).grid(row=10, column=0, columnspan=3, sticky="ew")


    return frame


def others_frame(master):
    frame = ctk.CTkScrollableFrame(master)
    configure_frames(frame)
    heading = configure_heading(frame, "Contact Us").grid(row=0, column=0, sticky="n", columnspan=3)
    frame.columnconfigure(0, weight=2)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=1)

    icon = Image.open("./Icons/editor.ico")
    title = developer_card(frame, "Share your experiences and feedback", icon, sub="", about="Let us know your opinions and feedback for futher improvement of this project and for your better experience.\n\nMail: gmakkithaya@gmail.com\nPh No: 8050475723")

    title.grid(row=2, column=0, columnspan=3, sticky="ew")
    return frame


# Load default configuration of frames
def configure_frames(f: ctk.CTkScrollableFrame):
    f.configure(corner_radius=4)
    f.configure(border_width=0)
    f.configure(fg_color="black")
    f.configure(scrollbar_fg_color=darker_color)
    f.configure(scrollbar_button_color=red_color)
    f.configure(scrollbar_button_color=red_color)
    f.configure(scrollbar_button_hover_color=light_color)
    f.configure(scrollbar_button_hover_color=light_color)
    f.configure(label_text_color=text_color)
    f.configure(label_anchor="n")
    # f.configure(orientation="vertical")


##Configuring style of heading
def configure_heading(master, heading):
    return ctk.CTkLabel(master,
                        text=heading,
                        font=('Comic Sans', 50, 'bold'),
                        anchor='center')


def developer_card(master, name, pic, about, sub="B.E CSE, SDMIT (2020-2024)"):
    card_frame = ctk.CTkFrame(master)
    card_frame.columnconfigure(0, weight=0)
    card_frame.columnconfigure(1, weight=2)
    card_frame.columnconfigure(2, weight=2)

    card_frame.rowconfigure(0, weight=0)

    dev_pic_frame = ctk.CTkFrame(card_frame)
    dev_pic_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    img = ctk.CTkImage(pic, size=(200, 200))
    img_label = ctk.CTkLabel(dev_pic_frame, image=img, text="")
    img_label.grid(row=0, column=0, sticky="nsew")

    dev_title_frame = ctk.CTkFrame(card_frame)
    dev_title_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")
    dev_title = ctk.CTkLabel(dev_title_frame, corner_radius=5, text_color="#FFFFFF", text=name,
                             padx=20, pady=5,
                             font=("Ariel", 32), fg_color="transparent").grid(row=0, column=0, sticky="nsw")
    dev_title = ctk.CTkLabel(dev_title_frame, corner_radius=5, text_color="#FFFFFF", text=sub, padx=30, pady=5,
                             font=("Ariel", 16), fg_color="transparent").grid(row=1, column=0, sticky="nsew")

    dev_desc = ctk.CTkTextbox(card_frame, height=100)
    dev_desc.grid(row=1, column=1, columnspan=2, sticky="nsew")
    dev_desc.insert(0.0, about)
    dev_desc.configure(state="disabled", font=("Helvetica", 20))

    return card_frame


#

#
def themes_gen(master):
    # global THEME_VAR
    THEME_VAR = tk.IntVar(value=0)
    frame = ctk.CTkFrame(master)
    frame1 = ctk.CTkLabel(frame, bg_color="transparent", padx=20, pady=20, anchor="ne", justify="left", compound="left", text="")
    frame2 = ctk.CTkLabel(frame, bg_color="transparent", padx=20, pady=20, anchor="ne", justify="left", compound="left", text="")
    frame3 = ctk.CTkLabel(frame, bg_color="transparent", padx=20, pady=20, anchor="ne", justify="left", compound="left", text="")
    frame4 = ctk.CTkLabel(frame, bg_color="transparent", padx=20, pady=20, anchor="ne", justify="left", compound="left", text="")
    frame5 = ctk.CTkLabel(frame, bg_color="transparent", padx=20, pady=20, anchor="ne", justify="left", compound="left", text="")
    frame1.grid(row=0,column=0)
    frame2.grid(row=1,column=0)
    frame3.grid(row=2,column=0)
    frame4.grid(row=3,column=0)
    frame5.grid(row=4,column=0)
    ctk.CTkRadioButton(frame1, text="Dark", command=lambda theme=1: set_theme(theme), variable=THEME_VAR,
                       value=1, font=('Ariel', 20)).grid(row=0, column=0, sticky="nsew")
    ctk.CTkRadioButton(frame2, text="Acrylic", command=lambda theme=2: set_theme(theme), variable=THEME_VAR,
                       value=2, font=('Ariel', 20)).grid(row=0, column=0, sticky="nsew")
    ctk.CTkRadioButton(frame3, text="Aero (GPU Heavy)", command=lambda theme=3: set_theme(theme),
                       variable=THEME_VAR, value=3, font=('Ariel', 20)).grid(row=0, column=0,sticky="nsew")
    ctk.CTkRadioButton(frame4, text="Transparent (GPU Heavy)", command=lambda theme=4: set_theme(theme),
                       variable=THEME_VAR,
                       value=4, font=('Ariel', 20)).grid(row=0, column=0, sticky="nsew")
    ctk.CTkRadioButton(frame5, text="Optimised", command=lambda theme=5: set_theme(theme), variable=THEME_VAR,
                       value=5, font=('Ariel', 20)).grid(row=0, column=0, sticky="nsew")

    return frame


def help_card(master, name, control, description, hands, number=1):
    card_frame = ctk.CTkFrame(master)
    card_frame.columnconfigure(0, weight=1)
    card_frame.columnconfigure(1, weight=1)
    card_frame.columnconfigure(2, weight=4)

    card_frame.rowconfigure(0, weight=0)

    name_frame = ctk.CTkFrame(card_frame)
    name_frame.grid(row=0, column=0,rowspan=2, sticky="ew")
    title = ctk.CTkLabel(name_frame, text=number,font=("Helvetica", 48), padx= 20).grid(row=0, column=0, sticky="ne")
    name_title = ctk.CTkLabel(name_frame, text=name,font=("Helvetica", 30))
    name_title.grid(row=0, column=1, sticky="ns")

    ctrl_frame = ctk.CTkFrame(card_frame)
    ctrl_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")
    ctrl_title = ctk.CTkLabel(ctrl_frame, corner_radius=5, text_color="#FFFFFF", text=control,
                             padx=20, pady=5,
                             font=("Ariel", 20), fg_color="transparent").grid(row=0, column=0, sticky="nsw")
    hands_title = ctk.CTkLabel(ctrl_frame, corner_radius=5, text_color="#FFFFFF", text=hands, padx=30, pady=5,
                             font=("Ariel", 16), fg_color="transparent").grid(row=1, column=0, sticky="nsew")

    descr = ctk.CTkTextbox(card_frame, height=100)
    descr.grid(row=1, column=1, columnspan=2, sticky="nsew")
    descr.insert(0.0, description)
    descr.configure(state="disabled", font=("Helvetica", 20))

    return card_frame