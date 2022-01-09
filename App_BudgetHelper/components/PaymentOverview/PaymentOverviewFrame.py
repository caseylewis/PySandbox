from Libs.GuiLib.gui_majors import *
from App_BudgetHelper.components.PaymentOverview.PaymentEntryFrame import *
from App_BudgetHelper.components.PaymentOverview.PaymentBreakdownFrame import *


class PaymentOverviewFrame(ContentFrame):
    def __init__(self, root, payment_dict, on_payment_info_changed_func=None):
        super().__init__(root, "Payment Overview")
        self.grid_columnconfigure(0, weight=1)

        # PAYMENT ENTRY FRAME
        self._payment_entry_frame = PaymentEntryFrame(self, payment_dict, on_submit_func=on_payment_info_changed_func)
        self._payment_entry_frame.grid(row=1, column=0, sticky=grid_style.sticky.all)

        # PAYMENT BREAKDOWN FRAME
        self._payment_breakdown_frame = PaymentBreakdownFrame(self)
        self._payment_breakdown_frame.grid(row=2, column=0, sticky=grid_style.sticky.all)

    def update_payment_overview(self, payment_dict, expenses_list):
        self._payment_breakdown_frame.update_breakdown(payment_dict, expenses_list)


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
            frame.update_payment_overview(payment_dict, expense_list)

    expense_list = test_expense_list
    frame = PaymentOverviewFrame(root, payment_dict, on_payment_info_changed_func=on_submit)
    frame.grid(row=0, column=0, sticky=grid_style.sticky.all)
    frame.update_payment_overview(payment_dict, expense_list)

    root.mainloop()
