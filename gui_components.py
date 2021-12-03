from tkinter import *
import platform


class ScrollFrame(Frame):
    def __init__(self, root, hide_scroll_bar=False, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        # CREATE A CANVAS OBJECT AND A VERTICAL SCROLLBAR FOR SCROLLING IT
        self._v_scrollbar = Scrollbar(self, orient=VERTICAL)
#         self._v_scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        # ONLY SHOW SCROLL BAR IF ASKED FOR
        if hide_scroll_bar is False:
            self._v_scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
        self._canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self._v_scrollbar.set, bg='green')
        self._canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self._v_scrollbar.config(command=self._canvas.yview)

        # RESET THE VIEW
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

        # CREATE A FRAME INSIDE THE CANVAS WHICH WILL BE SCROLLED WITH IT
        self.view_port = interior = Frame(self._canvas, bg='blue')
        interior_id = self._canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self._canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self._canvas.winfo_width():
                # update the self.canvas's width to fit the inner frame
                self._canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self._canvas.winfo_width():
                # update the inner frame's width to fill the self.canvas
                self._canvas.itemconfigure(interior_id, width=self._canvas.winfo_width())
                # self.view_port.config(width=interior.winfo_reqwidth())
        self._canvas.bind('<Configure>', _configure_canvas)

        # SET EVENTS FOR ENTERING/LEAVING VIEWPORT
        self.view_port.bind('<Enter>', self.__on_enter)
        self.view_port.bind('<Leave>', self.__on_leave)

        self.config(**kwargs)

    def __on_mouse_wheel(self, event):
        # GET SCROLL VECTORS
        top, bottom = self._v_scrollbar.get()

        # IF SCROLLBAR IS MAXED OUT, DON'T ALLOW SCROLL
        if top == 0 and bottom == 1:
            return
        else:
            # PERFORM SCROLL
            if platform.system() == 'Windows':
                self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif platform.system() == 'Darwin':
                self._canvas.yview_scroll(int(-1 * event.delta), "units")
            else:
                if event.num == 4:
                    self._canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self._canvas.yview_scroll(1, "units")

    def __on_enter(self, event):  # bind wheel events when the cursor enters the control
        if platform.system() == 'Linux':
            self._canvas.bind_all("<Button-4>", self.__on_mouse_wheel)
            self._canvas.bind_all("<Button-5>", self.__on_mouse_wheel)
            self.view_port.bind_all("<Button-4>", self.__on_mouse_wheel)
            self.view_port.bind_all("<Button-5>", self.__on_mouse_wheel)
        else:
            self._canvas.bind_all("<MouseWheel>", self.__on_mouse_wheel)

    def __on_leave(self, event):  # unbind wheel events when the cursorl leaves the control
        if platform.system() == 'Linux':
            self._canvas.unbind_all("<Button-4>")
            self._canvas.unbind_all("<Button-5>")
        else:
            self._canvas.unbind_all("<MouseWheel>")

    def config(self, *args, **kwargs):
        # LIST OF ARGS TO APPLY TO CANVAS, NOT FRAME
        canvas_arg_list = [
            'width',
            'height',
            'highlightthickness',
            'highlightbackground',
        ]
        # DICT TO CONFIGURE CANVAS
        canvas_arg_dict = {}

        # ITERATE THROUGH KWARGS TO SEE WHICH KEYS NEED TO BE APPLIED TO CANVAS
        for key in kwargs.keys():
            if key in canvas_arg_list:
                canvas_arg_dict[key] = kwargs[key]

        # REMOVE THE KEYS FROM KWARGS THAT WERE PUT IN CANVAS DICT
        for key in canvas_arg_dict.keys():
            kwargs.pop(key)

        # CONFIGURE CANVAS
        self._canvas.configure(**canvas_arg_dict)
        # for key, value in canvas_arg_dict.items():
        #     print('canvas_dict', key, value)

        # CONFIGURE FRAME
        self.view_port.configure(**kwargs)
        self['bg'] = self.view_port['bg']
        # for key, value in kwargs.items():
        #     print('kwargs', key, value)

        # ENSURE CANVAS HIGHLIGHT IS THE SAME AS THE BACKGROUND
        self._canvas.configure(highlightbackground=self['bg'], bg=self['bg'])


