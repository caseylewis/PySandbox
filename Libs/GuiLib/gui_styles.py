from tkinter import *


# todo finish style keys
class StyleKeys:
    WIDTH = 'width'
    HEIGHT = 'height'


# todo finish grid keys
class GridKeys:
    STICKY = 'sticky'
    PADY = 'pady'
    PADX = 'padx'


# FONT STYLES
standard_font = "Helvetica"
mono_spaced_font = "Consolas"

h1 = 12
h2 = 10
h3 = 8

# COLOR SCHEME
root_bg = '#484848'

primary = '#455a64'
p_light = '#718792'
p_dark = '#1c313a'
p_text = '#ffffff'

secondary = '#0d47a1'
s_light = '#5472d3'
s_dark = '#002171'
s_text = '#ffffff'

# DEFAULT VALUES FOR CERTAIN ATTRIBUTES
def_width = 20
def_pady = 5
def_padx = 5

# FRAME
style_frame_primary = {
    'bg': p_dark,
}

style_frame_secondary = {
    'bg': s_dark,
}

grid_frame_primary = {
    'sticky': 'nsew',
    'pady': 0,
    'padx': 0,
}

grid_frame_secondary = {
    'sticky': 'nsew',
    'pady': 5,
    'padx': 5,
}

grid_frame_padonly = {
    'pady': 0,
    'padx': 0,
}

# LABEL
style_lbl = {
    'font': (standard_font, h2),
    'bg': p_dark,
    'fg': p_text,
    'width': def_width,  # SEE STYLE CHECKBUTTON BEFORE CHANGING
    'relief': RIDGE,
    'bd': 2,
    'anchor': CENTER,
}

grid_lbl = {
    'sticky': 'nsew',
    'pady': 5,
    'padx': 5,
}

style_lbl_title = {
    'bg': style_frame_primary['bg'],
    'fg': p_text,
    'font': (standard_font, h1),
    'relief': FLAT,
    'bd': 4,
    'anchor': W,
}

# BUTTON
style_btn = {
    'bg': primary,
    'fg': p_text,
    'font': (standard_font, h2),
    'width': def_width,
    'justify': CENTER,
    'relief': RAISED,
    'height': 1,
}

grid_btn = {
    'sticky': 'nsew',
    'pady': 5,
    'padx': 5,
}

# NAVIGATION BUTTON
style_navbtn = {
    'bg': s_dark,
    'fg': s_text,
    'font': (standard_font, h1),
    'width': def_width,
    'justify': CENTER,
    'relief': RAISED,
    'height': 1,
}

grid_navbtn = {
    'sticky': 'nsew',
    'pady': 0,
    'padx': 0,
}

# DROPDOWN
style_dropdown = {
    'bg': primary,
    'font': (standard_font, h2),
    'width': 15,
    'bd': 0,
}

grid_dropdown = {
    'sticky': 'nsew',
    'pady': 0,
    'padx': 0,
}

# CHECKBUTTON
style_checkbtn = {
    'bg': p_dark,
    'selectcolor': p_dark,  # FOR THE BG COLOR OF THE LITTLE BOX
    'fg': p_text,  # FONT COLOR AND CHECK COLOR
    'font': (standard_font, h2),
    'bd': 2,
    'width': def_width-3,
    'justify': CENTER,
    'relief': RAISED,
    'height': 1,
    'anchor': W,
}

grid_checkbtn = {
    'sticky': 'nsew',
    'pady': 5,
    'padx': 10,
}

# ENTRY
style_entry = {
    'bg': 'white',
    'fg': 'black',
    'font': (standard_font, h2),
    'width': def_width,
}

grid_entry = {
    'sticky': 'ew',
    'pady': 6,
    'padx': 5,
}

# LOGGER
style_logger = {
    'bg': 'white',
    'fg': 'black',
    'height': 10,
    'font': (standard_font, h2),
    'width': def_width,
}

grid_logger = {
    'sticky': 'nsew',
    'pady': 5,
    'padx': 2,
}


def copy_dict(dict):
    new_dict = {}
    for key, value in dict.items():
        new_dict[key] = value
    return new_dict


