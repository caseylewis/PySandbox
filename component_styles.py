from tkinter import *
from abc import abstractmethod

# STYLES
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
        'font': (FONT_NAME_STANDARD, h2)
    }

    def __init__(self, root, text):
        super().__init__(
            root,
            text=text,
            **self.style_args,
        )


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


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.config(bg=ROOT_BG)

    # BUTTONS FRAME
    buttons_frame_lbl = TitleLabel(root, text="Buttons")
    buttons_frame_lbl.grid(row=0, column=0, **TitleLabel.grid_args)

    buttons_frame = StandardFrame(root)
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid(row=1, column=0, **StandardFrame.grid_args)

    # STANDARD BUTTON
    btn_standard = StandardButton(buttons_frame, text='Standard Button', command=lambda: print('standard button'))
    btn_standard.grid(row=0, column=0, **StandardButton.grid_args)

    # DELETE BUTTON
    btn_delete = DeleteButton(buttons_frame, command=lambda: print('delete button'))
    btn_delete.grid(row=1, column=0, **DeleteButton.grid_args)

    # LABELS FRAME
    labels_frame_lbl = TitleLabel(root, text="Labels")
    labels_frame_lbl.grid(row=2, column=0, **TitleLabel.grid_args)

    labels_frame = StandardFrame(root)
    labels_frame.grid_columnconfigure(0, weight=1)
    labels_frame.grid(row=3, column=0, **StandardFrame.grid_args)

    lbl_standard = StandardLabel(labels_frame, "Standard Label")
    lbl_standard.grid(row=0, column=0, **StandardLabel.grid_args)

    root.mainloop()

