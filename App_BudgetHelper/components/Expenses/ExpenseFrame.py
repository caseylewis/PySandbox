from App_BudgetHelper.components.Expenses.ExpenseForm import *
from App_BudgetHelper.components.Expenses.ExpenseCard import *
from Libs.GuiLib.gui_abstracts import *


class ExpenseFrame(AbstractObjectFrame):
    def __init__(self, root, on_add_func, on_update_func, on_delete_by_name_func, on_edit_by_name_func):
        super().__init__(root, "Expenses", ExpenseForm, ExpenseCard,
                         on_add_func=on_add_func,
                         on_update_func=on_update_func,
                         on_delete_by_name_func=on_delete_by_name_func,
                         on_edit_by_name_func=on_edit_by_name_func)


if __name__ == '__main__':
    root = Tk()
    root.config(bg=FRAME_BG_STANDARD)
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def get_object_from_list_by_name(account_name, account_list):
        for account in account_list:
            if account.name == account_name:
                return account

    # TEST FOR ACCOUNT FRAME
    def add_object(account):
        test_object_list.append(account)
        frame.add_object(account)
        frame.object_edit_frame.clear_entries()

    def update_account(new_account):
        old_account = get_object_from_list_by_name(new_account.name, test_object_list)
        old_account.copy_from(new_account)
        frame.update_object(new_account)

    def delete_account_by_name(account_name):
        frame.delete_object_by_name(account_name)

    def edit_account_by_name(account_name):
        account = get_object_from_list_by_name(account_name, test_object_list)
        frame.edit_object(account)

    test_object_list = [test_expense]
    frame = ExpenseFrame(root,
                         on_add_func=add_object,
                         on_update_func=update_account,
                         on_delete_by_name_func=delete_account_by_name,
                         on_edit_by_name_func=edit_account_by_name)
    frame.populate_objects(test_object_list)

    # GRID WHICHEVER FRAME
    frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()