if __name__ == '__main__':
    root = Tk()
    root.title("Test App")
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # FRAMES
    frame_1 = Frame(root, **style_frame_primary)
    frame_1.grid(row=0, column=0, **grid_frame_secondary)
    frame_1.grid_columnconfigure(0, weight=1)
    frame_1.grid_columnconfigure(1, weight=1)

    frame_2 = Frame(root, **style_frame_primary)
    frame_2.grid(row=0, column=1, **grid_frame_secondary)
    frame_2.grid_columnconfigure(0, weight=1)
    frame_2.grid_columnconfigure(1, weight=1)

    frame_3 = Frame(root, **style_frame_primary)
    frame_3.grid(row=1, column=0, **grid_frame_secondary)
    frame_3.grid_columnconfigure(0, weight=1)
    frame_3.grid_columnconfigure(1, weight=1)

    frame_4 = Frame(root, **style_frame_primary)
    frame_4.grid(row=1, column=1, **grid_frame_secondary)
    frame_4.grid_columnconfigure(0, weight=1)
    frame_4.grid_columnconfigure(1, weight=1)

    # FRAME 1 CHILD WIDGETS
    frame_1_title_lbl = Label(frame_1, text="Frame 1", **style_lbl_title)
    frame_1_title_lbl.grid(row=0, column=0, columnspan=2, **grid_lbl)

    frame_1_lbl = Label(frame_1, text="Label 1", **style_lbl)
    frame_1_lbl.grid(row=1, column=0, **grid_lbl)

    frame_1_entry = Entry(frame_1, **style_entry)
    frame_1_entry.grid(row=1, column=1, **grid_entry)

    frame_1_btn = Button(frame_1, text="Test Btn 1", **style_btn)
    frame_1_btn.grid(row=2, column=0, **grid_btn)

    frame_1_dropdown_var = StringVar()
    frame_1_dropdown = OptionMenu(frame_1, frame_1_dropdown_var, *['1', '2', '3'])
    frame_1_dropdown.config(**style_dropdown)
    frame_1_dropdown.grid(row=3, column=0, **grid_dropdown)

    frame_1_checkbtn = Checkbutton(frame_1, **style_checkbtn)
    frame_1_checkbtn.grid(row=3, column=1, **grid_checkbtn)

    frame_1_logger = Text(frame_1, **style_logger)
    frame_1_logger.grid(row=4, column=0, columnspan=2, **grid_logger)

    # FRAME 2 CHILD WIDGETS
    frame_2_title_lbl = Label(frame_2, text="Frame 2", **style_lbl_title)
    frame_2_title_lbl.grid(row=0, column=0, columnspan=2, **grid_lbl)

    frame_2_lbl = Label(frame_2, text="Label 2", **style_lbl)
    frame_2_lbl.grid(row=1, column=0, **grid_lbl)

    frame_2_entry = Entry(frame_2, **style_entry)
    frame_2_entry.grid(row=1, column=1, **grid_entry)

    # FRAME 3 CHILD WIDGETS
    frame_3_title_lbl = Label(frame_3, text="Frame 2", **style_lbl_title)
    frame_3_title_lbl.grid(row=0, column=0, columnspan=2, **grid_lbl)

    frame_3_lbl = Label(frame_3, text="Label 2", **style_lbl)
    frame_3_lbl.grid(row=1, column=0, **grid_lbl)

    frame_3_entry = Entry(frame_3, **style_entry)
    frame_3_entry.grid(row=1, column=1, **grid_entry)

    # FRAME 4 CHILD WIDGETS
    frame_4_title_lbl = Label(frame_4, text="Frame 2", **style_lbl_title)
    frame_4_title_lbl.grid(row=0, column=0, columnspan=2, **grid_lbl)

    frame_4_lbl = Label(frame_4, text="Label 2", **style_lbl)
    frame_4_lbl.grid(row=1, column=0, **grid_lbl)

    frame_4_entry = Entry(frame_4, **style_entry)
    frame_4_entry.grid(row=1, column=1, **grid_entry)

    root.mainloop()
