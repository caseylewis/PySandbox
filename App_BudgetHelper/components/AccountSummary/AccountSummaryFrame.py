from Libs.GuiLib.gui_majors import *
from App_BudgetHelper.components.AccountSummary.AccountExpenseMapFrame import *
from App_BudgetHelper.components.AccountSummary.AccountTotalsFrame import *
from App_BudgetHelper.components.AccountSummary.AccountInfoFrame import *


class AccountSummaryFrame(ContentFrame):
    def __init__(self, root,
                 on_assign_by_name_func=None,
                 on_unassign_by_name_func=None,
                 on_account_name_changed_func=None):
        super().__init__(root, "Account Summary")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self._account_expense_map_frame = AccountExpenseMapFrame(self,
                                                                 on_assign_by_name_func=on_assign_by_name_func,
                                                                 on_unassign_by_name_func=on_unassign_by_name_func,
                                                                 on_account_name_changed_func=on_account_name_changed_func)
        self._account_expense_map_frame.grid(row=0, column=1, columnspan=1, sticky=grid_style.sticky.all)
        self.default_account_option = self._account_expense_map_frame.default_account_option

        self._account_info_frame = StandardFrame(self)
        self._account_info_frame.grid(row=1, column=0, columnspan=3, sticky=grid_style.sticky.all, pady=(0, 25))
        self._account_info_frame.grid_columnconfigure(0, weight=1)
        self._account_info_frame.grid_columnconfigure(1, weight=1)

        self._account_totals_frame = AccountTotalsFrame(self._account_info_frame)
        self._account_totals_frame.grid(row=0, column=0, sticky=grid_style.sticky.all)

        self._account_data_frame = AccountInfoFrame(self._account_info_frame)
        self._account_data_frame.grid(row=0, column=1, sticky=grid_style.sticky.all)

    def populate_objects(self, accounts_list, expenses_list):
        self._account_expense_map_frame.populate_objects(accounts_list, expenses_list)

    def get_active_account_name(self):
        return self._account_expense_map_frame.get_active_account_name()

    def refresh_account_info(self, account_expense_list, active_account):
        self._account_totals_frame.show_account_stats(account_expense_list)
        self._account_data_frame.show_info(active_account)

    def clear_data(self):
        self._account_totals_frame.clear_displays()
        self._account_data_frame.clear_displays()
        self._account_expense_map_frame.clear_account_expense_scrollframe()

    def add_account(self, account):
        self._account_expense_map_frame.add_account(account)

    def delete_account_option(self, account):
        self._account_expense_map_frame.delete_account_option(account)

    def set_active_account_to_none(self):
        self._account_expense_map_frame.set_active_account_to_none()

    # ACCOUNT EXPENSE SCROLLFRAME
    def populate_account_expense_scrollframe(self, account_expense_list):
        self._account_expense_map_frame.populate_account_expense_scrollframe(account_expense_list)

    def add_account_expense(self, expense):
        self._account_expense_map_frame.add_account_expense(expense)

    def remove_account_expense(self, expense):
        self._account_expense_map_frame.remove_account_expense(expense)

    # AVAILABLE EXPENSE SCROLLFRAME
    def add_available_expense(self, expense):
        self._account_expense_map_frame.add_available_expense(expense)

    def remove_available_expense(self, expense):
        self._account_expense_map_frame.remove_available_expense(expense)


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

    def __get_expenses_of_account(account):
        account_expenses_list = []
        for expense in test_expense_list:
            if expense.account == account.name:
                account_expenses_list.append(expense)
        return account_expenses_list

    def __assign_to_account(expense_name):
        active_account = frame.get_active_account_name()
        if active_account != frame.default_account_option:
            expense = get_object_from_list_by_name(expense_name, test_expense_list)
            expense.account = active_account
            frame.add_account_expense(expense)
            frame.remove_available_expense(expense)
            # UPDATE ACCOUNT VALUES
            __account_values_changed_by_name(frame.get_active_account_name())

    def __unassign_from_account(expense_name):
        expense = get_object_from_list_by_name(expense_name, test_expense_list)
        expense.account = None
        frame.add_available_expense(expense)
        frame.remove_account_expense(expense)
        # UPDATE ACCOUNT VALUES
        __account_values_changed_by_name(frame.get_active_account_name())

    def __account_changed():
        active_account_name = frame.get_active_account_name()
        frame.clear_data()
        if active_account_name != frame.default_account_option:
            active_account = get_object_from_list_by_name(active_account_name, test_account_list)
            account_expense_list = __get_expenses_of_account(active_account)
            frame.populate_account_expense_scrollframe(account_expense_list)
            # UPDATE ACCOUNT VALUES
            __account_values_changed_by_name(active_account.name)

    def __account_values_changed_by_name(account_name):
        account = get_object_from_list_by_name(account_name, test_account_list)
        account_expense_list = __get_expenses_of_account(account)
        frame.refresh_account_info(account_expense_list, account)

    # START OF TEST
    frame = AccountSummaryFrame(root,
                                on_assign_by_name_func=__assign_to_account,
                                on_unassign_by_name_func=__unassign_from_account,
                                on_account_name_changed_func=__account_changed)
    frame.grid(row=0, column=0, sticky=grid_style.sticky.all)
    test_account_list = [test_account]
    test_expense_list = [test_expense]
    frame.populate_objects(test_account_list, test_expense_list)

    root.mainloop()
