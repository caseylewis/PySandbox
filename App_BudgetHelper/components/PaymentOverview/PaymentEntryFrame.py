from Libs.GuiLib.gui_standards import *
from App_BudgetHelper.components.PaymentOverview.PayFrequencies import *


KEY_SALARY = 'salary'
KEY_PAY_FREQUENCY = 'pay_frequency'


class PaymentEntryFrame(StandardFrame):
    class _rows:
        SALARY = 1
        PAY_FREQ = 2

    class _cols:
        LBLS = 0
        DATA = 1
        BTNS = 2

    def __init__(self, root, payment_dict, on_submit_func=None):
        super().__init__(root)
        self.grid_columnconfigure(self._cols.LBLS, weight=1)
        self.grid_columnconfigure(self._cols.DATA, weight=1)
        self.grid_columnconfigure(self._cols.BTNS, weight=0)

        # PAYMENT DICT
        self._payment_dict = payment_dict

        # FUNCTION CALLBACKS
        self.__on_submit_callback = on_submit_func

        # TITLE
        self._title = TitleLabel(self, "Payment Entry")
        self._title.grid(row=0, column=0, columnspan=3, **TitleLabel.grid_args)

        # SALARY
        self._salary_label = StandardLabel(self, "Salary")
        self._salary_label.grid(row=self._rows.SALARY, column=self._cols.LBLS, **StandardLabel.grid_args)

        self._salary_display = StandardLabel(self, str(self._payment_dict[KEY_SALARY]))
        self._salary_display.grid(row=self._rows.SALARY, column=self._cols.DATA, **StandardLabel.grid_args)

        self._salary_entry = StandardEntry(self)
        self._salary_entry.grid(row=self._rows.SALARY, column=self._cols.DATA, **StandardEntry.grid_args)
        self._salary_entry.grid_remove()

        # PAY FREQUENCY
        self._pay_frequency_lbl = StandardLabel(self, "Pay Frequency")
        self._pay_frequency_lbl.grid(row=self._rows.PAY_FREQ, column=self._cols.LBLS, **StandardLabel.grid_args)

        self._pay_frequency_display = StandardLabel(self, str(self._payment_dict[KEY_PAY_FREQUENCY]))
        self._pay_frequency_display.grid(row=self._rows.PAY_FREQ, column=self._cols.DATA, **StandardLabel.grid_args)

        self._pay_frequency_dropdown = StandardDropdown(self, PayFrequencies.all)
        self._pay_frequency_dropdown.grid(row=self._rows.PAY_FREQ, column=self._cols.DATA, **StandardDropdown.grid_args)
        self._pay_frequency_dropdown.grid_remove()

        # BUTTONS
        btn_width = 7
        self._edit_btn = StandardButton(self, "Edit", width=btn_width, command=lambda: self.__handle_edit_btn())
        self._edit_btn.grid(row=self._rows.SALARY, column=self._cols.BTNS, **StandardButton.grid_args)

        self._submit_btn = StandardButton(self, "Submit", width=btn_width, command=lambda: self.__handle_submit_btn())
        self._submit_btn.grid(row=self._rows.PAY_FREQ, column=self._cols.BTNS, **StandardButton.grid_args)
        self._submit_btn.grid_remove()

        self._cancel_btn = StandardButton(self, "Cancel", width=btn_width, command=lambda: self.__handle_cancel_btn())
        self._cancel_btn.grid(row=self._rows.SALARY, column=self._cols.BTNS, **StandardButton.grid_args)
        self._cancel_btn.grid_remove()

    def __handle_edit_btn(self):
        # HIDE DISPLAY
        self._salary_display.grid_remove()
        # SHOW ENTRY WITH VALUE
        self._salary_entry.grid()
        self._salary_entry.set(self._payment_dict[KEY_SALARY])
        # HIDE PAY FREQUENCY DISPLAY
        self._pay_frequency_display.grid_remove()
        # SHOW PAY FREQUENCY DROPDOWN WITH VALUE
        self._pay_frequency_dropdown.grid()
        self._pay_frequency_dropdown.set(self._payment_dict[KEY_PAY_FREQUENCY])
        # HIDE EDIT BUTTON
        self._edit_btn.grid_remove()
        # SHOW SUBMIT AND CANCEL BUTTONS
        self._submit_btn.grid()
        self._cancel_btn.grid()

    def __handle_submit_btn(self):
        if self.__on_submit_callback is not None:
            self._payment_dict[KEY_SALARY] = self._salary_entry.get()
            self._payment_dict[KEY_PAY_FREQUENCY] = self._pay_frequency_dropdown.get()
            self.__handle_cancel_btn()
            self.__on_submit_callback(self._payment_dict)

    def __handle_cancel_btn(self):
        # HIDE SALARY ENTRY
        self._salary_entry.grid_remove()
        # SHOW SALARY DISPLAY WITH VALUE
        self._salary_display.grid()
        self._salary_display.set(self._payment_dict[KEY_SALARY])
        # HIDE PAY FREQUENCY DROPDOWN
        self._pay_frequency_dropdown.grid_remove()
        # SHOW PAY FREQUENCY DISPLAY WITH VALUE
        self._pay_frequency_display.grid()
        self._pay_frequency_display.set(self._payment_dict[KEY_PAY_FREQUENCY])
        # HIDE SUBMIT AND CANCEL BUTTONS
        self._submit_btn.grid_remove()
        self._cancel_btn.grid_remove()
        # SHOW EDIT BUTTONS
        self._edit_btn.grid()


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    payment_dict = {
        KEY_SALARY: 50000,
        KEY_PAY_FREQUENCY: PayFrequencies.SEMI_MONTHLY
    }

    def on_submit(payment_dict):
        for key, value in payment_dict.items():
            print(key, value)

    frame = PaymentEntryFrame(root, payment_dict, on_submit_func=on_submit)
    frame.grid(row=0, column=0, sticky=grid_style.sticky.all)

    root.mainloop()
