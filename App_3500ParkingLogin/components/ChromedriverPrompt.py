from Libs.GuiLib.gui_standards import *
from App_3500ParkingLogin.data_types.parking_sessions import *


class ChromedriverPrompt(StandardModal):
    def __init__(self, root, on_upgrade_chromedriver_func=None):
        super().__init__(root)
        self.config(bg=ROOT_BG)
        self.title("Register Error: Upgrade Chromedriver")
        self.grid_columnconfigure(0, weight=1)

        # OUTSIDE FUNCTIONS
        self.__on_upgrade_chromedriver = on_upgrade_chromedriver_func

        # WIDGETS
        self.__content_frame = StandardFrame(self)
        self.__content_frame.grid(row=0, column=0, **StandardFrame.grid_args)
        self.__content_frame.grid_columnconfigure(0, weight=1)

        self.__upgrade_chromedriver_btn = StandardButton(self.__content_frame, "Upgrade Chromedriver", command=lambda: self.__handle_chromedriver_btn())
        self.__upgrade_chromedriver_btn.grid(row=0, column=0, sticky='nsew')

    def __handle_chromedriver_btn(self):
        if self.__on_upgrade_chromedriver is not None:
            self.__on_upgrade_chromedriver()
