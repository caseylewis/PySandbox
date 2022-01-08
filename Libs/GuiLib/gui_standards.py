from abc import abstractmethod

from Libs.GuiLib.gui_styles import style, grid_style
from Libs.GuiLib.gui_widgets_plus import *

# STYLES
STD_WIDTH = 15

# BUTTONS
BTN_BG_STANDARD = '#538FFB'
BTN_FG_STANDARD = 'white'

BTN_BG_DELETE = '#D31A50'
BTN_FG_DELETE = 'white'

# LABELS
LBL_BG_TITLE = '#253898'
LBL_FG_TITLE = 'white'

LBL_BG_STANDARD = '#758283'
LBL_FG_STANDARD = 'white'

# FRAMES
ROOT_BG = '#212121'
FRAME_BG_STANDARD = '#242B2E'


class AbstractGridWidget:

    @property
    @abstractmethod
    def grid_args(self):
        pass

    @property
    @abstractmethod
    def style_args(self):
        pass

    def __init__(self):
        pass


# BUTTONS
class StandardButton(Button, AbstractGridWidget):
    grid_args = {
        'pady': grid_style.pad.pady_std,
        'padx': grid_style.pad.padx_std,
    }
    style_args = {
        'bg': BTN_BG_STANDARD,
        'fg': BTN_FG_STANDARD,
        'font': (style.font.style.std, style.font.size.h2),
    }

    def __init__(self, root, text, *args, **kwargs):
        super().__init__(
            root,
            text=text,
            *args,
            **kwargs
        )
        self.config(**self.style_args)


class DeleteButton(Button, AbstractGridWidget):
    grid_args = {
        'pady': grid_style.pad.pady_std,
        'padx': grid_style.pad.padx_std,
    }
    style_args = {
        'bg': BTN_BG_DELETE,
        'fg': BTN_FG_DELETE,
        'font': (style.font.style.std, style.font.size.h2),
        'text': '[X]',
        'width': 3,
    }

    def __init__(self, root, *args, **kwargs):
        super().__init__(
            root,
            *args,
            **kwargs
        )
        self.config(**self.style_args)


class StandardCheckbutton(CheckbuttonPlus, AbstractGridWidget):

    style_args = {
        'bg': BTN_BG_STANDARD,
        'selectcolor': BTN_BG_STANDARD,  # FOR THE BG COLOR OF THE LITTLE BOX
        'fg': BTN_FG_STANDARD,  # FONT COLOR AND CHECK COLOR
        'font': (style.font.style.std, style.font.size.h2),
        'bd': 2,
        # 'width': def_width-3,
        'justify': CENTER,
        'relief': RAISED,
        'height': 1,
        'anchor': W,
    }
    grid_args = {

    }

    def __init__(self, root, select_func=None, deselect_func=None, *args, **kwargs):
        super().__init__(root, select_func=select_func, deselect_func=deselect_func, *args, **kwargs)
        self.config(self.style_args)


# DROPDOWN
class StandardDropdown(DropdownPlus, AbstractGridWidget):
    grid_args = {
        'sticky': 'nsew',
        'pady': 0,
        'padx': 0,
    }
    style_args = {
        'bg': 'white',
        'fg': 'black',
        'font': (style.font.style.std, style.font.size.h2),
        'width': STD_WIDTH,
    }

    def __init__(self, root, options_list=None, on_change_func=None):
        super().__init__(
            root,
            options_list=options_list,
            on_change_func=on_change_func,
            **self.style_args
        )


# LABELS
class TitleLabel(Label, AbstractGridWidget):
    grid_args = {
        'sticky': 'nsew',
        'pady': 0,
        'padx': 0,
    }
    style_args = {
        'bg': LBL_BG_TITLE,
        'fg': LBL_FG_TITLE,
        'font': (style.font.style.std, style.font.size.h1),
        'bd': 1,
    }

    def __init__(self, root, text):
        super().__init__(
            root,
            text=text,
            **self.style_args
        )


class StandardLabel(Label, AbstractGridWidget):
    grid_args = {
        'sticky': 'nsew',
        'pady': grid_style.pad.pady_std,
        'padx': grid_style.pad.padx_std,
    }
    style_args = {
        'bg': LBL_BG_STANDARD,
        'fg': LBL_FG_STANDARD,
        'font': (style.font.style.std, style.font.size.h2),
        'width': STD_WIDTH,
        'height': 1,
    }

    def __init__(self, root, text, **kwargs):
        super().__init__(
            root,
            text=text,
            **self.style_args,
        )
        self.config(**kwargs)

    def set(self, set_text):
        self['text'] = str(set_text)


# ENTRIES
class StandardEntry(EntryPlus):
    style_args = {
        'fg': 'black',
        'bg': 'white',
        'font': (style.font.style.std, style.font.size.h2),
        'width': STD_WIDTH,
    }

    grid_args = {
        'sticky': 'nsew',
        'pady': grid_style.pad.pady_std,
        'padx': grid_style.pad.padx_std,
    }

    def __init__(self, root):
        super().__init__(
            root,
            **self.style_args,
        )


# MODAL
class StandardModal(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.config(bg=ROOT_BG)

    def center_on_root(self):
        self.master.update_idletasks()

        # Tkinter way to find the screen resolution
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2

        self.geometry("+%d+%d" % (x, y))


# FRAMES
class StandardFrame(Frame, AbstractGridWidget):
    grid_args = {
        'sticky': 'nsew',
        'pady': 10,
        'padx': 10,
    }
    style_args = {
        'bg': FRAME_BG_STANDARD
    }

    def __init__(self, root):
        super().__init__(
            root,
            **self.style_args,
        )


class CardScrollFramePlus(ScrollFramePlus):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, bg=FRAME_BG_STANDARD, hide_scroll_bar=True)#, *args, **kwargs)
        self.view_port.grid_columnconfigure(0, weight=1)

        self._frame_dict = {}

    def add_frame_by_key(self, key, frame, grid_args=None):
        if key in self._frame_dict.keys():
            raise("Cannot add frame with a key that is already being used: [ {} ]".format(key))

        padx = 10
        pady = int(padx / 2)
        self._frame_dict[key] = frame
        if grid_args is None:
            frame.grid(column=0, sticky="nsew", pady=pady, padx=padx)
        else:
            frame.grid(column=0, **grid_args)

    def delete_frame_by_key(self, key):
        frame = self._frame_dict[key]
        for child in frame.winfo_children():
            child.destroy()
        frame.destroy()
        del self._frame_dict[key]

    def delete_all(self):
        for key in list(self._frame_dict.keys()):
            self.delete_frame_by_key(key)

    def get_frame_by_key(self, key):
        return self._frame_dict[key]

    def output_dict_keys(self):
        for key in self._frame_dict.keys():
            print(key)
