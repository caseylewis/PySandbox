from abc import ABC

from Libs.GuiLib.gui_majors import *
from App_3500ParkingLogin.components.SubFrames.AddUserSubFrame import *


class AddUserContentFrame(ContentFrame, ABC):
    def __init__(self, root, on_add_user=None):
        super().__init__(root, "Add User")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._add_user_frame = AddUserSubFrame(self, add_user_callback=on_add_user)
        self._add_user_frame.grid(row=0, column=0, sticky='nsew')

    def resize_thin(self):
        self._add_user_frame.grid(column=0, columnspan=3)

    def resize_wide(self):
        self._add_user_frame.grid(column=1, columnspan=1)


if __name__ == '__main__':
    from Libs.GuiLib.gui_functions import *
    root = Tk()
    root.config(bg=ROOT_BG)
    # CONFIGURE ROOT COLUMNS
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # GET SCREEN SIZES
    screen_width, screen_height = get_screen_size(root)

    def on_window_configure(event, root):
        root_width = root.winfo_width()
        if root_width < screen_width/2:
            # register_2_park_frame.grid(column=0, columnspan=3)
            register_2_park_frame.resize_thin()
        else:
            # register_2_park_frame.grid(column=1, columnspan=1)
            register_2_park_frame.resize_wide()
    root.bind("<Configure>", lambda x: on_window_configure(x, root))

    register_2_park_frame = AddUserContentFrame(root)
    register_2_park_frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()
