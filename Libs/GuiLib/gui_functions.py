import platform
from abc import abstractmethod
from tkinter import *
from Libs.GuiLib.gui_styles import *


########################################################################################################################
# GUI FUNCTIONS
########################################################################################################################
def focus_in(widget):
    bg = "white"
    if widget['bg'] != bg:
        widget['bg'] = bg


def focus_out(widget):
    focus_out_bg = 'red'
    text = widget.get()
    if text == '':
        widget['bg'] = focus_out_bg


def to_upper(textvariable):
    textvariable.set(textvariable.get().upper())


def first_to_upper(textvariable):
    if len(textvariable.get()) == 1:
        textvariable.set(textvariable.get().upper())


def center_on_screen(toplevel):
    """
    Centers the passed Tkinter widget on the screen
    :param toplevel: Tk or Toplevel Tkinter widget to center in the screen
    :return:
    """
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))


def get_screen_size(root):
    """
    Get the screen height and width.
    :param root: Main Tk Window
    :return: screenwidth, screenheight
    """
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return width, height


def copy_dict(dict):
    new_dict = {}
    for key, value in dict.items():
        new_dict[key] = value
    return new_dict


if __name__ == '__main__':
    from Libs.GuiLib.gui_styles import *

    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # CREATE NAVIGABLETKAPP()
    app = NavigableTkFrame(root)
    app.grid(row=0, column=0, sticky='nsew')

    app.config(bg='black')
    app.set_nav_btn_style(**style_navbtn)
    app.set_pad(10, 10)
    # root.set_sub_frame_bg(SUB_FRAME_BG)
    # root.set_nav_btn_pad((10, 0), 0)
    # root.set_nav_bar_bg('green')

    # FIRST FRAME
    first_content_frame = ContentFrame(app.content_frame, "1st Content Frame", **style_frame_primary)
    first_content_frame.grid_columnconfigure(0, weight=1)

    first_title_lbl = Label(first_content_frame.view_port, text="1st label", **style_lbl_title)
    first_title_lbl.grid(row=0, column=0, **grid_lbl)

    first_logger = LoggerPlus(first_content_frame.view_port, **style_logger)
    first_logger.grid(row=1, column=0, **grid_logger)
    first_logger.log('test')

    # SECOND FRAME
    second_content_frame = ContentFrame(app.content_frame, "2nd Content Frame", **style_frame_primary)
    second_content_frame.grid_columnconfigure(0, weight=1)

    second_title_lbl = Label(second_content_frame.view_port, text="2nd label", **style_lbl_title)
    second_title_lbl.grid(row=0, column=0, **grid_lbl)

    # ADD CONTENT FRAMES
    app.add_content_frame(0, first_content_frame)
    app.add_content_frame(1, second_content_frame)
    # TEST RAISING EXCEPTION WHEN TRYING TO DUPLICATE INDEX
    # root.add_content_frame(1, second_content_frame)  # UNCOMMENT TO RAISE EXCEPTION - TESTED, WORKS

    root.mainloop()
