from App_3500ParkingLogin.components.UserCardFrame import *


class UserListSubFrame(StandardFrame):
    def __init__(self, root, user_data_list: list, on_select_user=None, on_delete_user=None):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # FUNCTION CALLBACKS
        self.__on_select_user = on_select_user
        self.__on_delete_user = on_delete_user

        # USER DATA LIST
        self._user_data_list = user_data_list

        # TITLE
        self.user_list_frame_title = TitleLabel(self, text="User List")
        self.user_list_frame_title.grid(row=0, column=0, **TitleLabel.grid_args)

        # SCROLL FRAME
        self.user_list_scroll_frame = CardScrollFramePlus(self, hide_scroll_bar=True)
        self.user_list_scroll_frame.grid(row=1, column=0, sticky=grid_style.sticky.all)
        self.user_list_scroll_frame.view_port.grid_columnconfigure(0, weight=1)
        self.user_list_scroll_frame.view_port.grid_columnconfigure(1, weight=0)

        # POPULATE WITH DATA
        self.__populate_user_list()

    def __populate_user_list(self):
        sorted_by_name = sorted(self._user_data_list, key=lambda k: k[User.keys.NAME])
        for user in sorted_by_name:
            self.add_user_to_list(User(user))
        self.user_list_scroll_frame.scroll_to(0.0)

    def add_user_to_list(self, user: User):
        # self._user_data_list.append(user)
        user_frame = UserCardFrame(self.user_list_scroll_frame.view_port, user, on_name_func=self.__on_select_user, on_delete_func=self.__on_delete_user)
        self.user_list_scroll_frame.add_frame_by_key(user_frame.key(), user_frame)
        self.user_list_scroll_frame.scroll_to(1.0)
        self.update()

    def delete_user_from_list(self, user_name):
        self.user_list_scroll_frame.delete_frame_by_key(user_name)


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    def select_user(name):
        print(name)

    def delete_user(name):
        user_list_frame.user_list_scroll_frame.delete_frame_by_key(name)

    user_list_frame = UserListSubFrame(root, test_user_list, on_select_user=select_user, on_delete_user=delete_user)
    user_list_frame.grid(row=0, column=0, sticky='nsew')

    root.mainloop()
