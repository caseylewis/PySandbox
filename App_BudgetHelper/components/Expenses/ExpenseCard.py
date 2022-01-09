from App_BudgetHelper.components.Expenses.expenses import *
from Libs.GuiLib.gui_standards import *
from Libs.GuiLib.gui_abstracts import *


class ExpenseCard(AbstractCard):
    def __init__(self, root, expense: Expense, on_delete_by_name_func=None, on_edit_by_name_func=None):
        super().__init__(root, expense)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # CALLBACK FUNCTIONS
        self.on_delete_by_name_callback = on_delete_by_name_func
        self.on_edit_by_name_callback = on_edit_by_name_func

        pad = 10

        self._name_lbl = StandardLabel(self, expense.name)
        self._name_lbl.grid(row=0, column=0, rowspan=2, sticky='nsew', pady=(pad, pad), padx=(pad, pad))

        self._value_lbl = StandardLabel(self, expense.value)
        self._value_lbl.grid(row=0, column=1, sticky='nsew', pady=(pad, 0), padx=(0, 0))

        self._frequency_lbl = StandardLabel(self, expense.frequency)
        self._frequency_lbl.grid(row=1, column=1, sticky='nsew', pady=(pad, pad), padx=(0, 0))

        self._edit_btn = StandardButton(self, 'Edit', command=lambda: self.__handle_edit_btn())
        self._edit_btn.grid(row=0, column=2, sticky='nsew', pady=(pad, 0), padx=(pad, pad))

        self._delete_btn = DeleteButton(self, command=lambda: self.__handle_delete_btn())
        self._delete_btn.grid(row=1, column=2, sticky='nsew', pady=(pad, pad), padx=(pad, pad))

    def __handle_edit_btn(self):
        if self.on_edit_by_name_callback is not None:
            self.on_edit_by_name_callback(self.key())

    def __handle_delete_btn(self):
        if self.on_delete_by_name_callback is not None:
            self.on_delete_by_name_callback(self.key())

    def update_from_object(self, object):
        self._value_lbl['text'] = object.value
        self._frequency_lbl['text'] = object.frequency


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def output_name(name):
        print(name)

    expense = test_expense
    test_card = ExpenseCard(root, expense, on_delete_by_name_func=output_name, on_edit_by_name_func=output_name)
    test_card.grid(row=0, column=0, sticky='nsew')

    root.mainloop()
