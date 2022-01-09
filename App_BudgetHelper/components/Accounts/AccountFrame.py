from Libs.GuiLib.gui_abstracts import *
from App_BudgetHelper.components.Accounts.AccountForm import *
from App_BudgetHelper.components.Accounts.AccountCard import *


class AccountFrame(AbstractObjectFrame):
    def __init__(self, root, on_add_func, on_update_func, on_delete_by_name_func, on_edit_by_name_func):
        super().__init__(root, "Accounts", AccountForm, AccountCard,
                         on_add_func=on_add_func,
                         on_update_func=on_update_func,
                         on_delete_by_name_func=on_delete_by_name_func,
                         on_edit_by_name_func=on_edit_by_name_func)


# class AccountFrame(ContentFrame):
#     def __init__(self, root, on_add_func=None, on_update_func=None, on_delete_by_name_func=None, on_edit_account_by_name_func=None):
#         super().__init__(root, "Accounts", bg=FRAME_BG_STANDARD)
#
#         class AccountFrameIndices:
#             EDIT_FRAME = 0
#             VIEW_FRAME = 1
#             # LOGGER = 2
#         self._account_frame_idxs = AccountFrameIndices
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=0)
#         self.grid_columnconfigure(2, weight=1)
#         self.grid_rowconfigure(self._account_frame_idxs.EDIT_FRAME, weight=0)
#         self.grid_rowconfigure(self._account_frame_idxs.VIEW_FRAME, weight=1)
#
#         # FUNCTION CALLBACKS
#         self.__on_add_callback = on_add_func
#         self.__on_update_callback = on_update_func
#         self.__on_edit_by_name_callback = on_edit_account_by_name_func
#         self.__on_delete_by_name_callback = on_delete_by_name_func
#
#         # ACCOUNT EDIT FRAME
#         self.account_edit_frame = AccountForm(self, self.__on_add_callback, self.__on_update_callback)
#         self.account_edit_frame.grid(row=self._account_frame_idxs.EDIT_FRAME, column=1, **StandardFrame.grid_args)
#
#         # ACCOUNT VIEW FRAME
#         self.account_scroll_frame = CardScrollFramePlus(self, hide_scroll_bar=True, **StandardFrame.style_args)
#         self.account_scroll_frame.grid(row=self._account_frame_idxs.VIEW_FRAME, column=0, columnspan=3, sticky='nsew')
#
#     def handle_close(self):
#         # self._accounts_json_manager.export_data(self._accounts_list)
#         return
#
#     def __edit_account(self, account):
#         self.account_edit_frame.change_to_update_mode(account)
#
#     def delete_account_by_name(self, account_name):
#         self.account_scroll_frame.delete_frame_by_key(account_name)
#
#     def populate_objects(self, objects_list):
#         for object in objects_list:
#             self.add_account(object)
#
#     def get_object_from_entries(self):
#         return self.account_edit_frame.get_object_from_entries()
#
#     def add_account(self, account: Account):
#         account_card = AccountCard(self.account_scroll_frame.view_port, account,
#                                    on_edit_by_name_func=self.__on_edit_by_name_callback,
#                                    on_delete_by_name_func=self.__on_delete_by_name_callback)
#         self.account_scroll_frame.add_frame_by_key(account.name, account_card)
#
#     def update_account(self, account):
#         account_card = self.account_scroll_frame.get_frame_by_key(account.name)
#         account_card.update_from_account(account)
#         self.account_edit_frame.change_to_add_mode()
#
#     def edit_account(self, account):
#         self.account_edit_frame.change_to_update_mode(account)


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
        test_account_list.append(account)
        frame.add_object(account)
        frame.object_edit_frame.clear_entries()

    def update_account(new_account):
        old_account = get_object_from_list_by_name(new_account.name, test_account_list)
        old_account.copy_from(new_account)
        frame.update_object(new_account)

    def delete_account_by_name(account_name):
        frame.delete_object_by_name(account_name)

    def edit_account_by_name(account_name):
        account = get_object_from_list_by_name(account_name, test_account_list)
        frame.edit_object(account)

    test_account_list = [test_account]
    frame = AccountFrame(root,
                         on_add_func=add_object,
                         on_update_func=update_account,
                         on_delete_by_name_func=delete_account_by_name,
                         on_edit_by_name_func=edit_account_by_name)
    frame.populate_objects(test_account_list)

    # GRID WHICHEVER FRAME
    frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()