class CardScrollFrame(ScrollFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.view_port.grid_columnconfigure(0, weight=1)

        self._frame_dict = {}

    def add_frame_by_key(self, key, frame, grid_args=None):
        print(key)
        if key in self._frame_dict.keys():
            raise("Cannot add frame with a key that is already being used: [ {} ]".format(key))

        self._frame_dict[key] = frame
        if grid_args is None:
            frame.grid(column=0, sticky="nsew", pady=5)
        else:
            frame.grid(column=0, **grid_args)

    def delete_frame_by_key(self, key):
        print(key)
        frame = self._frame_dict[key]
        for child in frame.winfo_children():
            child.destroy()
        frame.destroy()
        del self._frame_dict[key]

    def get_frame_by_key(self, key):
        return self._frame_dict[key]

    def output_dict_keys(self):
        for key in self._frame_dict.keys():
            print(key)


class AbstractCardKeys:
    KEY_NAME = 'name'

    all_keys = [
        KEY_NAME
    ]


class AbstractCard(Frame):
    keys = AbstractCardKeys

    def __init__(self, root, value_dict, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self._value_dict = value_dict

    def key(self):
        return self._value_dict[self.keys.KEY_NAME]

    def get(self, key):
        return self._value_dict[key]


class UserKeys:
    NAME = 'name'
    MAKE = 'make'
    MODEL = 'model'
    LICENSE_PLATE = 'license_plate'
    EMAIL = 'email'
    all_keys = [
        NAME,
        MAKE,
        MODEL,
        LICENSE_PLATE,
        EMAIL,
    ]


class User(dict):
    keys = UserKeys

    @property
    def name(self):
        return self[self.keys.NAME]

    @name.setter
    def name(self, val):
        self[self.keys.NAME] = val

    def __init__(self, user_dict):
        super().__init__()
        for key, value in user_dict.items():
            self[key] = value


test_user_list = []
for x in range(10):
    user_index = str(x+1)
    user_dict = {
        UserKeys.NAME: "User {}".format(user_index),
        UserKeys.MAKE: "Make {}".format(user_index),
        UserKeys.MODEL: "Model {}".format(user_index),
        UserKeys.LICENSE_PLATE: "License {}".format(user_index),
        UserKeys.EMAIL: "Email {}".format(user_index)
    }
    test_user_list.append(User(user_dict))

btn_bg = '#538FFB'
btn_fg = 'white'
delete_btn_bg = '#FD297A'
lbl_bg = '#253898'
lbl_fg = 'white'


class UserFrame(AbstractCard):
    def __init__(self, root, user: User, on_name_func=None, on_delete_func=None, *args, **kwargs):
        super().__init__(root, user, *args, **kwargs)
        self.config(bg='#E1A2B8')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=0)

        self.on_delete_callback = on_delete_func
        self.on_name_callback = on_name_func

        # USER NAME
        self._user_name_btn = Button(self, text=user[user.keys.NAME], command=lambda: self.__handle_btn_user_name(), bg=btn_bg, fg=btn_fg)
        self._user_name_btn.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(10, 0), pady=5)

        self._email_lbl = Label(self, text=user[user.keys.EMAIL], bg=lbl_bg, fg=lbl_fg)
        self._email_lbl.grid(row=0, column=1, columnspan=3, sticky='nsew', padx=10, pady=(5, 0))

        self._make_lbl = Label(self, text=user[user.keys.MAKE], bg=lbl_bg, fg=lbl_fg)
        self._make_lbl.grid(row=1, column=1, sticky='nsew', padx=10, pady=5)

        self._model_lbl = Label(self, text=user[user.keys.MODEL], bg=lbl_bg, fg=lbl_fg)
        self._model_lbl.grid(row=1, column=2, sticky='nsew', pady=5)

        self._license_lbl = Label(self, text=user[user.keys.LICENSE_PLATE], bg=lbl_bg, fg=lbl_fg)
        self._license_lbl.grid(row=1, column=3, sticky='nsew', padx=10, pady=5)

        # DELETE BTN
        self._delete_btn = Button(self, text='[X]', command=lambda: self.__handle_btn_delete(), width=3, bg=delete_btn_bg)
        self._delete_btn.grid(row=0, column=4, rowspan=2, sticky='nsew', padx=(0, 10), pady=5)

    def __handle_btn_user_name(self):
        if self.on_name_callback is not None:
            self.on_name_callback(self.key())

    def __handle_btn_delete(self):
        if self.on_delete_callback is not None:
            self.on_delete_callback(self.key())


# class AccountFrame(Frame):
#
#     @property
#     def name(self):
#         return self._name
#
#     # @name.setter
#     # def name(self, val):
#     #     return
#
#     @property
#     def description(self):
#         return
#
#     @description.setter
#     def description(self, val):
#         self._lbl_desc['text'] = str(val)
#
#     def __init__(self, root, account: Account, on_delete_func=None, *args):
#         super().__init__(root, *args, **style_frame_primary)
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=0)
#
#         self.on_delete_callback = on_delete_func
#
#         self._name = account[Account.keys.NAME]
#
#         self._lbl_name = Label(self, text=account[Account.keys.NAME], height=2, **style_lbl)
#         self._lbl_name.grid(row=0, column=0, **grid_lbl)
#
#         self._lbl_desc = Label(self, text=account[Account.keys.DESC], height=2, **style_lbl)
#         self._lbl_desc.grid(row=1, column=0, **grid_lbl)
#
#         style_btn_delete = copy_dict(style_btn)
#         style_btn_delete['width'] = 3
#         self._btn_delete = Button(self, text="[x]", command=lambda: self.__handle_btn_delete(), **style_btn_delete)
#         self._btn_delete.grid(row=0, column=1, rowspan=2, **grid_btn)
#
#     def __handle_btn_delete(self):
#         if self.on_delete_callback is not None:
#             self.on_delete_callback(self.name)


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=5)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)

    screen_width = root.winfo_screenwidth()

    def on_window_configure(event):
        root_width = root.winfo_width()
        if root_width < screen_width/2:
            scrollframe.grid(column=0, columnspan=3)
        else:
            scrollframe.grid(column=1, columnspan=1)

    root.bind("<Configure>", lambda x: on_window_configure(x))

    scrollframe = CardScrollFrame(root, bg='#00BC40')
    scrollframe.grid(row=0, column=0, sticky='nsew')

    def delete_frame_by_key(frame_key):
        scrollframe.delete_frame_by_key(frame_key)
        # scrollframe.output_dict_keys()

    def print_user_name(name):
        print(name)

    # # ADD ALL ACCOUNTS IN TEST ACCOUNT LIST
    # for account in test_account_list:
    #     account_frame = AccountFrame(scrollframe.view_port, account)
    #     account_frame.on_delete_callback = delete_frame_by_key
    #     scrollframe.add_frame_by_key(account_frame.name, account_frame)

    # ADD ALL USERS IN TEST USER LIST
    for user in test_user_list:
        user_frame = UserFrame(scrollframe.view_port, user, on_name_func=print_user_name, on_delete_func=delete_frame_by_key)
        scrollframe.add_frame_by_key(user_frame.key(), user_frame)

    root.mainloop()
