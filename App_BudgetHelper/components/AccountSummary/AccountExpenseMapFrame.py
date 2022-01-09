from App_BudgetHelper.components.AccountSummary.AccountExpenseCards import *
from App_BudgetHelper.components.Accounts.accounts import *


class AccountExpenseMapFrame(StandardFrame):
    default_account_option = "Select Account"

    def __init__(self, root,
                 on_assign_by_name_func=None,
                 on_unassign_by_name_func=None,
                 on_account_name_changed_func=None):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        # FUNCTION CALLBACKS
        self.__on_assign_by_name_callback = on_assign_by_name_func
        self.__on_unassign_by_name_callback = on_unassign_by_name_func
        self.__on_account_name_changed_callback = on_account_name_changed_func

        # TITLE
        self._title = TitleLabel(self, text="Account Expense Map")
        self._title.grid(row=0, column=0, **TitleLabel.grid_args)

        # ACTION FRAME
        self._action_frame = StandardFrame(self)
        self._action_frame.grid(row=1, column=0, **StandardFrame.grid_args)
        self._action_frame.grid_columnconfigure(0, weight=1)
        self._action_frame.grid_columnconfigure(1, weight=1)
        self._action_frame.grid_rowconfigure(0, weight=0)
        self._action_frame.grid_rowconfigure(1, weight=1)

        # ACCOUNT DROPDOWN
        self._account_dropdown = StandardDropdown(self._action_frame,
                                                  on_change_func=self.__on_account_name_changed_callback)
        self._account_dropdown.grid(row=0, column=0, **StandardDropdown.grid_args)

        # ACCOUNT EXPENSE SCROLLFRAME
        self._account_expense_scrollframe = CardScrollFramePlus(self._action_frame, hide_scroll_bar=True)
        self._account_expense_scrollframe.grid(row=1, column=0, sticky=grid_style.sticky.all)

        # AVAILABLE EXPENSE LABEL
        self._available_expense_lbl = StandardLabel(self._action_frame, text="Available Expenses")
        self._available_expense_lbl.grid(row=0, column=1, **StandardLabel.grid_args)

        # AVAILABLE EXPENSE SCROLLFRAME
        self._available_expense_scrollframe = CardScrollFramePlus(self._action_frame, hide_scroll_bar=True)
        self._available_expense_scrollframe.grid(row=1, column=1, sticky=grid_style.sticky.all)

    def populate_objects(self, accounts_list, expenses_list):
        self.__populate_accounts(accounts_list)
        self.__populate_expenses(expenses_list)

    def __populate_accounts(self, accounts_list):
        options_list = [self.default_account_option]
        for account in accounts_list:
            options_list.append(account[Account.keys.NAME])
        self._account_dropdown.set_options(options_list)

    def __populate_expenses(self, expenses_list):
        for expense in expenses_list:
            if expense.account is None:
                self.add_available_expense(expense)
        self.grid_propagate()

    def add_account_expense(self, expense):
        account_expense_card = AccountExpenseCard(self._account_expense_scrollframe.view_port, expense,
                                                  on_delete_by_name_func=self.__on_unassign_by_name_callback)
        self._account_expense_scrollframe.add_frame_by_key(account_expense_card.key(), account_expense_card)
        self.grid_propagate()

    def remove_account_expense(self, expense):
        self._account_expense_scrollframe.delete_frame_by_key(expense.name)

    def add_available_expense(self, expense):
        available_expense_card = AvailableExpenseCard(self._available_expense_scrollframe.view_port, expense,
                                                      on_add_by_name_func=self.__on_assign_by_name_callback)
        self._available_expense_scrollframe.add_frame_by_key(available_expense_card.key(), available_expense_card)

    def remove_available_expense(self, expense):
        self._available_expense_scrollframe.delete_frame_by_key(expense.name)

    def set_active_account_to_none(self):
        self._account_dropdown.set(self.default_account_option)

    def get_active_account_name(self):
        return self._account_dropdown.get()

    def delete_account_option(self, account):
        self._account_dropdown.remove_option(account.name)

    def add_account(self, account):
        self._account_dropdown.add_option(account.name)

    def populate_account_expense_scrollframe(self, account_expense_list):
        for expense in account_expense_list:
            self.add_account_expense(expense)

    def clear_account_expense_scrollframe(self):
        self._account_expense_scrollframe.delete_all()


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def output_expenses():
        for expense in test_expense_list:
            print(expense.name, expense.account)

    def get_object_from_list_by_name(object_name, object_list):
        for object in object_list:
            if object.name == object_name:
                return object

    def assign_account(expense_name):
        active_account = frame.get_active_account_name()
        if active_account != frame.default_account_option:
            expense = get_object_from_list_by_name(expense_name, test_expense_list)
            expense.account = active_account
            frame.add_account_expense(expense)
            frame.remove_available_expense(expense)

    def unassign_account(expense_name):
        expense = get_object_from_list_by_name(expense_name, test_expense_list)
        expense.account = None
        frame.add_available_expense(expense)
        frame.remove_account_expense(expense)

    def account_changed():
        print('printing account', frame.get_active_account_name())

    frame = AccountExpenseMapFrame(root,
                                   on_assign_by_name_func=assign_account,
                                   on_unassign_by_name_func=unassign_account,
                                   on_account_name_changed_func=account_changed)
    frame.grid(row=0, column=0, sticky=grid_style.sticky.all)
    test_account_list = [test_account]
    test_expense_list = [test_expense]
    frame.populate_objects(test_account_list, test_expense_list)
    # frame.populate_accounts(test_account_list)
    # frame.populate_expenses(test_expense_list)

    root.mainloop()
