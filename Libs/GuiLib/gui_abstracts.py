from Libs.GuiLib.gui_majors import ContentFrame
from Libs.GuiLib.gui_standards import *


class AbstractCardKeys:
    KEY_NAME = 'Name'

    all_keys = [
        KEY_NAME
    ]


class AbstractCard(StandardFrame):
    keys = AbstractCardKeys

    def __init__(self, root, value_dict):
        super().__init__(root)
        self._value_dict = value_dict

    def key(self):
        return self._value_dict[self.keys.KEY_NAME]

    def get(self, key):
        return self._value_dict[key]

    @abstractmethod
    def update_from_object(self, object):
        pass


class AbstractEditFrame(StandardFrame):
    class EditFrameModes:
        ADD = 0
        UPDATE = 1
    _modes = EditFrameModes

    def __init__(self, root, object_type, on_add_func=None, on_update_func=None):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # FUNCTION CALLBACKS
        self.__on_add_callback = on_add_func
        self.__on_update_callback = on_update_func

        # SET OBJECT TYPE FOR LATER
        self.object_type = object_type

        # SET MODE TO CREATE BY DEFAULT
        self.mode = self._modes.ADD

        # TITLE
        self._title = TitleLabel(self, text="Create {}".format(object_type.object_name))
        self._title.grid(row=0, column=0, sticky='nsew', pady=(0, grid_style.pad.pady_std), padx=0)

        # INPUT FRAME
        self._input_frame = StandardFrame(self)
        self._input_frame.grid(row=1, column=0, **StandardFrame.grid_args)
        self._input_frame.grid_columnconfigure(0, weight=1)
        self._input_frame.grid_columnconfigure(1, weight=1)

        # INPUT LABELS
        # style_lbl_input = copy_dict(style_lbl)
        # style_lbl_input['anchor'] = E
        for key, idx in zip(self.object_type.keys.all_keys, self.object_type.idxs.all_indices):
            lbl = StandardLabel(self._input_frame, text=key)
            lbl.grid(row=idx, column=0, **StandardLabel.grid_args)

        # INPUT ENTRIES
        self._entry_dict = {}
        self.set_entries()

        # CREATE NAME LABEL FOR WHEN UPDATING AN OBJECT, BUT DON'T GRID
        self._name_lbl = StandardLabel(self._input_frame, text='')
        self._name_lbl.grid(row=self.object_type.idxs.NAME, column=1, **StandardLabel.grid_args)
        self._name_lbl.grid_remove()

        # BUTTONS FRAME
        self._buttons_frame = StandardFrame(self._input_frame)
        self._buttons_frame.grid(row=len(self.object_type.idxs.all_indices)+1, column=1, **StandardFrame.grid_args)
        self._buttons_frame.grid_columnconfigure(0, weight=1)
        self._buttons_frame.grid_columnconfigure(1, weight=1)

        button_width = 7

        # ADD
        self.add_object_btn = StandardButton(self._buttons_frame, text="Add", command=lambda: self.__handle_add_btn(), width=button_width)
        self.add_object_btn.grid(row=0, column=1, **StandardButton.grid_args)

        # UPDATE
        self.update_object_btn = StandardButton(self._buttons_frame, text="Update", command=lambda: self.__handle_update_btn(), width=button_width)
        self.update_object_btn.grid(row=0, column=1, **StandardButton.grid_args)
        self.update_object_btn.grid_remove()

        # CLEAR
        self._clear_btn = StandardButton(self._buttons_frame, text="Clear", command=lambda: self.__handle_clear_btn(), width=button_width)
        self._clear_btn.grid(row=0, column=0, **StandardButton.grid_args)

        # CANCEL
        self._cancel_btn = StandardButton(self._buttons_frame, text="Cancel", command=lambda: self.__handle_cancel_btn(), width=button_width)
        self._cancel_btn.grid(row=0, column=0, **StandardButton.grid_args)
        self._cancel_btn.grid_remove()

    @abstractmethod
    def set_entries(self):
        pass

    def __handle_add_btn(self):
        if self.__on_add_callback is not None:
            self.__on_add_callback(self.get_object_from_entries())

    def __handle_update_btn(self):
        if self.__on_update_callback is not None:
            self.__on_update_callback(self.get_object_from_entries())

    def clear_entries(self):
        for key, entry in self._entry_dict.items():
            entry.default()

    def get_object_from_entries(self):
        value_dict = {}
        if self.mode == self._modes.ADD:
            for key, entry in self._entry_dict.items():
                value_dict[key] = entry.get()
        elif self.mode == self._modes.UPDATE:
            value_dict[self.object_type.keys.NAME] = self._name_lbl['text']
            for key, entry in self._entry_dict.items():
                if key == self.object_type.keys.NAME:
                    continue
                value_dict[key] = entry.get()
        object = self.object_type(**value_dict)
        return object

    def __set_entries(self, object):
        self._name_lbl['text'] = object[self.object_type.keys.NAME]
        for key, entry in self._entry_dict.items():
            if key == self.object_type.keys.NAME:
                continue
            entry.set(object[key])

    def change_to_add_mode(self):
        self.mode = self._modes.ADD
        # BUTTONS
        self.update_object_btn.grid_remove()
        self._cancel_btn.grid_remove()

        self.add_object_btn.grid()
        self._clear_btn.grid()

        # SWITCH LABEL TO ENTRY
        self._name_lbl.grid_remove()
        self._entry_dict[self.object_type.keys.NAME].grid()

        # CLEAR ENTRIES
        self.clear_entries()

    def change_to_update_mode(self, object):
        self.mode = self._modes.UPDATE
        # BUTTONS
        self.add_object_btn.grid_remove()
        self._clear_btn.grid_remove()

        self.update_object_btn.grid()
        self._cancel_btn.grid()

        # SWITCH ENTRY TO LABEL
        self._entry_dict[self.object_type.keys.NAME].grid_remove()
        self._name_lbl.grid()

        self.__set_entries(object)

    def __handle_clear_btn(self):
        self.clear_entries()

    def __handle_cancel_btn(self):
        self.change_to_add_mode()
        self.clear_entries()


