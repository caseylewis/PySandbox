from Libs.GuiLib.gui_abstracts import *


class AvailableExpenseCard(AbstractCard):
    def __init__(self, root, expense, on_add_by_name_func=None):
        super().__init__(root, expense)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.__on_add_by_name_callback = on_add_by_name_func

        self._name_lbl = StandardLabel(self, expense.name)
        self._name_lbl.grid(row=0, column=0, sticky=grid_style.sticky.all, pady=grid_style.pad.pady_std, padx=grid_style.pad.padx_std)

        self._add_btn = StandardButton(self, '[+]', command=lambda: self.__handle_add_btn())
        self._add_btn.grid(row=0, column=1, sticky=grid_style.sticky.all, pady=grid_style.pad.pady_std, padx=(0, grid_style.pad.padx_std))

    def __handle_add_btn(self):
        if self.__on_add_by_name_callback is not None:
            self.__on_add_by_name_callback(self.key())

    def update_from_object(self, object):
        return


class AccountExpenseCard(AbstractCard):
    def __init__(self, root, expense, on_delete_by_name_func=None):
        super().__init__(root, expense)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.__on_delete_by_name_callback = on_delete_by_name_func

        self._name_lbl = StandardLabel(self, expense.name)
        self._name_lbl.grid(row=0, column=0, sticky=grid_style.sticky.all, pady=grid_style.pad.pady_std, padx=grid_style.pad.padx_std)

        self._delete_btn = DeleteButton(self, command=lambda: self.__handle_add_btn())
        self._delete_btn.grid(row=0, column=1, sticky=grid_style.sticky.all, pady=grid_style.pad.pady_std, padx=(0, grid_style.pad.padx_std))

    def __handle_add_btn(self):
        if self.__on_delete_by_name_callback is not None:
            self.__on_delete_by_name_callback(self.key())

    def update_from_object(self, object):
        return


if __name__ == '__main__':
    from App_BudgetHelper.Expenses.expenses import *
    root = Tk()
    root.grid_columnconfigure(0, weight=1)

    def output_name(name):
        print(name)

    card = AccountExpenseCard(root, test_expense, on_delete_by_name_func=output_name)
    card.grid(row=0, column=0, sticky=grid_style.sticky.all)

    root.mainloop()
