from App_3500ParkingLogin.data_types.users import *
from Libs.GuiLib.gui_abstracts import *


class UserCardFrame(AbstractCard):

    def __init__(self, root, user: User, on_name_func=None, on_delete_func=None):
        super().__init__(root, user)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)

        self.on_delete_callback = on_delete_func
        self.on_name_callback = on_name_func

        PADY = 15
        PADX = 10

        # USER NAME
        self._user_name_btn = StandardButton(self, text=user[user.keys.NAME], command=lambda: self.__handle_btn_user_name(), width=10)
        self._user_name_btn.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(PADX, 0), pady=PADY)

        self._email_lbl = StandardLabel(self, text=user[user.keys.EMAIL])
        self._email_lbl.grid(row=0, column=1, columnspan=3, sticky='nsew', padx=PADX, pady=(PADY, 0))

        self._make_lbl = StandardLabel(self, text=user[user.keys.MAKE])
        self._make_lbl.grid(row=1, column=1, sticky='nsew', padx=PADX, pady=PADY)

        self._model_lbl = StandardLabel(self, text=user[user.keys.MODEL])
        self._model_lbl.grid(row=1, column=2, sticky='nsew', pady=PADY)

        self._license_lbl = StandardLabel(self, text=user[user.keys.LICENSE_PLATE])
        self._license_lbl.grid(row=1, column=3, sticky='nsew', padx=PADX, pady=PADY)

        # DELETE BTN
        self._delete_btn = DeleteButton(self, command=lambda: self.__handle_btn_delete())
        self._delete_btn.grid(row=0, column=4, rowspan=2, sticky='ns', padx=(0, PADX), pady=PADY)

    def __handle_btn_user_name(self):
        if self.on_name_callback is not None:
            self.on_name_callback(self.key())

    def __handle_btn_delete(self):
        if self.on_delete_callback is not None:
            self.on_delete_callback(self.key())

    def update_from_object(self, object):
        pass