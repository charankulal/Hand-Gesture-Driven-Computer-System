AUTH = 0
AUTH_FRAME = None
STATUS = 1

THEMES = {
    1: "mica",
    2: "acrylic",
    3: "aero",
    4: "transparent",
    5: "optimised"
}

GLOBAL_THEME = "optimised"
THEME_CHANGE_FLAG = 0
ROOT_WIN = None
def get_root():
    global ROOT_WIN
    return ROOT_WIN

def set_root(r):
    global ROOT_WIN
    ROOT_WIN = r
def get_auth():
    global AUTH
    return AUTH


def set_auth(a):
    global AUTH
    AUTH = a


def set_auth_frame(f):
    global AUTH_FRAME
    AUTH_FRAME = f


def get_auth_frame():
    global AUTH_FRAME
    return AUTH_FRAME


def set_theme(s):
    global THEMES,GLOBAL_THEME, THEME_CHANGE_FLAG
    GLOBAL_THEME = THEMES[s]
    print("Set theme")
    THEME_CHANGE_FLAG = 1


def get_theme():
    global GLOBAL_THEME
    return GLOBAL_THEME


def get_theme_change_flag():
    global THEME_CHANGE_FLAG
    return THEME_CHANGE_FLAG


def set_theme_change_flag(s=0):
    global THEME_CHANGE_FLAG
    print("Theme flag set ",s)
    THEME_CHANGE_FLAG = s


def set_global_status(s):
    global STATUS
    if s == "on":
        STATUS = 1
        print("Changed to",STATUS)
    else:
        STATUS = 0
        print("Changed to",STATUS)

def get_global_status():
    global STATUS
    return STATUS

# Authentication Panel Settings
AUTH_PHOTO = None
AUTH_NAME = None
AUTH_BUTTON_STATUS = "Disabled"
def get_auth_photo():
    global AUTH_PHOTO
    return AUTH_PHOTO

def set_auth_photo(p):
    global AUTH_PHOTO
    AUTH_PHOTO = p

def get_auth_name():
    global AUTH_NAME
    return AUTH_NAME

def set_auth_name(n):
    global AUTH_NAME
    AUTH_NAME = n

def get_auth_btn_status():
    global AUTH_BUTTON_STATUS
    return AUTH_BUTTON_STATUS

def set_auth_btn_status(a):
    global AUTH_BUTTON_STATUS
    AUTH_BUTTON_STATUS = a

