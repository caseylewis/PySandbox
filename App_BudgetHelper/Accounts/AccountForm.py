from App_BudgetHelper.Accounts.accounts import *
from Libs.GuiLib.gui_abstracts import *


class AccountForm(AbstractEditFrame):
    def __init__(self, root, on_add_func=None, on_update_func=None):
        super().__init__(root, Account, on_add_func, on_update_func)

    def set_entries(self):
        for key, idx in zip(self.object_type.keys.all_keys, self.object_type.idxs.all_indices):
            entry = StandardEntry(self._input_frame)
            entry.grid(row=idx, column=1, sticky=grid_style.sticky.all, pady=grid_style.pad.pady_std, padx=0)
            self._entry_dict[key] = entry


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def on_add(account):
        print('printing', account.name)
        test_form.change_to_add_mode()

    def on_update(account):
        print(account.name)
        test_form.change_to_add_mode()

    test_form = AccountForm(root, on_add_func=on_add, on_update_func=on_update)
    test_form.change_to_update_mode(test_account)
    test_form.grid(row=0, column=0, sticky='nsew')

    root.mainloop()
