from Libs.GuiLib.gui_standards import *
from App_BudgetHelper.components.PaymentOverview.PaymentEntryFrame import KEY_SALARY, KEY_PAY_FREQUENCY
from App_BudgetHelper.components.PaymentOverview.PayFrequencies import *
from App_BudgetHelper.components.Expenses.expenses import *


class PaymentBreakdownFrame(StandardFrame):
    def __init__(self, root):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        display_kwargs = {
            'anchor': E,
        }

        # TITLE
        self._title = TitleLabel(self, "Pay Breakdown")
        self._title.grid(row=0, column=0, columnspan=3, **TitleLabel.grid_args)

        # PAYMENT INFO DISPLAY
        self._payment_info_frame = StandardFrame(self)
        self._payment_info_frame.grid(row=1, column=1, **StandardFrame.grid_args)
        self._payment_info_frame.grid_columnconfigure(0, weight=1)
        self._payment_info_frame.grid_columnconfigure(1, weight=1)

        self._salary_lbl = StandardLabel(self._payment_info_frame, "Salary")
        self._salary_lbl.grid(row=0, column=0, **StandardLabel.grid_args)

        self._salary_display = StandardLabel(self._payment_info_frame, "")
        self._salary_display.grid(row=0, column=1, **StandardLabel.grid_args)

        self._pay_freq_lbl = StandardLabel(self._payment_info_frame, "Pay Frequency")
        self._pay_freq_lbl.grid(row=1, column=0, **StandardLabel.grid_args)

        self._pay_freq_display = StandardLabel(self._payment_info_frame, "")
        self._pay_freq_display.grid(row=1, column=1, **StandardLabel.grid_args)

        self._gross_paycheck_lbl = StandardLabel(self._payment_info_frame, "Gross Paycheck")
        self._gross_paycheck_lbl.grid(row=2, column=0, **StandardLabel.grid_args)

        self._gross_paycheck_display = StandardLabel(self._payment_info_frame, "")
        self._gross_paycheck_display.grid(row=2, column=1, **StandardLabel.grid_args)

        # EXPENSE/LEFTOVER DISPLAY
        self._expense_leftover_display_frame = StandardFrame(self)
        self._expense_leftover_display_frame.grid(row=2, column=0, columnspan=3, **StandardFrame.grid_args)
        self._expense_leftover_display_frame.grid_columnconfigure(0, weight=0)
        self._expense_leftover_display_frame.grid_columnconfigure(1, weight=1)
        self._expense_leftover_display_frame.grid_columnconfigure(2, weight=1)

        # HEADER ROW
        self._blank_lbl = StandardLabel(self._expense_leftover_display_frame, "")
        self._blank_lbl.grid(row=0, column=0, **StandardLabel.grid_args)

        self._amount_per_check_lbl = StandardLabel(self._expense_leftover_display_frame, "Amount/Check")
        self._amount_per_check_lbl.grid(row=0, column=1, **StandardLabel.grid_args)

        self._percent_of_check_lbl = StandardLabel(self._expense_leftover_display_frame, "% of Check")
        self._percent_of_check_lbl.grid(row=0, column=2, **StandardLabel.grid_args)

        # EXPENSES ROW
        self._expenses_lbl = StandardLabel(self._expense_leftover_display_frame, "Expenses")
        self._expenses_lbl.grid(row=1, column=0, **StandardLabel.grid_args)

        self._expense_amount_display = StandardLabel(self._expense_leftover_display_frame, "", **display_kwargs)
        self._expense_amount_display.grid(row=1, column=1, **StandardLabel.grid_args)

        self._expense_percent_display = StandardLabel(self._expense_leftover_display_frame, "", **display_kwargs)
        self._expense_percent_display.grid(row=1, column=2, **StandardLabel.grid_args)

        # LEFTOVER ROW
        self._leftover_lbl = StandardLabel(self._expense_leftover_display_frame, "Leftover")
        self._leftover_lbl.grid(row=2, column=0, **StandardLabel.grid_args)

        self._leftover_amount_display = StandardLabel(self._expense_leftover_display_frame, "", **display_kwargs)
        self._leftover_amount_display.grid(row=2, column=1, **StandardLabel.grid_args)

        self._leftover_percent_display = StandardLabel(self._expense_leftover_display_frame, "", **display_kwargs)
        self._leftover_percent_display.grid(row=2, column=2, **StandardLabel.grid_args)

    def update_breakdown(self, payment_dict, expenses_list):
        salary = int(payment_dict[KEY_SALARY])
        pay_frequency = payment_dict[KEY_PAY_FREQUENCY]
        gross_paycheck = 0
        yearly_expenses = 0
        for expense in expenses_list:
            yearly_expenses += expense.get_yearly_value()
        print(yearly_expenses)
        expenses_per_paycheck = 0

        # UPDATE PAYMENT INFO DISPLAY
        self._salary_display.set(salary)
        self._pay_freq_display.set(pay_frequency)

        # CALCULATE GROSS PAYCHECK AND EXPENSES PER PAYCHECK
        if pay_frequency == PayFrequencies.WEEKLY:
            gross_paycheck = salary / 52
            expenses_per_paycheck = yearly_expenses / 52
        elif pay_frequency == PayFrequencies.BI_WEEKLY:
            gross_paycheck = salary / 26
            expenses_per_paycheck = yearly_expenses / 26
        elif pay_frequency == PayFrequencies.SEMI_MONTHLY:
            gross_paycheck = salary / 24
            expenses_per_paycheck = yearly_expenses / 24
        elif pay_frequency == PayFrequencies.MONTHLY:
            gross_paycheck = salary / 12
            expenses_per_paycheck = yearly_expenses / 12
        self._gross_paycheck_display.set("{:.2f}".format(gross_paycheck))

        # CALCULATE LEFTOVER
        leftover = gross_paycheck - expenses_per_paycheck

        # SET AMOUNTS
        self._expense_amount_display.set("{:.2f}".format(expenses_per_paycheck))
        self._leftover_amount_display.set("{:.2f}".format(leftover))

        # CALCULATE PERCENTAGES
        expense_percentage = float(float(expenses_per_paycheck) / float(gross_paycheck)) * 100
        leftover_percentage = 100 - expense_percentage

        # SET PERCENTAGES
        self._expense_percent_display.set("{:.1f}".format(expense_percentage))
        self._leftover_percent_display.set("{:.1f}".format(leftover_percentage))


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

    frame = PaymentBreakdownFrame(root)
    frame.grid(row=0, column=0, sticky=grid_style.sticky.all)
    frame.update_breakdown(payment_dict, test_expense_list)

    root.mainloop()
