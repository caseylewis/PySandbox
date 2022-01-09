from Libs.GuiLib.gui_standards import *


class AccountInfoFrame(StandardFrame):
    def __init__(self, root):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # INFO TITLE
        self._info_lbl_title = TitleLabel(self, text="Account Info")
        self._info_lbl_title.grid(row=0, column=0, columnspan=2, **TitleLabel.grid_args)

        lbl_kwargs = {
            'anchor': W,
        }

        display_kwargs = {
            'anchor': E,
        }

        # ACCOUNT NUMBER
        self._account_number_lbl = StandardLabel(self, text="Account #", **lbl_kwargs)
        self._account_number_lbl.grid(row=1, column=0, **StandardLabel.grid_args)

        self._account_number_display = StandardLabel(self, "", **display_kwargs)
        self._account_number_display.grid(row=1, column=1, **StandardLabel.grid_args)

        # ROUTE NUMBER
        self._route_number_lbl = StandardLabel(self, text="Route #", **lbl_kwargs)
        self._route_number_lbl.grid(row=2, column=0, **StandardLabel.grid_args)

        self._route_number_display = StandardLabel(self, "", **display_kwargs)
        self._route_number_display.grid(row=2, column=1, **StandardLabel.grid_args)

        # DESCRIPTION
        self._description_lbl = StandardLabel(self, text="Description", **lbl_kwargs)
        self._description_lbl.grid(row=3, column=0, **StandardLabel.grid_args)

        self._description_display = StandardLabel(self, "")  # NOT PART OF DISPLAY KWARGS
        self._description_display.grid(row=3, column=1, **StandardLabel.grid_args)

    def show_info(self, account):
        account_number = account.account_num
        self._account_number_display['text'] = account_number
        self._route_number_display['text'] = account.route_num
        self._description_display['text'] = account.description

    def clear_displays(self):
        for display in [
            self._account_number_display,
            self._route_number_display,
            self._description_display,
        ]:
            display['text'] = ""


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    frame = AccountInfoFrame(root)
    frame.grid(row=0, column=0, sticky=grid_style.sticky.all)
    frame.show_info(test_account)

    root.mainloop()
