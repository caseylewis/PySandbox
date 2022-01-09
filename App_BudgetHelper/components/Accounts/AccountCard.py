from App_BudgetHelper.components.Accounts.accounts import *
from Libs.GuiLib.gui_abstracts import *


class AccountCard(AbstractCard):
    def __init__(self, root, account: Account, on_delete_by_name_func=None, on_edit_by_name_func=None):
        super().__init__(root, account)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=0)

        # CALLBACK FUNCTIONS
        self.on_delete_by_name_callback = on_delete_by_name_func
        self.on_edit_by_name_callback = on_edit_by_name_func

        pad = 10
        num_width = 12

        self._name_lbl = StandardLabel(self, account.name)
        self._name_lbl.grid(row=0, column=0, rowspan=2, sticky=grid_style.sticky.all, pady=(pad, pad), padx=(pad, pad))

        self._account_num_lbl = StandardLabel(self, account.account_num, width=num_width)
        self._account_num_lbl.grid(row=0, column=1, sticky=grid_style.sticky.all, pady=(pad, 0), padx=(0, 0))

        self._route_num_lbl = StandardLabel(self, account.route_num, width=num_width)
        self._route_num_lbl.grid(row=1, column=1, sticky=grid_style.sticky.all, pady=(pad, pad), padx=(0, 0))

        self._description_lbl = StandardLabel(self, account.description)
        self._description_lbl.grid(row=0, column=2, rowspan=2, sticky=grid_style.sticky.all, pady=(pad, pad), padx=(pad, 0))

        self._edit_btn = StandardButton(self, 'Edit', command=lambda: self.__handle_edit_btn())
        self._edit_btn.grid(row=0, column=3, sticky=grid_style.sticky.all, pady=(pad, 0), padx=(pad, pad))

        self._delete_btn = DeleteButton(self, command=lambda: self.__handle_delete_btn())
        self._delete_btn.grid(row=1, column=3, sticky=grid_style.sticky.all, pady=(pad, pad), padx=(pad, pad))

    def __handle_edit_btn(self):
        if self.on_edit_by_name_callback is not None:
            self.on_edit_by_name_callback(self.key())

    def __handle_delete_btn(self):
        if self.on_delete_by_name_callback is not None:
            self.on_delete_by_name_callback(self.key())

    def update_from_object(self, object):
        self._account_num_lbl['text'] = object.account_num
        self._route_num_lbl['text'] = object.route_num
        self._description_lbl['text'] = object.description


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def output_name(name):
        print(name)

    account = test_account
    test_card = AccountCard(root, account, on_delete_by_name_func=output_name, on_edit_by_name_func=output_name)
    test_card.grid(row=0, column=0, sticky='nsew')

    root.mainloop()
