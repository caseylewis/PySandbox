import platform
from abc import abstractmethod
from tkinter import *
from Libs.GuiLib.gui_styles import *


########################################################################################################################
# GUI FUNCTIONS
########################################################################################################################
def focus_in(widget):
    bg = "white"
    if widget['bg'] != bg:
        widget['bg'] = bg


def focus_out(widget):
    focus_out_bg = 'red'
    text = widget.get()
    if text == '':
        widget['bg'] = focus_out_bg


def to_upper(textvariable):
    textvariable.set(textvariable.get().upper())


def first_to_upper(textvariable):
    if len(textvariable.get()) == 1:
        textvariable.set(textvariable.get().upper())


def center_on_screen(toplevel):
    """
    Centers the passed Tkinter widget on the screen
    :param toplevel: Tk or Toplevel Tkinter widget to center in the screen
    :return:
    """
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))


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

    def scroll_to(self, index):
        self.update_idletasks()
        self._canvas.yview_moveto(index)
        self.update()

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


class ContentFrame(Frame):
    def __init__(self, root, title, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.title = title

    @abstractmethod
    def handle_close(self):
        return


class NavigableTkFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        row_header = 0
        row_content = 1
        row_footer = 2
        col_nav = 0
        col_content = 1
        # ENSURE NAV BAR DOES NOT GROW HORIZONTALLY, BUT CONTENT FRAME DOES
        self.grid_columnconfigure(col_nav, weight=0)
        self.grid_columnconfigure(col_content, weight=1)
        # ENSURE BOTH WILL GROW VERTICALLY
        self.grid_rowconfigure(row_header, weight=0)
        self.grid_rowconfigure(row_content, weight=1)
        self.grid_rowconfigure(row_footer, weight=0)

        # HEADER BAR
        self._header_bar = Label(self)
        self._header_bar.grid(row=row_header, column=0, columnspan=2, sticky='nsew')

        # CREATE NAV BAR
        self._nav_bar = ScrollFrame(self, hide_scroll_bar=True)
        self._nav_bar.grid(row=row_content, column=col_nav, sticky='nsew')
        # NAV BAR SHOULD COLUMNS SHOULD STRETCH ALL THE WAY
        self._nav_bar.view_port.grid_columnconfigure(0, weight=1)
        self._nav_bar_width = 10  # DEFAULT NAV BAR WIDTH
        self._nav_btns_dict = {}  # DICTIONARY THAT TRACKS THE NAV BAR BUTTONS BY INDEX
        self._nav_btn_style = {}  # PLACEHOLDER FOR IF NAV BTN STYLE IS SET LATER

        # CREATE CONTENT FRAME
        self.content_frame = Frame(self)
        self.content_frame.grid(row=1, column=1, sticky='nsew')
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self._content_frame_child_dict = {}  # DICTIONARY THAT TRACKS CONTENT FRAMES BY INDEX

        # FOOTER BAR
        self._footer_bar = Label(self)
        self._footer_bar.grid(row=2, column=0, columnspan=2, sticky='nsew')

        self.set_pad(20, 20)

    def set_nav_btn_style(self, **nav_btn_kwargs):
        self._nav_btn_style = nav_btn_kwargs
        for index, nav_btn in self._nav_btns_dict.items():
            nav_btn.config(**self._nav_btn_style)

    def set_pad(self, pady, padx):
        self._nav_bar.grid(padx=(padx, 0), pady=pady)
        self.content_frame.grid(padx=padx, pady=pady)

    def set_nav_btn_pad(self, pady, padx):
        for index, nav_btn in self._nav_btns_dict.items():
            nav_btn.grid(pady=pady, padx=padx)

    def add_content_frame(self, index, content_frame: ContentFrame):
        # IF INDEX ALREADY IN USE, RAISE EXCEPTION
        if index in self._content_frame_child_dict.keys():
            raise Exception("Cannot add a content frame with an index that has already been used before. "
                            "Index '{}' already used.".format(str(index)))

        # CREATE NAV BUTTON AND ADD TO NAV BTN DICT
        nav_btn = Button(self._nav_bar.view_port, text=content_frame.title, command=lambda i=index: self.show_frame(i), **self._nav_btn_style)
        self._nav_btns_dict[index] = nav_btn

        # ADD CONTENT FRAME TO CONTENT FRAME CHILD DICT
        self._content_frame_child_dict[index] = content_frame

        # SET NAV BUTTON IN CORRECT SPOT IN NAV BAR
        self._nav_btns_dict[index].grid(row=index, column=0, sticky='ew')

        # SET UP CONTENT FRAME WHERE IT SHOULD BE, THEN REMOVE IT BECAUSE IT SHOULD NOT BE SHOWN YET
        self._content_frame_child_dict[index].grid(row=0, column=0, **grid_frame_primary)
        self._content_frame_child_dict[index].grid_remove()

        # DERIVE HEADER AND FOOTER BG FROM CONTENT FRAME STYLE
        for frame in [
            self._nav_bar,
            self._header_bar,
            self._footer_bar,
        ]:
            frame.config(bg=content_frame['bg'])

        # ALWAYS SHOW THE FIRST FRAME
        self.show_frame(0)

    def show_frame(self, index):
        # HIDE ALL OTHER FRAMES
        for frame in self._content_frame_child_dict.values():
            frame.grid_remove()
        # SHOW THE FRAME FROM THE INDEX PROVIDED, SINCE THEY HAVE ALREADY BEEN GRIDDED THE GRID FUNCTION NEEDS NO ARGS.
        self._content_frame_child_dict[index].grid()

    def handle_close(self):
        for frame in self._content_frame_child_dict.values():
            frame.handle_close()


if __name__ == '__main__':
    from Libs.GuiLib.gui_styles import *

    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # CREATE NAVIGABLETKAPP()
    app = NavigableTkFrame(root)
    app.grid(row=0, column=0, sticky='nsew')

    app.config(bg='black')
    app.set_nav_btn_style(**style_navbtn)
    app.set_pad(10, 10)
    # root.set_sub_frame_bg(SUB_FRAME_BG)
    # root.set_nav_btn_pad((10, 0), 0)
    # root.set_nav_bar_bg('green')

    # FIRST FRAME
    first_content_frame = ContentFrame(app.content_frame, "1st Content Frame", **style_frame_primary)
    first_content_frame.grid_columnconfigure(0, weight=1)

    first_title_lbl = Label(first_content_frame.view_port, text="1st label", **style_lbl_title)
    first_title_lbl.grid(row=0, column=0, **grid_lbl)

    first_logger = LoggerPlus(first_content_frame.view_port, **style_logger)
    first_logger.grid(row=1, column=0, **grid_logger)
    first_logger.log('test')

    # SECOND FRAME
    second_content_frame = ContentFrame(app.content_frame, "2nd Content Frame", **style_frame_primary)
    second_content_frame.grid_columnconfigure(0, weight=1)

    second_title_lbl = Label(second_content_frame.view_port, text="2nd label", **style_lbl_title)
    second_title_lbl.grid(row=0, column=0, **grid_lbl)

    # ADD CONTENT FRAMES
    app.add_content_frame(0, first_content_frame)
    app.add_content_frame(1, second_content_frame)
    # TEST RAISING EXCEPTION WHEN TRYING TO DUPLICATE INDEX
    # root.add_content_frame(1, second_content_frame)  # UNCOMMENT TO RAISE EXCEPTION - TESTED, WORKS

    root.mainloop()
