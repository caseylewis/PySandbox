from Libs.GuiLib.gui_standards import *
from Libs.GuiLib.gui_functions import *
from App_3500ParkingLogin.data_types.users import *
from datetime import timedelta, datetime
from App_3500ParkingLogin.data_types.parking_sessions import *


class Register2ParkSubFrame(StandardFrame):
    register_frequency = timedelta(seconds=10)
    register_frequency_text = "10 seconds"

    def __init__(self, root, config_data_dict, on_new_session_func=None):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._config_data_dict = config_data_dict
        self._on_new_session_func = on_new_session_func

        # TITLE
        self._register_frame_title = TitleLabel(self, text="Register 2 Park")
        self._register_frame_title.grid(row=0, column=0, columnspan=2, **StandardLabel.grid_args)

        # LABELS COLUMN
        self._register_apt_number_lbl = StandardLabel(self, text="Apt. #")
        self._register_apt_number_lbl.grid(row=1, column=0, **StandardLabel.grid_args)

        self._register_apt_desc_lbl = StandardLabel(self, text="Apt. Description")
        self._register_apt_desc_lbl.grid(row=2, column=0, **StandardLabel.grid_args)

        self._register_make_lbl = StandardLabel(self, text="Make")
        self._register_make_lbl.grid(row=3, column=0, **StandardLabel.grid_args)

        self._register_model_lbl = StandardLabel(self, text="Model")
        self._register_model_lbl.grid(row=4, column=0, **StandardLabel.grid_args)

        self._register_licence_lbl = StandardLabel(self, text="License Plate #")
        self._register_licence_lbl.grid(row=5, column=0, **StandardLabel.grid_args)

        self._register_email_lbl = StandardLabel(self, text="Email")
        self._register_email_lbl.grid(row=6, column=0, **StandardLabel.grid_args)

        self.extended_stay_btn = StandardCheckbutton(self, text="Staying Long?", select_func=lambda: self.__show_extended_stay_frame(), deselect_func=lambda: self.__hide_extended_stay_frame())
        self.extended_stay_btn.grid(row=7, column=0, **StandardButton.grid_args)

        # ENTRIES COLUMN
        self.register_apt_number_display = StandardLabel(self, text=self._config_data_dict['apartment_number'])
        self.register_apt_number_display.grid(row=1, column=1, **StandardLabel.grid_args)

        self._register_apt_desc_display = StandardLabel(self, text=self._config_data_dict['apartment_description'])
        self._register_apt_desc_display.grid(row=2, column=1, **StandardLabel.grid_args)

        self._register_make_var = StringVar()
        self._register_make_var.trace('w', lambda event, x, y: first_to_upper(self._register_make_var))
        self._register_make_entry = Entry(self, textvariable=self._register_make_var)
        self._register_make_entry.grid(row=3, column=1, **StandardLabel.grid_args)

        self._register_model_var = StringVar()
        self._register_model_var.trace('w', lambda event, x, y: first_to_upper(self._register_model_var))
        self._register_model_entry = Entry(self, textvariable=self._register_model_var)
        self._register_model_entry.grid(row=4, column=1, **StandardLabel.grid_args)

        self._register_license_number_var = StringVar()
        self._register_license_number_var.trace('w', lambda event, x, y: to_upper(self._register_license_number_var))
        self._register_licence_entry = Entry(self, textvariable=self._register_license_number_var, **StandardEntry.style_args)
        self._register_licence_entry.grid(row=5, column=1, **StandardLabel.grid_args)

        self._register_email_var = StringVar()
        self._register_email_entry = Entry(self, textvariable=self._register_email_var, **StandardEntry.style_args)
        self._register_email_entry.grid(row=6, column=1, **StandardLabel.grid_args)

        self.register_btn = StandardButton(self, text="Register", command=lambda: self.__handle_register_btn())
        self.register_btn.grid(row=7, column=1, **StandardButton.grid_args)

        # EXTENDED STAY FRAME
        self._duration_lbl = StandardLabel(self, text="Repeat every\n[ {} ]\nfor x times".format(self.register_frequency_text))
        self._duration_lbl.grid(row=8, column=0, **StandardLabel.grid_args)
        self._duration_lbl.grid_remove()

        self._register_count_entry = StandardEntry(self)
        self._register_count_entry.set('2')
        self._register_count_entry.grid(row=8, column=1, **StandardEntry.grid_args)
        self._register_count_entry.grid_remove()

        # SET LABEL VALUES
        # self.__set_label_values(self._config_data_dict)

    def __show_extended_stay_frame(self):
        self._duration_lbl.grid()
        self._register_count_entry.grid()

    def __hide_extended_stay_frame(self):
        self._duration_lbl.grid_remove()
        self._register_count_entry.grid_remove()

    def __set_label_values(self, value_dict):
        self.register_apt_number_display['text'] = 'test'#value_dict[APT_NUM_KEY]

    def get_from_entries(self):
        make = self._register_make_var.get()
        model = self._register_model_var.get()
        license_num = self._register_license_number_var.get()
        email = self._register_email_var.get()

        re_register_count = self._register_count_entry.get()

        one_time = not self.extended_stay_btn.get()

        reg_dict = {
            User.keys.MAKE: make,
            User.keys.MODEL: model,
            User.keys.LICENSE_PLATE: license_num,
            User.keys.EMAIL: email,
        }

        new_session = NewParkingSession('test', reg_dict, datetime.now(), self.register_frequency, re_register_count, one_time)

        for entry in [make, model, license_num, email]:
            if entry == '':
                return False
        return new_session

    def __handle_register_btn(self):
        new_session = self.get_from_entries()

        # ONLY BEGIN REGISTER IF REGISTER KWARGS PASSED
        if new_session is not False:
            if self._on_new_session_func is not None:
                self._on_new_session_func(new_session)

    def __clear_entries(self):
        for entry in [
            self._register_make_entry,
            self._register_model_entry,
            self._register_licence_entry,
            self._register_email_entry,
        ]:
            entry.delete(0, END)

    def insert_user_register_info(self, user: User):
        self.__clear_entries()

        self._register_make_entry.insert(0, user[User.keys.MAKE])
        self._register_model_entry.insert(0, user[User.keys.MODEL])
        self._register_licence_entry.insert(0, user[User.keys.LICENSE_PLATE])
        self._register_email_entry.insert(0, user[User.keys.EMAIL])