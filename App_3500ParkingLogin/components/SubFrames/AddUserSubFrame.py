from Libs.GuiLib.gui_standards import *
from App_3500ParkingLogin.data_types.users import *


class AddUserSubFrame(StandardFrame):
    def __init__(self, root, add_user_callback=None):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._add_user_callback = add_user_callback

        # TITLE
        self.register_user_title_lbl = TitleLabel(self, text="Add User")
        self.register_user_title_lbl.grid(row=0, column=0, columnspan=2, **TitleLabel.grid_args)

        # LABELS COLUMN
        self.register_user_name_lbl = StandardLabel(self, text="Name")
        self.register_user_name_lbl.grid(row=1, column=0, **StandardLabel.grid_args)

        self.register_user_make_lbl = StandardLabel(self, text="Make")
        self.register_user_make_lbl.grid(row=2, column=0, **StandardLabel.grid_args)

        self.register_user_model_lbl = StandardLabel(self, text="Model")
        self.register_user_model_lbl.grid(row=3, column=0, **StandardLabel.grid_args)

        self.register_user_license_lbl = StandardLabel(self, text="License Plate")
        self.register_user_license_lbl.grid(row=4, column=0, **StandardLabel.grid_args)

        self.register_user_email_lbl = StandardLabel(self, text="Email")
        self.register_user_email_lbl.grid(row=5, column=0, **StandardLabel.grid_args)

        # ENTRIES COLUMN
        self.register_user_name_entry = StandardEntry(self)
        self.register_user_name_entry.grid(row=1, column=1, **StandardEntry.grid_args)

        self.register_user_make_entry = StandardEntry(self)
        self.register_user_make_entry.grid(row=2, column=1, **StandardEntry.grid_args)

        self.register_user_model_entry = StandardEntry(self)
        self.register_user_model_entry.grid(row=3, column=1, **StandardEntry.grid_args)

        self.register_user_license_entry = StandardEntry(self)
        self.register_user_license_entry.grid(row=4, column=1, **StandardEntry.grid_args)

        self.register_user_email_entry = StandardEntry(self)
        self.register_user_email_entry.grid(row=5, column=1, **StandardEntry.grid_args)

        # CREATE USER BTN
        self.register_user_create_user_btn = StandardButton(self, text="Create User", command=lambda: self.__handle_create_user_btn())
        self.register_user_create_user_btn.grid(row=6, column=1, **StandardButton.grid_args)

    def get_user_from_entries(self):
        # GET VALUES FROM ENTRIES
        user_name = self.register_user_name_entry.get()
        user_make = self.register_user_make_entry.get()
        user_model = self.register_user_model_entry.get()
        user_license = self.register_user_license_entry.get()
        user_email = self.register_user_email_entry.get()
        # CREATE USER DICT
        user_dict = {
            User.keys.NAME: user_name,
            User.keys.MAKE: user_make,
            User.keys.MODEL: user_model,
            User.keys.LICENSE_PLATE: user_license,
            User.keys.EMAIL: user_email,
        }
        return User(user_dict)

    def __handle_create_user_btn(self):
        if self._add_user_callback is not None:
            self._add_user_callback(self.get_user_from_entries())

        self.clear_entries()

    def clear_entries(self):
        # CLEAR ALL ENTRIES UPON SUCCESS
        for entry in [
            self.register_user_name_entry,
            self.register_user_make_entry,
            self.register_user_model_entry,
            self.register_user_license_entry,
            self.register_user_email_entry,
        ]:
            entry.delete(0, END)


if __name__ == '__main__':
    from Libs.GuiLib.gui_functions import *
    root = Tk()
    root.config(bg=ROOT_BG)
    # CONFIGURE ROOT COLUMNS
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # GET SCREEN SIZES
    screen_width, screen_height = get_screen_size(root)

    def on_window_configure(event, root):
        root_width = root.winfo_width()
        if root_width < screen_width/2:
            add_user_frame.grid(column=0, columnspan=3)
        else:
            add_user_frame.grid(column=1, columnspan=1)
    root.bind("<Configure>", lambda x: on_window_configure(x, root))

    def add_user(user: User):
        print(user[User.keys.NAME])

    add_user_frame = AddUserSubFrame(root, add_user_callback=add_user)
    add_user_frame.grid(row=0, column=1, sticky='nsew')

    root.mainloop()
