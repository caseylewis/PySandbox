from tkinter import messagebox

import yaml

from App_3500ParkingLogin.components.ChromedriverPrompt import *
from App_3500ParkingLogin.components.ConfigPrompt import *
from App_3500ParkingLogin.components.ContentFrames.AddUserContentFrame import *
from App_3500ParkingLogin.components.ContentFrames.Register2ParkContentFrame import *
from App_3500ParkingLogin.register_2_park import *
from Libs.DataLib.json_helper import *
from Libs.GuiLib.gui_majors import *
from Libs.GuiLib.gui_functions import *
from Libs.OSLib.chromedriver_helper import *


class ParkingLoginApp(NavigableTkFrame):
    app_data = StandardAppDirStruct(os.getcwd(), "3500ParkingLogin")

    chromedriver_dir = os.path.join(app_data.data_dir, 'chromedriver')
    dir_create(chromedriver_dir)
    # JSON DATA
    users_json = JsonManager(os.path.join(app_data.data_dir, 'users.json'))
    # YAML FILES
    config_yaml = os.path.join(app_data.data_dir, 'config.yml')

    class FrameIndices:
        REGISTER = 0
        ADD_USER = 1

    f_idxs = FrameIndices

    def __init__(self, root):
        super().__init__(root)
        self.config(bg='black')
        self.set_nav_btn_style(**{
            'bg': 'green',
            'fg': 'white',
            'font': (style.font.style.std, style.font.size.h1),
        })
        self.master.protocol('WM_DELETE_WINDOW', lambda: self.__handle_window_close())

        # DATA OBJECTS
        # self._user_list = test_user_list
        self._user_list = []
        self._config_data = {"apartment_number": "621", "apartment_description": "3500 Westlake"}
        # self._config_data = {}

        # IMPORT DATA - MUST BE BEFORE SETTING UP FRAMES
        self.__import_data()

        # CONTENT FRAMES
        self.register_2_park_content_frame = Register2ParkContentFrame(self.content_frame, self._user_list, self._config_data,
                                                                       on_select_user=self.insert_user,
                                                                       on_delete_user=self.delete_user,
                                                                       on_new_session_func=self.register_user)
        self.add_user_content_frame = AddUserContentFrame(self.content_frame, on_add_user=self.add_user)

        # ADD THE CONTENT FRAMES IN THE CORRECT ORDER
        self.add_content_frame(self.f_idxs.REGISTER, self.register_2_park_content_frame)
        self.add_content_frame(self.f_idxs.ADD_USER, self.add_user_content_frame)

    def resize_thin(self):
        self.register_2_park_content_frame.resize_thin()
        self.add_user_content_frame.resize_thin()

    def resize_wide(self):
        self.register_2_park_content_frame.resize_wide()
        self.add_user_content_frame.resize_wide()

    def add_user(self, user: User):
        self.register_2_park_content_frame.add_user_to_list(user)
        self.data_add_user(user)
        self.show_frame(self.f_idxs.REGISTER)

    def delete_user(self, user_name):
        self.register_2_park_content_frame.delete_user(user_name)
        self.data_delete_user(user_name)

    def register_user(self, session: NewParkingSession):
        try:
            register_2_park(
                chromedriver_path=self.chromedriver_dir,
                make=session.reg_dict[User.keys.MAKE],
                model=session.reg_dict[User.keys.MODEL],
                license_plate=session.reg_dict[User.keys.LICENSE_PLATE],
                email=session.reg_dict[User.keys.EMAIL],
            )
        except Exception as e:
            messagebox.showerror("Register Error", str(e))

    def get_user_by_name(self, user_name):
        for user in self._user_list:
            if user_name == user.name:
                return user

    def data_add_user(self, user: User):
        self._user_list.append(user)

    def data_delete_user(self, user_name):
        for user in self._user_list:
            if user_name == user.name:
                self._user_list.remove(user)

    def insert_user(self, user_name):
        self.register_2_park_content_frame.insert_user(self.get_user_by_name(user_name))

    def upgrade_chromedriver(self):
        download_chrome_driver(self.chromedriver_dir)

    # DATA IMPORT/EXPORT FUNCTIONS
    def __import_user_json(self):
        import_users = self.users_json.import_data()
        for raw_user in import_users:
            user = User(raw_user)
            if not any(x[User.keys.NAME] == user.name for x in self._user_list):
                self._user_list.append(user)

    def __export_user_json(self):
        self.users_json.export_data(self._user_list)

    def __import_config_yaml(self):
        if not file_exists(self.config_yaml):
            prompt = ConfigPrompt(self.master, on_submit_func=self.__handle_config_from_prompt)
            prompt.lift()
            self.master.wait_window(prompt)
        else:
            # IMPORT FROM CONFIG YAML
            with open(self.config_yaml, 'r') as file:
                self._config_data = yaml.safe_load(file)
                file.close()

    def __handle_config_from_prompt(self, config_dict):
        self._config_data = config_dict

    def __export_config_yaml(self):
        with open(self.config_yaml, 'w') as file:
            yaml.dump(self._config_data, file)

    # IMPORT EXPORT ALL DATA FUNCTIONS
    def __import_data(self):
        self.__import_config_yaml()
        self.__import_user_json()

    def __export_data(self):
        self.__export_config_yaml()
        self.__export_user_json()

    # WINDOW CLOSE
    def __handle_window_close(self):
        self.__export_data()
        self.master.destroy()


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.config(bg=ROOT_BG)

    screen_width, screen_height = get_screen_size(root)
    root_width = int((screen_width * 3) / 4)
    root_height = int((screen_height * 3) / 4)
    width_offset = int((screen_width - root_width) / 2)
    height_offset = int((screen_height - root_height) / 2)
    root.geometry("{}x{}+{}+{}".format(root_width, root_height, width_offset, height_offset))

    app = ParkingLoginApp(root)
    app.grid(row=0, column=0, sticky='nsew')

    def on_window_configure(event, root):
        root_width = root.winfo_width()
        if root_width < screen_width/2:
            app.resize_thin()
        else:
            app.resize_wide()
    root.bind("<Configure>", lambda x: on_window_configure(x, root))

    root.mainloop()

