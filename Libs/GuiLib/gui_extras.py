from Libs.GuiLib.gui_helpers import *


def get_screen_size(root):
    """
    Get the screen height and width.
    :param root: Main Tk Window
    :return: screenwidth, screenheight
    """
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    return width, height


# STYLES
STD_WIDTH = 15

BTN_BG_STANDARD = '#538FFB'
BTN_FG_STANDARD = 'white'

BTN_BG_DELETE = '#D31A50'
BTN_FG_DELETE = 'white'

LBL_BG_TITLE = '#253898'
LBL_FG_TITLE = 'black'

LBL_BG_STANDARD = '#758283'
LBL_FG_STANDARD = 'white'

ROOT_BG = '#212121'
FRAME_BG_STANDARD = '#242B2E'

FONT_NAME_STANDARD = 'Helvetica'
h1 = 20
h2 = 16
h3 = 12


class CardScrollFrame(ScrollFrame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
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
        'pady': 0,
        'padx': 0,
    }
    style_args = {
        'bg': BTN_BG_STANDARD,
        'fg': BTN_FG_STANDARD,
        'font': (FONT_NAME_STANDARD, h2),
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
        'pady': 0,
        'padx': 0,
    }
    style_args = {
        'bg': BTN_BG_DELETE,
        'fg': BTN_FG_DELETE,
        'font': (FONT_NAME_STANDARD, h2),
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
        'font': (FONT_NAME_STANDARD, h1)
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
        'pady': 0,
        'padx': 0,
    }
    style_args = {
        'bg': LBL_BG_STANDARD,
        'fg': LBL_FG_STANDARD,
        'font': (FONT_NAME_STANDARD, h2),
        'width': STD_WIDTH,
        'height': 1,
    }

    def __init__(self, root, text):
        super().__init__(
            root,
            text=text,
            **self.style_args,
        )


# ENTRIES
class StandardEntry(EntryPlus):
    style_args = {
        'fg': 'black',
        'bg': 'white',
        'font': (FONT_NAME_STANDARD, h2),
        'width': STD_WIDTH,
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


class AbstractCardKeys:
    KEY_NAME = 'name'

    all_keys = [
        KEY_NAME
    ]


class AbstractCard(StandardFrame):
    keys = AbstractCardKeys

    def __init__(self, root, value_dict):
        super().__init__(root)
        # self.config(**self.style_args)
        self._value_dict = value_dict

    def key(self):
        return self._value_dict[self.keys.KEY_NAME]

    def get(self, key):
        return self._value_dict[key]
