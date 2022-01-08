from Libs.GuiLib.gui_standards import *


class ConfigPrompt(StandardModal):
    def __init__(self, root, on_submit_func=None):
        super().__init__(root)
        self.title("3500 Parking Login Config Entry")
        self.config(bg=ROOT_BG)
        self.grid_columnconfigure(0, weight=1)

        # ON SUBMIT FUNCTION
        self.__on_submit_func = on_submit_func

        padx = 5
        pady = 5

        # CONFIG FRAME
        self.config_frame = StandardFrame(self)
        self.config_frame.grid(row=0, column=0, **StandardFrame.grid_args)
        self.config_frame.grid_columnconfigure(0, weight=1)
        self.config_frame.grid_columnconfigure(1, weight=1)

        class PromptRows:
            APT_NUM = 0
            APT_DESC = 1
            SUBMIT = 2
        p_rows = PromptRows

        self.apt_num_lbl = StandardLabel(self.config_frame, "Apt. Number")
        self.apt_num_lbl.grid(row=p_rows.APT_NUM, column=0, sticky='nsew', pady=pady, padx=padx)
        self.apt_num_entry = StandardEntry(self.config_frame)
        self.apt_num_entry.grid(row=p_rows.APT_NUM, column=1, sticky='nsew', pady=pady, padx=padx)

        self.apt_desc_lbl = StandardLabel(self.config_frame, "Apt. Description")
        self.apt_desc_lbl.grid(row=p_rows.APT_DESC, column=0, sticky='nsew', pady=pady, padx=padx)
        self.apt_desc_entry = StandardEntry(self.config_frame)
        self.apt_desc_entry.grid(row=p_rows.APT_DESC, column=1, sticky='nsew', pady=pady, padx=padx)

        self.submit_btn = StandardButton(self.config_frame, "Submit", command=lambda: self.__handle_submit_clicked())
        self.submit_btn.grid(row=p_rows.SUBMIT, column=1, sticky='nsew', pady=(0, pady), padx=padx)

        self.center_on_root()

    def get_entries(self):
        config_dict = dict()
        config_dict['apartment_number'] = self.apt_num_entry.get()
        config_dict['apartment_description'] = self.apt_desc_entry.get()
        return config_dict

    def __handle_submit_clicked(self):
        if self.__on_submit_func is not None:
            self.__on_submit_func(self.get_entries())
            self.destroy()


if __name__ == '__main__':
    root = Tk()

    def output_config(config_dict):
        print(config_dict)

    def close_modal():
        modal.destroy()
        root.after(500, root.destroy)

    modal = ConfigPrompt(root, on_submit_func=output_config)
    modal.protocol('WM_DELETE_WINDOW', lambda: close_modal())

    root.mainloop()