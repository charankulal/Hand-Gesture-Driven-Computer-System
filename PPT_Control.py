import pygetwindow as gw

def is_powerpoint_in_presentation_mode():
    # Get a list of all open windows
    windows = gw.getAllWindows()

    # Iterate through the windows and check if any contain "PowerPoint Slide Show" in the title
    for window in windows:
        if "PowerPoint Slide Show" in window.title:
            return True
    return False  # If no PowerPoint presentation window is found

# Example usage
while True:
    if is_powerpoint_in_presentation_mode():
        print("PowerPoint is in presentation mode.")

