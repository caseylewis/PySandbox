from Libs.GuiLib.gui_helpers import *
# importing whole module
from tkinter import *


# class VerticalScrolledFrame(Frame):
#     def __init__(self, root, hide_scroll_bar=False, *args, **kwargs):
#         super().__init__(root, *args, **kwargs)
#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(0, weight=1)
#
#         # create a canvas object and a vertical scrollbar for scrolling it
#         self._v_scrollbar = Scrollbar(self, orient=VERTICAL)
#         # ONLY SHOW SCROLL BAR IF ASKED FOR
#         if hide_scroll_bar is False:
#             self._v_scrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
#
#         self._canvas = Canvas(self, bd=0, highlightthickness=0, bg='red', yscrollcommand=self._v_scrollbar.set)
#         self._canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
#         self._v_scrollbar.config(command=self._canvas.yview)
#
#         # reset the view
#         self._canvas.xview_moveto(0)
#         self._canvas.yview_moveto(0)
#
#         # create a frame inside the canvas which will be scrolled with it
#         self.view_port = interior = Frame(self._canvas, bg='blue')
#         interior_id = self._canvas.create_window(0, 0, window=interior, anchor=NW)
#
#         # track changes to the canvas and frame width and sync them,
#         # also updating the scrollbar
#         def _configure_interior(event):
#             print('config interior')
#             # UPDATE THE SCROLLBAR TO MATCH THE SIZE OF THE INNER FRAME
#             size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
#             self._canvas.config(scrollregion="0 0 %s %s" % size)
#             if interior.winfo_reqwidth() != self._canvas.winfo_width():
#                 # UPDATE THE CANVAS'S WIDTH TO FIT THE INNER FRAME
#                 self._canvas.config(width=interior.winfo_reqwidth())
#             if interior.winfo_reqheight() != self._canvas.winfo_height():
#                 # UPDATE THE CANVAS'S HEIGHT TO FIT THE INNER FRAME
#                 self._canvas.config(height=interior.winfo_reqheight())
#         interior.bind('<Configure>', _configure_interior)
#
#         def _configure_canvas(event):
#             if interior.winfo_reqwidth() != self._canvas.winfo_width():
#                 # update the inner frame's width to fill the canvas
#                 self._canvas.itemconfigure(interior_id, width=self._canvas.winfo_width())
#             if interior.winfo_reqheight() != self._canvas.winfo_height():
#                 # update the inner frame's height to fill the canvas
#                 self._canvas.itemconfigure(interior_id, height=self._canvas.winfo_height())
#         self._canvas.bind('<Configure>', _configure_canvas)
#
#         # SET EVENTS FOR ENTERING/LEAVING VIEWPORT
#         self.view_port.bind('<Enter>', self.__on_enter)
#         self.view_port.bind('<Leave>', self.__on_leave)
#
#         self.config(**kwargs)
#
#     def __on_mouse_wheel(self, event):
#         # GET SCROLL VECTORS
#         top, bottom = self._v_scrollbar.get()
#
#         # IF SCROLLBAR IS MAXED OUT, DON'T ALLOW SCROLL
#         if top == 0 and bottom == 1:
#             return
#         else:
#             # PERFORM SCROLL
#             if platform.system() == 'Windows':
#                 self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
#             elif platform.system() == 'Darwin':
#                 self._canvas.yview_scroll(int(-1 * event.delta), "units")
#             else:
#                 if event.num == 4:
#                     self._canvas.yview_scroll(-1, "units")
#                 elif event.num == 5:
#                     self._canvas.yview_scroll(1, "units")
#
#     def __on_enter(self, event):  # bind wheel events when the cursor enters the control
#         if platform.system() == 'Linux':
#             self._canvas.bind_all("<Button-4>", self.__on_mouse_wheel)
#             self._canvas.bind_all("<Button-5>", self.__on_mouse_wheel)
#             self.view_port.bind_all("<Button-4>", self.__on_mouse_wheel)
#             self.view_port.bind_all("<Button-5>", self.__on_mouse_wheel)
#         else:
#             self._canvas.bind_all("<MouseWheel>", self.__on_mouse_wheel)
#
#     def __on_leave(self, event):  # unbind wheel events when the cursorl leaves the control
#         if platform.system() == 'Linux':
#             self._canvas.unbind_all("<Button-4>")
#             self._canvas.unbind_all("<Button-5>")
#         else:
#             self._canvas.unbind_all("<MouseWheel>")
#
#     def config(self, *args, **kwargs):
#         # LIST OF ARGS TO APPLY TO CANVAS, NOT FRAME
#         canvas_arg_list = [
#             'width',
#             'height',
#             'highlightthickness',
#             'highlightbackground',
#         ]
#         # DICT TO CONFIGURE CANVAS
#         canvas_arg_dict = {}
#
#         # ITERATE THROUGH KWARGS TO SEE WHICH KEYS NEED TO BE APPLIED TO CANVAS
#         for key in kwargs.keys():
#             if key in canvas_arg_list:
#                 canvas_arg_dict[key] = kwargs[key]
#
#         # REMOVE THE KEYS FROM KWARGS THAT WERE PUT IN CANVAS DICT
#         for key in canvas_arg_dict.keys():
#             kwargs.pop(key)
#
#         # CONFIGURE CANVAS
#         self._canvas.configure(**canvas_arg_dict)
#         # for key, value in canvas_arg_dict.items():
#         #     print('canvas_dict', key, value)
#
#         # CONFIGURE FRAME
#         self.view_port.configure(**kwargs)
#         self['bg'] = self.view_port['bg']
#         # for key, value in kwargs.items():
#         #     print('kwargs', key, value)
#
#         # ENSURE CANVAS HIGHLIGHT IS THE SAME AS THE BACKGROUND
#         self._canvas.configure(highlightbackground=self['bg'], bg=self['bg'])


class ScrollFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        self._v_scrollbar = Scrollbar(self, orient=VERTICAL)
        self._v_scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self._canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self._v_scrollbar.set, bg='green')
        self._canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self._v_scrollbar.config(command=self._canvas.yview)

        # reset the view
        self._canvas.xview_moveto(0)
        self._canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.view_port = interior = Frame(self._canvas, bg='blue')
        interior_id = self._canvas.create_window(0, 0, window=interior,
                                                 anchor=NW)

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


if __name__ == "__main__":
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    frame = ScrollFrame(root, **style_frame_primary)
    frame.grid(row=0, column=0, sticky='nsew')
    frame.view_port.grid_columnconfigure(0, weight=1)
    # self.label = Label(text="Shrink the window to activate the scrollbar.")
    # self.label.pack()
    buttons = []
    for i in range(10):
        buttons.append(Button(frame.view_port, text="Button " + str(i)))
        buttons[-1].grid(sticky='ew')

    root.mainloop()
