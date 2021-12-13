from tkinter import *


########################################################################################################################
# SIMPLE GUI OBJECTS
########################################################################################################################
class CheckbuttonPlus(Checkbutton):
    ON = 1
    OFF = 0

    def __init__(self, root, select_func=None, deselect_func=None, *args, **kwargs):
        self._select_func = select_func
        self._deselect_func = deselect_func
        self._var = IntVar()
        self._var.trace('w', lambda x, y, z: self.__on_val_change())
        super().__init__(root, variable=self._var, *args, **kwargs)

    def get(self):
        return self._var.get()

    def __on_val_change(self):
        if self.get() == self.ON:
            if self._select_func is not None:
                self._select_func()
        else:
            if self._deselect_func is not None:
                self._deselect_func()


class EntryPlus(Entry):
    def __init__(self, root, default_text='', *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self._default_text = default_text

    def default(self):
        self.set(self._default_text)

    def clear(self):
        self.delete(0, END)

    def set(self, set_text):
        self.clear()
        self.insert(0, set_text)


class DropdownPlus(OptionMenu):
    def __init__(self, root, options_list=None, on_change_func=None, **kwargs):
        if options_list is None:
            self._options_list = ['Empty']
        else:
            self._options_list = options_list
        self.on_change_func = on_change_func

        self._var = StringVar(root)
        self._var.set(self._options_list[0])
        self._var.trace('w', lambda x, y, z: self.__on_change_callback())
        super().__init__(root, self._var, *self._options_list)

        self.config(**kwargs)

    def __on_change_callback(self):
        if self.on_change_func is not None:
            self.on_change_func()

    def add_option(self, option):
        self._options_list.append(option)
        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))

    def remove_option(self, option_string):
        for option in self._options_list:
            if option_string == option:
                self._options_list.remove(option)

        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))
        self.default()

    def set_options(self, options_list):
        self._options_list = options_list

        menu = self["menu"]
        menu.delete(0, "end")
        for string in self._options_list:
            menu.add_command(label=string, command=lambda value=string: self._var.set(value))
        self.default()

    def default(self):
        self._var.set(self._options_list[0])

    def get(self):
        return self._var.get()

    def set(self, value):
        if value in self._options_list:
            self._var.set(value)


class LoggerPlus(Text):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.config(state=DISABLED)

    def log(self, message):
        self.config(state=NORMAL)
        self.insert(END, message)
        self.config(state=DISABLED)