class AbstractObjectFrame(ContentFrame):
    def __init__(self, root, title, ObjectForm, ObjectCard,
                 on_add_func=None,
                 on_update_func=None,
                 on_delete_by_name_func=None,
                 on_edit_by_name_func=None):
        super().__init__(root, title)#, bg=FRAME_BG_STANDARD)
        self._ObjectCard = ObjectCard

        class FrameIndices:
            EDIT_FRAME = 0
            VIEW_FRAME = 1
            # LOGGER = 2
        self._frame_idxs = FrameIndices
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(self._frame_idxs.EDIT_FRAME, weight=0)
        self.grid_rowconfigure(self._frame_idxs.VIEW_FRAME, weight=1)

        # FUNCTION CALLBACKS
        self.__on_add_callback = on_add_func
        self.__on_update_callback = on_update_func
        self.__on_edit_by_name_callback = on_edit_by_name_func
        self.__on_delete_by_name_callback = on_delete_by_name_func

        # ACCOUNT EDIT FRAME
        self.object_edit_frame = ObjectForm(self, self.__on_add_callback, self.__on_update_callback)
        self.object_edit_frame.grid(row=self._frame_idxs.EDIT_FRAME, column=1, **StandardFrame.grid_args)

        # ACCOUNT VIEW FRAME
        self.object_scroll_frame = CardScrollFramePlus(self, hide_scroll_bar=True, **StandardFrame.style_args)
        self.object_scroll_frame.grid(row=self._frame_idxs.VIEW_FRAME, column=0, columnspan=3, sticky='nsew')

    def handle_close(self):
        # self._accounts_json_manager.export_data(self._accounts_list)
        return

    def clear_entries(self):
        self.object_edit_frame.clear_entries()

    def __edit_object(self, object):
        self.object_edit_frame.change_to_update_mode(object)

    def delete_object_by_name(self, object_name):
        self.object_scroll_frame.delete_frame_by_key(object_name)

    def populate_objects(self, objects_list):
        for object in objects_list:
            self.add_object(object)

    def get_object_from_entries(self):
        return self.object_edit_frame.get_object_from_entries()

    def add_object(self, object):
        object_card = self._ObjectCard(self.object_scroll_frame.view_port, object,
                                        on_edit_by_name_func=self.__on_edit_by_name_callback,
                                        on_delete_by_name_func=self.__on_delete_by_name_callback)
        self.object_scroll_frame.add_frame_by_key(object.name, object_card)

    def update_object(self, object):
        object_card = self.object_scroll_frame.get_frame_by_key(object.name)
        object_card.update_from_object(object)
        self.object_edit_frame.change_to_add_mode()

    def edit_object(self, object):
        self.object_edit_frame.change_to_update_mode(object)


if __name__ == '__main__':
    from App_BudgetHelper.Accounts.AccountForm import AccountForm
    from App_BudgetHelper.Accounts.AccountCard import AccountCard

    class AccountFrame(AbstractObjectFrame):
        def __init__(self, root, on_add_func, on_update_func, on_delete_by_name_func, on_edit_by_name_func):
            super().__init__(root, "Accounts", AccountForm, AccountCard,
                             on_add_func=on_add_func,
                             on_update_func=on_update_func,
                             on_delete_by_name_func=on_delete_by_name_func,
                             on_edit_by_name_func=on_edit_by_name_func)


    def get_object_from_list_by_name(object_name, object_list):
        for object in object_list:
            if object.name == object_name:
                return object

    # TEST FOR ACCOUNT FRAME
    def add_object(object):
        test_object_list.append(object)
        frame.add_object(object)
        frame.object_edit_frame.clear_entries()

    def update_object(new_object):
        old_object = get_object_from_list_by_name(new_object.name, test_object_list)
        old_object.copy_from(new_object)
        frame.update_object(new_object)

    def delete_object_by_name(object_name):
        frame.delete_object_by_name(object_name)

    def edit_object_by_name(object_name):
        object = get_object_from_list_by_name(object_name, test_object_list)
        frame.edit_object(object)

    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    test_object_list = [test_account]

    frame = AccountFrame(root, add_object, update_object, delete_object_by_name, edit_object_by_name)
    frame.populate_objects(test_object_list)
