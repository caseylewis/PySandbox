from Libs.GuiLib.gui_standards import *


class ContentFrame(Frame):
    def __init__(self, root, title, *args, **kwargs):
        super().__init__(root, bg=FRAME_BG_STANDARD, *args, **kwargs)
        self.title = title


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
        self._nav_bar = ScrollFramePlus(self, hide_scroll_bar=True)
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
        self._content_frame_child_dict[index].grid(row=0, column=0, sticky='nsew', pady=0, padx=0)
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
        # STYLE ALL NAV BTNS
        for nav_btn in self._nav_btns_dict.values():
            nav_btn.config(**self._nav_btn_style)
        # INVERT NAV BTN AT INDEX
        self.__invert_nav_btn_at_idx(index)
        # SHOW THE FRAME FROM THE INDEX PROVIDED, SINCE THEY HAVE ALREADY BEEN GRIDDED THE GRID FUNCTION NEEDS NO ARGS.
        self._content_frame_child_dict[index].grid()

    def __invert_nav_btn_at_idx(self, index):
        self._nav_btns_dict[index].config(bg=self._nav_btn_style['fg'], fg=self._nav_btn_style['bg'])

    def handle_close(self):
        for frame in self._content_frame_child_dict.values():
            frame.handle_close()