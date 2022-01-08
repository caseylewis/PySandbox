from abc import ABC

from Libs.GuiLib.gui_majors import *
from App_3500ParkingLogin.components.SubFrames.UserListSubFrame import *
from App_3500ParkingLogin.components.SubFrames.Register2ParkSubFrame import *


class Register2ParkContentFrame(ContentFrame, ABC):
    def __init__(self, root, user_data_list, config_dict, on_delete_user=None, on_select_user=None, on_new_session_func=None):
        super().__init__(root, "Register2Park")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self._register_2_park_frame = Register2ParkSubFrame(self, config_dict, on_new_session_func=on_new_session_func)
        self._register_2_park_frame.grid(row=0, column=1, sticky='nsew', pady=(0, 20))
        self._add_user_frame = UserListSubFrame(self, user_data_list, on_delete_user=on_delete_user, on_select_user=on_select_user)
        self._add_user_frame.grid(row=1, column=1, sticky='nsew')

    def resize_thin(self):
        self._register_2_park_frame.grid(column=0, columnspan=3)
        self._add_user_frame.grid(column=0, columnspan=3)

    def resize_wide(self):
        self._register_2_park_frame.grid(column=1, columnspan=1)
        self._add_user_frame.grid(column=1, columnspan=1)

    def add_user_to_list(self, user: User):
        self._add_user_frame.add_user_to_list(user)

    def delete_user(self, user_name):
        self._add_user_frame.delete_user_from_list(user_name)

    def insert_user(self, user: User):
        self._register_2_park_frame.insert_user_register_info(user)


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

    register_2_park_frame = Register2ParkContentFrame(root)
    register_2_park_frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()
